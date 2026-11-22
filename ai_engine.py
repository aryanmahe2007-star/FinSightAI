import pandas as pd
import numpy as np
import re

from sklearn.ensemble import RandomForestRegressor


def prepare_daily_data(df):

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    inflows = (
        df[df["type"] == "Inflow"]
        .groupby("date")["amount"]
        .sum()
    )

    outflows = (
        df[df["type"] == "Outflow"]
        .groupby("date")["amount"]
        .sum()
    )

    daily = pd.DataFrame(index=pd.date_range(
        df["date"].min(),
        df["date"].max(),
        freq="D"
    ))

    daily["inflow"] = inflows
    daily["outflow"] = outflows

    daily = daily.fillna(0)

    return daily


def create_features(series, date):

    values = list(series)

    return [
        values[-1],
        values[-7],
        values[-14],
        np.mean(values[-7:]),
        date.dayofweek,
        date.day,
        date.month
    ]


def forecast_cashflow(df, days=7, opening_balance=50000):

    daily = prepare_daily_data(df)

    if len(daily) < 30:
        raise ValueError("At least 30 days of data are required.")

    models = {}

    for column in ["inflow", "outflow"]:

        X = []
        y = []

        series = daily[column].tolist()

        for i in range(14, len(series)):

            features = create_features(
                series[:i],
                daily.index[i]
            )

            X.append(features)
            y.append(series[i])

        model = RandomForestRegressor(
            n_estimators=150,
            max_depth=8,
            random_state=42
        )

        model.fit(X, y)

        models[column] = model

    inflow_history = daily["inflow"].tolist()
    outflow_history = daily["outflow"].tolist()

    current_balance = (
        opening_balance
        + daily["inflow"].sum()
        - daily["outflow"].sum()
    )

    predictions = []

    for _ in range(days):

        next_date = daily.index[-1] + pd.Timedelta(days=1)

        inflow_features = create_features(
            inflow_history,
            next_date
        )

        outflow_features = create_features(
            outflow_history,
            next_date
        )

        predicted_inflow = max(
            0,
            models["inflow"].predict([inflow_features])[0]
        )

        predicted_outflow = max(
            0,
            models["outflow"].predict([outflow_features])[0]
        )

        current_balance += (
            predicted_inflow - predicted_outflow
        )

        predictions.append({
            "date": next_date,
            "predicted_inflow": round(predicted_inflow, 2),
            "predicted_outflow": round(predicted_outflow, 2),
            "closing_balance": round(current_balance, 2)
        })

        inflow_history.append(predicted_inflow)
        outflow_history.append(predicted_outflow)

        daily.loc[next_date] = [
            predicted_inflow,
            predicted_outflow
        ]

    return pd.DataFrame(predictions)


from sklearn.ensemble import IsolationForest


def detect_anomalies(df, contamination=0.05):

    expenses = df[df["type"] == "Outflow"].copy()

    if len(expenses) < 20:
        raise ValueError("At least 20 expense transactions are required.")

    expenses["date"] = pd.to_datetime(expenses["date"])

    expenses["log_amount"] = np.log1p(expenses["amount"])
    expenses["day_of_week"] = expenses["date"].dt.dayofweek
    expenses["day_of_month"] = expenses["date"].dt.day

    features = pd.concat(
        [
            expenses[["log_amount", "day_of_week", "day_of_month"]],
            pd.get_dummies(
                expenses[["category", "payment_mode"]],
                dtype=int
            )
        ],
        axis=1
    )

    model = IsolationForest(
        n_estimators=150,
        contamination=contamination,
        random_state=42
    )

    predictions = model.fit_predict(features)

    expenses["anomaly_score"] = model.decision_function(features)

    expenses["anomaly_status"] = [
        "Unusual Expense" if prediction == -1 else "Normal"
        for prediction in predictions
    ]

    expenses = expenses.sort_values(
        "anomaly_score",
        ascending=True
    )

    return expenses

def calculate_business_health(df, opening_balance=50000):

    daily = prepare_daily_data(df)

    # Calculate estimated current balance
    current_balance = (
        opening_balance
        + daily["inflow"].sum()
        - daily["outflow"].sum()
    )

    # Use the latest 30 days
    recent = daily.tail(30)

    total_inflow = recent["inflow"].sum()
    total_outflow = recent["outflow"].sum()

    avg_daily_expense = recent["outflow"].mean()

    # 1. Cash Reserve Score (40%)
    if avg_daily_expense <= 0:
        runway_days = 30
    else:
        runway_days = max(0, current_balance / avg_daily_expense)

    reserve_score = min(100, (runway_days / 30) * 100)

    # 2. Cash Flow Coverage Score (35%)
    if total_outflow <= 0:
        coverage_ratio = 1
    else:
        coverage_ratio = total_inflow / total_outflow

    if coverage_ratio >= 1.5:
        coverage_score = 100
    elif coverage_ratio >= 1.2:
        coverage_score = 85
    elif coverage_ratio >= 1:
        coverage_score = 70
    elif coverage_ratio >= 0.8:
        coverage_score = 45
    else:
        coverage_score = 20

    # 3. Cash Flow Consistency Score (25%)
    daily_net = recent["inflow"] - recent["outflow"]

    positive_days = (daily_net >= 0).sum()

    consistency_score = (
        positive_days / len(recent) * 100
        if len(recent) > 0 else 0
    )

    # Final weighted score
    final_score = (
        reserve_score * 0.40
        + coverage_score * 0.35
        + consistency_score * 0.25
    )

    final_score = round(final_score)

    if final_score >= 80:
        status = "Excellent"
    elif final_score >= 65:
        status = "Good"
    elif final_score >= 45:
        status = "Average"
    else:
        status = "Needs Attention"

    return {
        "health_score": final_score,
        "status": status,
        "current_balance": round(current_balance, 2),
        "runway_days": round(runway_days, 1),
        "coverage_ratio": round(coverage_ratio, 2),
        "positive_days": int(positive_days),
        "reserve_score": round(reserve_score),
        "coverage_score": coverage_score,
        "consistency_score": round(consistency_score)
    }

