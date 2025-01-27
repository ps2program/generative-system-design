import pkg_resources

packages = [
    "Flask",
    "Flask-CORS",
    "langchain_core",
    "langgraph",
    "langchain_openai",
    "python-dotenv",
    "flask-swagger-ui",
    "pydantic",
    "langgraph-checkpoint-sqlite",
    "langchain-ollama"
]

with open("requirements.txt", "w") as req_file:
    for package in packages:
        try:
            version = pkg_resources.get_distribution(package).version
            req_file.write(f"{package}=={version}\n")
        except pkg_resources.DistributionNotFound:
            print(f"{package} is not installed and will not be added to requirements.txt")
