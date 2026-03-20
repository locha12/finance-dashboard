import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import os

st.set_page_config(page_title="Alex's Finance Dashboard", layout="wide")
st.title("💰 Alex's Personal Finance Dashboard")
st.markdown("**Your exact expenses are now the default** — just edit amounts & groups")

# File paths
EXP_FILE = "expenses.csv"
SUPPLEMENTS_FILE = "supplements.csv"
DEBT_FILE = "debts.csv"
INV_FILE = "investments.csv"
BTC_FILE = "bitcoin.csv"
INCOME_FILE = "income.csv"
SAVINGS_FILE = "savings.csv"
METALS_FILE = "metals.csv"
ALTCOINS_FILE = "altcoins.csv"
RETIREMENT_FILE = "retirement.csv"

def load_df(file, default):
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        df = pd.DataFrame(default)
        df.to_csv(file, index=False)
        return df

def save_df(df, file):
    df.to_csv(file, index=False)
    st.success("✅ Saved!")

def load_income():
    if os.path.exists(INCOME_FILE):
        df = pd.read_csv(INCOME_FILE)
        return float(df["Alex"].iloc[0]), float(df["Katrin"].iloc[0])
    else:
        df = pd.DataFrame({"Alex": [3100.0], "Katrin": [3100.0]})
        df.to_csv(INCOME_FILE, index=False)
        return 3100.0, 3100.0

def save_income(alex, katrin):
    df = pd.DataFrame({"Alex": [alex], "Katrin": [katrin]})
    df.to_csv(INCOME_FILE, index=False)

# Your expenses
expenses = load_df(EXP_FILE, {
    "Category": ["Haus", "GYM", "Audible", "Spotify", "Gas", "Lebensversicherung", "Internet", "Health Insurance", "Powerwall", "Affirm", "Wasser", "Rise wellness", "ADT", "Auto", "Strom", "Supplements", "Benzin", "Landscaping", "Lebensmittel", "Paypal", "Pets", "Eating out", "Counseling", "Church", "Shopping"],
    "Amount": [3225.0, 199.0, 8.5, 19.0, 60.0, 41.0, 120.0, 1100.0, 257.0, 0.0, 67.0, 588.0, 50.0, 0.0, 208.0, 0.0, 100.0, 48.0, 2000.0, 500.0, 200.0, 500.0, 0.0, 0.0, 800.0]
})

if "Group" not in expenses.columns:
    def assign_group(cat):
        c = str(cat).lower()
        if any(x in c for x in ["haus","powerwall","strom","wasser","internet","gas","benzin","auto","landscaping","adt"]):
            return "Housing"
        elif any(x in c for x in ["lebensmittel","eating out"]):
            return "Food"
        elif any(x in c for x in ["health insurance","rise wellness","counseling"]):
            return "Health"
        elif "supplements" in c:
            return "Supplements"
        return "Other"
    expenses["Group"] = expenses["Category"].apply(assign_group)
    expenses.to_csv(EXP_FILE, index=False)

# Other data
debts = load_df(DEBT_FILE, {"Debt Name": ["Mortgage", "Solar Battery Loan"], "Current Balance": [245000.0, 8500.0], "Monthly Payment": [1850.0, 145.0], "Interest Rate %": [3.8, 4.2]})
investments = load_df(INV_FILE, {"Ticker": ["AAPL", "MSFT", "TSLA"], "Shares": [15, 8, 5], "Avg Purchase Price": [170.0, 320.0, 220.0]})
btc_data = load_df(BTC_FILE, {"BTC Amount": [0.42]})
alex_income, katrin_income = load_income()
savings = load_df(SAVINGS_FILE, {"Savings USD": [5000.0]})["Savings USD"].iloc[0]
metals = load_df(METALS_FILE, {"Gold Grams": [50.0], "Silver Ounces": [100.0]})
altcoins = load_df(ALTCOINS_FILE, {"Ticker": ["XRP", "ADA", "SOL", "DOT"], "Coins": [5000.0, 3000.0, 25.0, 150.0], "Avg Purchase Price": [0.50, 0.30, 120.0, 5.0]})
retirement = load_df(RETIREMENT_FILE, {"Alex 401k": [45000.0], "Katrin 401k": [32000.0]})
supplements = load_df(SUPPLEMENTS_FILE, {
    "Supplement": ["Viome", "Bodybio", "Glutaryl", "Mitopure", "Stemregen", "Dake", "Beam Minerals", "WholeFoods", "Fatti15", "IM8"],
    "Amount": [260.0, 95.0, 115.0, 100.0, 250.0, 40.0, 80.0, 30.0, 80.0, 300.0]
})

if "alex_income" not in st.session_state: st.session_state.alex_income = alex_income
if "katrin_income" not in st.session_state: st.session_state.katrin_income = katrin_income

tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📋 Expenses & Income", "💳 Debts", "📈 Investments"])

