# xSystemsAI Setup Guide

## Setting Up Your Environment

1. **Create `.env` Files:**
   - Create `.env` files in the root directory for your Flask application and define environment variables needed. Here's an example:

     ```
      # NETVIBES_API_KEY="S3FyOzwwmvQkh2VH+j8VPpQ5cvZznoHANIKTTwF8GuY="
      # AZURE_OPENAI_KEY="b7d2034788ce48b9a34d64a94537211a"

      # GPT-4o environment variables
      OPENAI_API_TYPE="azure"
      AZURE_OPENAI_ENDPOINT="https://sw-oai.openai.azure.com"
      AZURE_OPENAI_API_VERSION="2024-05-01-preview"
      AZURE_OPENAI_API_KEY="b7d2034788ce48b9a34d64a94537211a"
      AZURE_OPENAI_GPT4O_MODEL_NAME="gpt-4o"
      AZURE_OPENAI_GPT4O_DEPLOYMENT_NAME="gpt-4o"

      # GPT-4o-2 environment variables
      OPENAI_API_TYPE="azure"
      AZURE_OPENAI_ENDPOINT="https://sw-oai.openai.azure.com"
      AZURE_OPENAI_API_VERSION="2023-03-15-preview"
      AZURE_OPENAI_API_KEY="b7d2034788ce48b9a34d64a94537211a"
      AZURE_OPENAI_GPT4O_2_MODEL_NAME="gpt-4o-2"
      AZURE_OPENAI_GPT4O_2_DEPLOYMENT_NAME="gpt-4o-2"

      # gpt-35-turbo environment variables
      OPENAI_API_TYPE="azure"
      AZURE_OPENAI_ENDPOINT="https://sw-oai.openai.azure.com"
      AZURE_OPENAI_API_VERSION="2023-03-15-preview"
      AZURE_OPENAI_API_KEY="b7d2034788ce48b9a34d64a94537211a"
      AZURE_OPENAI_GPT35_MODEL_NAME="gpt-35-turbo"
      AZURE_OPENAI_GPT35_DEPLOYMENT_NAME="gpt-35-turbo"

      # netvibes llama environment variables
      NETVIBES_API_KEY="S3FyOzwwmvQkh2VH+j8VPpQ5cvZznoHANIKTTwF8GuY="
      NETVIBES_OPENAI_LLAMA_MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"
      NETVIBES_OPENAI_LLAMA_DEPLOYMENT_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"
      NETVIBES_BASE_URL = "http://px101.prod.exalead.com:8110/v1"
      NETVIBES_BASE_URL_COMPLETION = "http://px101.prod.exalead.com:8110/v1/chat/completions"
     ```

2. **Install Dependencies:**
   - Make sure Python and pip are installed. Then, install dependencies using:

     ```
     pip install -r requirements.txt
     ```

## Running the Flask Application

### Local Setup

- To run the Flask app locally on your system:

  ```bash
  flask run --host=localhost --port=5001


- To allow access to your Flask app over LAN (local area network):
  ```bash
  flask run --host=0.0.0.0 --port=5001

