import marimo

__generated_with = "0.16.2"
app = marimo.App(width="full")


@app.cell
def _():
    import pandas as pd
    import plotly.express as px
    import plotly.figure_factory as ff
    return (pd,)


@app.cell
def _():
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.model_selection import train_test_split, TimeSeriesSplit
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    from sklearn.pipeline import Pipeline
    return (
        LinearRegression,
        Pipeline,
        StandardScaler,
        mean_absolute_error,
        mean_squared_error,
        r2_score,
        train_test_split,
    )


@app.cell
def _(pd):
    meteo_data = pd.read_csv(
        "data/meteo-summary.csv", index_col=0, parse_dates=["date"]
    )
    pricing_data = pd.read_csv(
        "data/pvpc-summary.csv", index_col=0, parse_dates=["date"]
    )
    pricing_data_simplified = pricing_data[pricing_data.toll == "2.0.DHA"][
        ["date", "pvpc_eur_MWh"]
    ]
    pricing_data_simplified.columns = ["date", "price"]
    df = pd.merge(meteo_data, pricing_data_simplified, on="date", how="inner")
    df = df.sort_values("date")
    df["rainfall_weekly_mm"] = df.rainfall_mm.rolling(7).agg("sum")
    df["rainfall_monthly_mm"] = df.rainfall_mm.rolling(30).agg("sum")
    df["rainfall_quarterly_mm"] = df.rainfall_mm.rolling(30).agg("sum")
    return (df,)


@app.cell
def _(df):
    df.columns
    return


@app.cell
def _():
    selected_features = [
        "windspeed_m_s",
        # "rainfall_mm",
        # "sunshine_MJ_daym2",
        # "tmax_C",
        # "tmed_C",
        # "tmin_C",
        # "rainfall_weekly_mm",
        # "rainfall_monthly_mm",
        # "rainfall_quarterly_mm",
    ]
    return (selected_features,)


@app.cell
def _(df, selected_features):
    dataset = df.dropna(subset=selected_features)
    X = dataset[selected_features].values
    y = dataset["price"].values
    return X, y


@app.cell
def _(X, train_test_split, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    return X_test, X_train, y_test, y_train


@app.cell
def _(X_test, X_train):
    X_train.shape[0], X_test.shape[0]
    return


@app.cell
def _(LinearRegression, Pipeline, StandardScaler, X_train, y_train):
    model = Pipeline(
        [("scaler", StandardScaler()), ("regressor", LinearRegression())]
    )
    _ = model.fit(X_train, y_train)
    return (model,)


@app.cell
def _(model):
    model.named_steps["regressor"].coef_
    return


@app.cell
def _(model):
    model.named_steps["regressor"].intercept_
    return


@app.cell
def _(X_test, model):
    y_pred = model.predict(X_test)
    return (y_pred,)


@app.cell
def _(mean_absolute_error, mean_squared_error, r2_score, y_pred, y_test):
    (
        r2_score(y_test, y_pred),
        mean_absolute_error(y_test, y_pred),
        mean_squared_error(y_test, y_pred),
    )
    return


@app.cell
def _(df, pd, selected_features):
    splitting_date = pd.to_datetime("2017-01-01")
    df_train = df[df.date < splitting_date].dropna(subset=selected_features)
    df_test = df[df.date >= splitting_date]
    return df_test, df_train


@app.cell
def _(df_test, df_train, selected_features):
    X_train_time = df_train[selected_features].values
    X_test_time = df_test[selected_features].values
    y_train_time = df_train.price.values
    y_test_time = df_test.price.values
    return X_test_time, X_train_time, y_test_time, y_train_time


@app.cell
def _(LinearRegression, Pipeline, StandardScaler, X_train_time, y_train_time):
    model_time = Pipeline(
        [("scaler", StandardScaler()), ("regressor", LinearRegression())]
    )
    _ = model_time.fit(X_train_time, y_train_time)
    return (model_time,)


@app.cell
def _(model_time):
    model_time.named_steps["regressor"].coef_
    return


@app.cell
def _(model_time):
    model_time.named_steps["regressor"].intercept_
    return


@app.cell
def _(X_test_time, model_time):
    y_pred_time = model_time.predict(X_test_time)
    return (y_pred_time,)


@app.cell
def _(
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    y_pred_time,
    y_test_time,
):
    (
        r2_score(y_test_time, y_pred_time),
        mean_absolute_error(y_test_time, y_pred_time),
        mean_squared_error(y_test_time, y_pred_time),
    )
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
