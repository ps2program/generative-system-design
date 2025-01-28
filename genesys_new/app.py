import sqlite3
# from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from graph.GraphBuilder import create_question_handling_graph, create_schema
from graph.models import set_global_model, get_global_model
from langchain_core.messages import RemoveMessage
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, send_from_directory, jsonify,request, make_response
import os
from dotenv import load_dotenv
import requests

import sqlite3
import json
from graph.ds_query_methods import *  # Use this if you run as a module
from database.schema_init import init_db
from langchain_core.messages import HumanMessage
# new db
# main.py
# from database.db_module import session, add_requirement, add_function, add_component
# from database.state_memory import *
# from database.state_memory import StateMemory
from database.state_memory import state_memory
from pubsub.pub_sub_manager import pubsub_manager
import threading
from flask import Response
# batch_requirement_upload()

# app = Flask(__name__)
app = Flask(__name__, static_folder='chat-app/build/static', template_folder='chat-app/build')
CORS(app)

# Initialize the default model
# set_global_model("OLLAMA_MISTRAL")
set_global_model("LOCAL")
# set_global_model("LLAMA3")
set_global_model("MISTRAL")
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
        
# generate_svg
def generate_svg(user_id, query):
    nextPrompt = HumanMessage(
        content=f"""
                your job is to give SVG for the asked question in 20x20

                    Here is the user's question:
                    \n ------- \n
                    {query}
                    \n ------- \n
                    do not say anything else. just give the svg for the icon in 20x20.  \n
                    
                    example-
                    an SVG for "CHAT" icon
                    
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path 
                        d="M10 1.5C5.30558 1.5 1.5 4.97613 1.5 9C1.5 11.3304 2.793 13.3912 4.83108 14.7466C4.72302 15.3251 4.39038 16.7554 4.24968 17.3401C4.15708 17.7233 4.62802 17.9612 4.93899 17.6768C5.42351 17.2294 6.14841 16.5868 6.53556 16.2527C7.68722 16.6316 8.90597 16.8548 10 16.8548C14.6944 16.8548 18.5 13.3787 18.5 9C18.5 4.97613 14.6944 1.5 10 1.5ZM6.5 8.5C7.05228 8.5 7.5 8.94772 7.5 9.5C7.5 10.0523 7.05228 10.5 6.5 10.5C5.94772 10.5 5.5 10.0523 5.5 9.5C5.5 8.94772 5.94772 8.5 6.5 8.5ZM10 8.5C10.5523 8.5 11 8.94772 11 9.5C11 10.0523 10.5523 10.5 10 10.5C9.44772 10.5 9 10.0523 9 9.5C9 8.94772 9.44772 8.5 10 8.5ZM13.5 8.5C14.0523 8.5 14.5 8.94772 14.5 9.5C14.5 10.0523 14.0523 10.5 13.5 10.5C12.9477 10.5 12.5 10.0523 12.5 9.5C12.5 8.94772 12.9477 8.5 13.5 8.5Z" 
                        fill="#000000"/>
                    </svg>

                """
            )   
    model = get_global_model()
    
    response = model.invoke([nextPrompt])
    return response
  

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
    insert_chat_history(user_id, question, response['content'])

    # insert_chat_history(user_id, question['question'], response['content'])
    
    message = {"answer": response}
    return jsonify(message)

# #  1. closing connection when done
# @app.post("/predict_stream")
# def predict_stream():
#     data = request.get_json()
#     user_id = data.get("user_id", "default_user")

#     # Subscribe to PubSubManager
#     queue = pubsub_manager.subscribe()

#     # A flag to indicate when the worker is done processing
#     processing_complete = threading.Event()

#     def worker():
#         try:
#             with app.app_context():  # Push Flask application context
#                 call_agent(data)  # Call the handler that publishes responses to the queue
#         finally:
#             pubsub_manager.unsubscribe(queue)  # Clean up the subscription
#             processing_complete.set()  # Signal that processing is complete

#     # Start the worker in a separate thread
#     threading.Thread(target=worker, daemon=True).start()
#     from queue import Empty

