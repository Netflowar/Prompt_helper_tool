from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class ToolPromptRequest(BaseModel):
    """Defines the expected input structure for generating a tool prompt."""
    goal: str = Field(..., description="Primary objective or function of the tool.", examples=["Create a Python script to scrape website titles"])
    tech_stack: List[str] = Field(default=[], description="Programming languages, frameworks, libraries, databases.", examples=[["Python", "BeautifulSoup4", "Requests"]])
    coding_style: Optional[str] = Field(None, description="Preferred coding style or paradigms.", examples=["Object-Oriented", "Functional", "Clean Code principles", "Heavily commented"])
    key_features: List[str] = Field(default=[], description="Specific features the tool must include.", examples=["Input: list of URLs", "Output: CSV file with URL and Title", "Handle HTTP errors gracefully"])
    target_audience: Optional[str] = Field(None, description="Who will use this tool or in what environment?", examples=["Developers via CLI", "Non-technical users via simple GUI", "Run inside a Docker container"])
    constraints: List[str] = Field(default=[], description="Any limitations or specific requirements.", examples=["Must run on Python 3.9+", "Avoid external libraries if possible", "Prioritize readability over performance"])
    output_format_request: Literal['full_code', 'pseudocode', 'architectural_plan', 'function_definition', 'step_by_step_plan'] = Field(default='full_code', description="What kind of output should the final prompt ask the AI for?")
    ai_model_target: Optional[str] = Field("GPT-4 or similar", description="Which AI model is the generated prompt intended for?", examples=["GPT-4", "Claude 3 Opus", "Gemini Pro"])

    # Example for OpenAPI docs / Swagger UI
    class Config:
        json_schema_extra = {
            "example": {
                "goal": "Create a Python CLI tool to check website status",
                "tech_stack": ["Python", "requests"],
                "coding_style": "Functional with clear comments",
                "key_features": [
                    "Takes a URL as a command-line argument",
                    "Prints 'UP' if status code is 2xx or 3xx",
                    "Prints 'DOWN' otherwise",
                    "Includes timeout handling",
                    "Uses argparse for arguments"
                ],
                "target_audience": "Developers via CLI",
                "constraints": ["Use only standard libraries if possible (except requests)"],
                "output_format_request": "full_code",
                "ai_model_target": "GPT-4"
            }
        }


class ToolPromptResponse(BaseModel):
    """Defines the output structure containing the generated prompt."""
    generated_prompt: str = Field(description="The detailed prompt generated for the AI.")
    meta_prompt_used: Optional[str] = Field(None, description="The meta-prompt sent to the LLM to generate the final prompt (for debugging/transparency).") # Optional
