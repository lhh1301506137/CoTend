# Example Workflow

This example shows the expected shape of a small CoTend project. It is intentionally simple so each decision and completion boundary is visible.

## Goal

Build a local Python command-line tool that divides an amount among participants using exact cents. It has no account, backend, network call, or external dependency.

## 1. Initialize

The user selects **CoTend Init** and asks CoTend to initialize the project. CoTend inspects the directory, establishes project continuity records, restates the goal and constraints, and reports readiness. It stops for the next instruction instead of writing unrelated product code immediately.

## 2. Resolve a product decision

The amount may not divide evenly. The requirement does not say who receives the remaining cents, so CoTend presents a concrete recommendation and alternatives. The user chooses that the remainder is distributed from the first participant onward, one cent at a time.

That answer becomes durable project truth. A later `Continue` may implement it, but could not have selected it before the user answered.

## 3. Implement and verify

Within the approved scope, CoTend creates the smallest implementation and tests:

- valid amounts with even division;
- deterministic remainder distribution;
- invalid decimal precision;
- positive participant-count validation;
- a property check that every share sums to the original amount.

CoTend reports test and review evidence. Passing AI checks is not yet user acceptance.

## 4. User acceptance

CoTend gives the user a short, readable walkthrough with representative commands and expected outputs. The user either accepts the goal or identifies a behavior to change. Only explicit acceptance closes the goal; `Continue` does not.

## 5. Handoff and fresh-task resume

After acceptance, CoTend can create a handoff document without reopening development. In a fresh task, CoTend Init reads the handoff and project records, independently reruns relevant checks, confirms that the project is already complete, and waits for a new goal.

This sequence demonstrates the central CoTend contract: AI development may continue autonomously inside approved work, while product choices, conflicting truth, and final acceptance remain visible human decisions.
