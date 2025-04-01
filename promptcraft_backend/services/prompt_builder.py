from models.prompts import ToolPromptRequest # Import the Pydantic model

def build_tool_creation_meta_prompt(request: ToolPromptRequest) -> str:
    """Constructs a meta-prompt to guide an LLM in creating a detailed tool prompt."""

    # Helper function to format lists nicely or provide a default message
    def format_list(items: list, default_message="None specified."):
        if not items:
            return f"  - {default_message}"
        return "- " + "\n    - ".join(items)

    meta_prompt = f"""
You are an expert Prompt Engineer specializing in generating prompts for AI models (like {request.ai_model_target or 'a capable coding AI'}) tasked with software development and tool creation. Your goal is to create a clear, detailed, and effective prompt based on the user's requirements provided below.

**User's Request Summary:**

*   **Primary Goal:** {request.goal}
*   **Desired Tech Stack:** {', '.join(request.tech_stack) if request.tech_stack else 'Not specified, suggest appropriate stack based on the goal.'}
*   **Coding Style/Approach:** {request.coding_style if request.coding_style else 'Standard best practices, prioritize clarity and maintainability.'}
*   **Key Features Required:**
    {format_list(request.key_features)}
*   **Target Audience/Environment:** {request.target_audience if request.target_audience else 'General purpose.'}
*   **Constraints/Requirements:**
    {format_list(request.constraints)}
*   **Desired Output Format from AI:** {request.output_format_request}

**Your Task:**

Generate a comprehensive prompt that instructs an AI (like {request.ai_model_target or 'a capable coding AI'}) on how to fulfill the user's request. The generated prompt should:

1.  **Set the Context:** Clearly state the overall goal of the tool.
2.  **Define the AI's Role:** Assign a suitable persona (e.g., "You are an expert Python developer specializing in building robust command-line tools.").
3.  **Specify Requirements:** Detail the tech stack (or instruct the AI to choose wisely if unspecified), key features, coding style, and constraints. Use bullet points or numbered lists for clarity within the prompt you generate.
4.  **Provide Structure:** Suggest a logical structure for the output if applicable (e.g., request specific functions, class definitions, file structure).
5.  **Handle Ambiguities:** If details are missing (like specific error handling methods), instruct the AI to make reasonable, standard assumptions suitable for the task.
6.  **Request the Output Format:** Explicitly ask the AI to provide the output strictly in the format specified by the user ({request.output_format_request}). For 'full_code', ask for complete, runnable code.
7.  **Encourage Best Practices:** Include reminders for error handling, comments, documentation (docstrings), and potentially suggestions for basic tests or usage examples, where appropriate for the requested format.

**Constraint for Your Output (The Prompt You Generate):**
- The output should ONLY be the generated prompt itself, ready to be copy-pasted and used with the target AI model.
- Do not include any preamble, introduction, or explanation from your side (the Prompt Engineer). Just the prompt.
- Make the prompt highly detailed, actionable, and unambiguous for the target AI model.

**Generate the prompt now:**
"""
    return meta_prompt.strip() # Remove leading/trailing whitespace
