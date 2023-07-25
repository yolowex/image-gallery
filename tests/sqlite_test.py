import sqlite3


def get_table_items(table_name):
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()

    return rows


def create_table(table_name: str, **kwargs):
    x = "".join(i[0] + " " + i[1] + "," for i in kwargs.items())
    command = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
        {x[:-1]}
        )
    """
    c.execute(command)

    conn.commit()


def table_exists(table_name):
    c.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
    )
    result = c.fetchone()
    return result is not None


def add_item_to_table(table_name, item_data):
    columns = ", ".join(item_data.keys())
    placeholders = ", ".join("?" * len(item_data))
    values = tuple(item_data.values())

    c.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)

    conn.commit()


def delete_item_by_column(table_name, column_name, value_to_delete):
    c.execute(f"DELETE FROM {table_name} WHERE {column_name} = ?", (value_to_delete,))

    conn.commit()


def item_exists_in_table(table_name, column_name, value_to_check):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(f"SELECT 1 FROM {table_name} WHERE {column_name} = ?", (value_to_check,))
    result = c.fetchone()

    conn.close()

    return result is not None


conn = sqlite3.connect("./tmp/test.db")
c = conn.cursor()

create_table("name_tags", path="TEXT", text="TEXT", x="FLOAT", y="FLOAT")
create_table("perma_tags", path="TEXT", text="TEXT")


for i in range(1):
    add_item_to_table(
        "name_tags",
        {"path": f"path/to/file-{i}", "text": "this is a text", "x": 2.395, "y": 0.502},
    )

for i in range(10):
    add_item_to_table(
        "name_tags",
        {
            "path": f"pathme/to/file-{i}",
            "text": "this is a text",
            "x": 2.395,
            "y": 0.502,
        },
    )

for i in range(10):
    add_item_to_table(
        "name_tags",
        {"path": f"pathyou/to/file", "text": "this is a text", "x": 2.395, "y": 0.502},
    )

delete_item_by_column("name_tags", "path", "pathyou/to/file-0")
print(get_table_items("name_tags"))


conn.close()
