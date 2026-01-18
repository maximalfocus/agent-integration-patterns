import requests
from src.config import Config


class GithubSDK:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.headers = {
            "Authorization": f"token {Config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }

    def get_issues(
        self, repo_name: str, limit: int = 10, state: str = "open", creator: str = None
    ) -> list[dict]:
        """
        Retrieves issues, optionally filtering by a specific creator.
        """
        issues = []
        page = 1
        per_page = 30

        # Log that we are using the optimized path
        if creator:
            print(
                f"   [SDK Internal] ⚡ Optimized Search: Filtering for creator '{creator}' on Server Side."
            )
        else:
            print(f"   [SDK Internal] Starting fetch loop for {limit} issues...")

        while len(issues) < limit:
            url = f"{self.BASE_URL}/repos/{repo_name}/issues"

            # Param Logic
            params = {"state": state, "per_page": per_page, "page": page}
            if creator:
                params["creator"] = creator

            try:
                resp = requests.get(url, headers=self.headers, params=params)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                return [{"error": str(e)}]

            if not data:
                break

            for item in data:
                issues.append(
                    {
                        "number": item["number"],
                        "title": item["title"],
                        "user": item["user"]["login"],
                        "state": item["state"],
                        "created_at": item["created_at"],
                    }
                )
                if len(issues) >= limit:
                    break

            print(f"   [SDK Internal] Page {page} fetched. Total so far: {len(issues)}")
            page += 1

        return issues


def get_rpc_tool_schema():
    return {
        "type": "function",
        "function": {
            "name": "get_issues_rpc",
            "description": "Fetch a list of issues from a GitHub repository. Handles pagination and filtering automatically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_name": {
                        "type": "string",
                        "description": "The repository name (e.g., 'pandas-dev/pandas')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "The maximum number of issues to return.",
                    },
                    "state": {"type": "string", "enum": ["open", "closed", "all"]},
                    "creator": {
                        "type": "string",
                        "description": "Filter issues created by a specific username.",
                    },
                },
                "required": ["repo_name"],
            },
        },
    }
