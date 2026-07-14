---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, mentions "grill me", or wants one-question-at-a-time clarification where replying `1` accepts the recommended default answer.
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

For each question:

1. Ask one question only.
2. Explain why the question matters.
3. Provide your recommended answer as option `1`.
4. Tell the user that replying only `1` means "accept your recommended answer and continue".
5. Wait for the user's answer before asking the next question.

Compact response rule:

- Always include `1 = accept my recommended answer` after the question.
- If the user replies only `1`, treat it as agreement with the recommended answer and continue to the next question.
- If the user replies with any other text, treat it as their custom answer.
- Do not pack multiple unresolved decisions into one `1`; one question still means one decision.

If a question can be answered by exploring the codebase, explore the codebase instead.