#     def stream_responses():
#         try:
#             while not processing_complete.is_set() or not queue.empty():
#                 try:
#                     message = queue.get(timeout=1)
#                     if message is not None:
#                         yield f"data: {json.dumps(message)}\n\n"
#                 except Empty:  # Use the imported Empty exception
#                     continue
#         finally:
#             yield "data: [END]\n\n"

#     return Response(stream_responses(), content_type="text/event-stream")

# 2. streaming with history maintenance
@app.post("/predict_stream")
def predict_stream():
    data = request.get_json()
    user_id = data.get("user_id", "default_user")  # Assuming you are handling users
    question = data.get("message")
    # Subscribe to PubSubManager
    queue = pubsub_manager.subscribe()

    # A flag to indicate when the worker is done processing
    processing_complete = threading.Event()

    # List to accumulate all responses
    accumulated_responses = []

    def worker():
        try:
            with app.app_context():  # Push Flask application context
                question = data.get("message")
                
                # Call the handler that publishes responses to the queue
                call_agent(data)
                
        finally:
            pubsub_manager.unsubscribe(queue)  # Clean up the subscription
            processing_complete.set()  # Signal that processing is complete

    # Start the worker in a separate thread
    threading.Thread(target=worker, daemon=True).start()

    from queue import Empty

    def stream_responses():
        accumulated_responses = []  # Initialize a list to accumulate responses
        try:
            while not processing_complete.is_set() or not queue.empty():
                try:
                    message = queue.get(timeout=1)
                    if message is not None:
                        # Accumulate responses
                        if "data" in message:
                            accumulated_responses.append(json.dumps(message["data"]))  # Serialize dict to string
                        yield f"data: {json.dumps(message)}\n\n"
                except Empty:  # Handle queue empty exceptions
                    continue
        finally:
            # Commit the accumulated responses to the database at the end
            if accumulated_responses:
                final_response = "\n".join(accumulated_responses)  # Join serialized strings
                insert_chat_history(user_id, question, final_response)
            yield "data: [END]\n\n"


    return Response(stream_responses(), content_type="text/event-stream")


# for getting SVG directly using model. not using Model

@app.post("/getSVG")
def get_svg():
    data = request.get_json()
    user_id = data.get("user_id", "default_user")  # Assuming user-specific SVGs are handled

    try:
        # Assuming `generate_svg` generates or retrieves the SVG content as a string
        svg_content = generate_svg(user_id, data)

        if not svg_content:
            return jsonify({"status": "error", "message": "No SVG content found."}), 404

        # Sending SVG content as plain text to the client
        response = make_response(svg_content.content)
        return svg_content.content
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.post("/generic_endpoint")
def get_generic_answer():
    try:
        # Extract JSON data from the request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400
        
        # Get the user_id from the request payload, defaulting to 'default_user' if not provided
        user_id = data.get("user_id", "default_user")
        
        # Get the query from the request payload
        query = data.get("query")
        if not query:
            return jsonify({"error": "Missing 'query' in the request payload"}), 400

        # Prepare the next prompt for the model
        next_prompt = HumanMessage(
            content=f"""
            ------- 
            {query}
            ------- 
            """
        )

        # Retrieve the global model instance
        model = get_global_model()

        # Invoke the model with the prepared prompt
        response = model.invoke([next_prompt])

        # Return the model's response
        # return jsonify({"user_id": user_id, "response": response.content}), 200
        return response.content
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500

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
    url = os.getenv('NETVIBES_API_URL')
    bearer_token = os.getenv('NETVIBES_BEARER_TOKEN')

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }

    try:
        # response = ensure_session_id()
        # if response:
        #     return response
    
        response = requests.get(url, headers=headers)
        # response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return jsonify(data)
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
        return jsonify({"status": "success", "message": f"Requirement added with ID {requirement.id}", "requirement": requirement.data,"uuid": str(requirement.uuid)} ), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/add_sub_requirement", methods=["POST"])
