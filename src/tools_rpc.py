import requests
from src.config import Config


class GithubSDK:
    """
    The 'Agent-Native' SDK.
    It handles pagination, auth, and data cleaning internally.
    """

    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.headers = {
            "Authorization": f"token {Config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }

    def get_issues(
        self, repo_name: str, limit: int = 10, state: str = "open"
    ) -> list[dict]:
        """
        Retrieves a specific number of issues.
        Automatically handles pagination logic.
        """
        issues = []
        page = 1
        per_page = 30  # GitHub default max is usually 100, but we use 30 to force pagination logic to run earlier for the demo

        print(f"   [SDK Internal] Starting fetch loop for {limit} issues...")

        while len(issues) < limit:
            # 1. Calculate how many we still need
            remaining = limit - len(issues)  # noqa: F841

            # 2. Make the Request
            url = f"{self.BASE_URL}/repos/{repo_name}/issues"
            params = {"state": state, "per_page": per_page, "page": page}

            try:
                resp = requests.get(url, headers=self.headers, params=params)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                return [{"error": str(e)}]

            if not data:
                break  # No more data available

            # 3. Add to our list
            for item in data:
                # Only keep fields the agent cares about (saving tokens!)
                issues.append(
                    {
                        "number": item["number"],
                        "title": item["title"],
                        "user": item["user"]["login"],
                        "state": item["state"],
                    }
                )
                if len(issues) >= limit:
                    break

            print(f"   [SDK Internal] Page {page} fetched. Total so far: {len(issues)}")
            page += 1

        return issues


# --- OpenAI Tool Definition ---


def get_rpc_tool_schema():
    """Returns the JSON schema for the OpenAI Chat API."""
    return {
        "type": "function",
        "function": {
            "name": "get_issues_rpc",
            "description": "Fetch a list of issues from a GitHub repository. Handles pagination automatically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_name": {
                        "type": "string",
                        "description": "The repository name (e.g., 'pandas-dev/pandas')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "The maximum number of issues to return. Default is 10.",
                    },
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed", "all"],
                        "description": "Filter by issue state.",
                    },
                },
                "required": ["repo_name"],
            },
        },
    }
