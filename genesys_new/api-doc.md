
---

# API Usage Documentation

## Predict Endpoint

### Endpoint:
`http://10.85.86.15:5050/predict`

### Method:
`POST`

### Headers:
```json
Content-Type: application/json
```

### Request Body:
```json
{
  "message": "Garage Door Opener"
}
```

### Example Usage:
You can test the API using the following `curl` command:

```bash
curl -X POST \
  http://10.85.86.15:5050/predict \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "Garage Door Opener"
}'
```

### Swagger UI Documentation:

To interact with the API endpoints and view their documentation through a user-friendly interface, follow these steps:

1. **Navigate to Swagger UI**:
   Open the Swagger UI in your web browser by visiting the following URL:
   ```
   http://10.85.86.15:5050/swagger
   ```

2. **Explore Endpoints**:
   - On the Swagger UI page, you will see a list of available endpoints, including `/predict`, `/change_model`, and `/clear_history`.
   - Click on the endpoint you wish to explore. For example, click on the `/predict` endpoint to view details about how to use it.

3. **Try Out Endpoints**:
   - Swagger UI provides an interactive feature that allows you to test endpoints directly from the browser.
   - Enter the required parameters and click the "Try it out" button to make a request and see the response.

4. **Review API Documentation**:
   - Swagger UI will show you detailed information about each endpoint, including the expected request format and possible responses.
   - This documentation is automatically generated from the `swagger.json` file and updated with your API.

### Dummy UI Endpoint:

For additional interaction with our mock UI, use the following URL:
```
http://10.85.86.15:5050
```

This UI provides a basic interface to interact with the xSystemsAI system.

---
