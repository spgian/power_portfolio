# Power Portfolio Analytics

**Positions, wholesale cash flows and scenario comparison in Python.**

Developed by **Dr. Spyros Giannelos**.

Power Portfolio Analytics is a Python application for analysing the combined electricity position of a wind farm, a solar PV farm and an obligation to supply electricity to customers. The model calculates period-level generation, consumption, surpluses, shortages, wholesale purchases and sales, and the associated signed market cash flows.

The application analyses one illustrative delivery date with **48 half-hour settlement periods**. It also supports CSV-based scenarios, visualisation, a command-line interface and automated tests. It is a portfolio position and wholesale cash-flow model, **not a live trading system or a complete company-profit model**.

## Project Applications

The application provides a foundation for electricity portfolio analysis, energy supply management and quantitative trading support. It links physical electricity quantities to wholesale market transactions and financial outcomes.

The project demonstrates Python-based numerical modelling, structured data processing, scenario comparison, visualisation, command-line application development, automated testing and Git-based collaboration.

## Main Features

- **Portfolio modelling:** Analyse wind generation, solar PV generation and customer electricity consumption across 48 half-hour settlement periods.
- **Energy positions:** Calculate the portfolio's surplus (LONG), shortage (SHORT) or balanced position before wholesale transactions.
- **Wholesale market transactions:** Calculate required electricity purchases and sales for each period.
- **Cash-flow analysis:** Calculate purchase costs, sale revenues, net market cash flows, daily totals and volume-weighted purchase and sale prices.
- **Scenario comparison:** Compare two input datasets for the same delivery date and report scenario-minus-baseline differences.
- **CSV workflows:** Read validated input data and export period results and scenario comparisons.
- **Visualisation:** Produce four PNG charts of generation and demand, portfolio positions, wholesale prices and market cash flows.
- **Automated checks:** Use pytest to verify calculations, time labels, input rules, reporting and selected output files.

## Model Conventions

All generation and customer-consumption inputs are **energy quantities in MWh over a half-hour settlement period**, not instantaneous power values in MW. They must **not** be multiplied by 0.5 hours again.

For each settlement period, the model uses the following relationships:

```python
total_generation_mwh = wind_mwh + solar_mwh
net_position_mwh = total_generation_mwh - demand_mwh
purchase_mwh = max(-net_position_mwh, 0)
sale_mwh = max(net_position_mwh, 0)
purchase_cost_gbp = purchase_mwh * price_gbp_per_mwh
sale_revenue_gbp = sale_mwh * price_gbp_per_mwh
net_market_cash_flow_gbp = sale_revenue_gbp - purchase_cost_gbp
```

These expressions summarise the calculation rules. The implementation uses an `if` / `elif` / `else` structure to classify positions.

A **positive** pre-trade net position is LONG, a **negative** position is SHORT, and zero is BALANCED. Purchases and sales are non-negative energy quantities. Wholesale prices may be negative, so the monetary cost, revenue and cash-flow values may also be negative.

Each period is calculated independently before results are aggregated. An electricity surplus in one period does not offset a shortage in another period because this model contains no storage or inter-period energy transfer.

## Input Dataset

The supplied reference dataset is **illustrative**, generated from a reproducible example with random seed `42`. It is not based on measured company generation, customer demand or observed market prices. Its delivery date labels the sample and does not drive a historical weather or seasonal simulation.

The default input file is:

```text
data/portfolio_inputs_2026-09-01.csv
```

The CSV contains the following columns, in this order:

| Column | Meaning |
|---|---|
| `delivery_date` | Delivery date in `YYYY-MM-DD` format; all records must share one date. |
| `settlement_period` | Integer settlement-period number from 1 to 48. |
| `wind_mwh` | Wind-farm energy generated during the period, in MWh. |
| `solar_mwh` | Solar PV energy generated during the period, in MWh. |
| `demand_mwh` | Customer electricity consumption during the period, in MWh. |
| `price_gbp_per_mwh` | Assumed wholesale electricity price, in GBP/MWh. |

