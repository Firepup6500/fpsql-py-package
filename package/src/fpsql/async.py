"""Firepup650's SQL Package (Async)"""

# pylint: disable=attribute-defined-outside-init


from typing import Any
from asyncio import run as aRun
import aiosqlite
from .utils import safe_literal_eval


class sql:
    "ReplDB-like async SQL implementation"

    async def addTable(
        self, tableName: str  # , mode: int = 0, address: str = ""
    ) -> None:
        """# Function: sql.addTable
          Adds a table to the database
        # Inputs:
          tableName: str - The name of the table to create
          mode: int - Not yet implemented
          address: str - Not yet implemented

        # Returns:
          None

        # Raises:
          None"""
        async with aiosqlite.connect(self.__db) as con:
            await con.execute(
                f"""CREATE TABLE IF NOT EXISTS "{tableName}"
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    value TEXT NOT NULL)"""
            )
            await con.commit()
            self.__table = tableName

    def __init__(self, filename: str):
        """# Function: sql.__init__
          Constructs an SQL instance
        # Inputs:
          filename: str - The name of the database file to connect to

        # Returns:
          None

        # Raises:
          ValueError - If the filename is `:memory:`, because the memory table doesn't work with how I've setup my async logic
        """
        if filename == ":memory:":
            raise ValueError("Cannot use `:memory:` table with async code")
        if filename.endswith(".db"):
            self.__db = filename
        else:
            self.__db = filename + ".db"
        aRun(self.addTable("default"))

    async def setTable(self, tableName: str) -> None:
        """# Function: sql.setTable
          Sets the currently active table
        # Inputs:
          tableName: str - The name of the table to use

        # Returns:
          None

        # Raises:
          None"""
        self.__table = tableName

    async def __getitem__(self, name: str) -> Any:
        """# Function: sql.__getitem__
          Gets the value of a key
        # Inputs:
          name: str - The name of the key to retrieve

        # Returns:
          Any - If the key exists, return it's value (casted), otherwise, return `None`

        # Raises:
          AttributeError - If the table is unset"""
        return await self.get(name)

    async def get(self, name: str) -> Any:
        """# Function: sql.get
          Gets the value of a key
        # Inputs:
          name: str - The name of the key to retrieve

        # Returns:
          Any - If the key exists, return it's value (casted), otherwise, return `None`

        # Raises:
          AttributeError - If the table is unset"""
        if not self.__table:
            raise AttributeError("Attempted to read from unset table")
        async with aiosqlite.connect(self.__db) as con:
            cur = await con.execute(
                f"""SELECT value FROM "{self.__table}" WHERE name = ?""", (name,)
            )
            data = await cur.fetchone()
            return safe_literal_eval(data)

    async def __setitem__(self, name: str, value: object) -> int:
        """# Function: sql.__setitem__
          Sets the value of a key
          name: str - The name of the key to set
          value: object - The value of the key

        # Returns:
          int - `1` if the key was created, `2` if it was updated

        # Raises:
          AttributeError - If the table is unset"""
        return await self.set(name, value)

    async def set(self, name: str, value: object) -> int:
        """# Function: sql.set
          Sets the value of a key
        # Inputs:
          name: str - The name of the key to set
          value: object - The value of the key

        # Returns:
          int - `1` if the key was created, `2` if it was updated

        # Raises:
          AttributeError - If the table is unset"""
        async with aiosqlite.connect(self.__db) as con:
            if not self.__table:
                raise AttributeError("Attempted to write to unset table")
            if await self.get(name) is not None:
                await con.execute(
                    f"""UPDATE "{self.__table}" SET value = ? WHERE name = ?""",
                    (str(value), name),
                )
                await con.commit()
                return 2
            await con.execute(
                f"""INSERT INTO "{self.__table}" (name, value) VALUES (?, ?)""",
                (name, str(value)),
            )
            await con.commit()
            return 1

    async def delete(self, name: str) -> None:
        """# Function: sql.delete
          Deletes a key from the table
        # Inputs:
          name: str - The name of the key to delete

        # Returns:
          None

        # Raises:
          AttributeError - If the table is unset"""
        async with aiosqlite.connect(self.__db) as con:
            if not self.__table:
                raise AttributeError("Attempted to delete from unset table")
            if await self.get(name):
                await con.execute(
                    f"""DELETE FROM "{self.__table}" WHERE name = ?""", (name,)
                )
                await con.commit()

    async def deleteAll(self) -> None:
        """# Function: sql.delete_all
          Deletes all keys from the table
        # Inputs:
          None

        # Returns:
          None

        # Raises:
          AttributeError - If the table is unset"""
        async with aiosqlite.connect(self.__db) as con:
            if not self.__table:
                raise AttributeError("Attempted to delete from unset table")
            await con.execute(f"""DELETE FROM "{self.__table}" """)
            await con.commit()

    async def close(self) -> None:
        """# Function: sql.close
          Closes the database connection
        # Inputs:
          None

        # Returns:
          None

        # Raises:
          None"""
        self.__db = ""
        self.__table = ""
