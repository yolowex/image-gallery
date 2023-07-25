import sqlite3.dbapi2

from core.common.enums import LogLevel
from core.common.names import *
import core.common.resources as cr
import core.common.constants as constants


class SqlAgent:
    def __init__(self):
        self.connection: Optional[sqlite3.dbapi2.Connection] = None
        self.cursor: Optional[sqlite3.dbapi2.Cursor] = None

    def init(self):
        con_path = constants.APP_DATA_PATH + "/database.db"
        self.connection = sqlite3.connect(con_path)

        cr.log.write_log(
            f"Connected to Sql data base in path: {con_path}", LogLevel.INFO
        )

        self.cursor = self.connection.cursor()

        self.make_tables()

        print("name_tags!!")
        map(print, self.__get_table_items("name_tags"))
        print("perma_tags!!")
        list(map(print, self.__get_table_items("perma_tags")))

    def make_tables(self):
        self.__create_table("name_tags", path="TEXT", text="TEXT", x="FLOAT", y="FLOAT")
        self.__create_table("perma_tags", path="TEXT", key="TEXT", text="TEXT")

    def pull_item(self, path: str):
        name_tags = self.__get_table_items__where("name_tags", "path", path)
        perma_tags = self.__get_table_items__where("perma_tags", "path", path)

        return name_tags, perma_tags

    def push_item(
        self,
        path: str,
        name_tags: list[tuple[str, str, float, float]],
        perma_tags: list[tuple[str, str, str]],
    ):
        self.clear_item(path)

        for name in name_tags:
            self.__add_item_to_table(
                "name_tags",
                {"path": name[0], "text": name[1], "x": name[2], "y": name[3]},
            )

        for perma in perma_tags:
            self.__add_item_to_table(
                "perma_tags", {"path": perma[0], "key": perma[1], "text": perma[2]}
            )

    def clear_item(self, path: str):
        self.__delete_item_by_column("name_tags", "path", path)
        self.__delete_item_by_column("perma_tags", "path", path)

    def __get_table_items__where(self, table_name, key, value):
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE {key}='{value}'")
        rows = self.cursor.fetchall()

        return rows

    def __get_table_items(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()

        return rows

    def __create_table(self, table_name: str, **kwargs):
        x = "".join(i[0] + " " + i[1] + "," for i in kwargs.items())
        command = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
            {x[:-1]}
            )
        """
        self.cursor.execute(command)

        self.connection.commit()

    def __table_exists(self, table_name):
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        result = self.cursor.fetchone()
        return result is not None

    def __add_item_to_table(self, table_name, item_data):
        columns = ", ".join(item_data.keys())
        placeholders = ", ".join("?" * len(item_data))
        values = tuple(item_data.values())

        self.cursor.execute(
            f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values
        )

        self.connection.commit()

    def __delete_item_by_column(self, table_name, column_name, value_to_delete):
        self.cursor.execute(
            f"DELETE FROM {table_name} WHERE {column_name} = ?", (value_to_delete,)
        )

        self.connection.commit()

    def __item_exists_in_table(self, table_name, column_name, value_to_check):
        self.cursor.execute(
            f"SELECT 1 FROM {table_name} WHERE {column_name} = ?", (value_to_check,)
        )
        result = self.cursor.fetchone()

        return result is not None
