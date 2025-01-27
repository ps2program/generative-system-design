import difflib
from typing import Dict, Any
from pydantic import BaseModel

class OutputSchema(BaseModel):
    question_type: str  # Add other necessary fields here

class CustomStructuredOutputHandler:
    def __init__(self, model):
        self.model = model  # Initialize with your LLM model instance

    def with_structured_output(self, output_schema: BaseModel, classifications: Dict[str, str]):
        """
        Handles structured output with customizable classifications.

        Args:
            output_schema (BaseModel): The schema to validate and format the output.
            classifications (Dict[str, str]): A dictionary mapping classification keywords to output values.
        
        Returns:
            function: A function that takes a prompt and returns the structured output.
        """
        def invoke(prompt: Dict[str, Any]) -> Any:
            # Get the question from the prompt
            question = prompt["question"]

            # Call the model's invoke method
            raw_result = self.model.invoke(question)

            # Process the raw result and convert it to the structured format
            structured_result = self.parse_llm_output(raw_result, output_schema, classifications)
            return structured_result

        return invoke

    def parse_llm_output(self, raw_output: str, output_schema: BaseModel, classifications: Dict[str, str]):
        """
        Process the raw output from LLM into the structured output defined by the output schema.

        Args:
            raw_output (str): The raw output from the LLM.
            output_schema (BaseModel): The schema to validate and format the output.
            classifications (Dict[str, str]): A dictionary mapping classification keywords to output values.

        Returns:
            BaseModel: An instance of the output schema with the classified type.
        """
        raw_output_lower = raw_output.content.lower()

        # Directly check for classification keyword in the raw output
        for keyword, classification in classifications.items():
            if self.is_keyword_in_output(keyword, raw_output_lower):
                return output_schema(question_type=classification)

        # If no direct match, use semantic matching to determine the closest match
        closest_classification = self.semantic_match(raw_output_lower, classifications)
        return output_schema(question_type=closest_classification)

    def is_keyword_in_output(self, keyword: str, text: str) -> bool:
        """
        Check if a keyword or classification is directly mentioned in the text.
        """
        return keyword in text  # Check if the classification keyword is in the text

    def semantic_match(self, text: str, classifications: Dict[str, str]) -> str:
        """
        Use difflib to find the closest matching classification based on semantic similarity.

        Args:
            text (str): The LLM output text.
            classifications (Dict[str, str]): The mapping of keywords to classifications.

        Returns:
            str: The closest matching classification.
        """
        best_classification = None
        highest_similarity = 0

        for keyword, classification in classifications.items():
            # Calculate the similarity score using difflib's SequenceMatcher
            similarity = difflib.SequenceMatcher(None, keyword.lower(), text).ratio()
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_classification = classification

        return best_classification if best_classification else "unknown"
