import os
from langgraph.graph import END, StateGraph
from graph.AgentState import AgentState
from langchain_core.messages import HumanMessage
# from langchain_core.pydantic_v1 import BaseModel, Field
from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts import PromptTemplate
# from langgraph.checkpoint.sqlite import SqliteSaver
from flask import Flask, jsonify, request
from datetime import datetime
from graph.models import set_global_model, get_global_model, get_tool_model
from langchain_core.utils.function_calling import convert_to_openai_tool
from graph.CustomStructuredOutputHandler import CustomStructuredOutputHandler
# from ..database_utils.datase_query_methods import *
from graph.ds_query_methods import *  # Use this if you run as a module
from langgraph.checkpoint.memory import MemorySaver


# memory = SqliteSaver.from_conn_string(":memory:")
checkpointer = MemorySaver()
config = {"configurable": {"thread_id": "1"}}
default_app = None

import sqlite3
import json

# Path to the database file
DATABASE = 'chat_history.db'


def create_question_handling_graph():
    global default_app
    
    workflow = StateGraph(AgentState)
    workflow.set_entry_point("analyze_question")
    
    # Temporary condition based on the LLM model for structured output.
    model = get_global_model()
    workflow.add_node("analyze_question", analyze_question_type_main)

    # Conditional edges to route based on question type
    workflow.add_conditional_edges(
        "analyze_question",
        route_to_next_node,  # Route logic
        {
            "handle_general_question": "handle_general_question",
            "handle_list_question_with_subgraph": "handle_list_question_with_subgraph",  # List question logic contains your case
            "handle_option_question": "handle_option_question",
            "handle_tag_question": "handle_tag_question",
            "handle_crud_operation": "handle_crud_operation",
        },
    )

    # Handlers for each question type
    workflow.add_node("handle_general_question", handle_general_question)
    workflow.add_node("handle_list_question_with_subgraph", handle_list_question_with_subgraph)  # Modified this to include subgraph handling
    workflow.add_node("handle_option_question", handle_option_question)
    workflow.add_node("handle_tag_question", handle_tag_question)
    workflow.add_node("handle_crud_operation", handle_crud_operation)

    # Nodes for handling requirements, logical connections, and products
    workflow.add_node("handle_requirements_question", handle_requirements_question)
    workflow.add_node("handle_functions_question", handle_functions_question)
    workflow.add_node("handle_logical_connections_question", handle_logical_connections_question)
    workflow.add_node("handle_products_question", handle_products_question)

    # Conditional routing for list question subgraph
    workflow.add_conditional_edges(
        "handle_list_question_with_subgraph",
        route_to_next_sub_node,  # This will route to the next sub node based on subgraph logic
        {
            "handle_requirements_question": "handle_requirements_question",
            "handle_functions_question": "handle_functions_question",
            "handle_logical_connections_question": "handle_logical_connections_question",
            "handle_products_question": "handle_products_question",
        },
    )

    # Define the end of each path
    workflow.add_edge("handle_general_question", END)
    workflow.add_edge("handle_requirements_question", END)
    workflow.add_edge("handle_functions_question", END)
    workflow.add_edge("handle_logical_connections_question", END)
    workflow.add_edge("handle_products_question", END)
    workflow.add_edge("handle_option_question", END)
    workflow.add_edge("handle_tag_question", END)
    workflow.add_edge("handle_crud_operation", END)
    
    # Compile and return the graph
    # graph = workflow.compile(checkpointer=memory)
    graph = workflow.compile(checkpointer=checkpointer)
    default_app = graph
    return graph

