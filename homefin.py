# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 22:33:27 2023
"""
import numpy_financial as npf
import numpy as np
import pandas as pd
import plotly.graph_objects as go

class Loan:
    def __init__(self, name):
        # These are (public) class attributes
        self.name = name
        self.principal = None  # Darlehensbetrag
        self.interest_rate = None  # Zinssatz % p.a.
        self.payment_against_loan = None  # Tilgung
        self.payment = None  # Rückzahlung
        self.payment_period = None  # Kreditlaufzeit
        self.residual_debt = None  # Restschuld nach Sollzinsbindung
        # self.yearly_unscheduled_repayment = None  # Jährliche Sondertilgung

    def amortisation_table(self, rate, pmt, pv, fv=0, when='end'):
        # Laufzeit ermitteln
        # Number of periodic payments
        nper = npf.nper(rate / 12, pmt, pv, fv, when)

        # Create dataframe for each rate
        dfs = []
        for rate_v, nper_v, pmt_v, pv_v, rate_v in zip(rate, nper, pmt, pv, rate):
            try:
                per = np.arange(nper_v) + 1  # array of payment periods: array([1, 2, 3, ...])
                ipmt = npf.ipmt(rate_v / 12, per, nper_v, pv_v, fv, when)  # interest portion of payment (Zinsanteil)
                ppmt = npf.ppmt(rate_v / 12, per, nper_v, pv_v, fv, when)  # payment against loan principal (Tilgungsanteil)
                residual_debt = -npf.fv(rate_v / 12, per, pmt_v, pv_v, when)
                # interestpd = np.sum(ipmt)
                interestpd_cum = np.cumsum(ipmt)

                df = pd.DataFrame.from_dict({'Period': per,
                                             'Interest portion': ipmt,
                                             'Repayment portion': ppmt,
                                             'Residual debt': residual_debt,
                                             'Cumulated interest paid': interestpd_cum})
                err = None

            except ValueError:  # Catch value error (nper has nan values)
                df = None
                err = ValueError

            dfs.append((rate_v, df, err))

        return dfs

    def loan_period(self, rate, pmt, pv, fv=0, when='end'):
        nper = npf.nper(rate / 12, pmt, pv, fv, when)
        nper_a = nper / 12
        return nper_a, nper

    def present_value(self, rate, nper, pmt, fv=0, when='end'):
        pv = npf.pv(rate / 12, nper, pmt, fv=0, when='end')
        return pv

template = 'seaborn'  # 'seaborn', 'plotly_white', 'ggplot2', 'plotly_dark', 'presentation' (also: 'plotly+presentation')


def pmt_plot(datasets, x_label, y_label, title="", xformat='.1f', yformat=',.1f'):
    """Return plotly figure to show computation results."""
    fig = go.Figure()

    for (x, y, name) in datasets:

        fig.add_trace(
            go.Scatter(x=x,
                       y=y,
                       mode='lines',  # 'lines+markers'
                       name=name))

    # Tight layout, labels, etc.
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                      xaxis_title=x_label,
                      yaxis_title=y_label,
                      # paper_bgcolor="LightSteelBlue",
                      # legend_title_text='',
                      xaxis_tickformat=xformat,  # https://d3-wiki.readthedocs.io/zh_CN/master/Formatting/#numbers
                      yaxis_tickformat=yformat,
                      title=title,
                      template=template,
                      )

    fig.update_xaxes(showgrid=True,
                     minor_ticks="inside",
                     tick0=0,
                     dtick=5,
                     minor=dict(dtick=1)
                     )

    fig.update_yaxes(showgrid=True)

    return fig


if __name__ == "__main__":

    myloan = Loan('Test')

    rate = np.array([0.02, 0.03, 0.04, 0.045])  # % p.a.
    pmt = -2000.
    pmt = np.full_like(rate, pmt)

    pv = 500000.
    pv = np.full_like(rate, pv)

    dfs = myloan.amortisation_table(rate, pmt, pv)

    for (rate, df) in dfs:
        print("Rate:", rate * 100, "% p.a.")
        print(df)
