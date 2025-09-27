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

    # Check for API key
    print("Validating API key...")

    if not api_key:
        print("\n❌ No API key provided.")
        print("Please sign up for an API key at spinsphotonics.com")
        print("\nSomething doesn't look right? Contact us at spinsphotonics.com/contact")
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
            headers=headers,
            timeout=60  # Add explicit timeout
        )

        response.raise_for_status()  # raises HTTPError if status != 200
        data = response.json()

        # Extract user information from response (if provided by backend)
        user_info = data.get("user_info", {})
        user_email = user_info.get("email", data.get("user_email", "your account"))
        user_name = user_info.get("name", data.get("user_name", ""))

        # Extract or calculate user balance from credit cache if provided
        credit_cache = user_info.get("creditCache", data.get("credit_cache", {}))
        if credit_cache:
            total_purchased_millicredits = credit_cache.get("totalPurchasedMillicredits", 0)
            total_used_milliseconds = credit_cache.get("totalUsedMilliseconds", 0)
            # Calculate balance: (millicredits * 3600 - used milliseconds) / 1000
            user_balance = (total_purchased_millicredits * 3600 - total_used_milliseconds) / 1000
        else:
            user_balance = data.get("user_balance", 0)

        # Show successful API key validation
        if user_name:
            print(f"✓ API key verified for {user_email}. Welcome, {user_name}!")
        else:
            print(f"✓ API key verified for {user_email}.")

        # Show balance and simulation approval
        if user_balance > 0 or not credit_cache:  # Show message if we have balance or if balance info not available
            if user_balance > 0:
                print(f"\n✓ Simulation approved. Your current balance is: {user_balance:.4f} credits")
            else:
                print(f"\n✓ Simulation approved.")
            print("Starting simulation...")

        # Extract simulation metadata from response
        simulation_id = data.get("simulation_id", "")
        computation_time_seconds = data.get("computation_time_seconds", 0)
        result = data.get("result", None)
        rows = data.get("rows", 0)
        cols = data.get("cols", 0)
        execution_time = data.get("execution_time_seconds", 0)
        simulated_delay = data.get("simulated_delay_seconds", 0)

        # Calculate credits used (seconds / 3600)
        credits_used = computation_time_seconds / 3600

        # Print simulation results
        print(f"\n✓ Simulation completed successfully!")
        print(f"  - Simulation ID: {simulation_id[:8]}...")
        print(f"  - Duration: {computation_time_seconds:.2f} seconds")
        print(f"  - Credits used: {credits_used:.6f}")

        # Return only the result
        return result

    except requests.exceptions.HTTPError as e:
        # Access the response from the exception object
        if e.response is not None:
            status_code = e.response.status_code
            response_text = e.response.text

            if status_code == 401:
                print("\n❌ No API key provided.")
                print("Please sign up for an API key at spinsphotonics.com")
                print("\nSomething doesn't look right? Contact us at spinsphotonics.com/contact")
                return {"error": "API key is required. Please provide X-API-Key header."}
            elif status_code == 403:
                print("\n❌ Invalid API key.")
                print("Please check your API key or verify if it's still active at your dashboard on spinsphotonics.com")
                print("\nSomething doesn't look right? Contact us at spinsphotonics.com/contact")
                return {"error": "Invalid API key"}
            elif status_code == 402:
                print("\n❌ Insufficient balance.")
                print("Minimum credits required: 0.01 to start simulation")
                print("Please top up your account at spinsphotonics.com")
                print("\nSomething doesn't look right? Contact us at spinsphotonics.com/contact")
                return {"error": f"Insufficient balance: {response_text}"}
            elif status_code == 502:
                print("\n❌ Server error.")
                print("The service may be starting up or experiencing issues. Please try again in a moment.")
                print("\nSomething doesn't look right? Contact us at spinsphotonics.com/contact")
                return {"error": "Server error (502 Bad Gateway). The service may be starting up or experiencing issues. Please try again in a moment."}
            else:
                print(f"\n❌ Unexpected error (HTTP {status_code})")
                print("\nSomething doesn't look right? Contact us at spinsphotonics.com/contact")
                return {"error": f"HTTP {status_code}: {response_text}"}
        else:
            print(f"\n❌ HTTP error occurred")
            print("\nSomething doesn't look right? Contact us at spinsphotonics.com/contact")
            return {"error": f"HTTP error: {str(e)}"}

    except requests.exceptions.Timeout:
        print("\n❌ Request timed out.")
        print("The server may be slow to respond. Please try again.")
        print("\nSomething doesn't look right? Contact us at spinsphotonics.com/contact")
        return {"error": "Request timed out. The server may be slow to respond."}

    except requests.exceptions.ConnectionError as e:
        print("\n❌ Connection error.")
        print("Failed to connect to the server. Please check your internet connection.")
        print("\nSomething doesn't look right? Contact us at spinsphotonics.com/contact")
        return {"error": "Failed to connect to the server. Please check your internet connection."}

    except requests.exceptions.RequestException as e:
        print("\n❌ Request failed.")
        print("An unexpected error occurred while communicating with the server.")
        print("\nSomething doesn't look right? Contact us at spinsphotonics.com/contact")
        return {"error": f"Request failed: {str(e)}"}

    except ValueError as e:
        print("\n❌ Invalid server response.")
        print("The server returned an unexpected response format.")
        print("\nSomething doesn't look right? Contact us at spinsphotonics.com/contact")
        return {"error": "Invalid response from server"}