# top level question analyser
def analyze_question_type_main(state) -> Literal["general", "list", "options", "tag", "crud"]:
        """
        Analyze the user's prompt and determine if it is a general question, a question that requires a list of items, 
        an options question, a tag question, or a CRUD operation.

        Args:
            state (dict): The current state containing messages.

        Returns:
            dict: A dictionary with the response type and schema.
        """
        print("---DETERMINE QUESTION TYPE: GENERAL, LIST, OPTIONS, CRUD OR TAG---")

        class QuestionType(BaseModel):
            question_type: str = Field(description="The classification type of the question")

        # Define classifications
        classifications = {
            "general": "general",
            "list": "list",
            "options": "options",
            "tag": "tag",
            "crud": "crud"
        }
 
        # Prompt for classifying question
        prompt = PromptTemplate(
            template="""You are a grader assessing if a question is a general question, a list question, an options question, CRUD question or a tag question. \n
            Here is the user question: {question} \n
            
            "General" Question Criteria: If the user prompt contains a question mark ('?') or it is asking queries related to mechanical component, classify it as a general question.
            
            "List" Question Criteria: If the user prompt just mentions specific mechanical or electrical components with no context about it (e.g., 'Garage Door Opener', 'Electric Bike'), classify it as a list question. Also, Note: if user prompt asks for "Requirements", "Logical Connections", "Functions" or "products" related to a mechanical or electric component, then also categories this into "List Question". ('example - give requirements for Garage Door Opener')
            
            "Options" Question Criteria: If the user prompt asks for different choices or alternatives (e.g., 'What are my options for...'), classify it as an options question.
            Tag Question Criteria: If the user prompt asks for common tags related to a specific item or concept (e.g., 'What are the common tags related to...'), classify it as a tag question. \n
            
            "CRUD" Question Criteria:if the semantic meaning from the users prompts means to UPDATE,CREATE, READ, ADD, REAMOVE or DELETE then classify it as CRUD question
            examples - 'Add "Bluetooth" into requirements'
            example 2 '-garage door opener is in alaska'. this means user is asking to  to classify the prompt into CRUD because he wants to update the outputs for specific weather condition
            \n
            
            Classify the question as 'general', 'list', 'options', CRUD, or 'tag'.
            NOTE: you should only give response in either 'general', 'list', 'options', CRUD, or 'tag'. do not say anything else
            """,
            
            input_variables=["question"],
        )
 
        tool_model = get_global_model()
        custom_handler = CustomStructuredOutputHandler(tool_model)
        llm_with_tool = custom_handler.with_structured_output(QuestionType, classifications)
        
            # Extract the latest question from the state
        messages = state["messages"]
        question = messages[-1].content

        # Format the prompt using Langchain's PromptTemplate
        formatted_prompt = prompt.format(question=question)

        # Simulate a chain: Prompt template followed by the LLM with structured output
        chain = lambda data: llm_with_tool({"question": data["question"]})

        if state.get("questionType") and state["questionType"].get("subType"):
            question_type = state["questionType"]['type']
        else:
            scored_result = chain({"question": formatted_prompt})
            question_type = scored_result.question_type
        
        print(f"Question Type: {question_type}")

        if question_type == "general":
            print("---QUESTION TYPE: GENERAL---")
            response = "handle_general_question"
        elif question_type == "list":
            print("---QUESTION TYPE: LIST---")
            response = "handle_list_question"
        elif question_type == "options":
            print("---QUESTION TYPE: OPTIONS---")
            response = "handle_option_question"
        elif question_type == "tag":
            print("---QUESTION TYPE: TAG---")
            response = "handle_tag_question"
        elif question_type == "crud":
            print("---QUESTION TYPE: CRUD---")
            response = "handle_crud_operation"
        else:
            response = "unknown_question_type"

        # Create response schema
        agent_state = {
            "messages": [response],
            "response_schema": create_schema(response, "JSON_List_Handler")
        }
        
        return agent_state
