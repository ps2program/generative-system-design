# NON AI-CRUD Operations End Points

Below are the `curl` commands for each NON-AI endpoint, for now ping at `http://10.35.130.34:5050/`:

---

### **Component Endpoints**
#### Add a Component
```bash
curl -X POST http://10.35.130.34:5050//components -H "Content-Type: application/json" -d '{"name": "Component A", "description": "Description of Component A"}'
```

#### Get a Component by ID
```bash
curl -X GET http://10.35.130.34:5050//components/<component_id>
```

#### Update a Component
```bash
curl -X PUT http://10.35.130.34:5050//components/<component_id> -H "Content-Type: application/json" -d '{"name": "Updated Component Name", "description": "Updated Description"}'
```

#### Delete a Component
```bash
curl -X DELETE http://10.35.130.34:5050//components/<component_id>
```

---

### **Requirement Endpoints**
#### Add a Requirement
```bash
curl -X POST http://10.35.130.34:5050//requirements -H "Content-Type: application/json" -d '{"component_id": "<component_id>", "data": "Requirement data"}'
```

#### Get a Requirement by ID
```bash
curl -X GET http://10.35.130.34:5050//requirements/<requirement_id>
```

#### Update a Requirement
```bash
curl -X PUT http://10.35.130.34:5050//requirements/<requirement_id> -H "Content-Type: application/json" -d '{"data": "Updated requirement data"}'
```

#### Delete a Requirement
```bash
curl -X DELETE http://10.35.130.34:5050//requirements/<requirement_id>
```

---

### **Function Endpoints**
#### Add a Function
```bash
curl -X POST http://10.35.130.34:5050//functions -H "Content-Type: application/json" -d '{"data": "Function data"}'
```

#### Get a Function by ID
```bash
curl -X GET http://10.35.130.34:5050//functions/<function_id>
```

#### Update a Function
```bash
curl -X PUT http://10.35.130.34:5050//functions/<function_id> -H "Content-Type: application/json" -d '{"data": "Updated function data"}'
```

#### Delete a Function
```bash
curl -X DELETE http://10.35.130.34:5050//functions/<function_id>
```

---

### **Physical Endpoints**
#### Add a Physical
```bash
curl -X POST http://10.35.130.34:5050//physicals -H "Content-Type: application/json" -d '{"data": "Physical data"}'
```

#### Get a Physical by ID
```bash
curl -X GET http://10.35.130.34:5050//physicals/<physical_id>
```

#### Update a Physical
```bash
curl -X PUT http://10.35.130.34:5050//physicals/<physical_id> -H "Content-Type: application/json" -d '{"data": "Updated physical data"}'
```

#### Delete a Physical
```bash
curl -X DELETE http://10.35.130.34:5050//physicals/<physical_id>
```

---

### curls for miscellaneous

1. **Get All Components**:
   ```bash
   curl -X GET http://10.35.130.34:5050//get_all_components
   ```

2. **Get All Requirements**:
   ```bash
   curl -X GET http://10.35.130.34:5050//get_all_requirements
   ```

3. **Get All Functions**:
   ```bash
   curl -X GET http://10.35.130.34:5050//get_all_functions
   ```

4. **Get All Physicals**:
   ```bash
   curl -X GET http://10.35.130.34:5050//get_all_physicals
   ```

5. ### clear all Entities:
   ```bash
   curl -X POST http://10.35.130.34:5050//clear_all
   ```

xSystems client side please replace `<component_id>`, `<requirement_id>`, `<function_id>`, and `<physical_id>` with the actual UUID values.

### **Entity Relationships**
#### Add a Function to a Requirement
```bash
curl -X POST http://10.35.130.34:5050//requirements/<requirement_id>/functions -H "Content-Type: application/json" -d '{"function_id": "<function_id>"}'
```

#### Add a Physical to a Requirement
```bash
curl -X POST http://10.35.130.34:5050//requirements/<requirement_id>/physicals -H "Content-Type: application/json" -d '{"physical_id": "<physical_id>"}'
```

#### Add a Physical to a Function
```bash
curl -X POST http://10.35.130.34:5050//functions/<function_id>/physicals -H "Content-Type: application/json" -d '{"physical_id": "<physical_id>"}'
```



---

### Relational EndPoints

### 1. **Add Function to Requirement**
**Endpoint:** `/add_function_to_requirement`  
**Method:** `POST`

```bash
curl -X POST http://10.35.130.34:5050//add_function_to_requirement \
-H "Content-Type: application/json" \
-d '{
  "function_id": "e1234567-e89b-12d3-a456-426614174000",
  "requirement_id": "f1234567-e89b-12d3-a456-426614174000"
}'
```

---

### 2. **Add Physical to Requirement**
**Endpoint:** `/add_physical_to_requirement`  
**Method:** `POST`

```bash
curl -X POST http://10.35.130.34:5050//add_physical_to_requirement \
-H "Content-Type: application/json" \
-d '{
  "physical_id": "a1234567-e89b-12d3-a456-426614174000",
  "requirement_id": "b1234567-e89b-12d3-a456-426614174000"
}'
```

---

### 3. **Add Physical to Function**
**Endpoint:** `/add_physical_to_function`  
**Method:** `POST`

```bash
curl -X POST http://10.35.130.34:5050//add_physical_to_function \
-H "Content-Type: application/json" \
-d '{
  "physical_id": "c1234567-e89b-12d3-a456-426614174000",
  "function_id": "d1234567-e89b-12d3-a456-426614174000"
}'
```


---

# 7. Self-referential

## 1. Existing Node - Self Referential

#### **1.  Sub-Requirement Association**

```bash
curl -X POST http://10.35.130.34:5050/associate_sub_requirement_to_parent_requirement \
    -H "Content-Type: application/json" \
    -d '{
        "parent_requirement_id": "your_parent_requirement_id_here",
        "sub_requirement_id": "your_sub_requirement_id_here"
    }'
```
Replace `your_parent_requirement_id_here` and `your_sub_requirement_id_here` with the actual UUIDs of the parent requirement and sub-requirement.

---

#### **2. Sub-Function Association**
```bash
curl -X POST http://10.35.130.34:5050/associate_sub_function_to_function \
-H "Content-Type: application/json" \
-d '{
  "function_id": "func123",
  "sub_function_id": "subfunc456"
}'
```

#### **3. Sub-Physical Association**
```bash
curl -X POST http://10.35.130.34:5050/associate_sub_physical_to_physical \
-H "Content-Type: application/json" \
-d '{
  "physical_id": "phys123",
  "sub_physical_id": "subphys456"
}'
```



## 2. New Node - Self Referential

### 1. Add a Sub-Requirement to a Requirement**
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

### 2. Add a Sub-Function:
```bash
curl -X POST http://10.35.130.34:5050/add_sub_function_to_function \
-H "Content-Type: application/json" \
-d '{
    "parent_function_id": "123e4567-e89b-12d3-a456-426614174000",
    "sub_function_data": "Sub Function Example Data"
}'
```

### 3. Add a Sub-Physical:
```bash
curl -X POST http://10.35.130.34:5050/add_sub_physical_to_physical \
-H "Content-Type: application/json" \
-d '{
    "parent_physical_id": "123e4567-e89b-12d3-a456-426614174000",
    "sub_physical_data": "Sub Physical Example Data"
}'
```


