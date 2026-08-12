# Browser Tool Routing

Use this module only when UI/browser behavior or Chrome state affects verification. Combine it directly with `acceptance-test-harness.md`; it owns browser-surface selection and Chrome escalation behavior, not general acceptance evidence.

Use this routing before choosing a browser surface:

| Situation | Preferred Surface |
|---|---|
| Localhost, 127.0.0.1, file preview, quick visual inspection inside Codex Desktop. | `browser:control-in-app-browser` |
| Repeatable UI regression, scripted navigation, screenshots/traces, form flows, CI-like evidence. | `playwright` |
| Existing user Chrome login/session/cookies/profile, current Chrome tab, Chrome extension, OAuth/third-party account already signed in, Chrome-only bug, or explicit user request to use Chrome. | `chrome:control-chrome` |

Do not use Chrome merely because a connector/API auth expired. Ask the user to fix auth or explicitly approve Chrome fallback.

## Chrome Escalation Triggers

Use the canonical Chrome Escalation Triggers in `authority-and-triggers.md`. When any trigger appears, consider `chrome:control-chrome` and either use it or record why not.

If Chrome is required but unavailable, report `chrome_required_but_unavailable` and ask the user to open/sign in/enable Chrome rather than substituting unrelated web search or a different source.
