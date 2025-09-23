import requests

def hello_world():
    """Test function to verify package functionality."""
    print("Hello World from Hyperwave Mock!")
    return "Hello World from Hyperwave Mock!"
 
def simulate_mock():
      """Call deployed FastAPI endpoint."""

      # Update with your Render URL
      API_URL = "https://hyperwave-cloud.onrender.com"

      response = requests.post(
          f"{API_URL}/multiply",
          json={
              "matrix_a": [[1, 2], [3, 4]],
              "matrix_b": [[5, 6], [7, 8]]
          }
      )

      return response.json()