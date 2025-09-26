import requests

def hello_world():
    """Test function to verify package functionality."""
    print("Hello World from Hyperwave Mock!")
    return "Hello World from Hyperwave Mock!"
 
def simulate_mock(api_key=None):
    """
    Call deployed FastAPI endpoint with API key authentication.

    Args:
        api_key (str): The API key for authentication. Required.

    Returns:
        dict: The multiplication result if successful, None otherwise.
    """

    if not api_key:
        print("Error: API key is required")
        return {"error": "API key is required. Please provide a valid API key."}

    API_URL = "https://hyperwave-cloud.onrender.com"

    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            f"{API_URL}/multiply",
            json={
                "matrix_a": [[1, 2], [3, 4]],
                "matrix_b": [[5, 6], [7, 8]]
            },
            headers=headers
        )

        response.raise_for_status()  # raises HTTPError if status != 200
        return response.json()

    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("Error: API key is required")
            return {"error": "API key is required. Please provide X-API-Key header."}
        elif response.status_code == 403:
            print("Error: Invalid API key")
            return {"error": "Invalid API key"}
        else:
            print(f"HTTP error: {e}")
            print(f"Response: {response.text}")
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": f"Request failed: {str(e)}"}
    except ValueError:
        print(f"Invalid JSON response: {response.text}")
        return {"error": "Invalid response from server"}
