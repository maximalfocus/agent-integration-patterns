from src.tools_rest import make_http_request


def test_raw_access():
    print("Testing Raw REST Tool...")

    # 1. The Agent has to know the exact URL structure
    url = "https://api.github.com/repos/python/cpython/issues"

    # 2. The Agent has to manually decide parameters
    resp = make_http_request("GET", url, params={"per_page": 2})

    print("\nResponse Preview (First 200 chars):")
    print(resp[:200])

    if "HTTP Error" in resp:
        print("\nFAILURE: Request failed.")
    else:
        print("\nSUCCESS: Got raw JSON response.")


if __name__ == "__main__":
    test_raw_access()