def finance_copilot(df, question, opening_balance=50000):

    query = question.lower().strip()

    if not query:
        return "Please enter a financial question."

    # 1. Purchase affordability
    if any(word in query for word in ["afford", "purchase", "buy", "spend"]):

        match = re.search(
            r"(?:₹|rs\.?\s*)?([\d,]+(?:\.\d+)?)\s*(?:rupees|rs)?",
            query
        )

        if not match:
            return (
                "Please mention the purchase amount. "
                "Example: Can I afford ₹15,000 next week?"
            )

        purchase_amount = float(match.group(1).replace(",", ""))

        forecast = forecast_cashflow(
            df,
            days=7,
            opening_balance=opening_balance
        )

        projected_balance = forecast["closing_balance"].iloc[-1]

        remaining_balance = projected_balance - purchase_amount

        if remaining_balance >= 0:
            return (
                f"Your projected balance after 7 days is "
                f"₹{projected_balance:,.2f}. "
                f"After a purchase of ₹{purchase_amount:,.2f}, "
                f"you would have ₹{remaining_balance:,.2f} remaining. "
                "Based on this forecast, the purchase appears affordable. "
                "Keep upcoming obligations in mind."
            )

        return (
            f"Your projected balance after 7 days is "
            f"₹{projected_balance:,.2f}. "
            f"A purchase of ₹{purchase_amount:,.2f} "
            f"would leave a shortfall of ₹{abs(remaining_balance):,.2f}. "
            "This purchase does not appear affordable based on the "
            "current forecast."
        )

    # 2. Balance prediction
    elif any(word in query for word in ["balance", "cash", "money"]):

        forecast = forecast_cashflow(
            df,
            days=7,
            opening_balance=opening_balance
        )

        balance = forecast["closing_balance"].iloc[-1]

        return (
            f"Your estimated balance is based on the assumed starting "
            f"balance and historical transactions. "
            f"Your projected closing balance after 7 days is "
            f"₹{balance:,.2f}."
        )

    # 3. Expense analysis
    elif any(word in query for word in ["expense", "expenses", "spending", "cost"]):

        daily = prepare_daily_data(df)

        recent = daily.tail(30)["outflow"].sum()
        previous = daily.iloc[-60:-30]["outflow"].sum()

        if previous > 0:
            change = ((recent - previous) / previous) * 100
        else:
            change = 0

        if change > 5:
            trend = "increased"
        elif change < -5:
            trend = "decreased"
        else:
            trend = "remained relatively stable"

        return (
            f"Your expenses in the latest 30 days were "
            f"₹{recent:,.2f}. Previous 30-day expenses were "
            f"₹{previous:,.2f}. Expenses have {trend} by "
            f"{abs(change):.1f}% compared with the previous period."
        )

    # 4. Business health
    elif any(word in query for word in ["health", "score", "healthy"]):

        health = calculate_business_health(
            df,
            opening_balance=opening_balance
        )

        return (
            f"Your Business Health Score is "
            f"{health['health_score']}/100 ({health['status']}). "
            f"Cash runway: {health['runway_days']} days. "
            f"Cash flow coverage: {health['coverage_ratio']}x. "
            f"Positive cash-flow days: {health['positive_days']}/30."
        )

    # 5. Default response
    else:
        return (
            "I can help you analyse your business finances. "
            "Try asking:\n"
            "1. Can I afford a ₹15,000 purchase next week?\n"
            "2. What will my balance be after 7 days?\n"
            "3. Are my expenses increasing?\n"
            "4. What is my business health score?"
        )


def smart_purchase_planner(
    df,
    purchase_amount,
    opening_balance=50000,
    purchase_in_days=1,
    reserve_days=7
):

    if purchase_amount < 0:
        raise ValueError("Purchase amount cannot be negative.")

    if purchase_in_days < 1:
        raise ValueError("Purchase date must be at least 1 day ahead.")

    forecast_days = purchase_in_days + reserve_days

    forecast = forecast_cashflow(
        df,
        days=forecast_days,
        opening_balance=opening_balance
    )

    purchase_index = purchase_in_days - 1

    balance_before_purchase = forecast.iloc[purchase_index][
        "closing_balance"
    ]

    future_balances = forecast.iloc[purchase_index:][
        "closing_balance"
    ]

    post_purchase_balances = future_balances - purchase_amount

    minimum_balance = post_purchase_balances.min()

    average_daily_expense = forecast["predicted_outflow"].mean()

    safety_reserve = average_daily_expense * reserve_days

    maximum_safe_purchase = max(
        0,
        balance_before_purchase - safety_reserve
    )

    if minimum_balance < 0:
        risk = "High Risk"
        recommendation = "Avoid or postpone this purchase."
    elif minimum_balance < safety_reserve:
        risk = "Moderate Risk"
        recommendation = "Consider reducing the purchase amount."
    else:
        risk = "Low Risk"
        recommendation = "Purchase appears financially manageable."

    return {
        "purchase_amount": round(purchase_amount, 2),
        "balance_before_purchase": round(balance_before_purchase, 2),
        "balance_after_purchase": round(
            balance_before_purchase - purchase_amount, 2
        ),
        "minimum_projected_balance": round(minimum_balance, 2),
        "safety_reserve": round(safety_reserve, 2),
        "maximum_safe_purchase": round(maximum_safe_purchase, 2),
        "risk": risk,
        "recommendation": recommendation
    }
