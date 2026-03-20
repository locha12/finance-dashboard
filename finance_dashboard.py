import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import os

# ================== PASSWORD PROTECTION ==================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

PASSWORD = "your_strong_password_here"   # ← CHANGE THIS TO YOUR REAL PASSWORD!

if not st.session_state.logged_in:
    st.title("🔒 Alex's Personal Finance Dashboard")
    st.markdown("### Enter Password")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if pw == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect password")
    st.stop()

# ================== FULL DASHBOARD ==================
st.set_page_config(page_title="Alex's Finance Dashboard", layout="wide")
st.title("💰 Alex's Personal Finance Dashboard")
st.markdown("**Your exact expenses are now the default** — just edit amounts & groups")

# File paths (unchanged)
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

# Cached price fetch (this fixes the rate limit!)
@st.cache_data(ttl=300)  # cache 5 minutes
def get_price(ticker):
    try:
        price = yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1]
        return round(price, 2)
    except:
        return None

# Your full expenses (unchanged)
expenses = load_df(EXP_FILE, { ... })  # (your full list is still here - keep your existing data)

# ... (the rest of your data loading is the same)

# In the Overview tab, replace the old price calculations with this safe version:
stocks_value = 0.0
for _, row in investments.iterrows():
    price = get_price(row["Ticker"])
    if price:
        stocks_value += row["Shares"] * price

btc_value = get_price("BTC-USD") * btc_data["BTC Amount"].iloc[0] if get_price("BTC-USD") else 0
gold_value = get_price("GC=F") * (metals["Gold Grams"].iloc[0] / 31.1034768) if get_price("GC=F") else 0
silver_value = get_price("SI=F") * metals["Silver Ounces"].iloc[0] if get_price("SI=F") else 0

# Altcoins also use the cached function (same pattern)

# The rest of the tabs stay exactly the same

st.caption("Cloud version with password — live prices cached to avoid rate limits")
