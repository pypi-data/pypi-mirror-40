#!/usr/bin/env python
#
# Lara Maia <dev@lara.click> 2015 ~ 2018
#
# The stlib is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# The stlib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#
import asyncio
import contextlib
import json
import logging
import time
from typing import Any, Dict, List, NamedTuple, Optional

import aiohttp
import rsa
from bs4 import BeautifulSoup

from . import universe

log = logging.getLogger(__name__)


class Game(NamedTuple):
    name: str
    appid: int
    playtime: int
    icon_id: str
    logo_id: str


class Badge(NamedTuple):
    game_name: str
    game_id: int
    cards: int


class LoginData(NamedTuple):
    username: str
    auth: Dict[str, Any]
    oauth: Dict[str, Any]
    has_phone: bool


class Confirmation(NamedTuple):
    mode: str
    id: int
    key: int
    give: List[str]
    to: str
    receive: List[str]


class LoginError(ValueError): pass


class LoginBlockedError(LoginError): pass


class CaptchaError(LoginError):
    def __init__(self, captcha_gid: int, captcha: bytes, message: str) -> None:
        super().__init__(message)

        self.captcha_gid = captcha_gid
        self.captcha = captcha


class MailCodeError(LoginError): pass


class TwoFactorCodeError(LoginError): pass


class SMSCodeError(LoginError): pass


class PhoneNotRegistered(Exception): pass


class AuthenticatorExists(Exception): pass


class RevocationError(Exception): pass


