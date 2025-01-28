import os
from langchain_openai import AzureChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
# from openai import ChatOpenAI

# Global variable to store the current model instance
current_model = None

def create_mistral_model(model_name):
    """
    Creates and returns an AzureChatOpenAI model instance for GPT-3.5.

    Returns:
        AzureChatOpenAI: The configured GPT-3.5 model.
    """
    return ChatOpenAI(
        api_key=os.getenv("NETVIBES_API_KEY"),
        base_url=os.getenv("NETVIBES_BASE_URL"),
        model=os.getenv("NETVIBES_OPENAI_MISTRAL_DEPLOYMENT_NAME"),
        max_tokens=5000,
        name=model_name,
        # temperature=0,
        # streaming=True
    )

def create_ollama_mistral_model(model_name):
    """
    Creates and returns an AzureChatOpenAI model instance for GPT-3.5.

    Returns:
        AzureChatOpenAI: The configured GPT-3.5 model.
    """
    return ChatOllama(
            # model="mistral-nemo",
            model="llama3.1",
            temperature=0,
            # other params...
            )

def create_lmstudio_model(self):
    """
    Creates and returns a ChatOpenAI model instance for LM Studio.

    Returns:
        ChatOpenAI: The configured LM Studio model.
    """
    return ChatOpenAI(
        base_url="http://localhost:1234/v1", api_key="lm-studio", name="local"
    )
    
def create_gpt4o_model(model_name):
    """
    Creates and returns an AzureChatOpenAI model instance for GPT-4O.

    Returns:
        AzureChatOpenAI: The configured GPT-4O model.
    """
    return AzureChatOpenAI(
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_deployment=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT_NAME"),
        temperature=0,
        streaming=True,
        name = model_name
    )
    
def create_gpt35_model(model_name):
    """
    Creates and returns an AzureChatOpenAI model instance for GPT-3.5.

    Returns:
        AzureChatOpenAI: The configured GPT-3.5 model.
    """
    return AzureChatOpenAI(
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_deployment=os.getenv("AZURE_OPENAI_GPT35_DEPLOYMENT_NAME"),
        temperature=0,
        streaming=True,
        name = model_name
    )
    
def create_LLAMA3_model(model_name):
    """
    Creates and returns an AzureChatOpenAI model instance for GPT-3.5.

    Returns:
        AzureChatOpenAI: The configured GPT-3.5 model.
    """
    return ChatOpenAI(
        api_key=os.getenv("NETVIBES_API_KEY"),
        base_url=os.getenv("NETVIBES_BASE_URL"),
        model=os.getenv("NETVIBES_OPENAI_LLAMA_DEPLOYMENT_NAME"),
        max_tokens=5000,
        name=model_name,
        # temperature=0,
        # streaming=True
    )

def create_model(model_name):
    """
    Factory function to create models based on user selection.

    Args:
        model_name (str): The name of the model to create.

    Returns:
        The model instance.
    """
    if model_name == "GPT-4o":
        return create_gpt4o_model(model_name)
    elif model_name == "GPT-3.5":
        return create_gpt35_model(model_name)
    elif model_name == "LLAMA3":
        return create_LLAMA3_model(model_name)
    elif model_name == "MISTRAL":
        return create_mistral_model(model_name)
    elif model_name == "OLLAMA_MISTRAL":
        return create_ollama_mistral_model(model_name)
    elif model_name == "LOCAL":
        return create_lmstudio_model(model_name)
    else:
        return create_LLAMA3_model("LLAMA3")

def set_global_model(model_name):
    """
    Sets the global model instance based on the model name.

    Args:
        model_name (str): The name of the model to set globally.
    """
    global current_model
    current_model = create_model(model_name)

def get_global_model():
    """
    Gets the current global model instance.

    Returns:
        The current model instance.
    """
    return current_model

def get_tool_model() :
    """
    Creates and returns an AzureChatOpenAI model instance for GPT-34o.

    Returns:
        AzureChatOpenAI: The configured gpt-4o model.
    """
    return current_model