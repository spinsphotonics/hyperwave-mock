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
        print("\nAPI key required to proceed.")
        print("Sign up for free at spinsphotonics.com to get your API key.")
        print("\nNeed help? Contact us at spinsphotonics.com/contact")
        return None

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
            print(f"Authentication successful for {user_email}")
            print(f"Welcome back, {user_name}")
        else:
            print(f"Authentication successful for {user_email}")

        # Show balance and simulation approval
        if user_balance > 0 or not credit_cache:  # Show message if we have balance or if balance info not available
            print("\nSimulation approved")
            if user_balance > 0:
                print(f"Current balance: {user_balance:.4f} credits")
            print("Initializing simulation environment...")

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
        new_balance = user_balance - credits_used if user_balance > 0 else 0

        # Print simulation results
        print(f"\nSimulation complete")
        print(f"  Simulation ID: {simulation_id[:8] if len(simulation_id) > 8 else simulation_id}")
        print(f"  Runtime: {computation_time_seconds:.2f} seconds")
        print(f"  Credits consumed: {credits_used:.6f}")
        if user_balance > 0:
            print(f"  Remaining balance: {new_balance:.4f} credits")

        # Return only the result
        return result

    except requests.exceptions.HTTPError as e:
        # Access the response from the exception object
        if e.response is not None:
            status_code = e.response.status_code
            response_text = e.response.text

            if status_code == 401:
                print("\nNo API key detected in request.")
                print("Sign up for free at spinsphotonics.com to get your API key.")
                print("\nNeed help? Contact us at spinsphotonics.com/contact")
                return None
            elif status_code == 403:
                print("\nInvalid API key detected.")
                print("Please verify your API key in your dashboard at spinsphotonics.com/dashboard")
                print("\nNeed help? Contact us at spinsphotonics.com/contact")
                return None
            elif status_code == 402:
                # Try to extract current balance from response if available
                try:
                    error_data = e.response.json()
                    current_balance = error_data.get("current_balance", 0)
                    balance_msg = f"Current balance: {current_balance:.4f} credits"
                except:
                    balance_msg = ""

                print("\nInsufficient credits for simulation.")
                print("Minimum required: 0.01 credits")
                if balance_msg:
                    print(balance_msg)
                print("\nAdd credits to your account at spinsphotonics.com/billing")
                print("\nNeed help? Contact us at spinsphotonics.com/contact")
                return None
            elif status_code == 502:
                print("\nService temporarily unavailable.")
                print("Our servers are experiencing high load. Please retry in a few moments.")
                print("\nNeed help? Contact us at spinsphotonics.com/contact")
                return None
            else:
                print(f"\nUnexpected error (Code: {status_code})")
                print("Please try again or contact support if the issue persists.")
                print("\nNeed help? Contact us at spinsphotonics.com/contact")
                return None
        else:
            print(f"\nCommunication error.")
            print("Unable to process your request at this time. Please try again later.")
            print("\nNeed help? Contact us at spinsphotonics.com/contact")
            return None

    except requests.exceptions.Timeout:
        print("\nRequest timeout.")
        print("The simulation server is taking longer than expected. Please try again.")
        print("\nNeed help? Contact us at spinsphotonics.com/contact")
        return None

    except requests.exceptions.ConnectionError as e:
        print("\nConnection failed.")
        print("Unable to reach simulation servers. Please check your network connection and try again.")
        print("\nNeed help? Contact us at spinsphotonics.com/contact")
        return None

    except requests.exceptions.RequestException as e:
        print("\nCommunication error.")
        print("Unable to process your request at this time. Please try again later.")
        print("\nNeed help? Contact us at spinsphotonics.com/contact")
        return None

    except ValueError as e:
        print("\nInvalid server response.")
        print("Received malformed data from server. Our team has been notified.")
        print("\nNeed help? Contact us at spinsphotonics.com/contact")
        return None