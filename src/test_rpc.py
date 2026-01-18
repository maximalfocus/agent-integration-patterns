from src.tools_rpc import GithubSDK


def test_pagination():
    sdk = GithubSDK()
    repo = "python/cpython"  # A busy repo with lots of issues

    print(f"Testing RPC SDK against {repo}...")
    issues = sdk.get_issues(repo, limit=35)

    print(f"\nResult count: {len(issues)}")
    print(f"First issue: #{issues[0]['number']} - {issues[0]['title']}")
    print(f"Last issue:  #{issues[-1]['number']} - {issues[-1]['title']}")

    if len(issues) == 35:
        print("\nSUCCESS: SDK automatically handled pagination!")
    else:
        print("\nFAILURE: Did not get 35 issues.")


if __name__ == "__main__":
    test_pagination()
