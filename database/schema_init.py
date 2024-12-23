import sqlite3

# SQLite3 setup
DATABASE = 'chat_history.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create chat history table
    cursor.execute('''CREATE TABLE IF NOT EXISTS chat_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        question TEXT,
                        answer TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')
    
    # Create Requirements table with JSON storage
    cursor.execute('''CREATE TABLE IF NOT EXISTS Requirements (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        requirements_name TEXT,
                        requirements_json TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')
    
    # Create Functions table with JSON storage for additional details
    cursor.execute('''CREATE TABLE IF NOT EXISTS Functions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        functions_name TEXT,
                        functions_json TEXT,  -- JSON field for function details
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')


    # Create Products table with JSON storage for additional details
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        products_name TEXT,
                        products_json TEXT,  -- JSON field for product details
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')

    # Create Logical_Connections table with structured fields and JSON storage
    cursor.execute('''CREATE TABLE IF NOT EXISTS Logical_Connections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    connection_name TEXT,  -- Name or description of the connection
                    connection_type TEXT,   -- Type of the connection (optional)
                    connection_json TEXT,   -- JSON field to store the entire connection
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                  )''')



    conn.commit()
    conn.close()

