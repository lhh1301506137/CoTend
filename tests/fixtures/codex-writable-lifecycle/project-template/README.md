# Tiny Local Calculator

This is a one-file calculator used only by its owner. The confirmed goal is to
keep the existing addition behavior working while future small changes remain
easy to review.

Project constraints:

- local-only and disposable development data;
- one-off, low-risk work suitable for CoTend's `lite` profile;
- no backend, account, network service, secret, deployment, or public release;
- no Trellis, Plan Tree, CodeGraph, dependency installation, or Git commit is
  needed during framework initialization.
