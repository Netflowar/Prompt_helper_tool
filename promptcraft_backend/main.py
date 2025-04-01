from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from models.prompts import ToolPromptRequest, ToolPromptResponse # Import Pydantic models
from services.prompt_builder import build_tool_creation_meta_prompt # Import meta-prompt builder
from services.llm_service import generate_prompt_from_meta # Import LLM interaction service
from core.config import settings # Import settings to check API key existence
import logging
import os # Add this import

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PromptCraft API",
    description="API for generating AI prompts using meta-prompting techniques, starting with tool creation prompts.",
    version="0.1.0",
    contact={
        "name": "Your Name/Org",
        "url": "http://yourwebsite.com", # Optional
        "email": "your@email.com",      # Optional
    },
    license_info={ # Optional
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Mount static files directory
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Dependency check: Ensure API key is loaded at startup
if not settings.LLM_API_KEY:
    logger.critical("FATAL ERROR: LLM_API_KEY is not configured in the environment/.env file. Application cannot start properly.")
    # In a real-world scenario, you might prevent the app from fully starting or disable the endpoint.
    # For simplicity here, we let it start but the endpoint will fail.

@app.post(
    "/generate-tool-prompt/",
    response_model=ToolPromptResponse,
    tags=["Prompt Generation"], # Group endpoints in Swagger UI
    summary="Generate a detailed AI prompt for tool creation",
    description="Takes user specifications for a software tool, constructs a meta-prompt, uses an LLM to refine it into a final, detailed prompt suitable for another AI code generation model."
)
async def create_tool_prompt(
    request: ToolPromptRequest = Body(..., embed=True) # Use embed=True to expect {"request": {...}} structure
):
    """
    Generates a detailed AI prompt for tool creation based on user specifications.

    - **request**: Input object containing details about the desired tool.
    \f
    :param request: The user's request containing tool specifications.
    :return: A response containing the generated prompt.
    """
    logger.info(f"Received request to generate tool prompt for goal: {request.goal}")

    if not settings.LLM_API_KEY:
         logger.error("Attempted to call endpoint but LLM API key is missing.")
         raise HTTPException(
             status_code=500,
             detail="Server configuration error: LLM API key is not configured."
         )

    try:
        # 1. Build the meta-prompt based on the user's request
        logger.info("Building meta-prompt...")
        meta_prompt = build_tool_creation_meta_prompt(request)
        logger.debug(f"Meta-prompt generated:\n{meta_prompt[:500]}...") # Log start of meta-prompt

        # 2. Call the LLM service with the meta-prompt to get the final prompt
        logger.info("Sending meta-prompt to LLM service...")
        final_prompt = await generate_prompt_from_meta(meta_prompt)
        logger.info("Successfully generated final prompt.")

        # 3. Return the generated prompt (optionally include the meta-prompt for debugging)
        return ToolPromptResponse(
            generated_prompt=final_prompt,
            # meta_prompt_used=meta_prompt # Uncomment if you want client to see the meta-prompt
        )

    except ConnectionError as e:
         logger.error(f"LLM Service connection error: {e}")
         raise HTTPException(
             status_code=503, # Service Unavailable
             detail=f"Could not connect to the underlying LLM service: {e}"
         )
    except HTTPException:
        # Re-raise HTTPExceptions (like validation errors from FastAPI)
        raise
    except Exception as e:
        # Catch any other unexpected errors
        logger.exception(f"An unexpected error occurred processing the request: {e}") # Logs traceback
        raise HTTPException(
            status_code=500, # Internal Server Error
            detail=f"An internal server error occurred while generating the prompt."
        )

@app.get("/", tags=["General"], summary="API Root/UI")
async def read_root():
    """Redirects to the user interface."""
    logger.info("Root endpoint '/' accessed, redirecting to UI.")
    return RedirectResponse(url="/static/index.html")

# Example of how to run using uvicorn:
# In your terminal in the promptcraft_backend directory:
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
