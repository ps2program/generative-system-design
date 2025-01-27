import sqlite3
import json

# Path to the database file
DATABASE = 'chat_history.db'

# getters
def get_requirements_from_db(requirements_name):
    """
    Retrieves the JSON array of requirements from the database for a given product name.

    Args:
        product_name (str): The name of the product for which requirements are to be fetched.

    Returns:
        list: The JSON array of requirements as a Python list, or None if not found.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Query to fetch the JSON requirements for the specified product
    cursor.execute('''SELECT requirements_json FROM Requirements WHERE requirements_name = ?''', (requirements_name,))
    row = cursor.fetchone()

    conn.close()

    if row:
        requirements_json_str = row[0]  # Get the JSON string from the row
        try:
            requirements = json.loads(requirements_json_str)  # Convert JSON string back to Python list
            return requirements
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No requirements found for the given product.")
        return None

def get_functions_from_db(functions_name):
    """
    Retrieves the JSON array of requirements from the database for a given product name.

    Args:
        product_name (str): The name of the product for which requirements are to be fetched.

    Returns:
        list: The JSON array of requirements as a Python list, or None if not found.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Query to fetch the JSON requirements for the specified product
    cursor.execute('''SELECT functions_json FROM Functions WHERE functions_name = ?''', (functions_name,))
    row = cursor.fetchone()

    conn.close()

    if row:
        functions_json_str = row[0]  # Get the JSON string from the row
        try:
            functions = json.loads(functions_json_str)  # Convert JSON string back to Python list
            return functions
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No functions found for the given product.")
        return None

def get_products_from_db(products_name):
    """
    Retrieves the JSON array of requirements from the database for a given product name.

    Args:
        product_name (str): The name of the product for which requirements are to be fetched.

    Returns:
        list: The JSON array of requirements as a Python list, or None if not found.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Query to fetch the JSON requirements for the specified product
    cursor.execute('''SELECT products_json FROM Products WHERE products_name = ?''', (products_name,))
    row = cursor.fetchone()

    conn.close()

    if row:
        products_json_str = row[0]  # Get the JSON string from the row
        try:
            products = json.loads(products_json_str)  # Convert JSON string back to Python list
            return products
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No products found for the given product.")
        return None

def get_logicalConnections_from_db(connections_name):
    """
    Retrieves the JSON array of requirements from the database for a given product name.

    Args:
        product_name (str): The name of the product for which requirements are to be fetched.

    Returns:
        list: The JSON array of requirements as a Python list, or None if not found.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Query to fetch the JSON requirements for the specified product
    cursor.execute('''SELECT connection_json FROM Logical_Connections WHERE connection_name = ?''', (connections_name,))
    row = cursor.fetchone()

    conn.close()

    if row:
        connections_json_str = row[0]  # Get the JSON string from the row
        try:
            connections = json.loads(connections_json_str)  # Convert JSON string back to Python list
            return connections
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No connections found for the given product.")
        return None

#inserters
def insert_requirements_json_to_db(requirements_name, requirements_json):
    """
    Inserts the entire JSON array of requirements into the 'Requirements' table in the SQLite database.
    
    Args:
        product_name (str): The name of the product the requirements belong to.
        requirements_json (str): The JSON string representing the requirements array.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Insert the product and requirements JSON as a single entry
    cursor.execute('''INSERT INTO Requirements (requirements_name, requirements_json) 
                      VALUES (?, ?)''', (requirements_name, requirements_json))
    
    conn.commit()
    conn.close()
    
def insert_functions_json_to_db(functions_name, functions_json):
    """
    Inserts the entire JSON array of functions into the 'Functions' table in the SQLite database.
    
    Args:
        function_name (str): The name of the function the list belongs to.
        functions_json (str): The JSON string representing the functions array.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Insert the function and functions JSON as a single entry
    cursor.execute('''INSERT INTO Functions (functions_name, functions_json) 
                      VALUES (?, ?)''', (functions_name, functions_json))
    
    conn.commit()
    conn.close()
   
def insert_products_json_to_db(products_name, products_json):
    """
    Inserts the entire JSON array of requirements into the 'Requirements' table in the SQLite database.
    
    Args:
        product_name (str): The name of the product the requirements belong to.
        requirements_json (str): The JSON string representing the requirements array.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Insert the product and requirements JSON as a single entry
    cursor.execute('''INSERT INTO Products (products_name, products_json) 
                      VALUES (?, ?)''', (products_name, products_json))
    
    conn.commit()
    conn.close()
    
def insert_logical_connection_to_db(connection_name, connection_json):
    """
    Inserts a logical connection into the 'Logical_Connections' table.

    Args:
        connection_name (str): The name describing the connection.
        connection_json (str): The JSON string representing the logical connection.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Insert the connection name and the entire JSON as a single entry
    cursor.execute('''INSERT INTO Logical_Connections (connection_name, connection_json) 
                      VALUES (?, ?)''', (connection_name, connection_json))
    
    conn.commit()
    conn.close()