# Overview
with tab1:
    st.header("Net Worth Snapshot")
    combined_income = st.session_state.alex_income + st.session_state.katrin_income
    total_exp = expenses["Amount"].sum()
    leftover = combined_income - total_exp
    total_debt = debts["Current Balance"].sum()

    stocks_value = sum(row["Shares"] * yf.Ticker(row["Ticker"]).history(period="1d")["Close"].iloc[-1] for _, row in investments.iterrows() if not yf.Ticker(row["Ticker"]).history(period="1d").empty)
    try: btc_value = btc_data["BTC Amount"].iloc[0] * yf.Ticker("BTC-USD").history(period="1d")["Close"].iloc[-1]
    except: btc_value = 0
    try: gold_value = (metals["Gold Grams"].iloc[0] / 31.1034768) * yf.Ticker("GC=F").history(period="1d")["Close"].iloc[-1]
    except: gold_value = 0
    try: silver_value = metals["Silver Ounces"].iloc[0] * yf.Ticker("SI=F").history(period="1d")["Close"].iloc[-1]
    except: silver_value = 0
    altcoins_value = sum(row["Coins"] * yf.Ticker(f"{row['Ticker']}-USD").history(period="1d")["Close"].iloc[-1] for _, row in altcoins.iterrows() if not yf.Ticker(f"{row['Ticker']}-USD").history(period="1d").empty)
    alex_401k = retirement["Alex 401k"].iloc[0]
    katrin_401k = retirement["Katrin 401k"].iloc[0]
    savings_value = savings
    net_worth = stocks_value + btc_value + altcoins_value + gold_value + silver_value + savings_value + alex_401k + katrin_401k - total_debt

    col1, col2, col3 = st.columns(3)
    col1.metric("Alex Income", f"${st.session_state.alex_income:,.0f}")
    col2.metric("Katrin Income", f"${st.session_state.katrin_income:,.0f}")
    col3.metric("Combined Income", f"${combined_income:,.0f}")

    colA, colB, colC, colD = st.columns(4)
    colA.metric("Monthly Expenses", f"${total_exp:,.0f}")
    colB.metric("Leftover", f"${leftover:,.0f}")
    colC.metric("Total Debt", f"${total_debt:,.0f}")
    colD.metric("Net Worth", f"${net_worth:,.0f}", "Updated live")

    st.subheader("Expense Breakdown")
    col_left, col_right = st.columns(2)
    with col_left:
        total_all = expenses["Amount"].sum()
        expenses["Display"] = expenses.apply(lambda x: f"${x['Amount']:,.0f}<br>({x['Amount']/total_all*100:.1f}%)" if total_all > 0 else "$0", axis=1)
        fig_all = px.pie(expenses, names="Category", values="Amount", title="All Individual Expenses")
        fig_all.update_traces(text=expenses["Display"], textinfo="text", textposition="inside")
        st.plotly_chart(fig_all, use_container_width=True)
    with col_right:
        supp_total = supplements["Amount"].sum()
        housing = expenses[expenses["Group"] == "Housing"]["Amount"].sum()
        food = expenses[expenses["Group"] == "Food"]["Amount"].sum()
        health = expenses[expenses["Group"] == "Health"]["Amount"].sum()
        major_df = pd.DataFrame({"Category": ["Housing", "Food", "Supplements", "Health"], "Amount": [housing, food, supp_total, health]})
        total_major = major_df["Amount"].sum()
        major_df["Display"] = major_df.apply(lambda x: f"${x['Amount']:,.0f}<br>({x['Amount']/total_major*100:.1f}%)" if total_major > 0 else "$0", axis=1)
        fig_major = px.pie(major_df, names="Category", values="Amount", title="Major Categories Breakdown")
        fig_major.update_traces(text=major_df["Display"], textinfo="text", textposition="inside")
        st.plotly_chart(fig_major, use_container_width=True)

    alloc_data = pd.DataFrame({
        "Category": ["Savings", "Stocks", "Bitcoin", "Altcoins", "Gold", "Silver", "Alex 401k", "Katrin 401k"],
        "Value": [savings_value, stocks_value, btc_value, altcoins_value, gold_value, silver_value, alex_401k, katrin_401k]
    })
    total_inv = alloc_data["Value"].sum()
    alloc_data["Display"] = alloc_data.apply(lambda x: f"${x['Value']:,.0f}<br>({x['Value']/total_inv*100:.1f}%)" if total_inv > 0 else "$0", axis=1)
    fig_alloc = px.pie(alloc_data, names="Category", values="Value", title="Investment Allocation (Live Values)")
    fig_alloc.update_traces(text=alloc_data["Display"], textinfo="text", textposition="inside")
    st.plotly_chart(fig_alloc, use_container_width=True)

