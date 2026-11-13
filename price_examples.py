"""Demonstrate price scenarios and daily cash-flow sensitivity."""

from datetime import date
from math import isfinite

from portfolio_calculations import calculate_portfolio_period
from portfolio_day import PortfolioDay
from sample_data import generate_sample_day


def show_single_period_examples() -> None:
    """Print six examples using the unchanged portfolio model."""
    solar_mwh: float = 2.0
    demand_mwh: float = 12.0

    # Wind of 8 MWh gives a 2 MWh shortage; 12 MWh gives a 2 MWh surplus.
    wind_examples = (8.0, 12.0)
    price_examples = (80.0, 0.0, -20.0)  # GBP/MWh, not customer tariffs.

    print("CONTROLLED PRICE EXAMPLES: ONE HALF-HOUR")
    print("Alternative cases, not six consecutive settlement periods.")
    print("Solar PV: 2.00 MWh | Customer consumption: 12.00 MWh")
    print("Position is measured BEFORE the model's purchase or sale.")
    print()
    print(
        f"{'Position':<8} {'Price GBP/MWh':>14} "
        f"{'Buy MWh':>9} {'Sell MWh':>10} "
        f"{'Net cash GBP':>15} {'Cash flow':>10}"
    )

    for wind_mwh in wind_examples:
        for price_gbp_per_mwh in price_examples:
            result = calculate_portfolio_period(
                wind_mwh=wind_mwh,
                solar_mwh=solar_mwh,
                demand_mwh=demand_mwh,
                price_gbp_per_mwh=price_gbp_per_mwh,
            )

            cash_flow_gbp = float(result["net_market_cash_flow_gbp"])
            if cash_flow_gbp > 0.0:
                direction = "INFLOW"
            elif cash_flow_gbp < 0.0:
                direction = "OUTFLOW"
            else:
                direction = "ZERO"

            print(
                f"{result['position']:<8} {price_gbp_per_mwh:>14.2f} "
                f"{result['purchase_mwh']:>9.2f} "
                f"{result['sale_mwh']:>10.2f} "
                f"{cash_flow_gbp:>+15.2f} {direction:>10}"
            )



def shift_wholesale_prices(
    period_inputs: list[dict[str, int | float]],
    shift_gbp_per_mwh: float,
) -> list[dict[str, int | float]]:
    """Copy the valid input records and add the same amount to each price.

    A shift of 20 means +20 GBP/MWh, not +20 percent.
    The original records and all energy quantities remain unchanged.
    """
    if type(shift_gbp_per_mwh) not in (int, float):
        raise TypeError("The price shift must be a number.")
    if not isfinite(shift_gbp_per_mwh):
        raise ValueError("The price shift must be finite.")



    shifted_inputs: list[dict[str, int | float]] = []
    for period in period_inputs:
        # Each record is flat, so copying its dictionary is sufficient here.
        updated_period = period.copy()
        updated_period["price_gbp_per_mwh"] = (
            period["price_gbp_per_mwh"] + shift_gbp_per_mwh
        )
        shifted_inputs.append(updated_period)

    return shifted_inputs


def show_daily_price_sensitivity() -> None:
    """Recalculate one fixed 48-period dataset at three price levels."""
    delivery_date = date(2026, 9, 1)
    baseline_inputs = generate_sample_day(seed=42)
    baseline_day = PortfolioDay(delivery_date, baseline_inputs)
    baseline_totals = baseline_day.calculate_totals()
    baseline_cash = baseline_totals["net_market_cash_flow_gbp"]

    # Every shift is relative to the ORIGINAL prices, not the previous case.
    cases = (("Baseline", 0.0), ("Prices lower", -20.0), ("Prices higher", 20.0))

    print("DAILY PRICE SENSITIVITY: 48 SETTLEMENT PERIODS")
    print(f"Delivery date: {delivery_date.isoformat()} | Example-data seed: 42")
    print("Same electricity quantities. Alternative prices for the same day.")
    print()
    print(
        f"{'Case':<14} {'Shift GBP/MWh':>14} {'Buy MWh':>9} "
        f"{'Sell MWh':>10} {'Net cash GBP':>15} {'Change GBP':>13}"
    )


    for label, shift in cases:
        scenario_inputs = shift_wholesale_prices(baseline_inputs, shift)
        scenario_day = PortfolioDay(delivery_date, scenario_inputs)
        totals = scenario_day.calculate_totals()
        cash = totals["net_market_cash_flow_gbp"]
        change_from_baseline = cash - baseline_cash

        print(
            f"{label:<14} {shift:>+14.2f} {totals['purchase_mwh']:>9.2f} "
            f"{totals['sale_mwh']:>10.2f} {cash:>+15.2f} "
            f"{change_from_baseline:>+13.2f}"
        )


def main() -> None:
    """Keep the 5.1 demonstration and then run the new 5.2 comparison."""
    show_single_period_examples()
    print()
    show_daily_price_sensitivity()


if __name__ == "__main__":
    main()
