curl -X GET "http://localhost:5050/get_history?user_id=default_user"


Here's the code for the endpoint to get the chat history for a specific user:

### Chat History Endpoint:

```python
@app.route("/get_history", methods=["GET"])
def get_history():
    user_id = request.args.get("user_id", "default_user")  # Assuming you are handling users
    try:
        history = get_chat_history(user_id)
        return jsonify({"status": "success", "history": history})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
```

### Curl Command to Use the Endpoint:

```bash
curl -X GET "http://localhost:5050/get_history?user_id=default_user"
```

This will retrieve the chat history for the user with the ID `default_user`. You can replace `"default_user"` in both the code and the curl command with the actual user ID.


________________________________________________________________________________________________

To add the additional tables for "Requirements," "Functions," "Products," and "Logical_Connections" to your SQLite3 database, follow these steps:

### 1. **Define the Tables**

You need to create the necessary tables with appropriate fields for each entity.

Here’s an example of what these tables might look like:

```python
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
    
    # Create Requirements table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Requirements (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        requirement_name TEXT,
                        description TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')
    
    # Create Functions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Functions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        function_name TEXT,
                        description TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')

    # Create Products table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_name TEXT,
                        description TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')

    # Create Logical_Connections table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Logical_Connections (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        source_id INTEGER,
                        destination_id INTEGER,
                        connection_type TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (source_id) REFERENCES Requirements(id),
                        FOREIGN KEY (destination_id) REFERENCES Products(id)
                      )''')

    conn.commit()
    conn.close()
```

### 2. **Explanation of the Tables**:
- **Requirements**: Stores requirement details (e.g., requirement name, description).
- **Functions**: Stores functions that might be associated with the requirements or products.
- **Products**: Stores product details.
- **Logical_Connections**: Stores relationships between different entities (for example, linking requirements and products).

### 3. **Curl Commands for the New Tables**

You will need endpoints to interact with these tables (e.g., adding, retrieving data). Below are the curl commands you can use to interact with them, assuming you create similar endpoints for inserting and retrieving data:

#### Curl Command to Insert a Requirement:
```bash
curl -X POST http://localhost:5050/add_requirement \
-H "Content-Type: application/json" \
-d '{"requirement_name": "Requirement A", "description": "This is a sample requirement."}'
```

#### Curl Command to Get All Requirements:
```bash
curl -X GET http://localhost:5050/get_requirements
```

#### Curl Command to Insert a Product:
```bash
curl -X POST http://localhost:5050/add_product \
-H "Content-Type: application/json" \
-d '{"product_name": "Product A", "description": "This is a sample product."}'
```

#### Curl Command to Insert a Logical Connection:
```bash
curl -X POST http://localhost:5050/add_logical_connection \
-H "Content-Type: application/json" \
-d '{"source_id": 1, "destination_id": 2, "connection_type": "dependency"}'
```

You can create similar endpoints to interact with each table as needed. Let me know if you want the endpoint code to insert or retrieve data from these tables!




# End points to get individual db tables


### Example Usage

## requirements
```bash
curl "http://localhost:5050/get_requirements?requirements_name=garage door openers Requirements"
```

## functions
```bash
curl "http://localhost:5050/get_functions?functions_name=garage door openers Functions"
```

## products
```bash
curl "http://localhost:5050/get_products?products_name=garage door openers Prodcuts"
```

## logical connections
```bash
curl -X GET "http://localhost:5000/get_logical_connections?connections_name=garage door openers logical connections"
```
## all history
```bash
curl -X GET "http://localhost:5000/get_history?user_id=default_user"
```