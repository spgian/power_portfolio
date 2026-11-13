"""Generate illustrative inputs for an ordinary 48-period day."""

from random import Random


def generate_sample_day(seed: int = 42) -> list[dict[str, int | float]]:
    """Return 48 input dictionaries in settlement-period order.

    Energy values are period totals in MWh. Prices are in GBP/MWh.
    The same seed, code and Python environment reproduce the same inputs.
    A fresh local random-number generator is created for each call.
    """
    if type(seed) is not int:
        raise TypeError("seed must be an integer.")

    rng = Random(seed)
    period_inputs: list[dict[str, int | float]] = []

    for settlement_period in range(1, 49):
        # Period 1 -> 0.0; period 25 -> 12.0; period 48 -> 23.5.
        start_hour = (settlement_period - 1) * 0.5

        # Wind: choose a period energy quantity between 6 and 14 MWh.
        # Independent draws are not a model of actual wind dynamics.
        wind_mwh = round(rng.uniform(6.0, 14.0), 2)

        # Solar: a fixed triangular profile indexed by period start hour.
        # Peak assigned period energy is 6 MWh at a start hour of 12:00.
        # Zero is assigned at/before 06:00 and at/after 18:00.
        solar_shape = max(0.0, 1.0 - abs(start_hour - 12.0) / 6.0)
        solar_mwh = round(6.0 * solar_shape, 2)

        if 7.0 <= start_hour < 10.0 or 17.0 <= start_hour < 20.0:
            base_demand_mwh = 15.0
            base_price_gbp_per_mwh = 110.0
        elif 6.0 <= start_hour < 22.0:
            base_demand_mwh = 12.0
            base_price_gbp_per_mwh = 80.0
        else:
            base_demand_mwh = 9.0
            base_price_gbp_per_mwh = 60.0

        # Small pseudo-random adjustments around the chosen base values.
        demand_mwh = round(base_demand_mwh + rng.uniform(-1.0, 1.0), 2)

        price_gbp_per_mwh = round(base_price_gbp_per_mwh + rng.uniform(-10.0, 10.0), 2)

        # Use the same input structure that PortfolioDay already accepts.
        period_inputs.append(
            {
                "settlement_period": settlement_period,
                "wind_mwh": wind_mwh,
                "solar_mwh": solar_mwh,
                "demand_mwh": demand_mwh,
                "price_gbp_per_mwh": price_gbp_per_mwh,
            }
        )

    return period_inputs