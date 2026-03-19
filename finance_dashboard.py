import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import os

# ================== PASSWORD PROTECTION ==================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

PASSWORD = "Swesda.14523!!"   # ← CHANGE THIS TO YOUR REAL PASSWORD RIGHT NOW!

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

# ================== YOUR FULL DASHBOARD ==================
st.set_page_config(page_title="Alex's Finance Dashboard", layout="wide")
st.title("💰 Alex's Personal Finance Dashboard")
st.markdown("**Your exact expenses are now the default** — just edit amounts & groups")

# ================== FILE PATHS ==================
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

# ================== YOUR FULL EXPENSE LIST ==================
expenses = load_df(EXP_FILE, {
    "Category": ["Haus", "GYM", "Audible", "Spotify", "Gas", "Lebensversicherung", "Internet", "Health Insurance", "Powerwall", "Affirm", "Wasser", "Rise wellness", "ADT", "Auto", "Strom", "Supplements", "Benzin", "Landscaping", "Lebensmittel", "Paypal", "Pets", "Eating out", "Counseling", "Church", "Shopping"],
    "Amount": [3225.0, 199.0, 8.5, 19.0, 60.0, 41.0, 120.0, 1100.0, 257.0, 0.0, 67.0, 588.0, 50.0, 0.0, 208.0, 0.0, 100.0, 48.0, 2000.0, 500.0, 200.0, 500.0, 0.0, 0.0, 800.0]
})

if "Group" not in expenses.columns:
    def assign_group(cat):
        c = str(cat).lower()
        if any(x in c for x in ["haus", "powerwall", "strom", "wasser", "internet", "gas", "benzin", "auto", "landscaping", "adt"]):
            return "Housing"
        elif any(x in c for x in ["lebensmittel", "eating out"]):
            return "Food"
       
