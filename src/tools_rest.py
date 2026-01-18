import requests
from src.config import Config


def make_http_request(method: str, url: str, params: dict = None) -> str:
    """
    A raw wrapper around requests.
    The Agent must construct the URL and handle the logic.
    """
    headers = {
        "Authorization": f"token {Config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Validation: Prevent Agent from accessing non-GitHub URLs (security)
    if "api.github.com" not in url:
        return "Error: You are only allowed to access api.github.com"

    try:
        # The 'dumb' request - no loops, no magic.
        resp = requests.request(method, url, headers=headers, params=params)

        # If it fails, the Agent sees the raw 403/404 error
        if resp.status_code >= 400:
            return f"HTTP Error {resp.status_code}: {resp.text}"

        # Return raw JSON text
        # We truncate it slightly to prevent overflowing the context window too fast in the demo,
        # but in reality, this is where Agents choke (too much text).
        return resp.text[:5000]

    except Exception as e:
        return f"Connection Error: {str(e)}"


# --- OpenAI Tool Definition ---


def get_rest_tool_schema():
    return {
        "type": "function",
        "function": {
            "name": "make_http_request",
            "description": "Make a raw HTTP request to the GitHub API. Use this to list issues, get repos, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "method": {
                        "type": "string",
                        "enum": ["GET", "POST"],
                        "description": "HTTP method",
                    },
                    "url": {
                        "type": "string",
                        "description": "Full URL (e.g., https://api.github.com/repos/...)",
                    },
                    "params": {
                        "type": "object",
                        "description": "URL parameters (e.g., {'state': 'open', 'page': 2})",
                    },
                },
                "required": ["method", "url"],
            },
        },
    }
