# Project instructions

## Purpose
This repository contains a Python model of a power portfolio.
It represents one wind farm producing electricity, 
one solar PV farm producing electricity and obligations to supply electricity to customers.
Read README.md when project background is needed, or run instructions are needed.
Do not assume that you have access to earlier conversations.

## Preserve the model conventions
- Generation and consumption are total MWh for the same half-hour period.
  Do not multiply these energy quantities by 0.5 again.
- Prices are in GBP/MWh. Monetary amounts are in GBP.
- Net position is wind generation plus solar generation minus electricity consumption.
  Positive means long; negative means short, before wholesale trades.
- Purchase and sale electricity quantities are non-negative. Negative prices are valid.
- Net market cash flow is sale revenue minus purchase cost.
  Preserve monetary signs; do not replace them with absolute values.
- Market cash flow is not complete company profit or an executed trade record.

## Keep changes focused
- Follow the current task and its acceptance criteria. Propose a short plan
  before editing and wait for the developer to approve implementation.
- Reuse the existing calculation functions. Do not duplicate their formulas
  or change them without explicit approval.
- Preserve main(input_csv=..., output_directory=...) and its existing defaults.
- Do not change the reference inputs or published outputs unless requested.
  Running main.py regenerates outputs, so ask before running it.
- Prefer small changes and existing modules. Do not add assets, dependencies
  or unrelated refactoring merely to complete a tooling improvement.
- Change this instruction file only when the task explicitly requests it.

## Actions and access
- A request for explanation or planning does not authorise edits or execution.
- Read only relevant, authorised project material. Do not read or expose
  credentials, tokens, private keys or unrelated personal files.
- Ask before installing packages, accessing external services or expanding
  permissions. Do not weaken sandbox or approval settings to bypass a block.
- Leave staging, commits, pushes, branch changes and merges to the developer. 
- Do not delete files or discard existing work.

## Checks and reporting
- Use the existing project Python environment. When test execution is approved,
  run relevant tests; the full macOS command from the project root is:
  `./.venv/bin/python -m pytest -q`
- Keep tests proportionate and use temporary output folders when appropriate.
  Do not alter correct expectations just to make incorrect code pass.
- Report what changed, the commands actually run and their actual outcomes.
  State clearly when tests were not run or information is missing.