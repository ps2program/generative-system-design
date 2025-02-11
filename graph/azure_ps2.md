
from langchain_openai import AzureChatOpenAI
import os

chat_model = AzureChatOpenAI(
    api_version="2024-08-01-preview",
    azure_deployment="https://ai-2024ab050835119ai697743905369.openai.azure.com",
    azure_endpoint="https://ai-2024ab050835119ai697743905369.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2024-08-01-preview",
    api_key="3ygiEqdbzsNbPdZ3O9n65EOWJCtFPHcT7dhSlL1avxERqT2BPvnsJQQJ99BBACHYHv6XJ3w3AAAAACOGu9KS",
    temperature=0,
    streaming=True
)