# Expenses tab
with tab2:
    st.header("Expenses vs Income")
    colA, colB = st.columns(2)
    with colA: new_alex = st.number_input("Alex Monthly Income", value=st.session_state.alex_income, step=100.0)
    with colB: new_katrin = st.number_input("Katrin Monthly Income", value=st.session_state.katrin_income, step=100.0)
    if st.button("💾 Save Incomes"):
        st.session_state.alex_income = new_alex
        st.session_state.katrin_income = new_katrin
        save_income(new_alex, new_katrin)
        st.rerun()
    st.metric("Combined Monthly Income", f"${combined_income:,.0f}")

    st.subheader("Your full expenses list")
    edited_exp = st.data_editor(expenses, num_rows="dynamic", use_container_width=True, column_config={"Group": st.column_config.SelectboxColumn("Major Group", options=["Housing", "Food", "Supplements", "Health", "Other"], required=True)})
    if st.button("💾 Save Main Expenses"):
        save_df(edited_exp, EXP_FILE)
        st.rerun()

    st.subheader("Supplements Breakdown")
    edited_supp = st.data_editor(supplements, num_rows="dynamic", use_container_width=True)
    if st.button("💾 Save Supplements List"):
        save_df(edited_supp, SUPPLEMENTS_FILE)
        st.rerun()
    st.metric("Total Supplements", f"${edited_supp['Amount'].sum():,.0f}")

# Debts tab
with tab3:
    st.header("Debt Tracker")
    edited_debts = st.data_editor(debts, num_rows="dynamic", use_container_width=True)
    if st.button("💾 Save Debt Changes"):
        save_df(edited_debts, DEBT_FILE)
        st.rerun()
    st.metric("Total Debt Owed", f"${total_debt:,.0f}")

# Investments tab
with tab4:
    st.header("📈 Investments (Live Prices)")
    with st.expander("💵 Cash Savings", expanded=True):
        new_savings = st.number_input("Savings Balance (USD)", value=float(savings), step=100.0)
        if st.button("💾 Save Savings"):
            pd.DataFrame({"Savings USD": [new_savings]}).to_csv(SAVINGS_FILE, index=False)
            st.rerun()
    with st.expander("🥇 Gold & Silver (Live)", expanded=True):
        colG, colS = st.columns(2)
        with colG: new_gold = st.number_input("Gold (grams)", value=float(metals["Gold Grams"].iloc[0]), step=1.0)
        with colS: new_silver = st.number_input("Silver (ounces)", value=float(metals["Silver Ounces"].iloc[0]), step=1.0)
        if st.button("💾 Save Metals"):
            pd.DataFrame({"Gold Grams": [new_gold], "Silver Ounces": [new_silver]}).to_csv(METALS_FILE, index=False)
            st.rerun()
        st.metric("Gold Value", f"${gold_value:,.0f}" if 'gold_value' in locals() else "Live price loading...")
        st.metric("Silver Value", f"${silver_value:,.0f}" if 'silver_value' in locals() else "Live price loading...")
    with st.expander("📈 Stocks", expanded=False):
        edited_inv = st.data_editor(investments, num_rows="dynamic", use_container_width=True)
        if st.button("💾 Save Stock Changes"):
            save_df(edited_inv, INV_FILE)
            st.rerun()
    with st.expander("🪙 Altcoins (XRP, ADA, SOL, DOT)", expanded=True):
        edited_alt = st.data_editor(altcoins, num_rows="dynamic", use_container_width=True)
        if st.button("💾 Save Altcoins"):
            save_df(edited_alt, ALTCOINS_FILE)
            st.rerun()
    with st.expander("₿ Bitcoin (Live)", expanded=True):
        edited_btc = st.data_editor(btc_data, use_container_width=True)
        if st.button("💾 Save Bitcoin Amount"):
            save_df(edited_btc, BTC_FILE)
            st.rerun()
        try:
            btc_price = yf.Ticker("BTC-USD").history(period="1d")["Close"].iloc[-1]
            btc_value = edited_btc["BTC Amount"].iloc[0] * btc_price
            st.metric("Bitcoin Value", f"${btc_value:,.0f}", f"@ ${btc_price:,.0f}")
        except: st.write("Bitcoin price temporarily unavailable")
    with st.expander("🏦 401k Accounts", expanded=True):
        colAx, colKa = st.columns(2)
        with colAx: new_alex401 = st.number_input("Alex 401k Balance", value=float(alex_401k), step=100.0)
        with colKa: new_katrin401 = st.number_input("Katrin 401k Balance", value=float(katrin_401k), step=100.0)
        if st.button("💾 Save 401k Balances"):
            pd.DataFrame({"Alex 401k": [new_alex401], "Katrin 401k": [new_katrin401]}).to_csv(RETIREMENT_FILE, index=False)
            st.rerun()
    if st.button("🔄 Refresh All Live Prices"): st.rerun()

st.caption("No password — direct access version")
