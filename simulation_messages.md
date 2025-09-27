# Simulation Endpoint Message Flow

## Workflow Paths and Messages

### 1. API Token Validation

#### Path 1.1: No Token Provided
```
Validating API key...

API key required to proceed.
Sign up for free at spinsphotonics.com to get your API key.

Need help? Contact us at spinsphotonics.com/contact
```

#### Path 1.2: Invalid/Wrong Token (HTTP 403)
```
Validating API key...

Invalid API key detected.
Please verify your API key in your dashboard at spinsphotonics.com/dashboard

Need help? Contact us at spinsphotonics.com/contact
```

#### Path 1.3: Valid Token
```
Validating API key...
Authentication successful for {user_email}
Welcome back, {user_name}
```
OR (if no name available)
```
Validating API key...
Authentication successful for {user_email}
```

### 2. Balance Check

#### Path 2.1: Insufficient Balance (HTTP 402)
```
Validating API key...

Insufficient credits for simulation.
Minimum required: 0.01 credits
Current balance: {current_balance} credits

Add credits to your account at spinsphotonics.com/billing

Need help? Contact us at spinsphotonics.com/contact
```

#### Path 2.2: Sufficient Balance
```
Simulation approved
Current balance: {balance:.4f} credits
Initializing simulation environment...
```
OR (if balance info not available from backend)
```
Simulation approved
Initializing simulation environment...
```

### 3. Simulation Execution

#### Path 3.1: Successful Simulation
```
Validating API key...
Authentication successful for {user_email}
Welcome back, {user_name}

Simulation approved
Current balance: {balance:.4f} credits
Initializing simulation environment...

Simulation complete
  Simulation ID: {first_8_chars_of_id}
  Runtime: {computation_time:.2f} seconds
  Credits consumed: {credits_used:.6f}
  Remaining balance: {new_balance:.4f} credits
```

### 4. Error Scenarios

#### Path 4.1: No API Key in Header (HTTP 401)
```
Validating API key...

No API key detected in request.
Sign up for free at spinsphotonics.com to get your API key.

Need help? Contact us at spinsphotonics.com/contact
```

#### Path 4.2: Server Error (HTTP 502)
```
Validating API key...

Service temporarily unavailable.
Our servers are experiencing high load. Please retry in a few moments.

Need help? Contact us at spinsphotonics.com/contact
```

#### Path 4.3: Request Timeout
```
Validating API key...

Request timeout.
The simulation server is taking longer than expected. Please try again.

Need help? Contact us at spinsphotonics.com/contact
```

#### Path 4.4: Connection Error
```
Validating API key...

Connection failed.
Unable to reach simulation servers. Please check your network connection and try again.

Need help? Contact us at spinsphotonics.com/contact
```

#### Path 4.5: Generic Request Failure
```
Validating API key...

Communication error.
Unable to process your request at this time. Please try again later.

Need help? Contact us at spinsphotonics.com/contact
```

#### Path 4.6: Invalid JSON Response
```
Validating API key...

Invalid server response.
Received malformed data from server. Our team has been notified.

Need help? Contact us at spinsphotonics.com/contact
```

#### Path 4.7: Other HTTP Errors
```
Validating API key...

Unexpected error (Code: {status_code})
Please try again or contact support if the issue persists.

Need help? Contact us at spinsphotonics.com/contact
```

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
Authentication successful for john.doe@example.com
Welcome back, John Doe

Simulation approved
Current balance: 114.9560 credits
Initializing simulation environment...

Simulation complete
  Simulation ID: abc12345
  Runtime: 10.50 seconds
  Credits consumed: 0.002917
  Remaining balance: 114.9531 credits
```

## Professional Message Guidelines

1. **Tone**: Clear, concise, and professional without being robotic
2. **Structure**: Status → Details → Action (if needed)
3. **Errors**: Always provide actionable next steps
4. **Support**: Include contact information only on terminal error states
5. **Numbers**:
   - Balance: 4 decimal places
   - Credits consumed: 6 decimal places
   - Runtime: 2 decimal places
6. **No emojis or special characters** except standard punctuation
7. **No technical jargon** in user-facing messages (no HTTP codes in main message, only in error codes)