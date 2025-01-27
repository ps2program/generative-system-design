Here’s a well-structured arrangement of your cURL commands for better clarity and organization:

---

# **Non-AI CRUD Operations Endpoints**

## **Base URL:**  
`http://10.35.130.34:5050/`

---

## **Component Endpoints**
1. **Add a Component**  
   ```bash
   curl -X POST http://10.35.130.34:5050/components \
   -H "Content-Type: application/json" \
   -d '{"name": "Component A", "description": "Description of Component A"}'
   ```

2. **Get a Component by ID**  
   ```bash
   curl -X GET http://10.35.130.34:5050/components/<component_id>
   ```

3. **Update a Component**  
   ```bash
   curl -X PUT http://10.35.130.34:5050/components/<component_id> \
   -H "Content-Type: application/json" \
   -d '{"name": "Updated Component Name", "description": "Updated Description"}'
   ```

4. **Delete a Component**  
   ```bash
   curl -X DELETE http://10.35.130.34:5050/components/<component_id>
   ```

5. **Get All Components**  
   ```bash
   curl -X GET http://10.35.130.34:5050/get_all_components
   ```

---

## **Requirement Endpoints**
1. **Add a Requirement**  
   ```bash
   curl -X POST http://10.35.130.34:5050/requirements \
   -H "Content-Type: application/json" \
   -d '{"component_id": "<component_id>", "data": "Requirement data"}'
   ```

2. **Get a Requirement by ID**  
   ```bash
   curl -X GET http://10.35.130.34:5050/requirements/<requirement_id>
   ```

3. **Update a Requirement**  
   ```bash
   curl -X PUT http://10.35.130.34:5050/requirements/<requirement_id> \
   -H "Content-Type: application/json" \
   -d '{"data": "Updated requirement data"}'
   ```

4. **Delete a Requirement**  
   ```bash
   curl -X DELETE http://10.35.130.34:5050/requirements/<requirement_id>
   ```

5. **Get All Requirements**  
   ```bash
   curl -X GET http://10.35.130.34:5050/get_all_requirements
   ```

---

## **Function Endpoints**
1. **Add a Function**  
   ```bash
   curl -X POST http://10.35.130.34:5050/functions \
   -H "Content-Type: application/json" \
   -d '{"data": "Function data"}'
   ```

2. **Get a Function by ID**  
   ```bash
   curl -X GET http://10.35.130.34:5050/functions/<function_id>
   ```

3. **Update a Function**  
   ```bash
   curl -X PUT http://10.35.130.34:5050/functions/<function_id> \
   -H "Content-Type: application/json" \
   -d '{"data": "Updated function data"}'
   ```

4. **Delete a Function**  
   ```bash
   curl -X DELETE http://10.35.130.34:5050/functions/<function_id>
   ```

5. **Get All Functions**  
   ```bash
   curl -X GET http://10.35.130.34:5050/get_all_functions
   ```

---

## **Physical Endpoints**
1. **Add a Physical**  
   ```bash
   curl -X POST http://10.35.130.34:5050/physicals \
   -H "Content-Type: application/json" \
   -d '{"data": "Physical data"}'
   ```

2. **Get a Physical by ID**  
   ```bash
   curl -X GET http://10.35.130.34:5050/physicals/<physical_id>
   ```

3. **Update a Physical**  
   ```bash
   curl -X PUT http://10.35.130.34:5050/physicals/<physical_id> \
   -H "Content-Type: application/json" \
   -d '{"data": "Updated physical data"}'
   ```

4. **Delete a Physical**  
   ```bash
   curl -X DELETE http://10.35.130.34:5050/physicals/<physical_id>
   ```

5. **Get All Physicals**  
   ```bash
   curl -X GET http://10.35.130.34:5050/get_all_physicals
   ```

---

## **Miscellaneous Endpoints**
1. **Clear All Entities**  
   ```bash
   curl -X POST http://10.35.130.34:5050/clear_all
   ```

---

# **Relational Endpoints**

## **Entity Relationships**
1. **Add a Function to a Requirement**  
   ```bash
   curl -X POST http://10.35.130.34:5050/requirements/<requirement_id>/functions \
   -H "Content-Type: application/json" \
   -d '{"function_id": "<function_id>"}'
   ```

2. **Add a Physical to a Requirement**  
   ```bash
   curl -X POST http://10.35.130.34:5050/requirements/<requirement_id>/physicals \
   -H "Content-Type: application/json" \
   -d '{"physical_id": "<physical_id>"}'
   ```

3. **Add a Physical to a Function**  
   ```bash
   curl -X POST http://10.35.130.34:5050/functions/<function_id>/physicals \
   -H "Content-Type: application/json" \
   -d '{"physical_id": "<physical_id>"}'
   ```

---

## **Self-Referential Relationship Endpoints**

### **During Creation**
1. **Add a Sub-Requirement to a Requirement**  
   ```bash
   curl -X POST http://10.35.130.34:5050/add_sub_requirement_to_requirement \
   -H "Content-Type: application/json" \
   -d '{
     "parent_requirement_id": "<PARENT_REQUIREMENT_ID>",
     "sub_requirement_data": {
       "name": "Sub Requirement Name",
       "description": "Description of the sub-requirement"
     }
   }'
   ```

2. **Add a Parent Requirement to a Sub-Requirement**  
   ```bash
   curl -X POST http://10.35.130.34:5050/add_parent_requirement_to_sub_requirement \
   -H "Content-Type: application/json" \
   -d '{
     "sub_requirement_id": "<SUB_REQUIREMENT_ID>",
     "parent_requirement_data": {
       "name": "Parent Requirement Name",
       "description": "Description of the parent requirement"
     }
   }'
   ```

---

### **For Existing Nodes**
1. **Associate a Sub-Requirement with a Parent Requirement**  
   ```bash
   curl -X POST http://10.35.130.34:5050/associate_sub_requirement_to_parent_requirement \
   -H "Content-Type: application/json" \
   -d '{
     "parent_requirement_id": "<PARENT_REQUIREMENT_ID>",
     "sub_requirement_id": "<SUB_REQUIREMENT_ID>"
   }'
   ```

2. **Associate a Sub-Function with a Function**  
   ```bash
   curl -X POST http://10.35.130.34:5050/associate_sub_function_to_function \
   -H "Content-Type: application/json" \
   -d '{
     "function_id": "<FUNCTION_ID>",
     "sub_function_id": "<SUB_FUNCTION_ID>"
   }'
   ```

3. **Associate a Sub-Physical with a Physical**  
   ```bash
   curl -X POST http://10.35.130.34:5050/associate_sub_physical_to_physical \
   -H "Content-Type: application/json" \
   -d '{
     "physical_id": "<PHYSICAL_ID>",
     "sub_physical_id": "<SUB_PHYSICAL_ID>"
   }'
   ```

---

### **Get Sub-Entities**
1. **Get All Sub-Requirements of a Requirement**  
   ```bash
   curl -X GET http://10.35.130.34:5050/get_sub_requirements/<PARENT_REQUIREMENT_ID>
   ```

2. **Get All Parent Requirements of a Sub-Requirement**  
   ```bash
   curl -X GET http://10.35.130.34:5050/get_parent_requirements/<SUB_REQUIREMENT_ID>
   ```

---

Replace placeholder values (e.g., `<component_id>`, `<requirement_id>`) with actual UUIDs during testing. This structure should make it easier to navigate and test the API endpoints.