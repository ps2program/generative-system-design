import sqlite3
# from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from graph.GraphBuilder import create_question_handling_graph, create_schema
from graph.models import set_global_model, get_global_model
from langchain_core.messages import RemoveMessage
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, send_from_directory, jsonify,request
import os
# from dotenv import load_dotenv
import requests

import sqlite3
import json
from graph.ds_query_methods import *  # Use this if you run as a module
from database.schema_init import init_db

# new db
# main.py
# from database.db_module import session, add_requirement, add_function, add_component
from database.state_memory import *


# app = Flask(__name__)
# app = Flask(__name__, static_folder='chat-app/build/static', template_folder='chat-app/build')   # for the server side chat-app UI

# for generative-system-design-frontend
app = Flask(__name__, static_folder='generative_system_design_frontend/build/static', template_folder='generative_system_design_frontend/build')

CORS(app)

# Initialize the default model
# set_global_model("OLLAMA_MISTRAL")
set_global_model("LOCAL")
# set_global_model("LLAMA3")
# set_global_model("MISTRAL")
graph = create_question_handling_graph()
config = {"configurable": {"thread_id": "1"}}

# _______________________________________________archival memory setup

# Import the session from the SQLAlchemy setup
from sqlalchemy.orm import Session
from datetime import datetime
from database.archival_memory import Archival_Session, Archival_ChatHistory

# Insert chat history
def insert_chat_history(user_id, question, answer):
    archival_session = Archival_Session()
    try:
        new_chat = Archival_ChatHistory(user_id=user_id, question=question, answer=answer, timestamp=datetime.now())
        archival_session.add(new_chat)
        archival_session.commit()
    except Exception as e:
        archival_session.rollback()
        print(f"Error inserting chat history: {e}")
    finally:
        archival_session.close()

# Get chat history for a specific user
def get_chat_history(user_id):
    archival_session = Archival_Session()
    try:
        history = archival_session.query(Archival_ChatHistory).filter(Archival_ChatHistory.user_id == user_id).all()
        return [
            {"question": record.question, "answer": record.answer, "timestamp": record.timestamp}
            for record in history
        ]
    except Exception as e:
        print(f"Error retrieving chat history: {e}")
        return []
    finally:
        archival_session.close()

# Clear chat history for a specific user
def clear_chat_history(user_id):
    archival_session = Archival_Session()
    try:
        archival_session.query(Archival_ChatHistory).filter(Archival_ChatHistory.user_id == user_id).delete()
        archival_session.commit()
    except Exception as e:
        archival_session.rollback()
        print(f"Error clearing chat history: {e}")
    finally:
        archival_session.close()

# endpoints

