from flask import Flask, request, Response
import concurrent.futures
import time
import os
from langchain_openai import ChatOpenAI

app = Flask(__name__)

# Simulated StateMemory class
class StateMemory:
    def __init__(self):
        self.requirements = {}
        self.physicals = {}

    def get_state_as_json(self):
        return {
            "requirements": {req_id: req.__dict__ for req_id, req in self.requirements.items()},
            "physicals": {phy_id: phy.__dict__ for phy_id, phy in self.physicals.items()}
        }


# Requirement and Physical classes
class Requirement:
    def __init__(self, name, description):
        self.id = str(time.time())  # Simulated unique ID
        self.name = name
        self.description = description


class Physical:
    def __init__(self, name, description, parent_id):
        self.id = str(time.time())  # Simulated unique ID
        self.name = name
        self.description = description
        self.parent_id = parent_id


# LLMProcessor class
class LLMProcessorParallel:
    def __init__(self, llm_client, state_memory):
        self.llm_client = llm_client
        self.state_memory = state_memory

    def process_requirement(self, requirement):
        physical_data = self.call_llm_to_create_physical(requirement)

        physical = Physical(
            name=physical_data["name"],
            description=physical_data["description"],
            parent_id=requirement.id
        )
        self.state_memory.physicals[physical.id] = physical

        created_physical = self.state_memory.physicals[physical.id]

        return {
            "requirement": requirement.name,
            "physical_name": created_physical.name,
            "description": created_physical.description
        }
        
        

    def call_llm_to_create_physical(self, requirement):
        prompt = f"""
                You are a mechanical designer. Your task is to generate a list of Physicals
                for the following requirement: "{requirement.description}". 

                Your response should be an array of JSON objects in the following format:
                [
                    {{"index": "1", "title": "Physical Title", "description": "Description of the Physical"}}
                ]

                Ensure that you only provide the list of functions. Do not include any additional commentary or explanations. each should be not more than 100 words in JSON format.
            """
        
        response = self.llm_client(prompt)
        return {
            "name": f"Physical for {requirement.name}",
            "description": response
        }


@app.route('/process-requirements', methods=['POST'])
def process_requirements():
    data = request.get_json()

    if not data or "requirements" not in data:
        return jsonify({"error": "Invalid input, 'requirements' key is required"}), 400

    requirements = []
    for req in data["requirements"]:
        if "name" in req and "description" in req:
            requirements.append(Requirement(req["name"], req["description"]))
        else:
            return jsonify({"error": "Each requirement must have 'name' and 'description'"}), 400

    llm_client = create_mistral_model("Mistral-Model")
    state_memory = StateMemory()
    llm_processor = LLMProcessorParallel(llm_client, state_memory)

    def generate():
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(llm_processor.process_requirement, requirement)
                for requirement in requirements
            ]

            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    yield f"data: {result}\n\n"  # Server-Sent Event format
                except Exception as e:
                    yield f"data: {{'error': 'An error occurred: {str(e)}'}}\n\n"

    return Response(generate(), content_type='text/event-stream')

def create_mistral_model(model_name):
    return ChatOpenAI(
        api_key=os.getenv("NETVIBES_API_KEY"),
        base_url=os.getenv("NETVIBES_BASE_URL"),
        model=os.getenv("NETVIBES_OPENAI_MISTRAL_DEPLOYMENT_NAME"),
        max_tokens=5000,
        name=model_name,
    )


if __name__ == '__main__':
    app.run(debug=True)
