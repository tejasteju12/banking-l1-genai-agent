# SOP-004

Title: ATM Cash Not Received
Category: ATM
Issue: Cash Not Received
Support Level: L1
Version: 1.0
Status: Active

## Symptoms

Customer attempted an ATM withdrawal but did not receive cash.

Examples:

- Cash not received
- ATM did not dispense cash
- Account debited but ATM gave no cash
- Partial cash received

## Resolution Steps

### Step 1

Identify transaction status:

- Successful
- Failed
- Pending
- Account debited

### Step 2

Collect only permitted transaction information:

- Transaction date
- Approximate transaction time
- ATM location
- Transaction amount
- Masked account/card identifier as permitted by policy

Never request PIN or CVV.

### Step 3

If account was not debited:

Explain that the transaction may have failed without financial impact.

Check transaction status in the authorized system.

### Step 4

If account was debited but cash was not received:

- Do not ask customer to retry immediately.
- Check transaction status.
- Create a dispute/request according to the approved ATM dispute process.

### Step 5

If partial cash was received:

Record the amount dispensed and the transaction amount.

Raise the applicable ATM cash discrepancy/dispute request.

## Escalation

Escalate when:

- Account is debited and cash was not received.
- Partial cash was received.
- Transaction cannot be located.
- ATM system status is unavailable.
- Customer reports repeated ATM discrepancies.

## Security

Never request:

- ATM PIN
- CVV
- OTP
- Full card number
