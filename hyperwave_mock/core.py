import requests

def hello_world():
    """Test function to verify package functionality."""
    print("Hello World from Hyperwave Mock!")
    return "Hello World from Hyperwave Mock!"
 
def simulate_mock(api_key=None):
    """
    Call deployed FastAPI endpoint with API key authentication.

    The backend tracks userId, apiKeyHash, status (pending → approved → running → completed),
    and all timestamps. This function calls the API, receives simulation_id and
    computation_time_seconds, calculates cost locally, and returns that info.

    Args:
        api_key (str): The API key for authentication. Required.

    Returns:
        dict: Simulation metadata including ID prefix, duration, cost, and result.
    """

    if not api_key:
        print("Error: API key is required")
        return {"error": "API key is required. Please provide a valid API key."}

    API_URL = "https://hyperwave-cloud.onrender.com"
    HOURLY_RATE = 12.0  # $12/hour compute rate

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
        data = response.json()

        # Extract simulation metadata from response
        simulation_id = data.get("simulation_id", "")
        computation_time_seconds = data.get("computation_time_seconds", 0)
        result = data.get("result", None)
        rows = data.get("rows", 0)
        cols = data.get("cols", 0)
        execution_time = data.get("execution_time_seconds", 0)
        simulated_delay = data.get("simulated_delay_seconds", 0)

        # Calculate cost locally based on compute time
        cost_per_second = HOURLY_RATE / 3600
        total_cost = computation_time_seconds * cost_per_second

        # Print summary for user
        print(f"✓ Simulation completed successfully!")
        print(f"  - Simulation ID: {simulation_id[:8]}...")
        print(f"  - Duration: {computation_time_seconds:.2f} seconds")
        print(f"  - Cost: ${total_cost:.6f} (at ${HOURLY_RATE}/hour)")

        # Return only the result
        return result

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