#  sub level question analyser
def analyze_question_type_sub(state) -> Literal["requirements", "functions" "logical_connections", "products"]:
        """
        Analyze the user's prompt and determine if it is a "requirements", "logical_connections", or "products" type question.

        Args:
            state (dict): The current state containing messages.

        Returns:
            dict: A dictionary with the response type and schema.
        """
        print("---DETERMINE QUESTION TYPE: requirements,functions, logical_connections, products ---")

        class QuestionType(BaseModel):
            question_type: str = Field(description="The classification type of the question")

        # Define classifications
        classifications = {
            "requirements":"requirements",
            "functions":"functions",
            "logical_connections":"logical_connections", 
            "products":"products"
        }
        
        # Extract the latest question from the state
        messages = state["messages"]
        # question = messages[-1]["content"]
        question = messages[-2].content

        # Prompt for classifying sub-level questions
        prompt = PromptTemplate(
            template="""You are a grader assessing if a user question is asking for one of the following: ["requirements", "logical_connections", "products"]. 
            Here is the user question: {question} \n
            Classification Criteria:
            
            - **Requirements**: If the user is asking for specific needs, conditions, or criteria that something must fulfill (e.g., 'What are the requirements for a garage door opener?', 'What do I need to build a smart home system?'), classify it as a requirements question.
            
            - **Functions**: If the user is asking about the "functions" of a mechanical or electrical component (e.g., 'garage door opener's functions?'), classify it as a "functions" question.
            
            - **Logical_Connections**: If the user is asking about how things are related, interconnected, or about reasoning processes (e.g., 'How does the motor connect to the drive mechanism?', 'What is the relationship between power and speed in this system?'), classify it as a "logical_connections" question.
            
            - **Products**: If the user is asking about specific items, tools, or finished goods, or asking for suggestions about products (e.g., 'What are some good garage door openers?', 'Which electric bike models are recommended?'), classify it as a "Products" question.
            
            NOTE: you should only give response in either 'requirements', 'functions', 'logical_connections', or 'products'. do not say anything else.
            """,
            input_variables=["question"],
        )
        
        tool_model = get_global_model()
        custom_handler = CustomStructuredOutputHandler(tool_model)
        llm_with_tool = custom_handler.with_structured_output(QuestionType, classifications)

        # Format the prompt using Langchain's PromptTemplate
        formatted_prompt = prompt.format(question=question)

        # Simulate a chain
        chain = lambda data: llm_with_tool({"question": data["question"]})

        # Check if state["questionType"] and state["questionType"]['subType'] exist
        if state.get("questionType") and state["questionType"].get("subType"):
            question_type = state["questionType"]['subType']
        else:
            scored_result = chain({"question": formatted_prompt})
            question_type = scored_result.question_type

        print(f"Question Type: {question_type}")

        # Handle the response based on the classified question type
        if question_type == "requirements":
            print("---QUESTION TYPE: REQUIREMENTS---")
            response = "handle_requirements_question"
        elif question_type == "functions":
            print("---QUESTION TYPE: FUNCTIONS---")
            response = "handle_functions_question"
        elif question_type == "logical_connections":
            print("---QUESTION TYPE: LOGICAL CONNECTIONS---")
            response = "handle_logical_connections_question"
        elif question_type == "products":
            print("---QUESTION TYPE: PRODUCTS---")
            response = "handle_products_question"
        else:
            print("---UNKNOWN QUESTION TYPE---")
            response = "unknown_question_type"

        # Create response schema
        agent_state = {
            "messages": [response],
            "response_schema": create_schema(response, "JSON_List_Handler")
        }

        return agent_state

# sub level router-> requirements, functions, logical connections and products
def handle_list_question_with_subgraph(state):
    """
    This function processes list-type questions and determines whether the next step involves
    handling requirements, logical connections, or products.
    """
    
    # Analyze the question type for the subgraph
    sub_question_type = analyze_question_type_sub(state)
    
    # Return the sub-question type (this will be routed via `route_to_next_sub_node`)
    return sub_question_type

# top level router , list, general, options and tag
def route_to_next_node(state):
    last_response = state['messages'][-1].content
    if last_response == "handle_general_question":
        return "handle_general_question"
    elif last_response == "handle_option_question":
        return "handle_option_question"
    elif last_response == "handle_tag_question":
        return "handle_tag_question"
    elif last_response == "handle_crud_operation":
        return "handle_crud_operation"
    elif last_response == "handle_list_question_with_subgraph":
        return "handle_list_question_with_subgraph"
    else:
        return "handle_list_question_with_subgraph"

#sub level routers - requirements, functions, logical connections and product
def route_to_next_sub_node(state):
    last_response = state['messages'][-1].content
    
    if last_response == "handle_requirements_question":
        return "handle_requirements_question"
    if last_response == "handle_functions_question":
        return "handle_functions_question"
    elif last_response == "handle_logical_connections_question":
        return "handle_logical_connections_question"
    elif last_response == "handle_products_question":
        return "handle_products_question"
    else:
        return "unknown_question_type"

