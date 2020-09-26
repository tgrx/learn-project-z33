import json
import os
from datetime import timedelta
from http import cookies
from typing import Any
from typing import Dict
from typing import Optional

import delorean
from delorean import Delorean

from framework import settings
from framework.consts import SESSION_AGE
from framework.consts import SESSION_COOKIE
from framework.consts import STRFTIME_FORMAT
from framework.settings import STORAGE_DIR


class Session:
    SESSIONS_FILE = (STORAGE_DIR / "sessions.json").resolve()

    @classmethod
    def from_headers(cls, headers: Dict) -> "Session":
        new_session = cls()

        if not headers:
            return new_session

        cookie_header = headers.get("Cookie")
        if not cookie_header:
            return new_session

        jar = cookies.SimpleCookie()
        jar.load(cookie_header)
        if SESSION_COOKIE not in jar:
            return new_session

        morsel = jar[SESSION_COOKIE]
        return Session(morsel.value)

    @property
    def new(self) -> bool:
        return self.__new

    @property
    def session_id(self) -> str:
        return self.__session_id

    @property
    def header(self) -> str:
        header = self._build_header()
        return header

    @property
    def expired_header(self) -> str:
        header = self._build_header(expires=True)
        return header

    @property
    def headers(self) -> Dict:
        headers = {"Set-Cookie": self.header} if self.new else {}
        return headers

    @property
    def expired_headers(self) -> Dict:
        headers = {"Set-Cookie": self.expired_header}
        return headers

    def __init__(self, session_id: Optional[str] = None):
        self.__session_id = session_id or self._generate_new_session()
        self.__new = not bool(session_id)

    def get(self, key: str, default: Any = None) -> Any:
        value = default
        try:
            value = self[key]
        except KeyError:
            pass
        return value

    def update(self, key_value_pairs: Dict) -> None:
        session = self._load_my_session()
        session.update(key_value_pairs)
        self._store_my_session(session)

    def __getitem__(self, key) -> Any:
        session = self._load_my_session()
        value = session[key]
        return value

    def __setitem__(self, key, value) -> None:
        session = self._load_my_session()
        session[key] = value
        self._store_my_session(session)

    def _load_my_session(self) -> Dict:
        sessions = self._load()
        session = sessions.get(self.__session_id, {})
        expired_at_s = session.get("_expired_at")
        if expired_at_s:
            expired_at = delorean.parse(expired_at_s, dayfirst=False, yearfirst=True)
            if expired_at <= delorean.utcnow():
                return {}
        return session

    def _store_my_session(self, session: Dict) -> None:
        sessions = self._load()
        stored_session = sessions.setdefault(self.__session_id, {})
        stored_session.update(session)

        instant = Delorean().datetime
        instant_s = instant.strftime(STRFTIME_FORMAT)
        stored_session["_updated_at"] = instant_s
        if self.new:
            expired_at = instant + timedelta(seconds=SESSION_AGE)
            expired_at_s = expired_at.strftime(STRFTIME_FORMAT)
            stored_session["_expired_at"] = expired_at_s
            stored_session["_created_at"] = instant_s
        self._store(sessions)

    def _load(self) -> Dict:
        empty_dict = {}

        if not self.SESSIONS_FILE.is_file():
            return empty_dict

        with self.SESSIONS_FILE.open("r") as src:
            sessions = {}
            try:
                sessions = json.load(src)
            except json.JSONDecodeError:
                pass

        return sessions or empty_dict

    def _store(self, sessions: Dict) -> None:
        with self.SESSIONS_FILE.open("w") as dst:
            json.dump(sessions, dst, sort_keys=True, indent=2)

    def _build_header(self, expires: bool = False) -> str:
        jar = cookies.SimpleCookie()
        jar[SESSION_COOKIE] = self.__session_id

        morsel = jar[SESSION_COOKIE]
        morsel["Domain"] = settings.SITE
        morsel["Path"] = "/"

        max_ages = {
            False: SESSION_AGE,
            True: 0,
        }

        morsel["Max-Age"] = max_ages[expires]

        header = jar[SESSION_COOKIE].OutputString()

        return header

    @staticmethod
    def _generate_new_session() -> str:
        session_id = os.urandom(16).hex()
        return session_id
