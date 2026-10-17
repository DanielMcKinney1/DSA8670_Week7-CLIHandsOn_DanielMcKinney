"""Analyze and graph the relationship between house size and construction year.

Run from any working directory with:
    python analysis/house_size_by_year.py

The script reads data/AmesHousing-1.csv and writes two PNG graphs beside this
file. It also prints summary statistics and a plain-language conclusion.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "AmesHousing-1.csv"
OUTPUT_DIR = Path(__file__).resolve().parent


def main():
    # Gr Liv Area measures above-grade living area in square feet.
    houses = pd.read_csv(DATA_FILE, usecols=["Year Built", "Gr Liv Area"])
    houses = houses.dropna().rename(
        columns={"Year Built": "year_built", "Gr Liv Area": "living_area_sqft"}
    )

    trend = linregress(houses["year_built"], houses["living_area_sqft"])

    # Graph 1: each point is a home; the line summarizes the overall linear trend.
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(
        houses["year_built"], houses["living_area_sqft"],
        alpha=0.28, s=16, color="#3478a8", edgecolors="none",
    )
    x_line = pd.Series(
        [houses["year_built"].min(), houses["year_built"].max()]
    )
    ax.plot(x_line, trend.intercept + trend.slope * x_line,
            color="#d1495b", linewidth=2.5, label="Linear trend")
    ax.set(
        title="House living area and year built",
        xlabel="Year built",
        ylabel="Above-grade living area (sq ft)",
    )
    ax.legend()
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "living_area_vs_year_built.png", dpi=180)
    plt.close(fig)

    # Graph 2: compare average living area by decade. Counts are shown to make
    # sparse decades visible in context.
    houses["decade"] = (houses["year_built"] // 10 * 10).astype(int)
    decade_summary = houses.groupby("decade")["living_area_sqft"].agg(
        ["mean", "count"]
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(
        decade_summary.index.astype(str), decade_summary["mean"],
        color="#3478a8",
    )
    ax.set(
        title="Average house living area by construction decade",
        xlabel="Construction decade",
        ylabel="Average above-grade living area (sq ft)",
    )
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", alpha=0.2)
    for bar, count in zip(bars, decade_summary["count"]):
        ax.annotate(
            f"n={count}",
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 3), textcoords="offset points",
            ha="center", va="bottom", fontsize=8,
        )
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "average_living_area_by_decade.png", dpi=180)
    plt.close(fig)

    direction = "larger" if trend.slope > 0 else "smaller"
    print(f"Homes analyzed: {len(houses):,}")
    print(f"Average living area: {houses['living_area_sqft'].mean():,.1f} sq ft")
    print(f"Estimated trend: {trend.slope:.2f} sq ft per later construction year")
    print(f"Pearson correlation: {trend.rvalue:.3f}; R-squared: {trend.rvalue**2:.3f}")
    print(
        f"Conclusion: newer houses are {direction} on average in this sample "
        "according to the overall linear trend. The relationship is an "
        "association; this analysis does not establish causation."
    )
    print("PNG graphs saved in:")
    print(f"  {OUTPUT_DIR / 'living_area_vs_year_built.png'}")
    print(f"  {OUTPUT_DIR / 'average_living_area_by_decade.png'}")


if __name__ == "__main__":
    main()