@app.post("/clear_history")
def clear_history():
    data = request.get_json()
    user_id = data.get("user_id", "default_user")  # Assuming you have user-specific histories

    def delete_messages():
        # Assuming `graph` and `config` are pre-defined elsewhere in your application
        messages = graph.get_state(config).values["messages"]
        for message in messages:
            graph.update_state(config, {"messages": RemoveMessage(id=message.id)})

    try:
        # Clear chat history from the database
        clear_chat_history(user_id)
        # Clear in-memory messages if applicable
        delete_messages()

        return jsonify({"status": "success", "message": "Chat history cleared successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/get_history", methods=["GET"])
def get_history():
    user_id = request.args.get("user_id", "default_user")  # Assuming you are handling users
    try:
        # Retrieve chat history from the database
        history = get_chat_history(user_id)
        return jsonify({"status": "success", "history": history})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



# __________________________________________________
# before archival
# # SQLite3 setup
# DATABASE = 'chat_history.db'
# # Initialize the database
# init_db()


# def insert_chat_history(user_id, question, answer):
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#     cursor.execute('''INSERT INTO chat_history (user_id, question, answer) VALUES (?, ?, ?)''',
#                    (user_id, question, answer))
#     conn.commit()
#     conn.close()

# def get_chat_history(user_id):
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#     cursor.execute('''SELECT question, answer, timestamp FROM chat_history WHERE user_id=?''', (user_id,))
#     history = cursor.fetchall()
#     conn.close()
#     return history

# def clear_chat_history(user_id):
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#     cursor.execute('''DELETE FROM chat_history WHERE user_id=?''', (user_id,))
#     conn.commit()
#     conn.close()

# Swagger setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Agent function to handle user input
def call_agent(data):
    
        # Check if 'message' and 'question' keys exist in data
    if 'message' in data and 'question' in data['message']:
        inputs = {
            "messages": [
                ("user", data['message']['question']),
            ],
            "questionType": data['message'].get('questionType')  # Use .get() for optional keys
        }
    else:
        inputs = {
            "messages": [
                ("user", data['message'])
            ]
        }
    
    config = {"configurable": {"thread_id": "1"}}
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

# @app.get("/")
# def index_get():
#     return render_template("base.html")

# before archival memory
@app.post("/predict")
def predict():
    data = request.get_json()
    user_id = data.get("user_id", "default_user")  # Assuming you are handling users
    question = data.get("message")
    
    # Get agent's response
    response = call_agent(data)
    
    # Store chat in SQLite
    insert_chat_history(user_id, question['question'], response['content'])
    
    message = {"answer": response}
    return jsonify(message)

# after archival
# @app.post("/predict")
# def predict():
#     data = request.get_json()
#     user_id = data.get("user_id", "default_user")  # Assuming you are handling users
#     question = data.get("message")

#     if not question:
#         return jsonify({"status": "error", "message": "Message is required."}), 400

#     try:
#         # Get agent's response
#         response = call_agent(data)

#         # Store chat in the database
#         insert_chat_history(user_id, question, response.get("content", ""))

#         message = {"answer": response}
#         return jsonify(message)

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500

# before archival
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

# after archival
# @app.post("/predict_v1")
# def predict_v1():
#     data = request.get_json()
#     user_id = data.get("user_id", "default_user")
#     question = data.get("message")

#     if not question:
#         return jsonify({"status": "error", "message": "Message is required."}), 400

#     try:
#         # Get agent's response
#         response = call_agent_v1(question)

#         # Store chat in the database
#         insert_chat_history(user_id, question, response)

#         message = {"answer": response}
#         return jsonify(message)

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500

# # before archival
# @app.post("/clear_history")
# def clear_history():
#     data = request.get_json()
#     user_id = data.get("user_id", "default_user")  # Assuming you have user-specific histories
    
#     def delete_messages():
#         messages = graph.get_state(config).values["messages"]
#         for message in messages:
#             graph.update_state(config, {"messages": RemoveMessage(id=message.id)})
            
    
#     try:
#         clear_chat_history(user_id)
#         delete_messages()
        
#         return jsonify({"status": "success", "message": "Chat history cleared successfully."})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500

# @app.route("/get_history", methods=["GET"])
# def get_history():
#     user_id = request.args.get("user_id", "default_user")  # Assuming you are handling users
#     try:
#         history = get_chat_history(user_id)
#         return jsonify({"status": "success", "history": history})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500

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

# ______________________________


# Route to serve React app at the root
@app.route('/')
def serve_react_app():
    return send_from_directory(app.template_folder, 'index.html')

# Serve static files (JS, CSS, etc.)
@app.route('/static/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder + '/static', path)

@app.route("/get_available_models", methods=["GET"])
def get_available_models():
    """
    Endpoint to fetch available models from the external service.
    """
    try:
        result = {
            "data": [
                {
                "id": "LLAMA-3.2"
                },
                {
                "id": "GPT-4o"
                },
                {
                "id": "Local "
                }
            ]
        }

        return jsonify(result)
    except requests.exceptions.RequestException as e:
         return jsonify({"status": "error", "message": str(e)}), 500

# @app.route("/change_model", methods=["POST"])
# def change_model():
#     """
#     Endpoint to change the current model for a session.
#     """
#     # response = ensure_session_id()
#     # if response:
#     #     return response
    
#     # app_instance, graph, model_manager = get_user_app_instance()
    
#     data = request.get_json()
#     model_name = data.get("model_name")
    
#     try:
#         set_global_model(model_name)
#         # model_manager.set_model(model_name)  # Set model only for this instance
#         return jsonify({"status": "success", "message": f"Model changed to {model_name}"})
#     except ValueError as e:
#         return jsonify({"status": "error", "message": str(e)}), 400

# Run the Flask app


# New database routes for all crud operations

@app.route("/add_component", methods=["POST"])
def add_component_route():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    
    try:
        component = add_component(session, name, description)
        return jsonify({
            "status": "success", 
            "message": f"Component '{component.name}' added successfully", 
            "component": {"uuid": str(component.uuid), "name": component.name, "description": component.description}
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/add_requirement", methods=["POST"])
def add_requirement_route():
    data = request.get_json()
    component_id = data.get("component_id")
    requirement_data = data.get("data")

    try:
        requirement = add_requirement(session, component_id, requirement_data)
        return jsonify({"status": "success", "message": f"Requirement added with ID {requirement.id}", "requirement": requirement.data}), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/add_sub_requirement", methods=["POST"])
def add_sub_requirement_route():
    data = request.get_json()
    parent_requirement_id = data.get("parent_requirement_id")
    sub_requirement_data = data.get("data")

    try:
        sub_requirement = add_sub_requirement(session, parent_requirement_id, sub_requirement_data)
        return jsonify({"status": "success", "message": f"Sub-requirement added with ID {sub_requirement.id}", "sub_requirement": sub_requirement.data}), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/add_function", methods=["POST"])
def add_function_route():
    data = request.get_json()
    function_data = data.get("data")

    try:
        function = add_function(session, function_data)
        return jsonify({"status": "success", "message": f"Function added with ID {function.id}", "function": function.data}), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/add_sub_function", methods=["POST"])
def add_sub_function_route():
    data = request.get_json()
    parent_function_id = data.get("parent_function_id")
    sub_function_data = data.get("data")

    try:
        sub_function = add_sub_function(session, parent_function_id, sub_function_data)
        return jsonify({"status": "success", "message": f"Sub-function added with ID {sub_function.id}", "sub_function": sub_function.data}), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/add_physical", methods=["POST"])
def add_physical_route():
    data = request.get_json()
    physical_data = data.get("data")

    try:
        physical = add_physical(session, physical_data)
        return jsonify({"status": "success", "message": f"Physical added with ID {physical.id}", "physical": physical.data}), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    
@app.route("/add_sub_physical", methods=["POST"])
def add_sub_physical_route():
    data = request.get_json()
    parent_physical_id = data.get("parent_physical_id")
    sub_physical_data = data.get("data")

    try:
        sub_physical = add_sub_physical(session, parent_physical_id, sub_physical_data)
        return jsonify({"status": "success", "message": f"Sub-physical added with ID {sub_physical.id}", "sub_physical": sub_physical.data}), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/get_requirement/<uuid:requirement_id>", methods=["GET"])
def get_requirement_route(requirement_id):
    try:
        requirement = session.query(Requirement).filter_by(uuid=requirement_id).first()
        if not requirement:
            return jsonify({"status": "error", "message": "Requirement not found"}), 404
        return jsonify({"status": "success", "requirement": requirement.data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/get_function/<uuid:function_id>", methods=["GET"])
def get_function_route(function_id):
    try:
        function = session.query(Function).filter_by(uuid=function_id).first()
        if not function:
            return jsonify({"status": "error", "message": "Function not found"}), 404
        return jsonify({"status": "success", "function": function.data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/get_physical/<uuid:physical_id>", methods=["GET"])
def get_physical_route(physical_id):
    try:
        physical = session.query(Physical).filter_by(uuid=physical_id).first()
        if not physical:
            return jsonify({"status": "error", "message": "Physical not found"}), 404
        return jsonify({"status": "success", "physical": physical.data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/search_components", methods=["GET"])
def search_components():
    partial_name = request.args.get("name")
    if not partial_name:
        return jsonify({"status": "error", "message": "Name parameter is required"}), 400

    try:
        components = search_components_by_name(session, partial_name)
        components_data = [{"id": c.id, "name": c.name} for c in components]
        return jsonify({"status": "success", "components": components_data})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404

# to get connected entries when a particular entry is changed
@app.route("/get_associated_data", methods=["POST"])
def get_associated_data_endpoint():
    data = request.get_json()
    updated_id = data.get("id")
    model_type = data.get("model_type")

    if not updated_id or not model_type:
        return jsonify({"status": "error", "message": "Both 'id' and 'model_type' are required"}), 400

    try:
        results = get_associated_data(session, updated_id, model_type)
        return jsonify({"status": "success", "data": results})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5050)
