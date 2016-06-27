from abc import ABC, abstractmethod
import sys
import asyncio


class AbstractDatabaseDriver(ABC):
    r"""
            a common abc for database operation
    """
    @asyncio.coroutine
    @abstractmethod
    def query(self, sql):
        """
                raw sql query operation

        """
    @asyncio.coroutine
    @abstractmethod
    def insert(self, sql):
        """
                raw sql insert operation
        """
    @asyncio.coroutine
    @abstractmethod
    def delete(self, sql):
        """
                raw sql delete operation
        """
    @asyncio.coroutine
    @abstractmethod
    def update(self, sql):
        """raw sql update operation"""
