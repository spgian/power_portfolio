# Contributing to the Power Portfolio Project

Use a separate branch for each proposed change.

Keep the existing financial calculations, units and sign conventions
unchanged unless the task explicitly requires otherwise.

Explain the purpose of the change and report only checks actually run.

Do not include credentials, private data, virtual environments or
unrelated experimental outputs.

## Fork contribution workflow

In your local clone, origin should identify your fork and upstream
should identify the original project repository.

Start from a clean main branch and retrieve the original project's updates:

```bash
git switch main
git fetch upstream
git merge --ff-only upstream/main
git push origin main
```

If the fast-forward update is refused, stop and inspect the histories.
Do not discard work or force-push to make the commands succeed.

Create a new contribution branch from the updated main. Commit your change
and push that branch to origin.

Open a pull request from your fork's contribution branch to the original
repository's main branch.