# # sub level handlers
def handle_requirements_question(state):
    """
    Generate an answer for a requirements question and store the results in the database.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with the answer
    """

    print("---GENERATE REQUIREMENTS ANSWERS---")

    messages = state["messages"]
    question = messages[-3].content  # The product or question about the requirements

    nextPrompt = HumanMessage(
        content=f"""
            You are a mechanical designer. Your task is to generate a list of Requirements for a given product user asked which is: {question}. 

            Your response should be an array of JSON objects in the following format:
            [
                {{"index": "1", "title": "Requirement Title", "description": "Description of the Requirement"}}
            ]

            Ensure that you only provide the list of requirements. Do not include any additional commentary or explanations.
        """
    )

    conversation_history = get_conversation_history()
    conversation_history.append(nextPrompt)
    
    # Get the current model
    model = get_global_model()
    
    response = model.invoke(conversation_history)

    # Assuming the response content is a JSON formatted string
    try:
        requirements_json = response.content  # This is the JSON array as a string
        json.loads(requirements_json)  # Optional: Validate if it's valid JSON
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {"error": "Invalid response format"}

    # # Insert the entire JSON string into the database
    # insert_requirements_json_to_db(question, requirements_json)
    
    # Insert the entire JSON string into the database as each elements
    # insert_requirements_json_to_db(requirements_json)

    # Create response schema
    agent_state = {
        "messages": [response],
        "response_schema": create_schema(response.content, "Requirements_Handler")
    }
    
    return agent_state

def handle_functions_question(state):
    """
    Generate an answer for a functions question and store the results in the database.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with the answer
    """

    print("---GENERATE FUNCTIONS ANSWERS---")

    messages = state["messages"]
    question = messages[-3].content  # The product or question about the functions

    nextPrompt = HumanMessage(
        content=f"""
            You are a mechanical designer. Your task is to generate a list of Functions for a given product the user asked, which is: {question}. 

            Your response should be an array of JSON objects in the following format:
            [
                {{"index": "1", "title": "Function Title", "description": "Description of the Function"}}
            ]

            Ensure that you only provide the list of functions. Do not include any additional commentary or explanations.
        """
    )

    conversation_history = get_conversation_history()
    conversation_history.append(nextPrompt)

    # Get the current model
    model = get_global_model()

    response = model.invoke(conversation_history)

    # Assuming the response content is a JSON formatted string
    try:
        functions_json = response.content  # This is the JSON array as a string
        json.loads(functions_json)  # Optional: Validate if it's valid JSON
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {"error": "Invalid response format"}

    # Insert the entire JSON string into the database
    # insert_functions_json_to_db(question, functions_json)

    # Create response schema
    agent_state = {
        "messages": [response],
        "response_schema": create_schema(response.content, "Functions_Handler")
    }

    return agent_state

def handle_products_question(state):
    """
        Generate an answer for a products-related question.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with the answer
    """

    print("---GENERATE PRODUCTS ANSWERS---")

    messages = state["messages"]
    question = messages[-3].content

    nextPrompt = HumanMessage(
        content=f"""
            You are a mechanical designer. Your task is to generate a list of **Components/Products** that are neede to buid the given product user asked which is : {question}. 

            Your response should be an array of JSON objects in the following format:
            [
                {{
                    "index": "1",
                    "title": "Product Title",
                    "description": "Description of the Product"
                }}
            ]

            Ensure that you only provide the list of requirements. Do not include any additional commentary or explanations.
        """
    )

    conversation_history = get_conversation_history()
    
    conversation_history.append(nextPrompt)
    
    # get current model
    model = get_global_model()
    
    response = model.invoke(conversation_history)
    
        # Assuming the response content is a JSON formatted string
    try:
        products_json = response.content  # This is the JSON array as a string
        json.loads(products_json)  # Optional: Validate if it's valid JSON
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {"error": "Invalid response format"}

    # Insert the entire JSON string into the database
    # insert_products_json_to_db(question, products_json)

    # Create response schema
    agent_state = {
        "messages": [response],
        "response_schema": create_schema(response.content, "Products_Handler")
    }
    
    return agent_state