The file loader validates the column names and numeric values. It rejects non-finite values, negative energy quantities and inconsistent delivery dates, but it allows negative wholesale prices. The full-day reporting application requires settlement periods **1 through 48**, once each and in increasing order.

The reference dataset contains 48 data records plus a header row. The main application reads the saved CSV without regenerating or overwriting its input data.

## Requirements and Installation

The application can be run from a terminal or through a Python IDE such as PyCharm. Its packages are listed in `requirements.txt`, including Matplotlib for plotting and pytest for automated tests.

Clone the repository:

```bash
git clone https://github.com/spgian/power_portfolio.git
cd power_portfolio
```

Create a virtual environment on macOS or Linux, then install the dependencies:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
```

In PyCharm, select the interpreter located at `power_portfolio/.venv/bin/python`. A virtual environment keeps the project's installed packages separate from those of other Python projects.

No paid AI subscription or external electricity market data-service account is required to run the supplied examples.

## Running the Portfolio Analysis

From the repository root, run the application with its default CSV and output folder:

```bash
./.venv/bin/python main.py
```

To select an existing input file and a different output directory:

```bash
./.venv/bin/python main.py \
  --input data/portfolio_inputs_2026-09-01.csv \
  --output-dir results
```

Both `--input` and `--output-dir` are optional. With no options, the application reads `data/portfolio_inputs_2026-09-01.csv` and writes its results to `outputs/`, with those default paths resolved relative to `main.py`. Explicit command-line paths are resolved relative to the terminal's working directory unless absolute paths are supplied.

View the available options without running the calculations or creating output files:

```bash
./.venv/bin/python main.py --help
```

The report prints the 48 settlement periods, their energy positions and monetary results, daily totals, counts of LONG/SHORT/BALANCED periods, and volume-weighted purchase and sale prices.

## Scenario Comparison

The separate `compare_scenarios.py` application compares two input CSV files: a **baseline** and an **alternative scenario**.

Both files must describe the same delivery date and contain the complete, ordered 48-period sequence. The comparison reuses the existing portfolio calculation functions rather than implementing a second financial model.

Run the supplied higher-demand comparison:

```bash
./.venv/bin/python compare_scenarios.py \
  --baseline data/portfolio_inputs_2026-09-01.csv \
  --scenario data/portfolio_inputs_more_demand.csv \
  --output outputs/scenario_comparison.csv
