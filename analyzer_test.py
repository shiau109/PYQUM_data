import expdata as expdata
from data_praser import PyqumPraser
import numpy as np
fn = "test_file/F_Response.pyqum(PD)"
p_praser = PyqumPraser()
print(f"Testing {fn}")
myexp = p_praser.import_data(f"{fn}" )
# print(myexp.dimension)
# print(myexp.shape)
power_dependent_df = myexp.to_DataFrame()
# print(power_dependent_df.columns)

from find_dress.ZY_method import PowerDepend

PDAnalyzer = PowerDepend(power_dependent_df)
min_bare, max_dress=PDAnalyzer.do_analysis()


import plotly.graph_objects as go

fig = go.Figure(data=go.Heatmap(
                   z=np.sqrt(myexp.data["I"]**2+myexp.data["Q"]**2),
                   x=myexp.exp_vars[1][1],
                   y=myexp.exp_vars[0][1],
                   hoverongaps = False))

ana_plot = PDAnalyzer.give_plot_info()
ana_res = ana_plot['scatter']
fig.add_trace(go.Scatter(x=ana_res['Fr'], y=ana_res['Power'],
                    mode='markers',
                    name='markers'))


bare_idx = (np.abs(ana_res['Power'] - min_bare)).argmin()
dress_idx = (np.abs(ana_res['Power'] - max_dress)).argmin()
fig.add_trace(go.Scatter(x=[ana_res['Fr'][bare_idx],ana_res['Fr'][dress_idx] ], y=[ana_res['Power'][bare_idx],ana_res['Power'][dress_idx]],
                    mode='markers',
                    name='markers'))
fig.show()