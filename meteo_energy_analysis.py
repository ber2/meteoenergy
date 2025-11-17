import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    import pandas as pd
    import plotly.express as px
    return pd, px


@app.cell
def _(pd):
    meteo_data = pd.read_csv(
        "https://raw.githubusercontent.com/ber2/meteoenergy/refs/heads/master/data/meteo-summary.csv", index_col=0, parse_dates=["date"]
    )
    return (meteo_data,)


@app.cell
def _(meteo_data):
    meteo_data
    return


@app.cell
def _(pd):
    pricing_data = pd.read_csv(
        "https://raw.githubusercontent.com/ber2/meteoenergy/refs/heads/master/data/pvpc-summary.csv", index_col=0, parse_dates=["date"]
    )
    return (pricing_data,)


@app.cell
def _(pricing_data, px):
    px.line(
        pricing_data,
        x="date",
        y="pvpc_eur_MWh",
        color="toll",
        template="plotly",
        title="Daily average PVPC by toll",
        labels={"date": "", "pvpc_eur_MWh": "€ / MWh"},
    )
    return


@app.cell
def _(pricing_data, px):
    px.line(
        pricing_data,
        x="date",
        y="prod_cost_eur_MWh",
        color="toll",
        template="plotly",
        title="Daily average Production Cost by toll",
        labels={"date": "", "prod_cost_eur_MWh": "€ / MWh"},
    )
    return


@app.cell
def _(pricing_data):
    heatmap_df = (
        pricing_data.pivot(columns=["toll"], index="date")
        .corr()
        .reset_index(drop=True)
    )
    return (heatmap_df,)


@app.cell
def _(heatmap_df):
    heatmap_df
    return


@app.cell
def _(heatmap_df, px):
    fig = px.imshow(
        heatmap_df,
        text_auto=True,
        template="plotly",
        title="Correlation between PVPC and Production Cost across tolls",
    )

    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.show()
    return


@app.cell
def _(pricing_data):
    pricing_data_simplified = pricing_data[pricing_data.toll == "2.0.DHA"][
        ["date", "pvpc_eur_MWh"]
    ]
    pricing_data_simplified.columns = ["date", "price"]
    return (pricing_data_simplified,)


@app.cell
def _(pricing_data_simplified):
    pricing_data_simplified
    return


@app.cell
def _(meteo_data, pd, pricing_data_simplified):
    df = pd.merge(meteo_data, pricing_data_simplified, on="date", how="inner")
    return (df,)


@app.cell
def _(df):
    df.date.min(), df.date.max()
    return


@app.cell
def _(df):
    df.corr()
    return


@app.cell
def _(df, px):
    px.imshow(
        df.drop("date", axis=1).corr(),
        text_auto=True,
        template="plotly",
        height=1000,
        title="Correlations between weather conditions and price",
    )
    return


@app.cell
def _(df):
    df.sort_values("date", inplace=True)
    return


@app.cell
def _(df):
    df["rainfall_weekly_mm"] = df.rainfall_mm.rolling(7).agg("sum")
    return


@app.cell
def _(df):
    df["rainfall_monthly_mm"] = df.rainfall_mm.rolling(30).agg("sum")
    df["rainfall_quarterly_mm"] = df.rainfall_mm.rolling(30).agg("sum")
    return


@app.cell
def _(df):
    df[
        [
            "price",
            "rainfall_mm",
            "rainfall_weekly_mm",
            "rainfall_monthly_mm",
            "rainfall_quarterly_mm",
        ]
    ].corr()
    return


@app.cell
def _(df, px):
    px.imshow(
        df[
            [
                "price",
                "rainfall_mm",
                "rainfall_weekly_mm",
                "rainfall_monthly_mm",
                "rainfall_quarterly_mm",
            ]
        ].corr(),
        text_auto=True,
        template="plotly",
        height=1000,
        title="Correlations between cumulative rainfall and price",
    )
    return


@app.cell
def _(pricing_data):
    pricing_data.date.min(), pricing_data.date.max()
    return


@app.cell
def _(pricing_data):
    pricing_data.pivot(columns=["toll"], index="date").corr()
    return


@app.cell
def _(pricing_data):
    pricing_data[["pvpc_eur_MWh", "prod_cost_eur_MWh"]].corr()
    return


@app.cell
def _(df):
    df.corr()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
