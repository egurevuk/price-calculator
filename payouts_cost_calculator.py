import streamlit as st

st.set_page_config(
    page_title="Payouts Cost Calculator",
    page_icon="💸",
    layout="wide"
)

# --- Stape-branded dark theme ---
st.markdown("""
<style>
    /* Page background */
    .stApp {
        background: radial-gradient(ellipse at 80% 10%, #4a1878 0%, #1e0a3c 40%, #090912 100%);
        color: #ffffff;
    }

    /* Hide default Streamlit header/footer */
    #MainMenu, footer, header { visibility: hidden; }

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    /* Section headers */
    h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Field labels (above inputs) */
    label, .stNumberInput label, .stTextInput label {
        color: #c4b5e8 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    /* Radio — widget label */
    .stRadio label {
        color: #c4b5e8 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    /* Radio — option text (the actual choices) */
    .stRadio div[role="radiogroup"] label,
    .stRadio div[role="radiogroup"] label p,
    .stRadio div[role="radiogroup"] span {
        color: #ffffff !important;
        font-size: 0.9rem !important;
    }

    /* Input fields */
    .stTextInput input, .stNumberInput input {
        background-color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 8px !important;
        color: #111111 !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 2px rgba(124,58,237,0.3) !important;
    }

    /* Radio buttons container */
    .stRadio > div {
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 0.5rem 0.75rem;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 12px;
        padding: 1.1rem 1.2rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #c4b5e8 !important;
        font-size: 0.8rem !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
    }

    /* Savings highlight card */
    .savings-card {
        background: linear-gradient(135deg, rgba(124,58,237,0.35), rgba(79,36,158,0.25));
        border: 1px solid rgba(167,139,250,0.4);
        border-radius: 14px;
        padding: 1.4rem 1.8rem;
        text-align: center;
    }
    .savings-card .label {
        color: #c4b5e8;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.3rem;
    }
    .savings-card .value {
        color: #a78bfa;
        font-size: 2.4rem;
        font-weight: 800;
        line-height: 1.1;
    }
    .savings-card .sub {
        color: #a78bfa;
        font-size: 0.9rem;
        margin-top: 0.4rem;
        opacity: 0.85;
    }

    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.1) !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        color: #c4b5e8 !important;
        background: rgba(255,255,255,0.04) !important;
        border-radius: 8px !important;
    }
    .streamlit-expanderContent {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 0 0 8px 8px !important;
        color: #e2d9f3 !important;
    }

    /* Caption */
    .stCaption {
        color: rgba(255,255,255,0.35) !important;
    }

    /* Column card */
    .col-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
    }
    .col-card h4 {
        color: #a78bfa;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.8rem;
    }

    /* Error messages */
    .stAlert {
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Formatting helpers ---
def fmt_usd(n):
    return "$" + f"{n:,.0f}".replace(",", " ")

def fmt_num(n):
    return f"{n:,.0f}".replace(",", " ")

def parse_int_input(raw: str, label: str):
    cleaned = raw.replace(" ", "").replace(",", "").strip()
    if not cleaned:
        return 0, None
    try:
        val = int(cleaned)
        if val < 0:
            return None, f"{label} must be 0 or greater."
        return val, None
    except ValueError:
        return None, f"'{raw}' is not a valid number for {label}."


# --- Logo + Title ---
st.markdown("""
<div style="display:flex; align-items:center; gap:10px; margin-bottom:0.5rem;">
    <svg width="28" height="28" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M20 4L36 13V27L20 36L4 27V13L20 4Z" fill="#7c3aed" opacity="0.9"/>
        <path d="M13 18C13 15.8 14.8 14 17 14H23C25.2 14 27 15.8 27 18C27 20.2 25.2 22 23 22H17C14.8 22 13 23.8 13 26C13 28.2 14.8 30 17 30H27" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
    </svg>
    <span style="font-size:1.3rem; font-weight:700; color:white; letter-spacing:-0.01em;">Stape</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:white; font-size:2rem; font-weight:800; margin-bottom:0.2rem;'>Payouts Cost Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#c4b5e8; margin-bottom:1.5rem;'>Compare your current payout costs against Stape and see how much you save.</p>", unsafe_allow_html=True)

st.divider()

# ── SECTION 1: Payout Details ─────────────────────────────────────────────────
st.markdown("### Payout Details")

col1, col2 = st.columns(2)

with col1:
    raw_amount = st.text_input(
        "Number of Payouts",
        value="10",
        help="Total number of payout transactions. Use spaces as thousands separator."
    )
    amount_val, amount_err = parse_int_input(raw_amount, "Number of Payouts")
    if amount_err:
        st.error(amount_err)
    amount_of_payouts = amount_val if amount_val is not None else 0

with col2:
    raw_volume = st.text_input(
        "Payouts Volume (USD)",
        value="300 000",
        help="Total USD volume of all payouts. Use spaces as thousands separator."
    )
    volume_val, volume_err = parse_int_input(raw_volume, "Payouts Volume")
    if volume_err:
        st.error(volume_err)
    payouts_volume = volume_val if volume_val is not None else 0

st.markdown("<br>", unsafe_allow_html=True)

# ── SECTION 2: Current vs Stape rates (each with own cost type) ───────────────
st.markdown("### Fee Rates")

curr_col, stape_col = st.columns(2, gap="large")

with curr_col:
    st.markdown('<div class="col-card"><h4>Current Provider</h4>', unsafe_allow_html=True)
    current_fx = st.number_input(
        "Current FX Rate (%)",
        min_value=0.0, max_value=100.0, value=2.5, step=0.01, format="%.2f",
        help="FX markup you are currently paying.",
        key="curr_fx"
    )
    curr_cost_type = st.radio(
        "Payout Cost Type",
        options=["Fixed (USD per payout)", "Percentage (% of volume)"],
        key="curr_cost_type",
        help="How your current provider charges the processing fee."
    )
    if curr_cost_type == "Fixed (USD per payout)":
        current_payout_cost = st.number_input(
            "Current Payout Cost (USD per payout)",
            min_value=0, value=50, step=1, format="%d",
            help="Fixed fee per payout you currently pay.",
            key="curr_pc"
        )
    else:
        current_payout_cost = st.number_input(
            "Current Payout Cost (% of volume)",
            min_value=0.0, max_value=100.0, value=2.0, step=0.01, format="%.2f",
            help="% of volume fee you currently pay.",
            key="curr_pc"
        )
    st.markdown('</div>', unsafe_allow_html=True)

with stape_col:
    st.markdown('<div class="col-card"><h4>With Stape</h4>', unsafe_allow_html=True)
    stape_fx = st.number_input(
        "Stape FX Rate (%)",
        min_value=0.0, max_value=100.0, value=1.0, step=0.01, format="%.2f",
        help="FX markup charged by Stape.",
        key="stape_fx"
    )
    stape_cost_type = st.radio(
        "Payout Cost Type",
        options=["Fixed (USD per payout)", "Percentage (% of volume)"],
        key="stape_cost_type",
        help="How Stape charges the processing fee."
    )
    if stape_cost_type == "Fixed (USD per payout)":
        stape_payout_cost = st.number_input(
            "Stape Payout Cost (USD per payout)",
            min_value=0, value=50, step=1, format="%d",
            help="Fixed fee per payout charged by Stape.",
            key="stape_pc"
        )
    else:
        stape_payout_cost = st.number_input(
            "Stape Payout Cost (% of volume)",
            min_value=0.0, max_value=100.0, value=0.5, step=0.01, format="%.2f",
            help="% of volume fee charged by Stape.",
            key="stape_pc"
        )
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ── CALCULATIONS ──────────────────────────────────────────────────────────────
has_errors = amount_err or volume_err

if not has_errors:
    # Current provider
    curr_fx_cost = (current_fx / 100) * payouts_volume
    if curr_cost_type == "Fixed (USD per payout)":
        curr_proc_cost = current_payout_cost * amount_of_payouts
        curr_proc_label = f"${fmt_num(current_payout_cost)} × {fmt_num(amount_of_payouts)} payouts"
    else:
        curr_proc_cost = (current_payout_cost / 100) * payouts_volume
        curr_proc_label = f"{current_payout_cost:.2f}% × {fmt_usd(payouts_volume)}"
    curr_total = curr_fx_cost + curr_proc_cost

    # Stape
    stape_fx_cost = (stape_fx / 100) * payouts_volume
    if stape_cost_type == "Fixed (USD per payout)":
        stape_proc_cost = stape_payout_cost * amount_of_payouts
        stape_proc_label = f"${fmt_num(stape_payout_cost)} × {fmt_num(amount_of_payouts)} payouts"
    else:
        stape_proc_cost = (stape_payout_cost / 100) * payouts_volume
        stape_proc_label = f"{stape_payout_cost:.2f}% × {fmt_usd(payouts_volume)}"
    stape_total = stape_fx_cost + stape_proc_cost

    # Savings
    savings = curr_total - stape_total
    savings_pct = (savings / curr_total * 100) if curr_total > 0 else 0

    # ── RESULTS ───────────────────────────────────────────────────────────────
    st.markdown("### Results")

    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric("Current FX Cost", fmt_usd(curr_fx_cost))
    with r2:
        st.metric("Current Processing Cost", fmt_usd(curr_proc_cost))
    with r3:
        st.metric("Current Total Cost", fmt_usd(curr_total))

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

    r4, r5, r6 = st.columns(3)
    with r4:
        st.metric("Stape FX Cost", fmt_usd(stape_fx_cost),
                  delta=fmt_usd(stape_fx_cost - curr_fx_cost) if stape_fx_cost != curr_fx_cost else None,
                  delta_color="inverse")
    with r5:
        st.metric("Stape Processing Cost", fmt_usd(stape_proc_cost),
                  delta=fmt_usd(stape_proc_cost - curr_proc_cost) if stape_proc_cost != curr_proc_cost else None,
                  delta_color="inverse")
    with r6:
        st.metric("Stape Total Cost", fmt_usd(stape_total),
                  delta=fmt_usd(stape_total - curr_total) if stape_total != curr_total else None,
                  delta_color="inverse")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Savings highlight
    if savings > 0:
        savings_html = f"""
        <div class="savings-card">
            <div class="label">💰 Total Savings with Stape</div>
            <div class="value">{fmt_usd(savings)}</div>
            <div class="sub">You save {savings_pct:.1f}% compared to your current provider</div>
        </div>
        """
    elif savings < 0:
        savings_html = f"""
        <div class="savings-card" style="background:linear-gradient(135deg,rgba(200,50,50,0.2),rgba(150,30,30,0.15));border-color:rgba(255,100,100,0.3);">
            <div class="label">⚠️ Cost Difference</div>
            <div class="value" style="color:#f87171;">{fmt_usd(abs(savings))}</div>
            <div class="sub" style="color:#f87171;">Stape costs more in this scenario — adjust the rates to compare</div>
        </div>
        """
    else:
        savings_html = f"""
        <div class="savings-card">
            <div class="label">Costs are equal</div>
            <div class="value">$0</div>
            <div class="sub">Both providers have the same total cost</div>
        </div>
        """
    st.markdown(savings_html, unsafe_allow_html=True)

    # Formula breakdown
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    with st.expander("🔍 How this was calculated"):
        st.markdown(f"""
| | Current Provider | Stape |
|---|---|---|
| FX Cost | `{current_fx:.2f}% × {fmt_usd(payouts_volume)}` = **{fmt_usd(curr_fx_cost)}** | `{stape_fx:.2f}% × {fmt_usd(payouts_volume)}` = **{fmt_usd(stape_fx_cost)}** |
| Processing Cost | `{curr_proc_label}` = **{fmt_usd(curr_proc_cost)}** | `{stape_proc_label}` = **{fmt_usd(stape_proc_cost)}** |
| **Total** | **{fmt_usd(curr_total)}** | **{fmt_usd(stape_total)}** |
| **Savings** | | **{fmt_usd(savings)}** ({savings_pct:.1f}%) |
        """)

st.caption("All values are in USD.")
