# NON AI-CRUD Operations End Points

Below are the `curl` commands for each NON-AI endpoint, for now ping at `http://10.35.130.34:5050/`:

---

### **Component Endpoints**
#### Add a Component
```bash
curl -X POST http://10.35.130.34:5050//components -H "Content-Type: application/json" -d '{"name": "Component A", "description": "Description of Component A"}'
```

#### Get All Components
```bash
curl -X GET http://10.35.130.34:5050//components
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

#### Get All Requirements
```bash
curl -X GET http://10.35.130.34:5050//requirements
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

#### Get All Functions
```bash
curl -X GET http://10.35.130.34:5050//functions
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

#### Get All Physicals
```bash
curl -X GET http://10.35.130.34:5050//physicals
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

#### curls for miscellaneous

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

5. **Generic Endpoint**
```bash
   curl -X POST http://10.35.130.34:5050/generic_endpoint \
   -H "Content-Type: application/json" \
   -d '{
   "user_id": "default ",
   "query": "give me good SVG for CHAT icon in 20x20"
   }'
```


xSystems client side please replace `<component_id>`, `<requirement_id>`, `<function_id>`, and `<physical_id>` with the actual UUID values.