def handle_logical_connections_question(state):
    """
    Generate an answer for a logical connections question and insert the connections into the database.

    Args:
        state (dict): The current state containing messages and other information.

    Returns:
        dict: The updated state with the answer.
    """

    print("---GENERATE LOGICAL CONNECTIONS ANSWERS---")

    messages = state["messages"]
    question = messages[-3].content

    # Create prompt for the model
    nextPrompt = HumanMessage(
        content=f"""
            You are a mechanical designer. Your task is to generate a logical connection between the "Requirements" and the "Products" for the given component: {question}.
            
            The "Requirements" and "Products" are already generated by you. You just need to give a logical connection between them.

            Your response should be an array of JSON objects in the following format:
            [
                {{
                    "connection_name": "Name describing the connection",
                    "connection_type": "Type of connection",
                    "description": {{"requirement": "requirement_name", "product": "product_name"}}
                }}
            ]

            Ensure that you only provide the list of logical connections. Do not include any additional commentary or explanations.
        """
    )

    conversation_history = get_conversation_history()
    conversation_history.append(nextPrompt)

    # Get the current model and generate the response
    model = get_global_model()
    response = model.invoke(conversation_history)

    # Parse the response (assume it's valid JSON format)
    try:
        logical_connections_json = response.content  # This is the JSON array as a string
        connections = json.loads(logical_connections_json)  # Validate if it's valid JSON
        
        # Insert the entire JSON string into the database
        # insert_logical_connection_to_db(question, logical_connections_json)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {"error": "Invalid response format"}
    
    # Create response schema
    agent_state = {
        "messages": [response],
        "response_schema": create_schema(response.content, "Logical_Connections_Handler")
    }

    return agent_state

#top level handlers
def handle_general_question(state):
    """
        Generate a an answer to a general question.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with the answer
    """

    print("---GENERATE GENERAL ANSWERS---")

    messages = state["messages"]
    question = messages[-2].content

    nextPrompt = HumanMessage(
        content=f""" \n
            You are a systems engineer. Look at the input and generate a general answer to the users question. \n
            Here is the question the user asked:
            \n ------- \n
            {question}
            \n ------- \n
            Now, formulate a well thought out general answer to the question, do not say anything else.\n
            Answer should be precise and to the point. No verbose 
        """,
    )


    conversation_history = get_conversation_history()
    
    conversation_history.append(nextPrompt)
    
    # get current model
    model = get_global_model()
    
    response = model.invoke(conversation_history)

    # Create response schema
    agent_state = {
        "messages": [response],
        "response_schema": create_schema(response.content, "General_Handler")
    }
    
    return agent_state

def handle_option_question(state):
    """
        Generate a an answer to a option based question.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with the answer
    """

    print("---GENERATE OPTION-BASED ANSWERS---")

    messages = state["messages"]
    question = messages[-2].content

    nextPrompt = HumanMessage(
        content=f""" \n
            You are a systems engineer. Look at the input and generate a OPTIONAL ANSWERS to the user's question. \n
            Here is the question the user asked:
            \n ------- \n
            {question}
            \n ------- \n
            Now, formulate a well thought out optional answers to the question, do not say anything else.\n
            Exampler - What are the target countries for garage door openers? you should give answers as 1.US 2.EU etc.\n
        """,
    )

    conversation_history = get_conversation_history()
    
    conversation_history.append(nextPrompt)
    
    # get current model
    model = get_global_model()
    
    response = model.invoke(conversation_history)
    
    # Create response schema
    agent_state = {
        "messages": [response],
        "response_schema": create_schema(response.content, "Options_Handler")
    }
    
    return agent_state