def add_sub_requirement_route():
    data = request.get_json()
    parent_requirement_id = data.get("parent_requirement_id")
    sub_requirement_data = data.get("data")

    try:
        sub_requirement = add_sub_requirement(session, parent_requirement_id, sub_requirement_data)
        return jsonify({"status": "success", "message": f"Sub-requirement added with ID {sub_requirement.id}", "sub_requirement": sub_requirement.data, "uuid": str(sub_requirement.uuid)}), 201
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


# ___________________________________________NON AI CRUD Routes______________________________

from uuid import UUID

# Instantiate the StateMemory
# state_memory = StateMemory()


def is_valid_uuid(uuid_to_test):
    try:
        UUID(str(uuid_to_test))
        return True
    except ValueError:
        return False


@app.route("/components", methods=["POST"])
def create_component():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    if not name:
        return jsonify({"error": "Component name is required"}), 400

    component = state_memory.add_component(name, description)
    return jsonify({"id": str(component.id), "name": component.name, "description": component.description}), 201


@app.route("/components/<component_id>", methods=["GET"])
def get_component(component_id):
    if not is_valid_uuid(component_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    component = state_memory.get_component(UUID(component_id))
    if not component:
        return jsonify({"error": "Component not found"}), 404

    return jsonify({"id": str(component.id), "name": component.name, "description": component.description})


@app.route("/components/<component_id>", methods=["PUT"])
def update_component(component_id):
    if not is_valid_uuid(component_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    data = request.json
    new_name = data.get("name")
    new_description = data.get("description")

    try:
        component = state_memory.update_component(UUID(component_id), new_name, new_description)
        return jsonify({"id": str(component.id), "name": component.name, "description": component.description})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@app.route("/components/<component_id>", methods=["DELETE"])
def delete_component(component_id):
    if not is_valid_uuid(component_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    state_memory.delete_component(UUID(component_id))
    return jsonify({"message": "Component deleted"}), 204


@app.route("/requirements", methods=["POST"])
def create_requirement():
    data = request.json
    component_id = data.get("component_id")
    req_data = data.get("data")

    if not component_id or not req_data:
        return jsonify({"error": "Component ID and requirement data are required"}), 400

    if not is_valid_uuid(component_id):
        return jsonify({"error": "Invalid UUID format for component_id"}), 400

    try:
        requirement = state_memory.add_requirement(UUID(component_id), req_data)
        return jsonify({"id": str(requirement.id), "data": requirement.data}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# @app.route("/requirements/<requirement_id>", methods=["GET"])
# def get_requirement(requirement_id):
#     if not is_valid_uuid(requirement_id):
#         return jsonify({"error": "Invalid UUID format"}), 400

#     requirement = state_memory.get_requirement(UUID(requirement_id))
#     if not requirement:
#         return jsonify({"error": "Requirement not found"}), 404

#     return jsonify({"id": str(requirement.id), "data": requirement.data})

@app.route("/requirements/<requirement_id>", methods=["GET"])
def get_requirement(requirement_id):
    if not is_valid_uuid(requirement_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    requirement = state_memory.get_requirement(UUID(requirement_id))
    if not requirement:
        return jsonify({"error": "Requirement not found"}), 404

    # Serialize the requirement including its parent and sub-requirement IDs
    response_data = {
        "id": str(requirement.id),
        "data": requirement.data,
        "parent_requirements": [str(parent.id) for parent in requirement.parent_requirements],
        "sub_requirements": [str(sub.id) for sub in requirement.sub_requirements],
    }

    return jsonify(response_data), 200

@app.route("/requirements/<requirement_id>", methods=["PUT"])
def update_requirement(requirement_id):
    if not is_valid_uuid(requirement_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    data = request.json
    new_data = data.get("data")

    try:
        requirement = state_memory.update_requirement(UUID(requirement_id), new_data)
        return jsonify({"id": str(requirement.id), "data": requirement.data})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@app.route("/requirements/<requirement_id>", methods=["DELETE"])
def delete_requirement(requirement_id):
    if not is_valid_uuid(requirement_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    state_memory.delete_requirement(UUID(requirement_id))
    return jsonify({"message": "Requirement deleted"}), 204


@app.route("/functions", methods=["POST"])
def create_function():
    data = request.json
    func_data = data.get("data")

    if not func_data:
        return jsonify({"error": "Function data is required"}), 400

    function = state_memory.add_function(func_data)
    return jsonify({"id": str(function.id), "data": function.data}), 201

@app.route("/functions/<function_id>", methods=["GET"])
def get_function(function_id):
    if not is_valid_uuid(function_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    function = state_memory.get_function(UUID(function_id))
    if not function:
        return jsonify({"error": "Function not found"}), 404

    # Serialize the function data, including parent and sub-functions
    response_data = {
        "id": str(function.id),
        "data": function.data,
        "parent_functions": [str(parent.id) for parent in function.parent_functions],
        "sub_functions": [str(sub.id) for sub in function.sub_functions],
        "requirements": [str(requirement.id) for requirement in function.requirements],
        "physicals": [str(physical.id) for physical in function.physicals]
    }

    return jsonify(response_data), 200

@app.route("/functions/<function_id>", methods=["PUT"])
def update_function(function_id):
    if not is_valid_uuid(function_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    data = request.json
    new_data = data.get("data")

    try:
        function = state_memory.update_function(UUID(function_id), new_data)
        return jsonify({"id": str(function.id), "data": function.data})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@app.route("/functions/<function_id>", methods=["DELETE"])
def delete_function(function_id):
    if not is_valid_uuid(function_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    state_memory.delete_function(UUID(function_id))
    return jsonify({"message": "Function deleted"}), 204


@app.route("/physicals", methods=["POST"])
def create_physical():
    data = request.json
    phys_data = data.get("data")

    if not phys_data:
        return jsonify({"error": "Physical data is required"}), 400

    physical = state_memory.add_physical(phys_data)
    return jsonify({"id": str(physical.id), "data": physical.data}), 201


# @app.route("/physicals/<physical_id>", methods=["GET"])
# def get_physical(physical_id):
#     if not is_valid_uuid(physical_id):
#         return jsonify({"error": "Invalid UUID format"}), 400

#     physical = state_memory.get_physical(UUID(physical_id))
#     if not physical:
#         return jsonify({"error": "Physical not found"}), 404

#     return jsonify({"id": str(physical.id), "data": physical.data})

@app.route("/physicals/<physical_id>", methods=["GET"])
def get_physical(physical_id):
    if not is_valid_uuid(physical_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    physical = state_memory.get_physical(UUID(physical_id))
    if not physical:
        return jsonify({"error": "Physical not found"}), 404

    # Serialize the physical data, including parent and sub-physical IDs
    response_data = {
        "id": str(physical.id),
        "data": physical.data,
        "parent_physicals": [str(parent.id) for parent in physical.parent_physicals],
        "sub_physicals": [str(sub.id) for sub in physical.sub_physicals],
        "functions": [str(function.id) for function in physical.functions],
        "requirements": [str(requirement.id) for requirement in physical.requirements],
    }

    return jsonify(response_data), 200


@app.route("/physicals/<physical_id>", methods=["PUT"])
def update_physical(physical_id):
    if not is_valid_uuid(physical_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    data = request.json
    new_data = data.get("data")

    try:
        physical = state_memory.update_physical(UUID(physical_id), new_data)
        return jsonify({"id": str(physical.id), "data": physical.data})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@app.route("/physicals/<physical_id>", methods=["DELETE"])
def delete_physical(physical_id):
    if not is_valid_uuid(physical_id):
        return jsonify({"error": "Invalid UUID format"}), 400

    state_memory.delete_physical(UUID(physical_id))
    return jsonify({"message": "Physical deleted"}), 204

@app.route('/all-entities-unrelated', methods=['GET'])
def get_all_entities_unrelated():
    try:
        data = state_memory.get_all_entities()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# miscellaneous routes

@app.route('/get_all_components', methods=['GET'])
def get_all_components():
    try:
        data = state_memory.get_all_components()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_all_requirements', methods=['GET'])
def get_all_requirements():
    try:
        data = state_memory.get_all_requirements()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_all_functions', methods=['GET'])
def get_all_functions():
    try:
        data = state_memory.get_all_functions()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_all_physicals', methods=['GET'])
def get_all_physicals():
    try:
        data = state_memory.get_all_physicals()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/clear_all', methods=['POST'])
def clear_all():
    """
    Endpoint to clear all components, requirements, functions, and physicals.
    """
    state_memory.clear_all()
    return jsonify({
        "message": "All components, requirements, functions, and physicals have been cleared.",
        "state": repr(state_memory)
    }), 200


#  _______________________relational endpoints___________________

# 1. Different Entities__________________________________________
@app.route('/add_function_to_requirement', methods=['POST'])
def add_function_to_requirement():
    try:
        data = request.json
        function_id = data.get('function_id')
        requirement_id = data.get('requirement_id')

        if not function_id or not requirement_id:
            return jsonify({"error": "Function ID and Requirement ID are required."}), 400

        # Convert IDs to UUID objects
        try:
            function_id = UUID(function_id)
            requirement_id = UUID(requirement_id)
        except ValueError:
            return jsonify({"error": "Invalid UUID format for Function ID or Requirement ID."}), 400

        state_memory.add_function_to_requirement(function_id, requirement_id)
        return jsonify({"message": "Function successfully associated with requirement."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

@app.route('/add_physical_to_requirement', methods=['POST'])
def add_physical_to_requirement():
    try:
        data = request.json
        physical_id = data.get('physical_id')
        requirement_id = data.get('requirement_id')

        if not physical_id or not requirement_id:
            return jsonify({"error": "Physical ID and Requirement ID are required."}), 400

        # Convert IDs to UUID objects
        try:
            physical_id = UUID(physical_id)
            requirement_id = UUID(requirement_id)
        except ValueError:
            return jsonify({"error": "Invalid UUID format for Physical ID or Requirement ID."}), 400

        state_memory.add_physical_to_requirement(physical_id, requirement_id)
        return jsonify({"message": "Physical successfully associated with requirement."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

@app.route('/add_physical_to_function', methods=['POST'])
def add_physical_to_function():
    try:
        data = request.json
        physical_id = data.get('physical_id')
        function_id = data.get('function_id')

        if not physical_id or not function_id:
            return jsonify({"error": "Physical ID and Function ID are required."}), 400

        # Convert IDs to UUID objects
        try:
            physical_id = UUID(physical_id)
            function_id = UUID(function_id)
        except ValueError:
            return jsonify({"error": "Invalid UUID format for Physical ID or Function ID."}), 400

        system.add_physical_to_function(physical_id, function_id)
        return jsonify({"message": "Physical successfully associated with function."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

# 2. Exisiting Node - Self Referential____________________________
## 1. Associate a sub-requirement with a parent requirement
@app.route('/associate_sub_requirement_to_parent_requirement', methods=['POST'])
def associate_sub_requirement_to_parent_requirement():
    try:
        data = request.json
        parent_requirement_id = data.get('parent_requirement_id')
        sub_requirement_id = data.get('sub_requirement_id')

        if not parent_requirement_id or not sub_requirement_id:
            return jsonify({"status": "error", "message": "Parent Requirement ID and Sub Requirement ID are required."}), 400

        parent_requirement_id = validate_uuid(parent_requirement_id, "Parent Requirement ID")
        sub_requirement_id = validate_uuid(sub_requirement_id, "Sub Requirement ID")

        # Call the method to associate the sub-requirement with the parent requirement
        state_memory.associate_sub_requirement_to_parent_requirement(sub_requirement_id, parent_requirement_id)
        
        return jsonify({"status": "success", "message": "Sub-requirement successfully associated with parent requirement."}), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": "An error occurred.", "details": str(e)}), 500

## 2. functions to subfunctions
@app.route('/associate_sub_function_to_function', methods=['POST'])
def associate_sub_function_to_function():
    try:
        data = request.json
        function_id = data.get('function_id')
        sub_function_id = data.get('sub_function_id')

        if not function_id or not sub_function_id:
            return jsonify({"status": "error", "message": "Function ID and Sub-Function ID are required."}), 400

        # Validate IDs
        function_id = validate_uuid(function_id, "Function ID")
        sub_function_id = validate_uuid(sub_function_id, "Sub-Function ID")

        # Associate Sub-Function with Function
        state_memory.associate_sub_function_to_function(sub_function_id, function_id)
        return jsonify({"status": "success", "message": f"Sub-Function {sub_function_id} successfully associated with Function {function_id}."}), 200

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": "An error occurred.", "details": str(e)}), 500

##  3. physical to  sub-physicals
@app.route('/associate_sub_physical_to_physical', methods=['POST'])
def associate_sub_physical_to_physical():
    try:
        data = request.json
        physical_id = data.get('physical_id')
        sub_physical_id = data.get('sub_physical_id')

        if not physical_id or not sub_physical_id:
            return jsonify({"status": "error", "message": "Physical ID and Sub-Physical ID are required."}), 400

        # Validate IDs
        physical_id = validate_uuid(physical_id, "Physical ID")
        sub_physical_id = validate_uuid(sub_physical_id, "Sub-Physical ID")

        # Associate Sub-Physical with Physical
        state_memory.associate_sub_physical_to_physical(sub_physical_id, physical_id)
        return jsonify({"status": "success", "message": f"Sub-Physical {sub_physical_id} successfully associated with Physical {physical_id}."}), 200

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": "An error occurred.", "details": str(e)}), 500


# 3. New Nodes - Self Referential__________________________________
# Helper function to validate UUID
def validate_uuid(id_str, field_name):
    try:
        return UUID(id_str)
    except ValueError:
        raise ValueError(f"Invalid UUID format for {field_name}.")

## 1. Add a sub-requirement to a requirement
@app.route('/add_sub_requirement_to_requirement', methods=['POST'])
def add_sub_requirement_to_requirement():
    try:
        data = request.json
        parent_requirement_id = data.get('parent_requirement_id')
        sub_requirement_data = data.get('sub_requirement_data')

        if not parent_requirement_id or not sub_requirement_data:
            return jsonify({"status": "error", "message": "Parent Requirement ID and Sub-Requirement Data are required."}), 400

        parent_requirement_id = validate_uuid(parent_requirement_id, "Parent Requirement ID")

        sub_requirement = state_memory.add_sub_requirement_to_requirement(parent_requirement_id, sub_requirement_data)
        return jsonify({"status": "success", "message": f"Sub-requirement added with ID {sub_requirement.id}", "requirement": sub_requirement.to_dict()}), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": "An error occurred.", "details": str(e)}), 500

@app.route('/add_sub_function_to_function', methods=['POST'])
def add_sub_function_to_function():
    try:
        data = request.json
        parent_function_id = data.get('parent_function_id')
        sub_function_data = data.get('sub_function_data')

        if not parent_function_id or not sub_function_data:
            return jsonify({"status": "error", "message": "Parent Function ID and Sub-Function Data are required."}), 400

        parent_function_id = validate_uuid(parent_function_id, "Parent Function ID")

        sub_function = state_memory.add_sub_function_to_function(parent_function_id, sub_function_data)
        return jsonify({"status": "success", "message": f"Sub-function added with ID {sub_function.id}", "function":sub_function.to_dict()}), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": "An error occurred.", "details": str(e)}), 500

@app.route('/add_sub_physical_to_physical', methods=['POST'])
def add_sub_physical_to_physical():
    try:
        data = request.json
        parent_physical_id = data.get('parent_physical_id')
        sub_physical_data = data.get('sub_physical_data')

        if not parent_physical_id or not sub_physical_data:
            return jsonify({"status": "error", "message": "Parent Physical ID and Sub-Physical Data are required."}), 400

        parent_physical_id = validate_uuid(parent_physical_id, "Parent Physical ID")

        sub_physical = state_memory.add_sub_physical_to_physical(parent_physical_id, sub_physical_data)
        return jsonify({"status": "success", "message": f"Sub-physical added with ID {sub_physical.id}", "physical": sub_physical.to_dict()}), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": "An error occurred.", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5050)
