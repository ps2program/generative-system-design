import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from graph.GraphBuilder import create_question_handling_graph, create_schema
from graph.models import set_global_model, get_global_model
from langchain_core.messages import RemoveMessage
from flask_swagger_ui import get_swaggerui_blueprint

import sqlite3
import json
from graph.ds_query_methods import *  # Use this if you run as a module
from database.schema_init import init_db


app = Flask(__name__)
CORS(app)

# Initialize the default model
set_global_model("OLLAMA_MISTRAL")
# set_global_model("LLAMA3")
# set_global_model("MISTRAL")
graph = create_question_handling_graph()
config = {"configurable": {"thread_id": "1"}}

# SQLite3 setup
DATABASE = 'chat_history.db'
# Initialize the database
init_db()


def insert_chat_history(user_id, question, answer):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO chat_history (user_id, question, answer) VALUES (?, ?, ?)''',
                   (user_id, question, answer))
    conn.commit()
    conn.close()

def get_chat_history(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''SELECT question, answer, timestamp FROM chat_history WHERE user_id=?''', (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history

def clear_chat_history(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM chat_history WHERE user_id=?''', (user_id,))
    conn.commit()
    conn.close()

# Swagger setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Agent function to handle user input
def call_agent(user_request):
    inputs = {
        "messages": [
            ("user", user_request['question']),
        ],
        "questionType": user_request['questionType']
    }
    
    config = {"configurable": {"thread_id": "1"}, "questionType": user_request['questionType']}
    output = graph.invoke(inputs, config)
    response = output['response_schema']
    return response

def call_agent_v1(user_prompt):
    inputs = {
        "messages": [
            ("user", user_prompt),
        ]
    }
    
    config = {"configurable": {"thread_id": "1"}}
    output = graph.invoke(inputs, config)
    response = output["messages"][-1].content
    return response

# API Routes

@app.route("/change_model", methods=["POST"])
def change_model():
    data = request.get_json()
    model_name = data.get("model_name")
    
    try:
        set_global_model(model_name)
        return jsonify({"status": "success", "message": f"Model changed to {model_name}"})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    data = request.get_json()
    user_id = data.get("user_id", "default_user")  # Assuming you are handling users
    question = data.get("message")
    
    # Get agent's response
    response = call_agent(data)
    
    # Store chat in SQLite
    insert_chat_history(user_id, question, response)
    
    message = {"answer": response}
    return jsonify(message)

@app.post("/predict_v1")
def predict_v1():
    data = request.get_json()
    user_id = data.get("user_id", "default_user")
    question = data.get("message")
    
    # Get agent's response
    response = call_agent_v1(question)
    
    # Store chat in SQLite
    insert_chat_history(user_id, question, response)
    
    message = {"answer": response}
    return jsonify(message)

@app.post("/clear_history")
def clear_history():
    data = request.get_json()
    user_id = data.get("user_id", "default_user")  # Assuming you have user-specific histories
    
    try:
        clear_chat_history(user_id)
        return jsonify({"status": "success", "message": "Chat history cleared successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/get_history", methods=["GET"])
def get_history():
    user_id = request.args.get("user_id", "default_user")  # Assuming you are handling users
    try:
        history = get_chat_history(user_id)
        return jsonify({"status": "success", "history": history})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Flask route to get the requirements for a specific product
@app.route('/get_requirements', methods=['GET'])
def get_requirements():
    """
    Endpoint to retrieve the requirements for a specific product.

    Example usage: GET /get_requirements?product_name=Example+Product
    """
    requirements_name = request.args.get('requirements_name')
    
    if not requirements_name:
        return jsonify({"error": "Product name is required"}), 400
    
    # Retrieve the requirements from the database
    requirements = get_requirements_from_db(requirements_name)
    
    if requirements:
        return jsonify({"product_name": requirements_name, "requirements": requirements}), 200
    else:
        return jsonify({"error": "No requirements found for the given product"}), 404

@app.route('/get_functions', methods=['GET'])
def get_functions():
    """
    Endpoint to retrieve the functions for a specific product.

    Example usage: GET /get_functions?product_name=Example+Product
    """
    functions_name = request.args.get('functions_name')
    
    if not functions_name:
        return jsonify({"error": "Functions name is required"}), 400
    
    # Retrieve the functions from the database
    functions = get_functions_from_db(functions_name)
    
    if functions:
        return jsonify({"product_name": functions_name, "functions": functions}), 200
    else:
        return jsonify({"error": "No functions found for the given product"}), 404

@app.route('/get_products', methods=['GET'])
def get_products():
    """
    Endpoint to retrieve products for a specific category.

    Example usage: GET /get_products?products_name=Example+Category
    """
    products_name = request.args.get('products_name')
    
    if not products_name:
        return jsonify({"error": "products name is required"}), 400
    
    # Retrieve the products from the database
    products = get_products_from_db(products_name)
    
    if products:
        return jsonify({"category_name": products_name, "products": products}), 200
    else:
        return jsonify({"error": "No products found for the given category"}), 404

# todo
@app.route('/get_logical_connections', methods=['GET'])
def get_logical_connections():
    """
    Endpoint to retrieve products for a specific category.

    Example usage: GET /get_products?products_name=Example+Category
    """
    connections_name = request.args.get('connections_name')
    
    if not connections_name:
        return jsonify({"error": "connections_name name is required"}), 400
    
    # Retrieve the products from the database
    connection = get_logicalConnections_from_db(connections_name)
    
    if connection:
        return jsonify({"connections_name": connections_name, "products": connection}), 200
    else:
        return jsonify({"error": "No products found for the given category"}), 404


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5050)
