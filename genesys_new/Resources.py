def getLLMName():
    return "mistralai/Mistral-7B-Instruct-v0.2"
# As of Feb 6, 2024 this is the only LLM model that is specific for code generation.
# NetVibes may stop running an LLM model. Thomas Schillaci is able to start them.

def getOpenAILLMName():
    return "gpt-3.5-turbo" 
# 10x cheaper than GPT-4o

def getMaxTokens():
    return 2048
# This is the maximum number of tokens that the LLM will return


def getTemperature():
    return 0.2
# controls how conservative the next token is chosen.
# Higher values means lower probability tokens have an increased chance of being selected
# which can result in less predictable outputs.


def getTopP():
    return 0.1
# Controls how many tokens the model has to choose from at each step. Higher values results in
# less predictable results.


xsystem_criteria = """
            """


def getXSystemCriteria():
    return xsystem_criteria

# The system prompt

def generateSystemPrompt():
    return f"""
you are a mechanical designer you job is as followings - 
you will take the user's input and generate a list of requirements to implement that design. you will only output the list of requirements, you will not say anything else. if user asks any questions regarding the design, give concise, to the point answer. to support you answer give very concise reason. Answer should of the  JSON formate as Index, Title and Description. e.g "index":"1", "title":"UL 325 Compliance", "description":"descrioption about a particular requirement". if further questions being asked about design, asnwer very concisely and to the point in simple text.
"""

def generateSystemPrompt_v1():
    return f"""
Your job is to gather specifications from a user about a mechanical part they need to create in the Solidworks CAD application.

You will get the following information from them:

1. Type of object or structure:
2. Key features (e.g., load-bearing capacity, aesthetic elements):
3. Material preferences:
4. Dimensions (please specify units):
5. Any specific standards or constraints (e.g., ISO certifications):
6. Additional notes or requirements (optional):"

If you are not able to discern this info, ask them to clarify! Do not attempt to wildly guess.

After you are able to discern all the information, you will format and output the specifications in human readable format.
"""
