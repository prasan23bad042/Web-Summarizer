import asyncio
from typing import Optional, Dict, Any
import json
from datetime import datetime, timedelta
import logging
from ..config import get_settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting and caching setup
RATE_LIMIT_WINDOW = 60  # 1 minute window
RATE_LIMIT_MAX_REQUESTS = 30  # Max requests per window

# In-memory cache (consider using Redis for production)
summary_cache: Dict[str, Dict[str, Any]] = {}
rate_limits: Dict[str, list] = {}

# Qwen-Agent client setup (you'll need to install the required package)
# pip install dashscope
import dashscope

def setup_qwen_client(api_key: str):
    """Initialize the Qwen-Agent client."""
    dashscope.api_key = api_key
    # You can add more configuration here if needed

class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""
    pass

def check_rate_limit(client_ip: str) -> bool:
    """Check if the client has exceeded the rate limit."""
    current_time = datetime.now()
    
    # Initialize rate limit tracking for new IPs
    if client_ip not in rate_limits:
        rate_limits[client_ip] = []
    
    # Remove timestamps older than the rate limit window
    rate_limits[client_ip] = [
        ts for ts in rate_limits[client_ip]
        if current_time - ts < timedelta(seconds=RATE_LIMIT_WINDOW)
    ]
    
    # Check if rate limit is exceeded
    if len(rate_limits[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
        return False
    
    # Add current request timestamp
    rate_limits[client_ip].append(current_time)
    return True

def generate_cache_key(text: str, max_length: int) -> str:
    """Generate a cache key for the given text and parameters."""
    import hashlib
    return hashlib.md5(f"{text}_{max_length}".encode()).hexdigest()

async def get_cached_summary(cache_key: str) -> Optional[Dict[str, Any]]:
    """Retrieve a cached summary if it exists and is not expired."""
    if cache_key in summary_cache:
        cached = summary_cache[cache_key]
        # Check if cache is expired (1 hour expiration)
        if datetime.now() - cached['timestamp'] < timedelta(hours=1):
            return cached['summary']
        del summary_cache[cache_key]
    return None

def cache_summary(cache_key: str, summary: str):
    """Cache a summary with the given key."""
    summary_cache[cache_key] = {
        'summary': summary,
        'timestamp': datetime.now()
    }

async def summarize_with_qwen(text: str, max_length: int = 300, client_ip: str = "default") -> str:
    """
    Summarize text using Qwen-Agent with error handling and rate limiting.
    
    Args:
        text: The text to summarize
        max_length: Maximum length of the summary
        client_ip: Client IP for rate limiting
        
    Returns:
        str: The generated summary
        
    Raises:
        RateLimitExceeded: If rate limit is exceeded
        Exception: For other errors during summarization
    """
    settings = get_settings()
    
    # Check rate limit
    if not check_rate_limit(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise RateLimitExceeded(
            f"Rate limit exceeded. Please try again in {RATE_LIMIT_WINDOW} seconds."
        )
    
    # Check cache first
    cache_key = generate_cache_key(text, max_length)
    cached = await get_cached_summary(cache_key)
    if cached:
        logger.info("Returning cached summary")
        return cached
    
    try:
        # Initialize Qwen client if not already done
        if not dashscope.api_key:
            setup_qwen_client(settings.dashscope_api_key)
        
        # Call Qwen API for summarization
        # Note: Adjust the model and parameters according to Qwen's API
        response = dashscope.Generation.call(
            model=settings.qwen_model,
            prompt=f"Please summarize the following text in about {max_length} characters:\n\n{text}",
            temperature=0.3,
            top_p=0.8,
            max_tokens=max_length
        )
        
        # Extract the summary from the response
        # Note: Adjust this based on Qwen's actual response format
        if response.status_code == 200:
            summary = response.output.text.strip()
            # Cache the result
            cache_summary(cache_key, summary)
            return summary
        else:
            error_msg = f"Qwen API error: {response.get('message', 'Unknown error')}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
    except Exception as e:
        logger.exception("Error in summarization")
        # You might want to implement a fallback summarization method here
        raise Exception(f"Failed to generate summary: {str(e)}")

# Alias for backward compatibility
summarize_text = summarize_with_qwen
