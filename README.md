# PromptCraft: AI Prompt Generation Tool

PromptCraft is a specialized tool designed to generate detailed AI prompts for software development and tool creation. Using meta-prompting techniques, it helps you create highly detailed, customized prompts that can be used with models like GPT-4, Claude, or Gemini to build better software tools.

## Features

- **Meta-Prompt Generation**: Uses AI to create prompts tailored to your specific tool requirements
- **Customizable Parameters**: Specify technology stack, features, constraints, and more
- **Multiple Output Formats**: Choose between full code, pseudocode, architectural plans, etc.
- **User-Friendly Interface**: Clean, modern UI for easy prompt creation
- **Responsive Design**: Works well on both desktop and mobile devices

## How It Works

1. You provide specifications for the tool you want to create (goal, tech stack, key features, etc.)
2. PromptCraft constructs a meta-prompt based on your requirements
3. The meta-prompt is sent to an LLM (like GPT-4) to generate a detailed, customized prompt
4. The resulting prompt can be used with any AI model to generate your actual tool code

## Getting Started

### Prerequisites

- Python 3.7+
- FastAPI
- OpenAI API key

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/Netflowar/Prompt_helper_tool.git
   cd Prompt_helper_tool
   ```

2. Install dependencies:
   ```
   pip install -r promptcraft_backend/requirements.txt
   ```

3. Create a `.env` file in the `promptcraft_backend` directory with your OpenAI API key:
   ```
   LLM_API_KEY=your_openai_api_key_here
   ```

4. Run the application:
   ```
   cd promptcraft_backend
   uvicorn main:app --reload
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:8000/
   ```

## API Documentation

FastAPI provides automatic API documentation. After starting the server, visit:
```
http://localhost:8000/docs
```

## Usage Example

Fill out the form with details about the tool you want to create:

- **Goal**: "Create a Python CLI tool to check website status"
- **Tech Stack**: ["Python", "requests"]
- **Coding Style**: "Functional with clear comments"
- **Key Features**: 
  - "Takes a URL as a command-line argument"
  - "Prints 'UP' if status code is 2xx or 3xx"
  - "Prints 'DOWN' otherwise" 
  - "Includes timeout handling"
  - "Uses argparse for arguments"
- **Target Audience**: "Developers via CLI"
- **Constraints**: ["Use only standard libraries if possible (except requests)"]
- **Output Format**: "full_code"

Click "Generate Prompt" to receive a detailed, customized prompt that you can use with GPT-4 or other AI models to create your tool.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