```

The program displays daily totals for both cases and calculates every difference as:

```text
difference = scenario total - baseline total
```

It also saves a comparison CSV with unrounded numerical values. It does not create additional charts. The `--baseline` and `--scenario` arguments are required; `--output` is optional.

Display the command-line help:

```bash
./.venv/bin/python compare_scenarios.py --help
```

## Reference Results

The results below are for the **unchanged saved illustrative reference dataset**. Values are rounded for display.

| Metric | Reference result |
|---|---:|
| Wind generation | 499.81 MWh |
| Solar PV generation | 72.00 MWh |
| Total generation | 571.81 MWh |
| Customer consumption | 554.67 MWh |
| Sum of pre-trade net positions | +17.14 MWh |
| Total purchases | 62.67 MWh |
| Total sales | 79.81 MWh |
| Wholesale purchase cost | £6,085.54 |
| Wholesale sale revenue | £5,648.26 |
| **Net wholesale market cash flow** | **−£437.28** |
| LONG / SHORT / BALANCED periods | 29 / 19 / 0 |
| Volume-weighted purchase price | £97.10/MWh |
| Volume-weighted sale price | £70.77/MWh |

Although more MWh are sold than purchased, the volume-weighted purchase price exceeds the sale price. Consequently, total purchase cost exceeds total sale revenue. The resulting **−£437.28 is a net wholesale market cash outflow**, not the company's overall loss.

For the supplied higher-demand scenario, the reference comparison is:

| Metric | Amount |
|---|---:|
| Baseline net market cash flow | −£437.28 |
| Higher-demand scenario net market cash flow | −£492.78 |
| **Scenario minus baseline** | **−£55.50** |

These figures are reference results for the supplied example files, not target values for arbitrary inputs.

## Outputs and Charts

For an input file named `portfolio_inputs_2026-09-01.csv`, the main application saves the following files to the chosen output directory:

| File | Contents |
|---|---|
| `portfolio_inputs_2026-09-01_results.csv` | Period-by-period calculated positions, transactions and cash flows. |
| `portfolio_inputs_2026-09-01_generation_demand.png` | Wind, solar PV, combined generation and customer demand. |
| `portfolio_inputs_2026-09-01_positions.png` | Signed pre-trade electricity positions. |
| `portfolio_inputs_2026-09-01_prices.png` | Assumed wholesale electricity prices. |
| `portfolio_inputs_2026-09-01_cash_flows.png` | Signed net wholesale market cash flow by period. |

The program creates a missing output directory as needed. Its four charts show energy or financial outcomes for the **half-hour periods**, with appropriate units. Negative prices and negative cash flows remain visible.

## Price Sensitivity Examples

The `price_examples.py` module provides controlled demonstrations of zero and negative wholesale prices, and a daily sensitivity analysis that applies constant price shifts to the same illustrative electricity quantities.

Run it with:

```bash
./.venv/bin/python price_examples.py
```

The sensitivity cases use shifts of **−20, 0 and +20 GBP/MWh** relative to the original assumed prices. These are absolute price shifts, not percentage changes; the generation and demand quantities remain unchanged.

## Automated Tests

The project includes automated tests covering period-level financial calculations, input validation, settlement-period timing, reproducible sample data, command-line arguments, reporting and selected output files.

Run the test suite from the repository root:

```bash
./.venv/bin/python -m pytest -q
```

Tests that write example CSV files or charts use temporary directories where appropriate. The tests are designed to check the model's intended numerical and operational behaviour without modifying the saved reference input dataset.

## Repository Structure

```text
power_portfolio/
├── main.py                       # Full-day report, exports and charts
├── compare_scenarios.py          # Baseline and alternative scenario comparison
├── portfolio_calculations.py     # Per-period calculations and totals
├── portfolio_day.py              # Dated portfolio inputs and validation
├── portfolio_io.py               # Input and results CSV functions
├── portfolio_plots.py            # Generation, position, price and cash-flow charts
├── settlement_periods.py         # Half-hour timing and labels
├── sample_data.py                # Illustrative input-data generator
├── price_examples.py             # Price examples and sensitivity analysis
├── test_main.py
├── test_portfolio_day.py
├── test_settlement_periods.py
├── requirements.txt
├── README.md
├── CONTRIBUTING.md
├── AGENTS.md
├── CLAUDE.md
├── data/                         # Saved illustrative input CSV files
├── outputs/                      # Reference results and PNG charts
└── docs/                         # Supporting project documentation
```

## Project Presentation

A short project overview is intended to be provided in two formats:

- [Project overview (PDF)](docs/power_portfolio_overview.pdf)
- [Editable presentation (PowerPoint)](docs/power_portfolio_overview.pptx)

**These links will work once the corresponding files have been added to `docs/` and committed to the repository.**

## Scope and Limitations

- The sample data and prices are **illustrative**, not observed market or operational records.
- The model assumes an **ordinary 48-period delivery day**. It does not implement special settlement-period handling for daylight-saving clock changes.
- Each period uses one assumed wholesale price for both purchases and sales.
- The model assumes that every surplus is sold and every shortage is purchased at that price, without trading fees.
- Generation and customer consumption are fixed inputs. They do not respond to wholesale prices.
- The model does not optimise dispatch, include battery storage or represent electricity transmission constraints.
- Wholesale market cash flow excludes other revenues, customer tariffs, operating costs, imbalance arrangements and taxes. It must not be interpreted as complete company profit.
- The application does not connect to an exchange, place orders or execute trades.

## Contributing

Guidelines for proposing changes are available in [CONTRIBUTING.md](CONTRIBUTING.md). Contributions can be developed on a separate branch and proposed through a pull request. Changes should preserve the documented financial conventions unless a deliberate model extension is being implemented.

## Author

**Dr. Spyros Giannelos**
**The Energy Data Scientist**
