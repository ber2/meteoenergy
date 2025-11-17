import marimo

__generated_with = "0.16.2"
app = marimo.App(
    width="full",
    layout_file="layouts/meteo_energy_app.grid.json",
)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import pandas as pd
    import plotly.express as px
    from scipy.stats import ttest_ind
    return pd, px, ttest_ind


@app.cell
def _(pd):
    meteo_data = pd.read_csv(
        "https://raw.githubusercontent.com/ber2/meteoenergy/refs/heads/master/data/meteo-summary.csv", index_col=0, parse_dates=["date"]
    )
    return (meteo_data,)


@app.cell
def _(pd):
    pricing_data = pd.read_csv(
        "https://raw.githubusercontent.com/ber2/meteoenergy/refs/heads/master/data/pvpc-summary.csv", index_col=0, parse_dates=["date"]
    )
    return (pricing_data,)


@app.cell
def _(pricing_data):
    pricing_data_simplified = pricing_data[pricing_data.toll == "2.0.DHA"][
        ["date", "pvpc_eur_MWh"]
    ]
    pricing_data_simplified.columns = ["date", "price"]
    return (pricing_data_simplified,)


@app.cell
def _(meteo_data, pd, pricing_data_simplified):
    df_base = pd.merge(meteo_data, pricing_data_simplified, on="date", how="inner")
    df_base = df_base.sort_values("date")
    df_base["rainfall_weekly_mm"] = df_base.rainfall_mm.rolling(7).agg("sum")
    df_base["rainfall_monthly_mm"] = df_base.rainfall_mm.rolling(30).agg("sum")
    df_base["rainfall_quarterly_mm"] = df_base.rainfall_mm.rolling(30).agg("sum")
    return (df_base,)


@app.cell
def _(mo):
    weather_col = mo.ui.dropdown(
        options=[
            "rainfall_mm",
            "sunshine_MJ_daym2",
            "tmax_C",
            "tmed_C",
            "tmin_C",
            "windspeed_m_s",
            "rainfall_weekly_mm",
            "rainfall_monthly_mm",
            "rainfall_quarterly_mm",
        ],
        value="windspeed_m_s",
        label="Weather condition",
        allow_select_none=False,
    )
    return (weather_col,)


@app.cell
def _(mo, weather_col):
    perc = mo.ui.slider(
        start=0,
        stop=1,
        step=0.05,
        value=0.85,
        label="Percentile for extreme weather",
    )

    alpha = mo.ui.text(value="0.01", label="Significance $\\alpha$ = ")

    controls = mo.hstack([weather_col, perc, alpha], justify="start")
    return alpha, controls, perc


@app.cell
def _(controls, mo):
    mo.md("## Controls").center()
    controls
    return


@app.cell
def _(df_base, perc, weather_col):
    threshold = df_base[weather_col.value].quantile(q=perc.value)
    df = df_base.copy()
    df["weather_type"] = df[weather_col.value].apply(
        lambda x: "High" if x >= threshold else "Low"
    )
    return df, threshold


@app.cell
def _():
    labels = {
        "price": "€",
        "weather_type": "Extremal",
        "windspeed_m_s": "Wind (m/s)",
        "rainfall_mm": "Daily rain (mm)",
        "sunshine_MJ_daym2": "Sunshine (MJ/m^2)",
        "tmax_C": "Max Temp (C)",
        "tmed_C": "Avg Temp (C)",
        "tmin_C": "Min Temp(C)",
        "rainfall_weekly_mm": "Weekly rain (mm)",
        "rainfall_monthly_mm": "Monthly rain (mm)",
        "rainfall_quarterly_mm": "Quarterly rain (mm)",
    }
    return (labels,)


@app.cell
def _(df, labels, px, weather_col):
    fig_scatter = px.scatter(
        df,
        x=weather_col.value,
        y="price",
        range_y=[0, df.price.max() * 1.15],
        color="weather_type",
        color_discrete_map={"High": "goldenrod", "Low": "#00A"},
        template="plotly",
        title=f"Relationship between <b>{labels[weather_col.value]}</b> and price",
        labels=labels,
        opacity=0.5,
        # trendline="ols",
        # width=500,
    )
    return (fig_scatter,)


@app.cell
def _(df, labels, px):
    fig_evo = px.scatter(
        df,
        x="date",
        y="price",
        range_y=[0, df.price.max() * 1.15],
        color="weather_type",
        color_discrete_map={"High": "goldenrod", "Low": "#00A"},
        template="plotly",
        title="Evolution of prices",
        opacity=0.5,
        labels=labels,
        # width=500,
    )
    return (fig_evo,)


@app.cell
def _(fig_scatter):
    fig_scatter
    return


@app.cell
def _(fig_evo):
    fig_evo
    return


@app.cell
def _(df, threshold, weather_col):
    high_values = df[df[weather_col.value] >= threshold].price
    low_values = df[df[weather_col.value] < threshold].price
    return high_values, low_values


@app.cell
def _(high_values, low_values):
    high_mean = high_values.mean()
    low_mean = low_values.mean()
    return high_mean, low_mean


@app.cell
def _(high_values, low_values, ttest_ind):
    t_test_result = ttest_ind(high_values, low_values)
    stat = t_test_result.statistic
    p_val = t_test_result.pvalue
    return p_val, stat


@app.cell
def _(high_mean, labels, low_mean, mo, p_val, perc, stat, weather_col):
    mo.md(
        f"""
    # T-test results

    Weather condition: {labels[weather_col.value]}\n
    Splitting at percentile: {perc.value}

    High mean price = {high_mean}\n
    Low mean price = {low_mean}\n
    Difference = {high_mean - low_mean}\n
    \n
    T-Statistic = {stat}\n
    p-value = {p_val}\n
    """
    )
    return


@app.cell
def _(alpha, mo, p_val):
    if p_val < float(alpha.value):
        text = mo.md(
            "Since $p < \\alpha$, we reject the null hypothesis that the two groups come from the same distribution"
        )
    else:
        text = mo.md("Since $p >= \\alpha$, we fail to reject the null hypothesis")
    text
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
