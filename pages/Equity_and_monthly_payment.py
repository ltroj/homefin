# -*- coding: utf-8 -*-
"""Equity and monthly payment app page"""
import streamlit as st
from homefin import Loan
import numpy_financial as npf

st.set_page_config(page_title='Equity and monthly payment | homefin.py', page_icon="💸", layout="wide")


for k, v in st.session_state.items():
    st.session_state[k] = v

st.title('Equity and monthly payment | Eigenkapital und Kreditrate')


with st.sidebar:
    st.header("Set equity")
    total_assets = st.number_input('Total assets | Gesamtvermögen', min_value=0., max_value=None, step=100., key='ta')
    equity = st.slider('Equity contributed for purchase | Eigenkapital für Kauf', min_value=0., max_value=float(total_assets), step=100., key='eq')

    st.divider()

    st.header("Local ancillary costs")

    broker = st.number_input('Broker commission (%)', min_value=0., max_value=None, step=0.1, key='br')

    notary = st.number_input('Notary fees (%)', min_value=0., max_value=None, step=0.1, key='not')

    tax = st.number_input('Land transfer tax (%)', min_value=0., max_value=None, step=0.1, key='tax')

    ancillary_costs_per = broker + notary + tax
    st.metric(label="🕳️ Ancillary costs", value=f"{ancillary_costs_per:,.2f} %")



tab1, tab2, tab3 = st.tabs(["💰 Assets and equity", "💸 Affordable monthly loan payment", "💵 Maximum purchase price"])

with tab1:
    st.header('💰 Assets and equity')

    col11, col12, col13, col14 = st.columns([1, 1, 1, 1])
    with col11:
        remains = total_assets-equity
        st.metric(label="💰 Remaining assets | Verbleibendes Vermögen", value=f"{remains:,.2f}")
    with col12:
        asset_rate = st.number_input('Interest (% p.a.)', min_value=0., max_value=10., step=0.1, key='ar')
    with col13:
        timeframe = st.number_input('Years', min_value=0., max_value=60., step=1., key='tf')
    with col14:
        fv = npf.fv(asset_rate / (100. * 12), timeframe * 12, 0., -remains)
        st.metric(label="💹 Future value", value=f"{fv:,.2f}", delta=f"{fv - remains:,.0f}")

with tab2:
    st.header('💸 Affordable monthly loan payment')

    col21, col22, col23, _ = st.columns([1, 1, 1, 1])
    with col21:
        rent = st.number_input('Current rent including utilities', min_value=0., max_value=None, step=1., key='rent')
    with col22:
        savings_rate = st.number_input('Monthly Savings rate', min_value=0., max_value=None, step=1., key='sav')

    with col21:
        running_costs = st.number_input('Expenses per m² and month', min_value=0., max_value=None, step=0.1, key='cst', help="A common rule of thumb for ongoing utility costs is 4 euros per month per square meter")
    with col22:
        living_area = st.number_input('Living area for cost calculation', min_value=0., max_value=None, step=1., key='area')
    with col23:
        liquid = rent + savings_rate
        st.metric(label="💧 Monthly liquid funds", value=f"{liquid:,.2f}")
        op_reserves = -running_costs * living_area
        st.metric(label="🕳️ Operating expenses/reserves", value=f"{op_reserves:,.2f}")
        aff_payment = -(rent + savings_rate + op_reserves)
        st.divider()
        st.metric(label="💸 Affordable monthly loan payment", value=f"{aff_payment:,.2f}")


with tab3:
    st.header("💵 Maximum purchase price")
    st.divider()
    st.subheader("⚓ Calculate with fixed purchase price")

    col11, col12, col13, _ = st.columns([1, 1, 1, 3])
    with col11:
        purchase_fix = st.number_input('Purchase price', min_value=0., max_value=None, step=100., key='purch')
    with col12:
        ancillary_costs = ancillary_costs_per / 100. * purchase_fix
        st.metric(label=f"🕳️ Ancillary costs ({ancillary_costs_per:,.1f}%)", value=f"{ancillary_costs:,.0f}")
    with col13:
        total_purchase = purchase_fix + ancillary_costs
        st.metric(label="Total purchase costs", value=f"{total_purchase:,.0f}")

    col11, col12, col13, _ = st.columns([1, 1, 1, 3])
    with col11:
        st.metric(label="Equity (absolute value)", value=f"{equity:,.0f}")

    with col12:
        equity_per = (equity / total_purchase) * 100.
        st.metric(label="Equity (relative to total costs)", value=f"{equity_per:,.1f} %")

    col11, col12, col13, col14 = st.columns([1, 1, 1, 3])
    with col11:
        loan_req = total_purchase - equity
        st.metric(label="Amount of credit required", value=f"{loan_req:,.0f}")
    with col12:
        rate = st.number_input('Credit rate (% p.a.)', min_value=0., max_value=10., step=0.01, key='crate', help='Choose rate in % p.a.')
    with col13:
        st.metric(label="💸 Affordable monthly loan payment", value=f"{aff_payment:,.2f}")
    with col14:
        myloan = Loan('')
        rate = rate / 100.
        loan_period, _ = myloan.loan_period(rate, aff_payment, loan_req)
        st.metric(label="Loan period | Kreditlaufzeit", value=f"{loan_period:,.1f} a")

    st.divider()
    st.subheader("🕐 Calculate with fixed loan period")

    col11, col12, col13, col14 = st.columns([1, 1, 1, 3])

    with col11:
        loan_period_fix = st.number_input('Loan period (years)', min_value=0., max_value=None, step=0.01, key='lpf')
    with col12:
        st.metric(label="💸 Affordable monthly loan payment", value=f"{aff_payment:,.2f}")
    with col13:
        rate_perfix = st.number_input('Credit rate (% p.a.)', min_value=0., max_value=10., step=0.01, key='crate_perfix', help='Choose rate in % p.a.')
    with col14:
        myloan = Loan('')
        rate = rate_perfix / 100.
        nper = loan_period_fix * 12
        max_credit = myloan.present_value(rate, nper, aff_payment)
        st.metric(label="Max. credit amount", value=f"{max_credit:,.0f}")

    col11, col12, col13, _ = st.columns([1, 1, 1, 3])
    with col11:
        st.metric(label="Equity (absolute value)", value=f"{equity:,.0f}")

    with col12:
        total_purchase = max_credit + equity
        st.metric(label="Total purchase costs", value=f"{total_purchase:,.0f}")

    with col13:
        equity_per = (equity / total_purchase) * 100.
        st.metric(label="Equity (relative to total costs)", value=f"{equity_per:,.1f} %")

    col11, col12, col13, _ = st.columns([1, 1, 1, 3])
    with col11:
        purchase_fix = total_purchase / (1 + ancillary_costs_per / 100.)
        st.metric(label="Purchase price", value=f"{purchase_fix:,.0f}")

    with col12:
        ancillary_costs = ancillary_costs_per / 100. * purchase_fix
        st.metric(label=f"🕳️ Ancillary costs ({ancillary_costs_per:,.1f}%)", value=f"{ancillary_costs:,.0f}")