def handle_tag_question(state):
    """
        Generate an answer to a tag-based question.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with the answer
    """

    print("---GENERATE TAG-BASED ANSWER---")

    messages = state["messages"]
    question = messages[-2].content

    nextPrompt = HumanMessage(
        content=f""" \n
            You are a systems engineer. Look at the input and generate a precise and categorical answer to the user's question. \n
            Here is the question the user asked:
            \n ------- \n
            {question}
            \n ------- \n
            Now, formulate a well-thought-out answer to the question, categorizing it into relevant tags. Provide the response in a structured format as follows: \n
            exampler
            Functional Tags
            - Motor Control
            - Variable Speed
            - Drive Mechanism
            
            Design and Performance Tags
            - Durability
            - Noise Reduction
            - Smooth Operation
            
            Safety and Compliance Tags
            - Safety Standards
            - Regulatory Compliance
            
            User Experience Tags
            - User-friendly
            - Easy Installation

            Connectivity and Technology Tags
            - Wi-Fi Connectivity
            - Bluetooth
            - IoT
            
            Additional Features Tags
            - Lighting System
            - Motion Detection
            - Auto-close Timer
            
            Provide the answer in categoies and each categorie should have 2 to 4 items. Do not say anything else.
        """
    )

    conversation_history = get_conversation_history()
    
    conversation_history.append(nextPrompt)
    
    # get current model
    model = get_global_model()
    
    response = model.invoke(conversation_history)
    
    # Create response schema
    agent_state = {
        "messages": [response],
        "response_schema": create_schema(response.content, "TAG_Handler")
    }
    
    return agent_state

def handle_crud_operation(state):
    """
        Generate an answer to a crud-based question.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with the answer
    """

    print("---GENERATE CRUD-BASED ANSWER---")

    messages = state["messages"]
    question = messages[-2].content
    
    nextPrompt = HumanMessage(
        content=f"""
            You are a systems engineer. Analyze the input to determine if the user is requesting a CRUD operation. CRUD stands for Create, Read, Update, and Delete.

            Here is the user's question:
            \n ------- \n
            {question}
            \n ------- \n

            Determine the CRUD operation requested:
             -If the user intent is to update the context then update the JSON based on users query. Example-(garage is in alaska, then user is asking to udpate the context for a cold region now you should update the json intelligently to specific to cold region.and do not say  anything else just give the JSON)
            - If the user asks to ADD, add the context to the JSON.
            - If the user asks to Remove/ DELETE, remove the context from the JSON.
            - If the user asks to READ, retrieve and display the current JSON.
            - If the user asks to CREATE, initialize a new JSON context.

            Provide the updated or retrieved JSON in the same JSON format. \n
            
            Your response should be an array of JSON objects. the response should have all entries updated according to above operations.
            the response should be of the following format:
            [
                {{
                    "index": "1",
                    "title": "Title",
                    "description": "Description",
                }}, {{
                    ...
                }}
            ]

            Example: If the user asks "Add "Legal and Regulatory"" to the requirements, update the JSON format with this addition. and return the whole JSON with updated entry, do not say anything else.
        """
    )   


    conversation_history = get_conversation_history()
    
    conversation_history.append(nextPrompt)
    
    # get current model
    model = get_global_model()
    
    response = model.invoke(conversation_history)
    
    # Create response schema
    agent_state = {
        "messages": [response],
        "response_schema": create_schema(response.content, "CRUD_Handler")
    }
    
    return agent_state

# helpers
def get_conversation_history():
    """
        Retrieve stored conversation history.
        
        Returns:
            list: A list of messages with both questions and answers.
    """
    # This should retrieve the history from your storage (e.g., database, in-memory list)
    # Example placeholder code:
    snapeshot = default_app.get_state(config)
    snapeshot.values["messages"]
    return snapeshot.values["messages"]

def create_schema(content=None, agent="None"):
    # Set default values if parameters are not provided
    default_content = "No content provided"
    default_agent = "UnknownAgent"
    
    # Use provided values or default values
    schema = {
        "content": content if content is not None else default_content,
        "metadata": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "requestId": request.headers.get('X-Request-ID', 'default-id'),
            "language": "en"  # Modify or dynamically set as needed
        },
        "agent": agent if agent is not None else default_agent,
        "status": {
            "code": 200,
            "message": "OK"
        },
        "model":get_global_model().name 
      
    }
    return schema
