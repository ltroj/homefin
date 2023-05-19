# -*- coding: utf-8 -*-
"""Loan scenarios app page"""
import streamlit as st
import numpy as np
from homefin import Loan, pmt_plot

st.set_page_config(page_title='Loan scenarios | homefin.py', page_icon="📈", layout="wide")

for k, v in st.session_state.items():
    st.session_state[k] = v
    
st.title('Loan scenarios | Kreditszenarien')

st.sidebar.header('Parameters | Einstellwerte')

principal = st.sidebar.slider('Principal | Darlehensbetrag', min_value=0., max_value=1000000., step=10000., key='pr')
payment = st.sidebar.slider('Monthly payment | Monatliche Rate', min_value=0., max_value=5000., step=100., key='pmt')

st.sidebar.header('Rates | Kreditzinsen (% p.a.)')
with st.sidebar:
    scol1, scol2 = st.columns([1, 1])
    with scol1:
        r1 = st.number_input('Rate #1', min_value=0., max_value=10., step=0.01, key='r1', help='Choose rate in % p.a.')
        r3 = st.number_input('Rate #3', min_value=0., max_value=10., step=0.01, key='r3')
        r5 = st.number_input('Rate #5', min_value=0., max_value=10., step=0.01, key='r5')
    with scol2:
        r2 = st.number_input('Rate #2', min_value=0., max_value=10., step=0.01, key='r2')
        r4 = st.number_input('Rate #4', min_value=0., max_value=10., step=0.01, key='r4')
        r6 = st.number_input('Rate #6', min_value=0., max_value=10., step=0.01, key='r6')

# Sanitize input rates
rs = np.array([r1, r2, r3, r4, r5, r6])
rs = rs[rs != 0]  # Remove all Zero values
rate = rs/100.  # Convert from % to decimal

# Create Central Layout
st.subheader('📈 How long to pay off at different interest rates?')

st.info("Effects not taken into account: Interest rate change after fixed interest period, possible debt rescheduling after 10 years, unscheduled repayments, closing fee, redemption-free period.", icon="ℹ️")
st.info("Nicht berücksichtigte Effekte: Zinsänderung nach Sollzinsbindung, mögliche Umschuldung nach 10 Jahren, Sondertilgungen, Abschlussgebühr, Tilgungsfreie Zeit.", icon="ℹ️")

myloan = Loan('Check scenarios')

# rate = np.array([0.02, 0.03, 0.04, 0.045]) # % p.a.
pmt = -payment
pmt = np.full_like(rate, pmt)

pv = principal
pv = np.full_like(rate, pv)

dfs = myloan.amortisation_table(rate, pmt, pv)

traces = []
for (rate, df, err) in dfs:
    if not err:
        traces.append((df['Period']/12.,
                       df['Residual debt'],
                       str(rate*100) + '% p.a.'))


fig_f = pmt_plot(traces, 'Credit period (years)', 'Residual debt')

st.plotly_chart(fig_f, use_container_width=True)

st.subheader('💸 Amortisation table | Tilgungsplan')
tabnames = []
for (rate, df, _) in dfs:
    tabnames.append(str(rate*100) + '% p.a.')

tabs = st.tabs(tabnames)

for tab, (_, df, err) in zip(tabs, dfs):
    with tab:
        if err is ValueError:  # If there appearead a ValueError for chosen rate
            st.error("No solution could be found. Make sure the monthly repayment is positive (reduce Principal/Credit rate, increase Monthly payment).", icon="🚨")

        else:
            col1, col2, _ = st.columns([1, 1, 1])
            with col1:
                v_period = df['Period'].iloc[-1]/12.
                st.metric(label="📆 Credit period | Kreditlaufzeit bis Tilgung", value=f"{v_period:.1f} a")

            with col2:
                interestpd_v = df['Cumulated interest paid'].iloc[-1]
                st.metric(label="💰 Accrued interest paid | Aufgelaufene Zinsen", value=f"{interestpd_v:,.2f} €")

            st.dataframe(df, use_container_width=True)

            traces = [(df['Period']/12.,
                       -df['Interest portion'],
                       'Interest portion of payment (Zinsanteil)'),
                      (df['Period']/12.,
                       -df['Repayment portion'],
                       'Repayment portion of payment (Tilgungsanteil)'),
                      (df['Period']/12.,
                       -(df['Interest portion']+df['Repayment portion']),
                       'Payment (Monatliche Kreditrate)')]

            fig_r = pmt_plot(traces, 'Credit period (years)', 'Payment')
            st.plotly_chart(fig_r, use_container_width=True)