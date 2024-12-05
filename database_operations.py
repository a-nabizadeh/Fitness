import sqlite3
from client import Client  # Add this import statement

def store_in_database(clients):
    conn = sqlite3.connect('client_data.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS clients
                 (name TEXT, age INTEGER, sex TEXT, weight REAL, height REAL, waist REAL, hip REAL, activity_index REAL, goal TEXT)''')

    for client in clients:
        c.execute("INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (client.name, client.age, client.sex, client.weight, client.height, client.waist, client.hip, client.activity_index, client.goal))

    conn.commit()
    conn.close()

def update_client_info(name, column, new_value):
    conn = sqlite3.connect('client_data.db')
    c = conn.cursor()

    c.execute(f"UPDATE clients SET {column} = ? WHERE name = ?", (new_value, name))

    conn.commit()
    conn.close()

def load_from_database():
    conn = sqlite3.connect('client_data.db')
    c = conn.cursor()

    c.execute("SELECT * FROM clients")
    data = c.fetchall()

    conn.close()

    clients = []
    for row in data:
        clients.append(Client(*row))
    
    return clients
