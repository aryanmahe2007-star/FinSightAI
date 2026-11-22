
import ollama
import pandas as pd


def create_financial_context(df, opening_balance=50000):
    """Create a financial summary from business transactions."""

    data = df.copy()

    data["date"] = pd.to_datetime(data["date"])
    data["amount"] = pd.to_numeric(data["amount"], errors="coerce")
    data = data.dropna(subset=["amount", "date"])

    inflows = data.loc[data["type"].str.lower() == "inflow", "amount"].sum()
    outflows = data.loc[data["type"].str.lower() == "outflow", "amount"].sum()

    category_summary = (
        data[data["type"].str.lower() == "outflow"]
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    recent_date = data["date"].max()
    recent_start = recent_date - pd.Timedelta(days=29)

    recent = data[data["date"] >= recent_start]

    recent_income = recent.loc[
        recent["type"].str.lower() == "inflow", "amount"
    ].sum()

    recent_expenses = recent.loc[
        recent["type"].str.lower() == "outflow", "amount"
    ].sum()

    balance = opening_balance + inflows - outflows

    categories = "\n".join(
        f"- {category}: ₹{amount:,.2f}"
        for category, amount in category_summary.items()
    )

    return f"""
BUSINESS FINANCIAL SNAPSHOT

Opening balance assumption: ₹{opening_balance:,.2f}
Total historical income: ₹{inflows:,.2f}
Total historical expenses: ₹{outflows:,.2f}
Estimated balance: ₹{balance:,.2f}

Recent 30-day income: ₹{recent_income:,.2f}
Recent 30-day expenses: ₹{recent_expenses:,.2f}

Expense categories:
{categories if categories else "No expense categories available."}

Number of transactions: {len(data)}
Data period: {data['date'].min().date()} to {data['date'].max().date()}
"""


def local_finance_copilot(df, question, history=None, opening_balance=50000):

    financial_context = create_financial_context(
        df, opening_balance
    )

    system_prompt = f"""
You are FinSightAI, an intelligent financial assistant for a small business.

Answer in the same language as the user's question.
Use simple, clear language.

BUSINESS DATA:
{financial_context}

RULES:
1. Personalise answers using the supplied business data.
2. Never invent financial figures.
3. If information is unavailable, clearly say so.
4. Explain financial concepts with practical examples.
5. Give useful suggestions based on actual business data.
6. Distinguish historical figures from estimates.
7. The estimated balance uses an assumed opening balance.
8. You are an informational assistant, not a certified financial advisor.
"""

    messages = [{"role": "system", "content": system_prompt}]

    if history:
        messages.extend(history[-8:])

    messages.append({"role": "user", "content": question})

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=messages,
        options={
            "temperature": 0.3,
            "num_ctx": 2048,
            "num_predict": 250,
        }
    )

    return response["message"]["content"]