class SteamWebAPI:
    def __init__(
            self,
            session: aiohttp.ClientSession,
            api_url: str = 'https://api.steampowered.com',
            mobileconf_url: str = 'https://steamcommunity.com/mobileconf',
            economy_url: str = 'https://steamcommunity.com/economy',
            community_url: str = 'https://steamcommunity.com',
            headers: Optional[Dict[str, str]] = None,
            key: Optional[str] = None,
    ) -> None:
        self.session = session
        self.api_url = api_url
        self.mobileconf_url = mobileconf_url
        self.economy_url = economy_url
        self.community_url = community_url
        self.key = key

        if not headers:
            headers = {'User-Agent': 'Unknown/0.0.0'}

        self.headers = headers

    @staticmethod
    async def _new_query(
            server_time: int,
            deviceid: str,
            steamid: int,
            identity_secret: str,
            tag: str,
    ) -> Dict[str, Any]:
        params = {
            'p': deviceid,
            'a': steamid,
            'k': universe.generate_time_hash(server_time, tag, identity_secret),
            't': server_time,
            'm': 'android',
            'tag': tag,
        }

        return params

    @staticmethod
    async def _new_mobile_query(oauth_data: Dict[str, Any], token_type: str = 'mobileapp') -> Dict[str, Any]:
        current_time = int(time.time())

        params = {
            'steamid': oauth_data['steamid'],
            'access_token': oauth_data['oauth_token'],
            'authenticator_time': current_time,
            'authenticator_type': universe._TOKEN_TYPE[token_type],
        }

        return params

    async def _get_data(
            self,
            interface: str,
            method: str,
            version: int,
            params: Optional[Dict[str, str]] = None,
            data: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        if not params:
            params = {}

        if self.key:
            params['key'] = self.key

        http_method = 'POST' if data else 'GET'

        kwargs: Dict[str, Any] = {
            'method': http_method,
            'url': f'{self.api_url}/{interface}/{method}/v{version}/',
            'params': params,
            'data': data,
            'headers': self.headers,
        }

        log.debug("Requesting %s:%s via %s with %s:%s", interface, method, http_method, params, data)

        try_again = True

        while True:
            try:
                async with self.session.request(**kwargs) as response:
                    json_data = await response.json()
                    assert isinstance(json_data, dict), "Json data from SteamWebAPI is not a dict"
                    return json_data
            except aiohttp.ClientResponseError as exception:
                if try_again:
                    try_again = False
                    log.debug("WebAPI response error. Trying again...")
                    await asyncio.sleep(3)
                    continue
                else:
                    raise exception from None

    async def get_server_time(self) -> int:
        data = await self._get_data('ISteamWebAPIUtil', 'GetServerInfo', 1)
        log.debug("server time found: %s", data['servertime'])
        return int(data['servertime'])

    async def get_user_id(self, nickname: str) -> int:
        data = await self._get_data('ISteamUser', 'ResolveVanityURL', 1, {'vanityurl': nickname})

        if not data['response']['success'] is 1:
            raise ValueError('Failed to get user id.')

        log.debug("steamid found: %s (from %s)", data['response']['steamid'], nickname)
        return int(data['response']['steamid'])

    async def get_nickname(self, steamid: int) -> str:
        data = await self._get_data('ISteamUser', 'GetPlayerSummaries', 2, {'steamids': str(steamid)})

        if not data['response']['players']:
            raise ValueError('Failed to get nickname.')

        nickname = str(data['response']['players'][0]['personaname'])
        log.debug("nickname found: %s (from %s)", nickname, steamid)
        return nickname

    async def get_owned_games(self, steamid: int) -> List[Game]:
        params = {
            'steamid': str(steamid),
            'include_appinfo': "1",
        }

        # fallback: <community>/id/<id>/games/?tab=all&sort=playtime&xml=1
        data = await self._get_data('IPlayerService', 'GetOwnedGames', 1, params)
        games = []

        if not data['response']['games']:
            raise ValueError('Failed to get owned games.')

        for game in data['response']['games']:
            games.append(
                Game(game['name'], game['appid'], game['playtime_forever'], game['img_icon_url'], game['img_logo_url']),
            )

        log.debug(f"{data['response']['game_count']} owned games found.")
        return games

    async def get_session_id(self) -> str:
        async with self.session.get(
                'https://steamcommunity.com',
                headers=self.headers,
        ) as response:
            if 'sessionid' in response.cookies:
                return str(response.cookies['sessionid'].value)
            else:
                html = await response.text()
                for line in html.splitlines():
                    if 'g_sessionID' in line:
                        _, raw_value = line.split('= "')
                        return raw_value[:-2]

                raise KeyError

    async def is_logged_in(self, nickname: str) -> bool:
        async with self.session.get(
                f'https://steamcommunity.com/id/{nickname}/edit',
                allow_redirects=False,
                headers=self.headers,
        ) as response:
            log.debug("login status code: %s", response.status)

            if 'profile could not be found' in await response.text():
                log.warning("nickname doesn't exist: %s", nickname)
                return False

            if response.status == 200:
                return True
            else:
                return False

    async def add_authenticator(
            self,
            login_data: LoginData,
            device_id: str,
            phone_id: int = 1,
    ) -> LoginData:
        data = await self._new_mobile_query(login_data.oauth)
        data['device_identifier'] = device_id
        data['sms_phone_id'] = phone_id

        json_data = await self._get_data('ITwoFactorService', 'AddAuthenticator', 1, data=data)
        response: Dict[str, Any] = json_data['response']

        if response['status'] == 29:
            raise AuthenticatorExists('An Authenticator is already active for that account.')
        elif response['status'] == 84:
            raise PhoneNotRegistered('Phone not registered on Steam Account.')
        elif response['status'] != 1:
            raise NotImplementedError(f"add_authenticator is returning status {response['status']}")

        return login_data._replace(oauth=response)

    async def finalize_add_authenticator(
            self,
            login_data: LoginData,
            sms_code: str,
            email_type: int = 2,
            time_offset: int = 0,
    ) -> bool:
        data = await self._new_mobile_query(login_data.oauth)
        server_time = int(time.time()) - time_offset
        data['authenticator_code'] = universe.generate_steam_code(server_time, login_data.auth['shared_secret'])
        data['activation_code'] = sms_code
        json_data = await self._get_data("ITwoFactorService", "FinalizeAddAuthenticator", 1, data=data)

        if json_data['response']['status'] == 89:
            raise SMSCodeError("Invalid sms code")

        if json_data['response']['status'] == 2:
            data.pop('authenticator_code')
            data.pop('activation_code')
            data['email_type'] = email_type

            try:
                await self._get_data('ITwoFactorService', 'SendEmail', 1, data=data)
            except aiohttp.ContentTypeError:
                return False
            else:
                return True

        return False

    async def remove_authenticator(
            self,
            login_data: LoginData,
            revocation_code: str,
            scheme: int = 2,
    ) -> bool:
        data = await self._new_mobile_query(login_data.oauth)
        data['revocation_code'] = revocation_code
        data['steamguard_scheme'] = scheme

        try:
            json_data = await self._get_data('ITwoFactorService', 'RemoveAuthenticator', 1, data=data)
        except aiohttp.ClientResponseError:
            return False

        if json_data['response']['revocation_attempts_remaining'] == 0:
            raise RevocationError('No more attempts')

        if 'success' in json_data['response'] and json_data['response']['success'] is True:
            return True
        else:
            return False

    async def __get_names_from_item_list(
            self,
            item_list: BeautifulSoup,
    ) -> List[str]:
        result = []
        for tradeoffer_item in item_list.find_all('div', class_="trade_item"):
            appid, classid = tradeoffer_item['data-economy-item'].split('/')[1:3]

            async with self.session.get(
                    f"{self.economy_url}/itemclasshover/{appid}/{classid}",
                    params={'content_only': 1},
                    headers=self.headers,
            ) as response:
                html = BeautifulSoup(await response.text(), "html.parser")
                javascript = html.find('script')

            json_data = js_to_json(javascript)

            if json_data:
                if 'market_name' in json_data:
                    item_name = f"{json_data['market_name']} ({json_data['type']})"
                    log.debug("Using `market_name' for %s:%s (%s)", appid, classid, item_name)
                    result.append(item_name)
                else:
                    item_name = json_data['name']
                    log.debug("Using `name' for %s:%s (%s)", appid, classid, item_name)
                    result.append(item_name)
            else:
                log.debug("Unable to find human readable name for %s:%s. Ignoring.", appid, classid)
                result.append('')

        return result

    async def get_confirmations(
            self,
            identity_secret: str,
            steamid: int,
            deviceid: str,
            time_offset: int = 0,
    ) -> List[Confirmation]:
        server_time = int(time.time()) - time_offset
        params = await self._new_query(server_time, deviceid, steamid, identity_secret, 'conf')

        async with self.session.get(
                f'{self.mobileconf_url}/conf',
                params=params,
                allow_redirects=False,
                headers=self.headers,
        ) as response:
            html = BeautifulSoup(await response.text(), 'html.parser')

            if response.status == 302:
                raise LoginError('User is not logged in')

        confirmations = []
        for confirmation in html.find_all('div', class_='mobileconf_list_entry'):
            # server_time is defined again here because
            # confirmations loop (steam server) can be slow
            server_time = int(time.time()) - time_offset

            details_params = await self._new_query(
                server_time,
                deviceid,
                steamid,
                identity_secret,
                f"details{confirmation['data-confid']}",
            )

            async with self.session.get(
                    f"{self.mobileconf_url}/details/{confirmation['data-confid']}",
                    params=details_params,
                    headers=self.headers,
            ) as response:
                json_data = await response.json()

                if not json_data['success']:
                    raise AttributeError(f"Unable to get details for confirmation {confirmation['data-confid']}")

                html = BeautifulSoup(json_data["html"], 'html.parser')

            log.debug(
                "Getting human readable information from %s as type %s (%s)",
                confirmation['data-confid'],
                confirmation['data-type'],
                "Market" if confirmation['data-type'] == '3' else 'Trade Item',
            )

            if confirmation['data-type'] == "1" or confirmation['data-type'] == "2":
                to = html.find('span', class_="trade_partner_headline_sub").get_text()

                item_list = html.find_all('div', class_="tradeoffer_item_list")
                give = await self.__get_names_from_item_list(item_list[0])
                receive = await self.__get_names_from_item_list(item_list[1])
            elif confirmation['data-type'] == "3":
                to = "Market"

                listing_prices = html.find('div', class_="mobileconf_listing_prices")
                prices = [item.next_sibling.strip() for item in listing_prices.find_all("br")]
                receive = ["{} ({})".format(*prices)]

                javascript = html.find_all("script")[2]
                json_data = js_to_json(javascript)
                if 'market_name' in json_data:
                    give = [f"{json_data['market_name']} - {json_data['type']}"]
                else:
                    give = [json_data['type']]
            else:
                raise NotImplementedError(f"Data Type: {confirmation['data-type']}")

            confirmations.append(
                Confirmation(
                    confirmation['data-accept'],
                    int(confirmation['data-confid']),
                    int(confirmation['data-key']),
                    give, to, receive,
                )
            )

        return confirmations

    async def finalize_confirmation(
            self,
            identity_secret: str,
            steamid: int,
            deviceid: str,
            trade_id: int,
            trade_key: int,
            action: str,
            time_offset: int = 0,
    ) -> Dict[str, Any]:
        extra_params = {'cid': trade_id, 'ck': trade_key, 'op': action}
        server_time = int(time.time()) - time_offset
        params = await self._new_query(server_time, deviceid, steamid, identity_secret, 'conf')

        async with self.session.get(
                f'{self.mobileconf_url}/ajaxop',
                params={**params, **extra_params},
                headers=self.headers,
        ) as response:
            json_data = await response.json()
            assert isinstance(json_data, dict), "Json data from ajaxop is not a dict"
            return json_data

    async def update_badge_drops(self, badge: Badge, nickname: str) -> Badge:
        params = {'l': 'english'}

        async with self.session.get(
                f"{self.community_url}/id/{nickname}/gamecards/{badge.game_id}",
                params=params,
                headers=self.headers,
        ) as response:
            html = BeautifulSoup(await response.text(), "html.parser")
            stats = html.find('div', class_='badge_title_stats_drops')
            progress = stats.find('span', class_='progress_info_bold')

        if not progress or "No" in progress.text:
            cards = 0
        else:
            cards = int(progress.text.split(' ', 3)[0])

        return badge._replace(cards=cards)

    async def get_badges(self, nickname: str, show_no_drops: bool = False) -> List[Badge]:
        badges = []
        params = {'l': 'english'}

        async with self.session.get(
                f"{self.community_url}/id/{nickname}/badges/",
                params=params,
                headers=self.headers,
        ) as response:
            html = BeautifulSoup(await response.text(), "html.parser")
            badges_raw = html.find_all('div', class_='badge_title_row')

        try:
            pages = int(html.find_all('a', class_='pagelink')[-1].text)
        except IndexError:
            pages = 1

        for page in range(1, pages):
            params['p'] = page

            async with self.session.get(
                    f"{self.community_url}/id/{nickname}/badges/",
                    params=params,
                    headers=self.headers,
            ) as response:
                html = BeautifulSoup(await response.text(), "html.parser")
                badges_raw += html.find_all('div', class_='badge_title_row')

        for badge_raw in badges_raw:
            title = badge_raw.find('div', class_='badge_title')
            game_name = title.text.split('\t\t\t\t\t\t\t\t\t', 2)[1]

            try:
                game_ref = badge_raw.find('a')['href']
            except TypeError:
                # FIXME: It's a foil badge. The game id is above the badge_title_row
                game_id = 000000
            else:
                try:
                    game_id = int(game_ref.split('/', 3)[3])
                except IndexError:
                    # Possibly a game without cards
                    game_id = int(game_ref.split('_', 6)[4])

            progress = badge_raw.find('span', class_='progress_info_bold')

            if not progress or "No" in progress.text:
                cards = 0
            else:
                cards = int(progress.text.split(' ', 3)[0])

            if cards != 0 or show_no_drops:
                badges.append(Badge(game_name, game_id, cards))

        return badges


class Login:
    def __init__(
            self,
            session: aiohttp.ClientSession,
            webapi_session: SteamWebAPI,
            username: str,
            password: str,
            login_url: str = 'https://steamcommunity.com/login',
            mobile_login_url: str = 'https://steamcommunity.com/mobilelogin',
            steamguard_url: str = 'https://steamcommunity.com/steamguard',
            headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.session = session
        self.webapi_session = webapi_session
        self.username = username
        self.__password = password
        self.login_url = login_url
        self.mobile_login_url = mobile_login_url
        self.steamguard_url = steamguard_url

        if not headers:
            headers = {'User-Agent': 'Unknown/0.0.0'}

        self.headers = headers

    async def _new_login_data(
            self,
            authenticator_code: str = '',
            emailauth: str = '',
            captcha_gid: int = -1,
            captcha_text: str = '',
            mobile_login: bool = False,
    ) -> Dict[str, Any]:
        steam_key = await self.get_steam_key(self.username)
        encrypted_password = universe.encrypt_password(steam_key, self.__password)

        data = {
            'username': self.username,
            "password": encrypted_password.decode(),
            "emailauth": emailauth,
            "twofactorcode": authenticator_code,
            "captchagid": captcha_gid,
            "captcha_text": captcha_text,
            "loginfriendlyname": "stlib",
            "rsatimestamp": steam_key.timestamp,
            "remember_login": 'true',
            "donotcache": ''.join([str(int(time.time())), '000']),
        }

        if mobile_login:
            data['oauth_client_id'] = universe._STEAM_UNIVERSE['public']

        return data

    async def get_steam_key(self, username: str) -> universe.SteamKey:
        async with self.session.get(
                f'{self.login_url}/getrsakey/',
                params={'username': username},
                headers=self.headers,
        ) as response:
            json_data = await response.json()

        if json_data['success']:
            public_mod = int(json_data['publickey_mod'], 16)
            public_exp = int(json_data['publickey_exp'], 16)
            timestamp = int(json_data['timestamp'])
        else:
            raise ValueError('Failed to get public key.')

        return universe.SteamKey(rsa.PublicKey(public_mod, public_exp), timestamp)

    async def get_captcha(self, gid: int) -> bytes:
        async with self.session.get(
                f'{self.login_url}/rendercaptcha/',
                params={'gid': gid},
                headers=self.headers,
        ) as response:
            data = await response.read()
            assert isinstance(data, bytes), "rendercaptcha response is not bytes"
            return data

    async def has_phone(self, sessionid: str) -> bool:
        data = {
            'op': "has_phone",
            'sessionid': sessionid,
        }

        async with self.session.post(
                f'{self.steamguard_url}/phoneajax',
                data=data,
                headers=self.headers,
        ) as response:
            json_data = await response.json()
            assert isinstance(json_data, dict), "phoneajax is not a dict"

        if not json_data['success']:
            if 'error_text' in json_data:
                raise LoginError(json_data['error_text'])
            else:
                raise LoginError("Current session is invalid")

        log.debug("User has phone? %s", json_data["has_phone"])

        if json_data["has_phone"]:
            return True
        else:
            return False

    async def do_login(
            self,
            shared_secret: str = '',
            emailauth: str = '',
            captcha_gid: int = -1,
            captcha_text: str = '',
            mobile_login: bool = False,
            time_offset: int = 0,
    ) -> LoginData:
        if shared_secret:
            server_time = int(time.time()) - time_offset
            authenticator_code = universe.generate_steam_code(server_time, shared_secret)
        else:
            log.warning("No shared secret found. Trying to log-in without two-factor authentication.")
            authenticator_code = ''

        data = await self._new_login_data(authenticator_code, emailauth, captcha_gid, captcha_text, mobile_login)

        if mobile_login:
            login_url = self.mobile_login_url

            self.session.cookie_jar.update_cookies({  # type: ignore
                'mobileClientVersion': '0 (2.3.1)',
                'mobileClient': "android",
            })
        else:
            login_url = self.login_url

        async with self.session.post(
                f'{login_url}/dologin',
                data=data,
                headers=self.headers,
        ) as response:
            json_data = await response.json()
            assert isinstance(json_data, dict), "Json data from dologin is not a dict"

            if json_data['success']:
                if mobile_login:
                    oauth_data = json.loads(json_data['oauth'])
                    steamid = oauth_data['steamid']
                    token = oauth_data['wgtoken']
                    token_secure = oauth_data['wgtoken_secure']
                else:
                    oauth_data = {}
                    steamid = json_data['transfer_parameters']['steamid']
                    token = json_data['transfer_parameters']['webcookie']
                    token_secure = json_data['transfer_parameters']['token_secure']

                self.session.cookie_jar.update_cookies({
                    'steamLogin': f'{steamid}%7C%7C{token}',
                    'steamLoginSecure': f'{steamid}%7C%7C{token_secure}',
                })

                sessionid = await self.webapi_session.get_session_id()
                has_phone = await self.has_phone(sessionid)

                return LoginData(self.username, json_data, oauth_data, has_phone)

            if 'emailauth_needed' in json_data and json_data['emailauth_needed']:
                raise MailCodeError("Mail code requested")
            elif 'requires_twofactor' in json_data and json_data['requires_twofactor']:
                raise TwoFactorCodeError("Authenticator code requested")
            elif 'captcha_needed' in json_data and json_data['captcha_needed']:
                if captcha_text and captcha_gid:
                    raise LoginError("Wrong captcha code")
                else:
                    captcha = await self.get_captcha(json_data['captcha_gid'])
                    raise CaptchaError(json_data['captcha_gid'], captcha, "Captcha code requested")
            elif 'too many login failures' in json_data['message']:
                raise LoginBlockedError("Your network is blocked. Please, try again later")
            elif mobile_login and not 'oauth' in json_data:
                raise LoginError(f"Unable to log-in on mobile session: {json_data['message']}")
            else:
                raise LoginError(f"Unable to log-in: {json_data['message']}")


def js_to_json(javascript: BeautifulSoup) -> Dict[str, Any]:
    json_data = {}

    for line in str(javascript).split('\t+'):
        if "BuildHover" in line:
            for item in line.split(','):
                with contextlib.suppress(ValueError):
                    key_raw, value_raw = item.split(':"')
                    key = key_raw.replace('"', '')
                    value = bytes(value_raw.replace('"', ''), 'utf-8').decode('unicode_escape')
                    json_data[key] = value
        break

    return json_data
