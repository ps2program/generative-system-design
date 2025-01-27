


# Request Query Schema 
```JSON

{
    "message": {
      "question": "garage door opener",
      "questionType": {
        "type": "list",
        "subType": "products"
      }
    }
}

{
    "message": {
      "question": "garage door opener",
      "questionType": {
        "type": "list",
        "subType": "requirements"
      }
    }
}

{
    "message": {
      "question": "garage door opener",
      "questionType": {
        "type": "list",
        "subType": "functions"
      }
    }
}

{
    "message": {
      "question": "garage door opener",
      "questionType": {
        "type": "list",
        "subType": "logical_connections"
      }
    }
}

{
    "message": {
      "question": "garage door opener",
      "questionType": {
        "type": "general",
        "subType": ""
      }
    }
}

{
    "message": {
      "question": "garage door opener",
      "questionType": {
        "type": "options",
        "subType": ""
      }
    }
}

{
    "message": {
      "question": "garage door opener",
      "questionType": {
        "type": "tag",
        "subType": ""
      }
    }
}
```


# LLMQueryTemplate Class

This project defines a JavaScript class `LLMQueryTemplate` for generating prompts based on different types of questions and their subtypes. This can be used to standardize query formatting when interacting with a language model (LLM) or other systems.


# source code of LLMQueryTemplate
```javascript

class LLMQueryTemplate {
    constructor(question, questionType, subType = null) {
        this.question = question;
        this.questionType = questionType;
        this.subType = subType;  // Optional subtype
    }

    generatePrompt() {
        if (this.subType) {
            return `Question: ${this.question}, Type: ${this.questionType}, SubType: ${this.subType}`;
        }
        return `Question: ${this.question}, Type: ${this.questionType}`;
    }
}

// Define question types and their subtypes
const QuestionType = Object.freeze({
    GENERAL: "general",
    LIST: {
        TYPE: "list",
        SUBTYPES: Object.freeze({
            PRODUCT: "products",
            REQUIREMENTS: "requirements",
            LOGICAL_CONNECTIONS: "logical_connections",
            FUNCTIONS: "functions"
        })
    },
    OPTIONS: "options",
    CRUD: "crud",
    TAG: "tag"
});

// Example usage
const query1 = new LLMQueryTemplate("garage door opener", QuestionType.LIST.TYPE, QuestionType.LIST.SUBTYPES.PRODUCT);
console.log(query1.generatePrompt());

const query2 = new LLMQueryTemplate("system requirements", QuestionType.LIST.TYPE, QuestionType.LIST.SUBTYPES.REQUIREMENTS);
console.log(query2.generatePrompt());

const query3 = new LLMQueryTemplate("generic question", QuestionType.GENERAL);
console.log(query3.generatePrompt());

```

## Class Overview

The `LLMQueryTemplate` class allows you to create structured queries with specified types and subtypes, and generate prompts accordingly. It also defines a set of predefined question types and subtypes.

## Structure

### `LLMQueryTemplate` Class

- **Constructor**
  - `question`: The main question (e.g., "garage door opener").
  - `questionType`: The type of the question (e.g., `general`, `list`).
  - `subType` (optional): The specific subtype of the question (e.g., `products`, `requirements`).

- **Methods**
  - `generatePrompt()`: This method generates a formatted prompt based on the question, question type, and optional subtype. If a subtype is provided, it includes it in the prompt.

### `QuestionType` Object

The `QuestionType` object provides a set of predefined question types and subtypes. It is used to ensure consistency in the types and subtypes across the project.

- `GENERAL`: General questions.
- `LIST`: For list-type questions. Contains subtypes:
  - `PRODUCT`: Product-related questions.
  - `REQUIREMENTS`: Requirement-related questions.
  - `LOGICAL_CONNECTIONS`: Logical connection-related questions.
  - `FUNCTIONS`: Function-related questions.
- `OPTIONS`: Option-related questions.
- `CRUD`: Questions related to Create, Read, Update, Delete operations.
- `TAG`: Tag-related questions.

