import openai # Using the OpenAI library
from core.config import settings # Import settings to get API key and model name
import logging # Optional: for better logging

# Configure logging (optional but recommended)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the OpenAI client using the API key from settings
# Ensure the openai library is installed: pip install openai
try:
    client = openai.AsyncOpenAI(api_key=settings.LLM_API_KEY)
    logger.info("OpenAI client initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    # You might want to handle this more gracefully depending on app requirements
    client = None

async def generate_prompt_from_meta(meta_prompt: str) -> str:
    """Sends the meta-prompt to the configured LLM and returns the generated target prompt."""
    if not client:
        logger.error("OpenAI client is not available.")
        raise ConnectionError("LLM service client is not initialized.")

    try:
        logger.info(f"Sending request to LLM model: {settings.LLM_MODEL_NAME}")
        response = await client.chat.completions.create(
            model=settings.LLM_MODEL_NAME,
            messages=[
                # System message guides the LLM performing *this* task (generating the prompt)
                {"role": "system", "content": "You are an expert Prompt Engineer. Your task is to generate a detailed and effective prompt based on the user's requirements provided in the user message. Output ONLY the generated prompt text, nothing else."},
                {"role": "user", "content": meta_prompt}
            ],
            temperature=0.5, # Lower temperature for more focused prompt generation
            max_tokens=1500, # Max length of the generated prompt
            n=1,             # Generate one completion choice
            stop=None        # Let the model decide when to stop
        )
        generated_prompt = response.choices[0].message.content.strip()
        logger.info("Successfully received response from LLM.")
        return generated_prompt
    except openai.APIConnectionError as e:
        logger.error(f"OpenAI API Connection Error: {e}")
        raise ConnectionError(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        logger.error(f"OpenAI API Rate Limit Error: {e}")
        if "insufficient_quota" in str(e):
            raise ConnectionError("OpenAI API quota exceeded. Please check your OpenAI account billing details and add more credits.")
        else:
            raise ConnectionError(f"OpenAI API request exceeded rate limit: {e}")
    except openai.APIStatusError as e:
        logger.error(f"OpenAI API Status Error: status={e.status_code}, response={e.response}")
        raise ConnectionError(f"OpenAI API returned an error status {e.status_code}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during LLM API call: {e}")
        # Consider more specific error handling based on potential issues
        raise ConnectionError(f"An unexpected error occurred while communicating with the LLM API: {e}")
