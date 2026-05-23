import os
from dotenv import load_dotenv
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from pydantic import BaseModel, Field

# Load the token from .env
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
GITHUB_TOKEN = os.getenv("GITHUB_PAT")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_PAT not found. Please set it in your .env file.")

# 1. Configure the GraphQL Transport
transport = RequestsHTTPTransport(
    url='https://api.github.com/graphql',
    headers={'Authorization': f'Bearer {GITHUB_TOKEN}'},
    use_json=True,
)

client = Client(transport=transport, fetch_schema_from_transport=False)

# 2. Define Pydantic Models for Validation
class FileNode(BaseModel):
    name: str
    path: str
    type: str

class RepoTreeResponse(BaseModel):
    entries: list[FileNode]

class FileContentResponse(BaseModel):
    text: str

# 3. Define the GraphQL Queries
TREE_QUERY = gql("""
    query GetRepoTree($owner: String!, $name: String!, $expression: String!) {
      repository(owner: $owner, name: $name) {
        object(expression: $expression) {
          ... on Tree {
            entries {
              name
              path
              type
            }
          }
        }
      }
    }
""")

CONTENT_QUERY = gql("""
    query GetFileContent($owner: String!, $name: String!, $expression: String!) {
      repository(owner: $owner, name: $name) {
        object(expression: $expression) {
          ... on Blob {
            text
          }
        }
      }
    }
""")

# 4. Helper Functions
def get_repo_tree(owner: str, repo_name: str, branch_or_commit: str = "HEAD") -> RepoTreeResponse:
    """Fetches the top-level directory tree of a repository."""
    # The expression format "HEAD:" points to the root tree
    params = {
        "owner": owner,
        "name": repo_name,
        "expression": f"{branch_or_commit}:" 
    }
    
    result = client.execute(TREE_QUERY, variable_values=params)
    entries = result['repository']['object']['entries']
    return RepoTreeResponse(entries=entries)

def get_file_content(owner: str, repo_name: str, file_path: str, branch: str = "HEAD") -> FileContentResponse:
    """Fetches the raw text content of a specific file."""
    # The expression format "HEAD:path/to/file.py" targets a specific blob
    params = {
        "owner": owner,
        "name": repo_name,
        "expression": f"{branch}:{file_path}"
    }
    
    result = client.execute(CONTENT_QUERY, variable_values=params)
    text = result['repository']['object']['text']
    return FileContentResponse(text=text)

# 5. Test Execution Block
if __name__ == "__main__":
    # Replace these with a repository you want to test against
    TEST_OWNER = "octocat"
    TEST_REPO = "Hello-World"
    
    print(f"--- Fetching Tree for {TEST_OWNER}/{TEST_REPO} ---")
    tree_data = get_repo_tree(TEST_OWNER, TEST_REPO)
    for entry in tree_data.entries:
        print(f"[{entry.type}] {entry.path}")
        
    print("\n--- Fetching Content for README.md ---")
    # Fetching a known file in that repo
    file_data = get_file_content(TEST_OWNER, TEST_REPO, "README")
    print(file_data.text)