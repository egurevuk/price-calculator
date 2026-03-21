import streamlit as st

st.set_page_config(page_title="Payouts Cost Calculator", page_icon="💸", layout="centered")

st.title("💸 Payouts Cost Calculator")
st.markdown("Calculate the total cost of your payouts including FX and processing fees.")

st.divider()

# --- Inputs ---
st.subheader("Enter Payout Details")

col1, col2 = st.columns(2)

with col1:
    amount_of_payouts = st.number_input(
        "Number of Payouts",
        min_value=0,
        value=100,
        step=1,
        help="Total number of individual payout transactions."
    )

with col2:
    payouts_volume = st.number_input(
        "Payouts Volume (USD)",
        min_value=0.0,
        value=10000.0,
        step=100.0,
        format="%.2f",
        help="Total USD volume of all payouts combined."
    )

st.subheader("Fee Structure")

col3, col4 = st.columns(2)

with col3:
    cost_type = st.radio(
        "Payouts Cost Type",
        options=["Fixed (USD per payout)", "Percentage (% of volume)"],
        help="Choose whether the payout fee is a fixed amount per transaction or a percentage of the volume."
    )

with col4:
    if cost_type == "Fixed (USD per payout)":
        payouts_cost = st.number_input(
            "Payouts Cost (USD per payout)",
            min_value=0.0,
            value=0.25,
            step=0.01,
            format="%.4f",
            help="Fixed cost charged per individual payout."
        )
    else:
        payouts_cost = st.number_input(
            "Payouts Cost (% of volume)",
            min_value=0.0,
            max_value=100.0,
            value=1.0,
            step=0.01,
            format="%.4f",
            help="Percentage of total volume charged as a processing fee."
        )

fx_rate = st.number_input(
    "FX Rate (%)",
    min_value=0.0,
    max_value=100.0,
    value=1.5,
    step=0.01,
    format="%.4f",
    help="Foreign exchange markup applied to the total payout volume."
)

st.divider()

# --- Calculation ---
fx_cost = (fx_rate / 100) * payouts_volume

if cost_type == "Fixed (USD per payout)":
    processing_cost = payouts_cost * amount_of_payouts
    formula_label = f"${payouts_cost:.4f} × {amount_of_payouts:,} payouts"
else:
    processing_cost = (payouts_cost / 100) * payouts_volume
    formula_label = f"{payouts_cost:.4f}% × ${payouts_volume:,.2f} volume"

total_cost = fx_cost + processing_cost

# --- Results ---
st.subheader("📊 Results")

res_col1, res_col2, res_col3 = st.columns(3)

with res_col1:
    st.metric(
        label="FX Cost",
        value=f"${fx_cost:,.2f}",
        help=f"{fx_rate:.4f}% × ${payouts_volume:,.2f} volume"
    )

with res_col2:
    st.metric(
        label="Processing Cost",
        value=f"${processing_cost:,.2f}",
        help=formula_label
    )

with res_col3:
    st.metric(
        label="Total Cost",
        value=f"${total_cost:,.2f}",
    )

# --- Formula Breakdown ---
with st.expander("🔍 How this was calculated"):
    if cost_type == "Fixed (USD per payout)":
        st.markdown(f"""
**Formula:**

`Cost = FX Rate × Volume + Payouts Cost × Number of Payouts`

**Values:**
- FX Cost: `{fx_rate:.4f}% × ${payouts_volume:,.2f}` = **${fx_cost:,.2f}**
- Processing Cost: `${payouts_cost:.4f} × {amount_of_payouts:,}` = **${processing_cost:,.2f}**
- **Total Cost = ${fx_cost:,.2f} + ${processing_cost:,.2f} = ${total_cost:,.2f}**
        """)
    else:
        st.markdown(f"""
**Formula:**

`Cost = FX Rate × Volume + Payouts Cost (%) × Volume`

**Values:**
- FX Cost: `{fx_rate:.4f}% × ${payouts_volume:,.2f}` = **${fx_cost:,.2f}**
- Processing Cost: `{payouts_cost:.4f}% × ${payouts_volume:,.2f}` = **${processing_cost:,.2f}**
- **Total Cost = ${fx_cost:,.2f} + ${processing_cost:,.2f} = ${total_cost:,.2f}**
        """)

st.caption("All values are in USD.")
