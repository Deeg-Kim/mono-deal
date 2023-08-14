import logging
import sqlite3
from abc import ABC, abstractmethod
from typing import Optional

from model.base import User
from model.exception import NotFoundError

logger = logging.getLogger(__name__)


class UsersDB(ABC):

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def update_user(self, user: User):
        raise NotImplementedError


class UsersDBSqlite(UsersDB):

    def __init__(self):
        self.conn = sqlite3.connect("./data/users.db")

        with open("./sql/create_users_table_sqlite.sql", "r") as f:
            contents = f.read()

            try:
                self.conn.execute(contents)
            except Exception as ex:
                logging.error(f"Exception initializing users table: {str(ex)}")

    def get_user(self, user_id: str) -> User:
        query = f"SELECT * FROM users WHERE id = '{user_id}'"
        res = self.conn.cursor().execute(query).fetchone()

        if not res:
            raise NotFoundError(f"Could not find user with id {user_id}")

        return User(id=res[0], first_name=res[1], last_name=res[2], email=res[3], password=res[4])

    def get_user_by_email(self, email: str) -> Optional[User]:
        query = f"SELECT * FROM users WHERE email = '{email}'"
        res = self.conn.cursor().execute(query).fetchone()

        if not res:
            return None

        return User(id=res[0], first_name=res[1], last_name=res[2], email=res[3], password=res[4])

    def create_user(self, user: User):
        query = f"""
            INSERT INTO users VALUES
            ('{user.id}', '{user.first_name}', '{user.last_name}', '{user.email}', '{user.password}')
        """
        self.conn.cursor().execute(query)
        self.conn.commit()

        return user

    def update_user(self, user: User):
        pass


users_db = UsersDBSqlite()


def get_users_db() -> UsersDB:
    return users_db
