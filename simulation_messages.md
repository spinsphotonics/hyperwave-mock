# Simulation Endpoint Message Flow

## Workflow Paths and Messages

### 1. Successful Simulation
```
Simulation complete.
Simulation ID: 1a65b4c9
Runtime: 9.44 seconds
Credits consumed: 0.002623
```

### 2. Error Scenarios

#### Path 2.1: No Token Provided
```
API key required to proceed.
Sign up for free at spinsphotonics.com to get your API key.
```

#### Path 2.2: Invalid/Wrong Token (HTTP 403)
```
Provided API key is invalid.
Please verify your API key in your dashboard at spinsphotonics.com/dashboard
```

#### Path 2.3: No API Key in Header (HTTP 401)
```
No API key detected in request.
Sign up for free at spinsphotonics.com to get your API key.
```

#### Path 2.4: Insufficient Balance (HTTP 402)
```
Insufficient credits for simulation.
Minimum required: 0.01 credits
Current balance: {current_balance} credits
Add credits to your account at spinsphotonics.com/billing
```
OR (if balance not available)
```
Insufficient credits for simulation.
Minimum required: 0.01 credits
Add credits to your account at spinsphotonics.com/billing
```

#### Path 2.5: Server Error (HTTP 502)
```
Service temporarily unavailable.
Our servers are experiencing high load. Please retry in a few moments.
```

#### Path 2.6: Request Timeout
```
Request timeout.
The simulation server is taking longer than expected. Please try again.
```

#### Path 2.7: Connection Error
```
Connection failed.
Unable to reach simulation servers. Please check your network connection and try again.
```

#### Path 2.8: Generic Request Failure
```
Communication error.
Unable to process your request at this time. Please try again later.
```

#### Path 2.9: Invalid JSON Response
```
Invalid server response.
Received malformed data from server. Our team has been notified.
```

#### Path 2.10: Other HTTP Errors
```
Unexpected error (Code: {status_code})
Please try again or contact support if the issue persists.
```

## Balance Calculation

When the backend provides a `creditCache` object, the balance is calculated as:
```
balance = (totalPurchasedMillicredits * 3600 - totalUsedMilliseconds) / 1000
```

## Credits Usage Calculation

Credits used for a simulation = `computation_time_seconds / 3600`

For example:
- 10 second simulation = 0.002778 credits
- 60 second simulation = 0.016667 credits
- 3600 second simulation = 1.0 credit

## Message Guidelines

1. **No intermediate status messages** - Only show final results or errors
2. **Success format**: Simple, no indentation, just the key metrics
3. **Error format**: State the problem and provide actionable next step
4. **Numbers**:
   - Runtime: 2 decimal places
   - Credits consumed: 6 decimal places
5. **No emojis or special characters**
6. **Clean and minimal output**