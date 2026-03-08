import sqlite3
from client import Client  # Add this import statement

ALLOWED_COLUMNS = {
    "name",
    "age",
    "sex",
    "weight",
    "height",
    "waist",
    "hip",
    "activity_index",
    "goal",
}


def _ensure_clients_table(cursor):
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS clients
           (name TEXT, age INTEGER, sex TEXT, weight REAL, height REAL, waist REAL, hip REAL, activity_index REAL, goal TEXT)"""
    )


def store_in_database(clients):
    with sqlite3.connect('client_data.db') as conn:
        c = conn.cursor()
        _ensure_clients_table(c)
        for client in clients:
            c.execute("INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (client.name, client.age, client.sex, client.weight, client.height, client.waist, client.hip, client.activity_index, client.goal))

def update_client_info(name, column, new_value):
    if column not in ALLOWED_COLUMNS:
        raise ValueError(f"Invalid column '{column}'.")

    with sqlite3.connect('client_data.db') as conn:
        c = conn.cursor()
        _ensure_clients_table(c)
        c.execute(f"UPDATE clients SET {column} = ? WHERE name = ?", (new_value, name))
        if c.rowcount == 0:
            raise ValueError(f"No client found with name '{name}'.")

def load_from_database():
    with sqlite3.connect('client_data.db') as conn:
        c = conn.cursor()
        _ensure_clients_table(c)
        c.execute("SELECT * FROM clients")
        data = c.fetchall()

    clients = []
    for row in data:
        clients.append(Client(*row))
    
    return clients
