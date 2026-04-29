import streamlit as st

st.set_page_config(
    page_title="Payouts Cost Calculator",
    page_icon="💸",
    layout="centered"
)

# ── Stape pricing (update here if rates change) ───────────────────────────────
STAPE_FX_RATE = 2.0   # % of volume

STAPE_TIERS = [
    (1,   9,  50),   # 1–9 payouts   → $50/payout
    (10,  25, 45),   # 10–25         → $45/payout
    (26,  50, 40),   # 26–50         → $40/payout
    (51, None, 35),  # 51+           → $35/payout
]

def stape_fee_per_payout(n: int) -> int:
    """Return Stape's per-payout fee based on number of payouts."""
    for low, high, fee in STAPE_TIERS:
        if high is None or n <= high:
            return fee
    return STAPE_TIERS[-1][2]

# ── Theme ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(ellipse at 75% 5%, #3b1068 0%, #160730 45%, #080810 100%);
        color: #ffffff;
    }
    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 4rem;
        max-width: 720px;
    }

    /* ── typography ── */
    h1, h2, h3 { color: #ffffff !important; font-weight: 800 !important; }

    /* ── field labels ── */
    label,
    .stNumberInput label,
    .stTextInput   label { color: #b8a8d8 !important; font-size: 0.82rem !important; font-weight: 500 !important; }

    /* ── radio label (widget title) ── */
    .stRadio > label { color: #b8a8d8 !important; font-size: 0.82rem !important; font-weight: 500 !important; }

    /* ── radio options ── */
    .stRadio div[role="radiogroup"] label,
    .stRadio div[role="radiogroup"] label p,
    .stRadio div[role="radiogroup"] span { color: #ffffff !important; font-size: 0.9rem !important; }
    .stRadio > div { background: rgba(255,255,255,0.04); border-radius: 10px; padding: 0.45rem 0.7rem; }

    /* ── inputs: white bg, dark text ── */
    .stTextInput input, .stNumberInput input {
        background-color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 8px !important;
        color: #111111 !important;
        font-size: 0.95rem !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 2px rgba(124,58,237,0.28) !important;
    }

    /* ── input card ── */
    .input-card {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 16px;
        padding: 1.6rem 1.8rem 1.2rem;
        margin-bottom: 1.4rem;
    }
    .input-card-title {
        color: #e2d4ff;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 0.01em;
        margin-bottom: 1.1rem;
    }

    /* ── Stape rate pill (subtle, top) ── */
    .stape-rates-bar {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: rgba(124,58,237,0.1);
        border: 1px solid rgba(124,58,237,0.22);
        border-radius: 10px;
        padding: 0.5rem 1rem;
        margin-bottom: 1.8rem;
        flex-wrap: wrap;
    }
    .stape-rates-bar .bar-label {
        color: #9b87c2;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        white-space: nowrap;
    }
    .stape-rates-bar .pill {
        background: rgba(167,139,250,0.13);
        border: 1px solid rgba(167,139,250,0.25);
        border-radius: 20px;
        color: #c4b5e8;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.15rem 0.65rem;
        white-space: nowrap;
    }

    /* ── metric cards ── */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.065);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem 1.1rem !important;
    }
    [data-testid="stMetricLabel"] { color: #b8a8d8 !important; font-size: 0.75rem !important; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 1.35rem !important; font-weight: 700 !important; }
    [data-testid="stMetricDelta"] { font-size: 0.82rem !important; }

    /* ── savings banner ── */
    .savings-banner {
        background: linear-gradient(135deg, rgba(124,58,237,0.38), rgba(79,36,158,0.28));
        border: 1px solid rgba(167,139,250,0.42);
        border-radius: 16px;
        padding: 1.6rem 2rem;
        text-align: center;
        margin: 1.2rem 0;
    }
    .savings-banner .s-label { color: #c4b5e8; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.3rem; }
    .savings-banner .s-value { color: #a78bfa; font-size: 2.6rem; font-weight: 800; line-height: 1.1; }
    .savings-banner .s-sub   { color: #a78bfa; font-size: 0.88rem; margin-top: 0.35rem; opacity: 0.85; }

    /* ── savings banner — green variant ── */
    .savings-banner-green {
        background: linear-gradient(135deg, rgba(16,185,129,0.22), rgba(5,150,105,0.14));
        border: 1.5px solid rgba(52,211,153,0.55);
        border-radius: 16px;
        padding: 1.6rem 2rem;
        text-align: center;
        margin: 1.2rem 0;
        box-shadow: 0 0 32px rgba(16,185,129,0.12);
    }
    .savings-banner-green .s-label { color: #6ee7b7; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.09em; margin-bottom: 0.3rem; }
    .savings-banner-green .s-value { color: #34d399; font-size: 2.8rem; font-weight: 800; line-height: 1.1; text-shadow: 0 0 24px rgba(52,211,153,0.45); }
    .savings-banner-green .s-sub   { color: #6ee7b7; font-size: 0.88rem; margin-top: 0.4rem; }

    /* ── divider ── */
    hr { border-color: rgba(255,255,255,0.08) !important; }

    /* ── expander ── */
    .streamlit-expanderHeader  { color: #b8a8d8 !important; background: rgba(255,255,255,0.03) !important; border-radius: 8px !important; }
    .streamlit-expanderContent { background: rgba(255,255,255,0.02) !important; color: #d4c8f0 !important; border-radius: 0 0 8px 8px !important; }

    .stCaption { color: rgba(255,255,255,0.3) !important; }
    .stAlert   { border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_usd(n):
    return "$" + f"{n:,.0f}".replace(",", " ")

def fmt_delta(n):
    if n < 0:  return "-$" + f"{abs(n):,.0f}".replace(",", " ")
    if n > 0:  return "+$" + f"{n:,.0f}".replace(",", " ")
    return "$0"

def fmt_num(n):
    return f"{n:,.0f}".replace(",", " ")

def parse_int_input(raw, label):
    cleaned = raw.replace(" ", "").replace(",", "").strip()
    if not cleaned: return 0, None
    try:
        val = int(cleaned)
        if val < 0: return None, f"{label} must be 0 or greater."
        return val, None
    except ValueError:
        return None, f"'{raw}' is not a valid number for {label}."


# ── Logo ──────────────────────────────────────────────────────────────────────
_LOGO_B64 = "PHN2ZyB3aWR0aD0iNTg0IiBoZWlnaHQ9IjI5MiIgdmlld0JveD0iMCAwIDU4NCAyOTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIGNsaXAtcGF0aD0idXJsKCNjbGlwMF8zNjcxXzQwNzQpIj4KCjxwYXRoIGQ9Ik0xODMuMTUxIDE3MC4yNzZDMTkwLjQ0NiAxNzguNDkyIDE5OS40NzcgMTgyLjYwMSAyMTAuMjQzIDE4Mi42MDFDMjE1LjEzMSAxODIuNjAxIDIxOS4wNDQgMTgxLjYyNyAyMjEuOTg0IDE3OS42NzlDMjI1LjQ1NCAxNzcuMzA2IDIyNy4xOSAxNzQuMDEyIDIyNy4xOSAxNjkuNzk4QzIyNy4xOSAxNjUuOTczIDIyNS42ODQgMTYyLjg1NyAyMjIuNjc0IDE2MC40NDhDMjIwLjY5MSAxNTguODU1IDIxNS45MSAxNTYuNTcxIDIwOC4zMzEgMTUzLjU5NkwyMDYuMzEyIDE1Mi43OTlMMjAyLjcgMTUxLjM2NUMyMDIuNDUyIDE1MS4yNTggMjAyLjAwOSAxNTEuMDgxIDIwMS4zNzIgMTUwLjgzM0MxOTMuNTgxIDE0Ny44OTQgMTg4LjUzNCAxNDUuNDY4IDE4Ni4yMzIgMTQzLjU1NUMxODUuODc4IDE0My4yMzcgMTg1LjQzNSAxNDIuNzk0IDE4NC45MDQgMTQyLjIyN0MxODEuMTE0IDEzOC4xNTUgMTc5LjIyIDEzMy4yNSAxNzkuMjIgMTI3LjUxMkMxNzkuMjIgMTIwLjExMSAxODEuODc2IDExNC4xNDMgMTg3LjE4OCAxMDkuNjFDMTkyLjc0OCAxMDQuODY0IDIwMC4yNTYgMTAyLjQ5MiAyMDkuNzEyIDEwMi40OTJDMjE2LjI5OSAxMDIuNDkyIDIyMi4xNzggMTAzLjQ2NiAyMjcuMzQ5IDEwNS40MTNDMjMxLjQ1NyAxMDcuMDA3IDIzNS41NDggMTA5LjQ1MSAyMzkuNjIgMTEyLjc0NEwyMzIuMjg5IDEyMi45NDRDMjI2LjAyMSAxMTYuOTk0IDIxOC41MzEgMTE0LjAxOSAyMDkuODE4IDExNC4wMTlDMjA0LjExNyAxMTQuMDE5IDE5OS45NzMgMTE1LjM0NyAxOTcuMzg4IDExOC4wMDNDMTk1LjE5MiAxMjAuMjcgMTk0LjA5NCAxMjMuMDE1IDE5NC4wOTQgMTI2LjIzN0MxOTQuMDk0IDEyOS45MjEgMTk1LjY4OCAxMzIuODYgMTk4Ljg3NSAxMzUuMDU2QzIwMC44OTQgMTM2LjQ3MiAyMDUuMTc5IDEzOC4zNDkgMjExLjczMSAxNDAuNjg3TDIxNS45ODEgMTQyLjIyN0MyMjUuMzMgMTQ1LjU5MiAyMzEuNzQgMTQ4Ljg4NSAyMzUuMjExIDE1Mi4xMDhDMjQwLjAyOCAxNTYuNjA2IDI0Mi40MzYgMTYyLjI1NSAyNDIuNDM2IDE2OS4wNTRDMjQyLjQzNiAxNzcuNDgzIDIzOS4xMjQgMTg0LjA1MyAyMzIuNTAyIDE4OC43NjNDMjI3LjA0OCAxOTIuNjIzIDIxOS42MTEgMTk0LjU1MyAyMTAuMTkgMTk0LjU1M0MxOTUuNTI4IDE5NC41NTMgMTgzLjc4OCAxODkuNTc3IDE3NC45NyAxNzkuNjI2TDE4My4xNTEgMTcwLjI3NlpNMjc4LjMyMSAxMDguMzg4VjEyOC40MTZIMjk4LjM0OFYxMzguNTA5SDI3OC4zMjFWMTczLjQxQzI3OC4zMjEgMTc2Ljg0NiAyNzguNzI4IDE3OS4yMTkgMjc5LjU0MyAxODAuNTI5QzI4MC42NDEgMTgyLjMzNSAyODIuNDY1IDE4My4yMzggMjg1LjAxNSAxODMuMjM4QzI4OC4xNjcgMTgzLjIzOCAyOTEuNDA3IDE4MS45OTkgMjk0LjczNiAxNzkuNTJMMjk4LjEzNiAxODkuNEMyOTIuOTY1IDE5Mi42OTQgMjg3LjUxMSAxOTQuMzQxIDI4MS43NzQgMTk0LjM0MUMyNzUuODI0IDE5NC4zNDEgMjcxLjMyNyAxOTIuNTcgMjY4LjI4MSAxODkuMDI4QzI2NS43NjcgMTg2LjA4OSAyNjQuNTA5IDE4MS44MzkgMjY0LjUwOSAxNzYuMjc5VjEzOC41MDlIMjUwLjE2NlYxMjguNDE2SDI2NC41MDlWMTE0LjcxTDI3OC4zMjEgMTA4LjM4OFpNMzQ5LjEwOCAxNTEuMjU4VjE1MC4yNDlDMzQ5LjEwOCAxNDEuNTAxIDM0NC45NDcgMTM3LjEyOCAzMzYuNjI0IDEzNy4xMjhDMzI4LjgzMyAxMzcuMTI4IDMyMS44MjEgMTM5LjQ4MyAzMTUuNTg4IDE0NC4xOTNMMzEwLjE2OSAxMzQuMzY1QzMxOC4zNSAxMjkuMDE4IDMyNy4zMjggMTI2LjM0NCAzMzcuMTAyIDEyNi4zNDRDMzQ2LjUyMyAxMjYuMzQ0IDM1My41NTMgMTI5LjA1MyAzNTguMTkyIDEzNC40NzJDMzYxLjQxNSAxMzguMTkgMzYzLjAyNiAxNDMuNjc5IDM2My4wMjYgMTUwLjk0VjE3My4zNTdDMzYzLjAyNiAxODEuNjQ0IDM2NC4zMDEgMTg4LjA1NSAzNjYuODUxIDE5Mi41ODhIMzUzLjg4OUMzNTIuMzY2IDE4OS42NDggMzUxLjM1NyAxODYuMjg0IDM1MC44NjEgMTgyLjQ5NEgzNTAuNDg5QzM0OC42ODMgMTg2LjAzNiAzNDUuNzc5IDE4OS4wMjggMzQxLjc3NyAxOTEuNDcyQzMzOC41MTkgMTkzLjQ1NSAzMzQuMjE2IDE5NC40NDcgMzI4Ljg2OCAxOTQuNDQ3QzMyMi41MjkgMTk0LjQ0NyAzMTcuMjg4IDE5Mi41ODggMzEzLjE0NCAxODguODY5QzMwOC44MjMgMTg0Ljk3MyAzMDYuNjYzIDE4MC4wMTUgMzA2LjY2MyAxNzMuOTk1QzMwNi42NjMgMTU4LjgzNyAzMTguOTE3IDE1MS4yNTggMzQzLjQyNCAxNTEuMjU4SDM0OS4xMDhaTTM0OS4xMDggMTYxLjI0NUgzNDQuODU4QzMzNi41NzEgMTYxLjI0NSAzMzAuMzU2IDE2Mi4zMDggMzI2LjIxMiAxNjQuNDMzQzMyMi42NzEgMTY2LjIzOSAzMjAuOSAxNjkuMzU1IDMyMC45IDE3My43ODJDMzIwLjkgMTc2Ljc1NyAzMjEuOTYzIDE3OS4xMTIgMzI0LjA4NyAxODAuODQ4QzMyNi4xMDYgMTgyLjUxMiAzMjguNzI3IDE4My4zNDQgMzMxLjk1IDE4My4zNDRDMzM2LjIzNSAxODMuMzQ0IDM0MC4wNzcgMTgxLjgyMiAzNDMuNDc3IDE3OC43NzZDMzQ3LjIzMSAxNzUuNDQ3IDM0OS4xMDggMTcxLjE2MiAzNDkuMTA4IDE2NS45MlYxNjEuMjQ1Wk0zOTQuOTI4IDEyOC40MTZWMTM3LjEyOEM0MDAuODA2IDEzMC4xNTEgNDA4LjE5MSAxMjYuNjYyIDQxNy4wOCAxMjYuNjYyQzQyNi4wMDQgMTI2LjY2MiA0MzMuMTk0IDEyOS42MzcgNDM4LjY0OCAxMzUuNTg3QzQ0My44NTQgMTQxLjIxOCA0NDYuNDU3IDE0OC43OTcgNDQ2LjQ1NyAxNTguMzI0QzQ0Ni40NTcgMTY2LjM2MyA0NDQuNTk3IDE3My4wOTIgNDQwLjg3OSAxNzguNTFDNDM1LjUzMSAxODYuMzAyIDQyNy42NjkgMTkwLjE5NyA0MTcuMjkyIDE5MC4xOTdDNDA3Ljg3MiAxOTAuMTk3IDQwMC43NzEgMTg2Ljk3NCAzOTUuOTkgMTgwLjUyOVYyMDIuODRIMzgxLjc1M1YxMjguNDE2SDM5NC45MjhaTTM5NS45OSAxNjguMjA0QzQwMS4wOSAxNzUuNTM1IDQwNy4wNCAxNzkuMjAxIDQxMy44MzkgMTc5LjIwMUM0MTkuMjU4IDE3OS4yMDEgNDIzLjU0MyAxNzcuNDEyIDQyNi42OTUgMTczLjgzNUM0MjkuOTUzIDE3MC4xNTIgNDMxLjU4MiAxNjQuOTI5IDQzMS41ODIgMTU4LjE2NEM0MzEuNTgyIDE1Mi4wMzcgNDMwLjIxOSAxNDcuMjIxIDQyNy40OTIgMTQzLjcxNUM0MjQuMzc1IDEzOS43NDggNDE5LjgyNCAxMzcuNzY1IDQxMy44MzkgMTM3Ljc2NUM0MDkuNTU0IDEzNy43NjUgNDA1LjcxMSAxMzkuMTExIDQwMi4zMTIgMTQxLjgwMkMzOTkuNjU1IDE0My44OTIgMzk3LjU0OCAxNDYuNzYxIDM5NS45OSAxNTAuNDA4VjE2OC4yMDRaTTUxOC4zNTkgMTYzLjI2NEg0NzAuNDk2QzQ3MC43NDQgMTY4Ljg5NSA0NzIuNTE0IDE3My40NjQgNDc1LjgwOCAxNzYuOTdDNDc5Ljc3NCAxODEuMTEzIDQ4NC44MjEgMTgzLjE4NSA0OTAuOTQ4IDE4My4xODVDNDk4LjE3MyAxODMuMTg1IDUwNC41NjUgMTc5LjgwMyA1MTAuMTI1IDE3My4wMzlMNTE4LjYyNSAxODEuNjQ0QzUxMS42NDggMTkwLjQyNyA1MDEuOTggMTk0LjgxOSA0ODkuNjIgMTk0LjgxOUM0NzkuNDkxIDE5NC44MTkgNDcxLjMyOCAxOTEuNTc4IDQ2NS4xMyAxODUuMDk3QzQ1OS4yMTYgMTc4Ljg2NCA0NTYuMjU5IDE3MC44MjUgNDU2LjI1OSAxNjAuOThDNDU2LjI1OSAxNTIuOTc2IDQ1OC4xODkgMTQ2LjAxNyA0NjIuMDQ5IDE0MC4xMDNDNDY1LjQ4NCAxMzQuODYxIDQ3MC4wNzEgMTMxLjA1NCA0NzUuODA4IDEyOC42ODFDNDc5LjczOSAxMjcuMDUyIDQ4My45MzYgMTI2LjIzNyA0ODguMzk4IDEyNi4yMzdDNDk1LjUxNiAxMjYuMjM3IDUwMS41OSAxMjguMjIxIDUwNi42MTkgMTMyLjE4N0M1MTEuODI1IDEzNi4yMjUgNTE1LjMzMSAxNDEuODczIDUxNy4xMzcgMTQ5LjEzM0M1MTcuOTUyIDE1Mi40MjcgNTE4LjM1OSAxNTUuODk4IDUxOC4zNTkgMTU5LjU0NVYxNjMuMjY0Wk01MDQuMTIyIDE1Mi45MDVDNTAzLjgzOSAxNDkuMjU3IDUwMi44ODMgMTQ2LjIxMiA1MDEuMjU0IDE0My43NjhDNDk4LjE3MyAxMzkuMjcgNDkzLjc0NiAxMzcuMDIxIDQ4Ny45NzMgMTM3LjAyMUM0ODIuODAyIDEzNy4wMjEgNDc4LjU1MyAxMzkuMTExIDQ3NS4yMjQgMTQzLjI5QzQ3My4xNjkgMTQ1Ljg3NSA0NzEuODk0IDE0OS4wOCA0NzEuMzk5IDE1Mi45MDVINTA0LjEyMloiIGZpbGw9IndoaXRlIi8+CjxnIGZpbHRlcj0idXJsKCNmaWx0ZXIwX2RfMzY3MV80MDc0KSI+CjxwYXRoIGQ9Ik0xMjYuOTM0IDc2Ljg3MkMxMjcuMjE1IDg3LjA1NDkgMTIyLjk1NCA5My42MzkzIDExNC4yODQgOTguNzIzM0MxMDMuNjY3IDEwNC45NDkgOTIuNjk2NSAxMTEuMzU0IDgyLjAwNzYgMTE3LjUwNUM3MC4xNjMzIDEyNC4zMjEgNjcuMjE0IDEzMi42NTQgNzUuNzE5NiAxNDMuNjQxQzcyLjk1MzkgMTQ5LjcwNCA2My4zMTU3IDE0OC41OSA1Ny45OTczIDE0Ny43MTFDNTIuMDM4OSAxNDQuMDg4IDUwLjMwNDEgMTM2LjE3IDUwLjY0MjUgMTI5LjY5QzUxLjEyMzcgMTIwLjQ3OSA1Ni4wMDU4IDExMS43MTQgNjIuNjk0NyAxMDUuNDg1Qzg0LjA2MDQgODkuMzc3NiAxMDUuNDUzIDczLjMwNDQgMTI2Ljg3OCA1Ny4yNzY1QzEyNi44NzcgNjMuODA4MyAxMjYuODk4IDcwLjM0MDcgMTI2LjkzNCA3Ni44NzJaIiBmaWxsPSJ1cmwoI3BhaW50MF9saW5lYXJfMzY3MV80MDc0KSIvPgo8cGF0aCBkPSJNNzUuNzE4NyAxNDMuNjQyQzc1LjcxODcgMTQzLjY0MiA3NC40MjU4IDE0Mi41OTQgNzIuMjk1NSAxNDAuNjk1QzYyLjE5NTUgMTMxLjY5IDQ5LjAxMDggMTE3Ljc2OCA2Mi42OTM4IDEwNS40ODVDNTguMTg2MSAxMDguOTAxIDU0LjQxNjYgMTEzLjAyOCA1MS4xNjU0IDExNy4zOEM0MS40ODUyIDEzMC4zNDEgNDMuMzY5OSAxNTEuMTkzIDQzLjgzNTUgMTY2Ljc0OUM0NC4wNTk1IDE3NC4yMjcgNTIuODkzNiAxNzUuODg2IDU4LjUxMTggMTcyLjg5NkM2NC42OTkxIDE2OS42MDUgNzEuMyAxNjUuOTExIDc3LjI4NzEgMTYyLjY4OEM4Ni40NzE4IDE1Ny43NDIgODEuOTUzIDE0OC42NTggNzUuNzE4NyAxNDMuNjQyWiIgZmlsbD0idXJsKCNwYWludDFfbGluZWFyXzM2NzFfNDA3NCkiLz4KPHBhdGggZD0iTTQ0LjE0OTkgMjExLjc1MkM0My44Njk1IDIwMS41NjkgNDguMTI4NCAxOTQuOTg1IDU2LjgwMTUgMTg5LjkwMUM2Ny40MjAyIDE4My42NzcgNzguMzg5NiAxNzcuMjY3IDg5LjA3NTcgMTcxLjExOEMxMDAuOTE4IDE2NC4zMDUgMTAzLjg3IDE1NS45NjggOTUuMzY0OCAxNDQuOTgzQzk4LjEzMjEgMTM4LjkxOSAxMDcuNzY5IDE0MC4wMzUgMTEzLjA4OCAxNDAuOTEzQzExOS4wNDQgMTQ0LjUzOCAxMjAuNzc4IDE1Mi40NTcgMTIwLjQ0MSAxNTguOTM0QzExOS45NjIgMTY4LjEzOSAxMTUuMDc2IDE3Ni45MDkgMTA4LjM5IDE4My4xNEM4Ny4wMjI5IDE5OS4yNDYgNjUuNjMxMiAyMTUuMzE5IDQ0LjIwNTIgMjMxLjM0OEM0NC4yMDYzIDIyNC44MTYgNDQuMTg2OSAyMTguMjg0IDQ0LjE0OTkgMjExLjc1MloiIGZpbGw9InVybCgjcGFpbnQyX2xpbmVhcl8zNjcxXzQwNzQpIi8+CjxwYXRoIGQ9Ik05NS4zNjg5IDE0NC45ODRDOTUuMzY4OSAxNDQuOTg0IDk2LjY2MTMgMTQ2LjAzMiA5OC43OTE2IDE0Ny45MzFDMTA4Ljg5NSAxNTYuOTM4IDEyMi4wNzMgMTcwLjg1MyAxMDguMzk1IDE4My4xNDFDMTEyLjkwMyAxNzkuNzI2IDExNi42NjkgMTc1LjU5OSAxMTkuOTIxIDE3MS4yNDZDMTI5LjYwNCAxNTguMjg0IDEyNy43MjEgMTM3LjQzIDEyNy4yNTIgMTIxLjg3N0MxMjcuMDI2IDExNC4zOTggMTE4LjE5NiAxMTIuNzQgMTEyLjU3NiAxMTUuNzI5QzEwNi4zODcgMTE5LjAyMSA5OS43ODcgMTIyLjcxNCA5My44MDA1IDEyNS45MzlDODQuNjE2MyAxMzAuODg2IDg5LjEzNDYgMTM5Ljk2NiA5NS4zNjg5IDE0NC45ODRaIiBmaWxsPSJ1cmwoI3BhaW50M19saW5lYXJfMzY3MV80MDc0KSIvPgo8L2c+CjwvZz4KPGRlZnM+CjxmaWx0ZXIgaWQ9ImZpbHRlcjBfZF8zNjcxXzQwNzQiIHg9Ii04Ljg0NDIiIHk9IjQ0LjIyMTEiIHdpZHRoPSIxODguNzc4IiBoZWlnaHQ9IjI3OC41MTUiIGZpbHRlclVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgY29sb3ItaW50ZXJwb2xhdGlvbi1maWx0ZXJzPSJzUkdCIj4KPGZlRmxvb2QgZmxvb2Qtb3BhY2l0eT0iMCIgcmVzdWx0PSJCYWNrZ3JvdW5kSW1hZ2VGaXgiLz4KPGZlQ29sb3JNYXRyaXggaW49IlNvdXJjZUFscGhhIiB0eXBlPSJtYXRyaXgiIHZhbHVlcz0iMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMTI3IDAiIHJlc3VsdD0iaGFyZEFscGhhIi8+CjxmZU9mZnNldCBkeT0iMzkuMTY2MyIvPgo8ZmVHYXVzc2lhbkJsdXIgc3RkRGV2aWF0aW9uPSIyNi4xMTA5Ii8+CjxmZUNvbXBvc2l0ZSBpbjI9ImhhcmRBbHBoYSIgb3BlcmF0b3I9Im91dCIvPgo8ZmVDb2xvck1hdHJpeCB0eXBlPSJtYXRyaXgiIHZhbHVlcz0iMCAwIDAgMCAwLjcyOTQxMiAwIDAgMCAwIDAuNDU0OTAyIDAgMCAwIDAgMC44NDMxMzcgMCAwIDAgMC4zNSAwIi8+CjxmZUJsZW5kIG1vZGU9Im5vcm1hbCIgaW4yPSJCYWNrZ3JvdW5kSW1hZ2VGaXgiIHJlc3VsdD0iZWZmZWN0MV9kcm9wU2hhZG93XzM2NzFfNDA3NCIvPgo8ZmVCbGVuZCBtb2RlPSJub3JtYWwiIGluPSJTb3VyY2VHcmFwaGljIiBpbjI9ImVmZmVjdDFfZHJvcFNoYWRvd18zNjcxXzQwNzQiIHJlc3VsdD0ic2hhcGUiLz4KPC9maWx0ZXI+CjxsaW5lYXJHcmFkaWVudCBpZD0icGFpbnQwX2xpbmVhcl8zNjcxXzQwNzQiIHgxPSIxMjYuOTQ3IiB5MT0iNTcuMjc2NSIgeDI9IjU2LjE4NDUiIHkyPSIxMzYuMzE5IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CjxzdG9wIHN0b3AtY29sb3I9IiNDQjdEREUiLz4KPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjNDgzOEE0Ii8+CjwvbGluZWFyR3JhZGllbnQ+CjxsaW5lYXJHcmFkaWVudCBpZD0icGFpbnQxX2xpbmVhcl8zNjcxXzQwNzQiIHgxPSI4Mi41IiB5MT0iMTA1LjQ4NSIgeDI9IjMwLjczNjYiIHkyPSIxNDQuNzIyIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CjxzdG9wIHN0b3AtY29sb3I9IiNDQjdEREUiLz4KPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjNzk2NUU2Ii8+CjwvbGluZWFyR3JhZGllbnQ+CjxsaW5lYXJHcmFkaWVudCBpZD0icGFpbnQyX2xpbmVhcl8zNjcxXzQwNzQiIHgxPSI0NC40NjMzIiB5MT0iMjM1Ljg4MSIgeDI9IjExOC42NTIiIHkyPSIxNTQuOTA3IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CjxzdG9wIHN0b3AtY29sb3I9IiNDQjdEREUiLz4KPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjNDgzOEE0Ii8+CjwvbGluZWFyR3JhZGllbnQ+CjxsaW5lYXJHcmFkaWVudCBpZD0icGFpbnQzX2xpbmVhcl8zNjcxXzQwNzQiIHgxPSIxMjcuNzEyIiB5MT0iMTE0LjMyNCIgeDI9Ijc1Ljk0NzkiIHkyPSIxNTMuNTYzIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CjxzdG9wIHN0b3AtY29sb3I9IiNDQjdEREUiLz4KPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjNzk2NUU2Ii8+CjwvbGluZWFyR3JhZGllbnQ+CjxjbGlwUGF0aCBpZD0iY2xpcDBfMzY3MV80MDc0Ij4KPHJlY3Qgd2lkdGg9IjU4NCIgaGVpZ2h0PSIyOTIiIGZpbGw9IndoaXRlIi8+CjwvY2xpcFBhdGg+CjwvZGVmcz4KPC9zdmc+Cg=="

st.markdown(f'<img src="data:image/svg+xml;base64,{_LOGO_B64}" height="48" style="display:block; margin-bottom:1rem;" />', unsafe_allow_html=True)

st.markdown("<h1 style='color:white;font-size:1.9rem;font-weight:800;margin-bottom:0.25rem;'>Payouts Cost Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#b8a8d8;margin-bottom:1.4rem;font-size:0.95rem;'>Enter your current payout costs below to see how much you could save.</p>", unsafe_allow_html=True)

# ── FX toggle (resolved before the bar so bar can react) ──────────────────────
include_fx = st.checkbox("I have FX to local currency", value=False)

# ── Stape pricing: subtle reference bar ───────────────────────────────────────
fx_pill = f'<span class="pill">{STAPE_FX_RATE:.0f}% FX rate</span>' if include_fx else ""
st.markdown(f"""
<div class="stape-rates-bar">
    <span class="bar-label">Stape pricing</span>
    <span class="pill">1–9 payouts: $50</span>
    <span class="pill">10–25: $45</span>
    <span class="pill">26–50: $40</span>
    <span class="pill">51+: $35</span>
    {fx_pill}
</div>
""", unsafe_allow_html=True)

# ── Single input card ─────────────────────────────────────────────────────────
st.markdown('<div class="input-card"><div class="input-card-title">Your current costs</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    raw_amount = st.text_input("Number of Payouts", value="10",
                               help="Use spaces as thousands separator, e.g. 1 000")
    amount_val, amount_err = parse_int_input(raw_amount, "Number of Payouts")
    if amount_err: st.error(amount_err)
    amount_of_payouts = amount_val if amount_val is not None else 0

with c2:
    raw_volume = st.text_input("Payouts Volume (USD)", value="300 000",
                               help="Use spaces as thousands separator, e.g. 300 000")
    volume_val, volume_err = parse_int_input(raw_volume, "Payouts Volume")
    if volume_err: st.error(volume_err)
    payouts_volume = volume_val if volume_val is not None else 0

# FX rate field — only shown when checkbox is on
if include_fx:
    c3, c4 = st.columns(2)
    with c3:
        current_fx = st.number_input("Your FX Rate (%)", min_value=0.0, max_value=100.0,
                                     value=2.5, step=0.01, format="%.2f",
                                     help="FX markup you currently pay.")
    with c4:
        curr_cost_type = st.radio(
            "Payout Cost Type",
            options=["Fixed (USD per payout)", "Percentage (% of volume)"],
            index=1,
            help="How your provider charges the processing fee."
        )
else:
    current_fx = 0.0
    curr_cost_type = st.radio(
        "Payout Cost Type",
        options=["Fixed (USD per payout)", "Percentage (% of volume)"],
        index=1,
        help="How your provider charges the processing fee."
    )

if curr_cost_type == "Fixed (USD per payout)":
    current_payout_cost = st.number_input(
        "Your Payout Cost (USD per payout)",
        min_value=0, value=50, step=1, format="%d"
    )
    curr_proc_label = f"${fmt_num(current_payout_cost)} × {fmt_num(amount_of_payouts)} payouts"
else:
    current_payout_cost = st.number_input(
        "Your Payout Cost (% of volume)",
        min_value=0.0, max_value=100.0, value=3.0, step=0.01, format="%.2f"
    )
    curr_proc_label = f"{current_payout_cost:.2f}% × {fmt_usd(payouts_volume)}"

st.markdown('</div>', unsafe_allow_html=True)

# ── Calculations ──────────────────────────────────────────────────────────────
has_errors = amount_err or volume_err

if not has_errors:
    curr_fx_cost    = (current_fx / 100) * payouts_volume if include_fx else 0.0
    curr_proc_cost  = (current_payout_cost * amount_of_payouts
                       if curr_cost_type == "Fixed (USD per payout)"
                       else (current_payout_cost / 100) * payouts_volume)
    curr_total      = curr_fx_cost + curr_proc_cost

    stape_fee       = stape_fee_per_payout(amount_of_payouts)
    stape_fx_cost   = (STAPE_FX_RATE / 100) * payouts_volume if include_fx else 0.0
    stape_proc_cost = stape_fee * amount_of_payouts
    stape_total     = stape_fx_cost + stape_proc_cost
    stape_proc_label = f"${stape_fee} × {fmt_num(amount_of_payouts)} payouts"

    savings     = curr_total - stape_total
    savings_pct = (savings / curr_total * 100) if curr_total > 0 else 0

    # ── Savings banner (hero) ─────────────────────────────────────────────────
    if savings > 0:
        st.markdown(f"""
        <div class="savings-banner-green">
            <div class="s-label">💰 Your savings with Stape</div>
            <div class="s-value">{fmt_usd(savings)}</div>
            <div class="s-sub">That's {savings_pct:.1f}% less than your current costs</div>
        </div>""", unsafe_allow_html=True)
    elif savings < 0:
        st.markdown(f"""
        <div class="savings-banner" style="background:linear-gradient(135deg,rgba(180,40,40,0.22),rgba(120,20,20,0.15));border-color:rgba(255,100,100,0.3);">
            <div class="s-label" style="color:#fca5a5;">Cost difference</div>
            <div class="s-value" style="color:#f87171;">{fmt_usd(abs(savings))}</div>
            <div class="s-sub" style="color:#f87171;">Stape costs more in this scenario</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="savings-banner">
            <div class="s-label">Costs are equal</div>
            <div class="s-value">$0</div>
        </div>""", unsafe_allow_html=True)

    # ── Breakdown metrics ─────────────────────────────────────────────────────
    st.markdown("<div style='height:0.2rem'></div>", unsafe_allow_html=True)

    if include_fx:
        r1, r2, r3 = st.columns(3)
        with r1: st.metric("Current FX Cost",         fmt_usd(curr_fx_cost))
        with r2: st.metric("Current Processing Cost", fmt_usd(curr_proc_cost))
        with r3: st.metric("Current Total",            fmt_usd(curr_total))
    else:
        r2, r3 = st.columns(2)
        with r2: st.metric("Current Processing Cost", fmt_usd(curr_proc_cost))
        with r3: st.metric("Current Total",            fmt_usd(curr_total))

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    if include_fx:
        r4, r5, r6 = st.columns(3)
        with r4:
            st.metric("Stape FX Cost", fmt_usd(stape_fx_cost),
                      delta=fmt_delta(stape_fx_cost - curr_fx_cost) if stape_fx_cost != curr_fx_cost else None,
                      delta_color="inverse")
        with r5:
            st.metric("Stape Processing Cost", fmt_usd(stape_proc_cost),
                      delta=fmt_delta(stape_proc_cost - curr_proc_cost) if stape_proc_cost != curr_proc_cost else None,
                      delta_color="inverse")
        with r6:
            st.metric("Stape Total", fmt_usd(stape_total),
                      delta=fmt_delta(stape_total - curr_total) if stape_total != curr_total else None,
                      delta_color="inverse")
    else:
        r5, r6 = st.columns(2)
        with r5:
            st.metric("Stape Processing Cost", fmt_usd(stape_proc_cost),
                      delta=fmt_delta(stape_proc_cost - curr_proc_cost) if stape_proc_cost != curr_proc_cost else None,
                      delta_color="inverse")
        with r6:
            st.metric("Stape Total", fmt_usd(stape_total),
                      delta=fmt_delta(stape_total - curr_total) if stape_total != curr_total else None,
                      delta_color="inverse")

    # ── Formula expander ──────────────────────────────────────────────────────
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    with st.expander("🔍 How this was calculated"):
        fx_row = (f"| FX Cost | `{current_fx:.2f}% × {fmt_usd(payouts_volume)}` = **{fmt_usd(curr_fx_cost)}** "
                  f"| `{STAPE_FX_RATE:.1f}% × {fmt_usd(payouts_volume)}` = **{fmt_usd(stape_fx_cost)}** |\n"
                  if include_fx else "")
        st.markdown(f"""
| | Your Current Provider | With Stape |
|---|---|---|
{fx_row}| Processing Cost | `{curr_proc_label}` = **{fmt_usd(curr_proc_cost)}** | `{stape_proc_label}` = **{fmt_usd(stape_proc_cost)}** |
| **Total** | **{fmt_usd(curr_total)}** | **{fmt_usd(stape_total)}** |
| **Savings** | | **{fmt_usd(savings)}** ({savings_pct:.1f}%) |
        """)

st.caption("All values are in USD.")
