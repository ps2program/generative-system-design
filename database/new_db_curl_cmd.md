Here are the `curl` commands for all the routes you defined above:

### 0. **Add a component**
```bash
curl -X POST http://127.0.0.1:5000/add_component \
     -H "Content-Type: application/json" \
     -d '{
           "name": "New Component", 
           "description": "This is a new component"
         }'

```

### 1. **Add a Requirement**
```bash
curl -X POST http://127.0.0.1:5000/add_requirement \
     -H "Content-Type: application/json" \
     -d '{
           "component_id": "123e4567-e89b-12d3-a456-426614174000", 
           "data": {"requirement_name": "Example Requirement", "description": "This is a requirement"}
         }'
```

### 2. **Add a Sub-Requirement**
```bash
curl -X POST http://127.0.0.1:5000/add_sub_requirement \
     -H "Content-Type: application/json" \
     -d '{
           "parent_requirement_id": "123e4567-e89b-12d3-a456-426614174000", 
           "data": {"sub_requirement_name": "Sub-requirement", "description": "This is a sub-requirement"}
         }'
```

### 3. **Add a Function**
```bash
curl -X POST http://127.0.0.1:5000/add_function \
     -H "Content-Type: application/json" \
     -d '{
           "data": {"function_name": "Example Function", "description": "This is a function"}
         }'
```

### 4. **Add a Sub-Function**
```bash
curl -X POST http://127.0.0.1:5000/add_sub_function \
     -H "Content-Type: application/json" \
     -d '{
           "parent_function_id": "123e4567-e89b-12d3-a456-426614174000", 
           "data": {"sub_function_name": "Sub-function", "description": "This is a sub-function"}
         }'
```

### 5. **Add a Physical**
```bash
curl -X POST http://127.0.0.1:5000/add_physical \
     -H "Content-Type: application/json" \
     -d '{
           "data": {"physical_name": "Example Physical", "description": "This is a physical entity"}
         }'
```

### 6. **Add a Sub-Physical**
```bash
curl -X POST http://127.0.0.1:5000/add_sub_physical \
     -H "Content-Type: application/json" \
     -d '{
           "parent_physical_id": "123e4567-e89b-12d3-a456-426614174000", 
           "data": {"sub_physical_name": "Sub-physical", "description": "This is a sub-physical entity"}
         }'
```

### 7. **Get a Requirement by ID**
```bash
curl -X GET http://127.0.0.1:5000/get_requirement/123e4567-e89b-12d3-a456-426614174000
```

### 8. **Get a Function by ID**
```bash
curl -X GET http://127.0.0.1:5000/get_function/123e4567-e89b-12d3-a456-426614174000
```

### 9. **Get a Physical by ID**
```bash
curl -X GET http://127.0.0.1:5000/get_physical/123e4567-e89b-12d3-a456-426614174000
```

### Explanation:
- **POST requests**: These are used to send data to the server, such as adding a requirement, function, or physical entity.
- **GET requests**: These are used to retrieve data by ID, such as getting a specific requirement, function, or physical entity.
- **Headers**: The `Content-Type: application/json` header is included to specify that the request body is in JSON format.
- **Data**: The data is provided in JSON format in the request body for `POST` requests.

Replace the UUIDs (`123e4567-e89b-12d3-a456-426614174000`) and the data in the request body with actual values as needed.


### partial search 
```bash
curl -X GET "http://127.0.0.1:5000/search_components?name=Part"
```

### get connected entries to an  entry when given entry is changed
```bash
curl -X POST http://127.0.0.1:5000/get_associated_data \
-H "Content-Type: application/json" \
-d '{"id": 1, "model_type": "Component"}'


```