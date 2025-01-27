Below are **cURL commands** for all the CRUD operations. Each example assumes the server is running at `http://127.0.0.1:5050`. Update the endpoints as needed to match your actual API routes.

---

### **Create Operations**

1. **Add Component**
   ```bash
   curl -X POST http://127.0.0.1:5050/add_component \
        -H "Content-Type: application/json" \
        -d '{
              "name": "New Component", 
              "description": "This is a new component"
            }'
   ```

2. **Add Requirement**
   ```bash
   curl -X POST http://127.0.0.1:5050/add_requirement \
        -H "Content-Type: application/json" \
        -d '{
              "component_id": 1, 
              "data": {"key": "value"}
            }'
   ```

3. **Add Sub-Requirement**
   ```bash
   curl -X POST http://127.0.0.1:5050/add_sub_requirement \
        -H "Content-Type: application/json" \
        -d '{
              "parent_requirement_id": 1, 
              "child_requirement_id": 2
            }'
   ```

4. **Add Function**
   ```bash
   curl -X POST http://127.0.0.1:5050/add_function \
        -H "Content-Type: application/json" \
        -d '{
              "data": {"key": "value"}
            }'
   ```

5. **Associate Function with Requirement**
   ```bash
   curl -X POST http://127.0.0.1:5050/associate_function_with_requirement \
        -H "Content-Type: application/json" \
        -d '{
              "requirement_id": 1, 
              "function_id": 1
            }'
   ```

6. **Add Sub-Function**
   ```bash
   curl -X POST http://127.0.0.1:5050/add_sub_function \
        -H "Content-Type: application/json" \
        -d '{
              "parent_function_id": 1, 
              "child_function_id": 2
            }'
   ```

7. **Add Physical**
   ```bash
   curl -X POST http://127.0.0.1:5050/add_physical \
        -H "Content-Type: application/json" \
        -d '{
              "data": {"key": "value"}
            }'
   ```

8. **Associate Physical with Function**
   ```bash
   curl -X POST http://127.0.0.1:5050/associate_physical_with_function \
        -H "Content-Type: application/json" \
        -d '{
              "function_id": 1, 
              "physical_id": 1
            }'
   ```

9. **Add Sub-Physical**
   ```bash
   curl -X POST http://127.0.0.1:5050/add_sub_physical \
        -H "Content-Type: application/json" \
        -d '{
              "parent_physical_id": 1, 
              "child_physical_id": 2
            }'
   ```

---

### **Read Operations**

1. **Get Component by ID**
   ```bash
   curl -X GET http://127.0.0.1:5050/get_component?id=1
   ```

2. **Get All Components**
   ```bash
   curl -X GET http://127.0.0.1:5050/get_all_components
   ```

3. **Get Requirement by ID**
   ```bash
   curl -X GET http://127.0.0.1:5050/get_requirement?id=1
   ```

4. **Get Requirements for a Component**
   ```bash
   curl -X GET http://127.0.0.1:5050/get_requirements_for_component?component_id=1
   ```

5. **Get Function by ID**
   ```bash
   curl -X GET http://127.0.0.1:5050/get_function?id=1
   ```

6. **Get Physical by ID**
   ```bash
   curl -X GET http://127.0.0.1:5050/get_physical?id=1
   ```

---

### **Update Operations**

1. **Update Component**
   ```bash
   curl -X PUT http://127.0.0.1:5050/update_component \
        -H "Content-Type: application/json" \
        -d '{
              "id": 1,
              "name": "Updated Component", 
              "description": "Updated description"
            }'
   ```

2. **Update Requirement**
   ```bash
   curl -X PUT http://127.0.0.1:5050/update_requirement \
        -H "Content-Type: application/json" \
        -d '{
              "id": 1, 
              "data": {"key": "new_value"}
            }'
   ```

3. **Update Function**
   ```bash
   curl -X PUT http://127.0.0.1:5050/update_function \
        -H "Content-Type: application/json" \
        -d '{
              "id": 1, 
              "data": {"key": "new_value"}
            }'
   ```

4. **Update Physical**
   ```bash
   curl -X PUT http://127.0.0.1:5050/update_physical \
        -H "Content-Type: application/json" \
        -d '{
              "id": 1, 
              "data": {"key": "new_value"}
            }'
   ```

---

### **Delete Operations**

1. **Delete Component**
   ```bash
   curl -X DELETE http://127.0.0.1:5050/delete_component?id=1
   ```

2. **Delete Requirement**
   ```bash
   curl -X DELETE http://127.0.0.1:5050/delete_requirement?id=1
   ```

3. **Delete Function**
   ```bash
   curl -X DELETE http://127.0.0.1:5050/delete_function?id=1
   ```

4. **Delete Physical**
   ```bash
   curl -X DELETE http://127.0.0.1:5050/delete_physical?id=1
   ```

---

These commands align with the CRUD operations you have defined. Ensure that the endpoints and request payloads match your API design. Let me know if you need further assistance!