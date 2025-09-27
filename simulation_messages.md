# Simulation Endpoint Message Flow

## Workflow Paths and Messages

### 1. API Token Validation

#### Path 1.1: No Token Provided
```
Validating API key...

❌ No API key provided.
Please sign up for an API key at spinsphotonics.com

Something doesn't look right? Contact us at spinsphotonics.com/contact
```
**Return Value:** `{"error": "API key is required. Please provide a valid API key."}`

#### Path 1.2: Invalid/Wrong Token (HTTP 403)
```
Validating API key...

❌ Invalid API key.
Please check your API key or verify if it's still active at your dashboard on spinsphotonics.com

Something doesn't look right? Contact us at spinsphotonics.com/contact
```
**Return Value:** `{"error": "Invalid API key"}`

#### Path 1.3: Valid Token
```
Validating API key...
✓ API key verified for {user_email}. Welcome, {user_name}!
```
OR (if no name available)
```
Validating API key...
✓ API key verified for {user_email}.
```

### 2. Balance Check

#### Path 2.1: Insufficient Balance (HTTP 402)
```
Validating API key...

❌ Insufficient balance.
Minimum credits required: 0.01 to start simulation
Please top up your account at spinsphotonics.com

Something doesn't look right? Contact us at spinsphotonics.com/contact
```
**Return Value:** `{"error": "Insufficient balance: {response_text}"}`

#### Path 2.2: Sufficient Balance
```
✓ Simulation approved. Your current balance is: {balance:.4f} credits
Starting simulation...
```
OR (if balance info not available from backend)
```
✓ Simulation approved.
Starting simulation...
```

### 3. Simulation Execution

#### Path 3.1: Successful Simulation
```
Validating API key...
✓ API key verified for {user_email}. Welcome, {user_name}!

✓ Simulation approved. Your current balance is: {balance:.4f} credits
Starting simulation...

✓ Simulation completed successfully!
  - Simulation ID: {first_8_chars_of_id}...
  - Duration: {computation_time:.2f} seconds
  - Credits used: {credits_used:.6f}
```
**Return Value:** The actual simulation result (matrix multiplication result or other computation data)

### 4. Error Scenarios

#### Path 4.1: No API Key in Header (HTTP 401)
```
Validating API key...

❌ No API key provided.
Please sign up for an API key at spinsphotonics.com

Something doesn't look right? Contact us at spinsphotonics.com/contact
```
**Return Value:** `{"error": "API key is required. Please provide X-API-Key header."}`

#### Path 4.2: Server Error (HTTP 502)
```
Validating API key...

❌ Server error.
The service may be starting up or experiencing issues. Please try again in a moment.

Something doesn't look right? Contact us at spinsphotonics.com/contact
```
**Return Value:** `{"error": "Server error (502 Bad Gateway). The service may be starting up or experiencing issues. Please try again in a moment."}`

#### Path 4.3: Request Timeout
```
Validating API key...

❌ Request timed out.
The server may be slow to respond. Please try again.

Something doesn't look right? Contact us at spinsphotonics.com/contact
```
**Return Value:** `{"error": "Request timed out. The server may be slow to respond."}`

#### Path 4.4: Connection Error
```
Validating API key...

❌ Connection error.
Failed to connect to the server. Please check your internet connection.

Something doesn't look right? Contact us at spinsphotonics.com/contact
```
**Return Value:** `{"error": "Failed to connect to the server. Please check your internet connection."}`

#### Path 4.5: Generic Request Failure
```
Validating API key...

❌ Request failed.
An unexpected error occurred while communicating with the server.

Something doesn't look right? Contact us at spinsphotonics.com/contact
```
**Return Value:** `{"error": "Request failed: {error_details}"}`

#### Path 4.6: Invalid JSON Response
```
Validating API key...

❌ Invalid server response.
The server returned an unexpected response format.

Something doesn't look right? Contact us at spinsphotonics.com/contact
```
**Return Value:** `{"error": "Invalid response from server"}`

#### Path 4.7: Other HTTP Errors
```
Validating API key...

❌ Unexpected error (HTTP {status_code})

Something doesn't look right? Contact us at spinsphotonics.com/contact
```
**Return Value:** `{"error": "HTTP {status_code}: {response_text}"}`

## Balance Calculation

When the backend provides a `creditCache` object, the balance is calculated as:
```
balance = (totalPurchasedMillicredits * 3600 - totalUsedMilliseconds) / 1000
```

Example creditCache:
```json
{
  "creditCache": {
    "lastCalculated": "2025-09-26T18:02:57-07:00",
    "totalPurchased": 32,
    "totalPurchasedMillicredits": 32000,
    "totalUsedMilliseconds": 244000,
    "totalUsedSeconds": 244,
    "version": 6
  }
}
```

For this example: `balance = (32000 * 3600 - 244000) / 1000 = 114,956 credits`

## Credits Usage Calculation

Credits used for a simulation = `computation_time_seconds / 3600`

For example:
- 10 second simulation = 0.002778 credits
- 60 second simulation = 0.016667 credits
- 3600 second simulation = 1.0 credit

## Complete Success Flow Example

```
Validating API key...
✓ API key verified for john.doe@example.com. Welcome, John Doe!

✓ Simulation approved. Your current balance is: 114.9560 credits
Starting simulation...

✓ Simulation completed successfully!
  - Simulation ID: abc12345...
  - Duration: 10.50 seconds
  - Credits used: 0.002917
```

## Notes

1. All terminal error messages (final messages in error paths) include the support contact line
2. Success messages use checkmarks (✓) while errors use X marks (❌)
3. The actual simulation result data is returned separately from these display messages
4. User information (email, name, balance) is only shown if provided by the backend
5. Balance is shown with 4 decimal places for precision
6. Credits used is shown with 6 decimal places for accuracy