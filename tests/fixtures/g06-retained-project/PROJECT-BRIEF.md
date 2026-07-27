# Expense Splitter G06 Project Brief

## Goal

Build a local Python standard-library command-line tool that divides a positive decimal amount among a positive integer number of participants. Every share is expressed in exact cents and the shares must sum to the original amount.

## Interface

```text
python expense_splitter.py AMOUNT PARTICIPANTS
```

Product output and error messages must be in English.

## Confirmed Rules

- `AMOUNT` is a positive ordinary decimal with at most two decimal places.
- `PARTICIPANTS` is a positive integer.
- When cents do not divide evenly, assign one extra cent in participant order, starting with Participant 1, until the remainder is exhausted.
- Invalid input returns a readable error without a traceback and uses a non-zero exit code.

## Acceptance

- `10.00 4` produces four shares of `2.50` and total `10.00`.
- `10.00 3` produces `3.34`, `3.33`, `3.33` and total `10.00`.
- `10.001 3` is rejected without a traceback.
- Automated tests cover validation, exact conservation, deterministic remainder order, and representative property checks.

## Non-Goals

- Accounts, backend services, network access, API keys, databases, package dependencies, UI, publishing, and deployment.

## G06 Boundary

This is a retained local project used for CoTend G06. Initialization must stop after reporting readiness. Product implementation starts only after the owner gives the next instruction. AI verification is not final user acceptance.
