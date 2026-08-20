# SOP-002

Title: UPI Payment Failed
Category: UPI
Issue: UPI Payment Failed
Support Level: L1
Version: 1.0
Status: Active

## Symptoms

Customer reports that a UPI payment failed.

Examples:

- UPI payment failed
- Payment unsuccessful
- UPI transaction failed
- Merchant did not receive payment

## Resolution Steps

### Step 1

Determine the transaction state:

- Failed
- Pending
- Successful
- Money debited but recipient did not receive

### Step 2

Check basic conditions:

- Customer account is active.
- UPI service is available.
- Customer is using the registered device.
- Network connectivity is available.
- Transaction amount is within applicable limits.

Never request the customer's UPI PIN or OTP.

### Step 3

If the transaction is confirmed as failed:

1. Check network connectivity.
2. Close and reopen the official banking application.
3. Retry the transaction once.
4. Do not repeatedly retry if the transaction continues to fail.

### Step 4

If money was debited:

- Do not ask the customer to make another payment immediately.
- Check transaction status.
- If pending, follow the pending transaction procedure.
- If failed but debit remains unresolved, escalate to transaction reconciliation/dispute support.

### Step 5

If the customer does not recognize the transaction:

- Treat it as a potential unauthorized transaction.
- Follow the fraud/security procedure.
- Escalate immediately.

## Escalation

Escalate when:

- Money is debited but final status cannot be determined.
- Payment remains pending beyond the defined resolution window.
- Unauthorized activity is reported.
- Multiple transactions fail.
- UPI service/system error is detected.
- L1 cannot resolve the issue.

## Security

Never request:

- UPI PIN
- OTP
- Password
- CVV
- Full card details
