#!/usr/bin/env python
# coding: utf-8

import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import plotly.graph_objects as go


# Plot of number of defaults as a function of p
path_insolv = os.path.join('results', 'p-no-of-insolvent-test.npy')
p_ib = np.load(path_insolv)

fig, ax = plt.subplots(1, 1, figsize=(8, 4))

xs = p_ib[0]
ys = p_ib[1:, :]
y_avg = np.mean(ys, axis=0)

ax.plot(xs, y_avg, color='darkmagenta')

plt.plot()
fig.suptitle('Number of insolvent banks as a function of $p$', fontsize=14)
ax.set_title('for $n=1000$, $t=20$, $\\alpha=0.5$, and $\\beta=0.5$', fontsize=9)
ax.set_xlabel('Probability of debt liability ($p$)')
ax.set_ylabel('Number of defaults')
ax.set_xlim(0.01,0.1)

savepath = os.path.join('results', 'p-no-of-insolvent-plot.png')
plt.savefig(savepath, bbox_inches='tight', dpi=300)


# Plot of systemic liquidity as a function of p
path_gcv = os.path.join('results', 'p-size-of-gcv-test.npy')
p_gcv = np.load(path_gcv)

fig, ax = plt.subplots(1, 1, figsize=(8, 4))

xs = p_gcv[0]
ys = p_gcv[1:, :]
y_avg = np.mean(ys, axis=0)

ax.plot(xs, y_avg, color='darkmagenta')

fig.suptitle('Systemic liquidity as a function of $p$', fontsize=14)
ax.set_title('for $n=1000$, $t=20$, $\\alpha=0.5$, and $\\beta=0.5$', fontsize=9)
ax.set_xlabel('Probability of debt liability ($p$)')
ax.set_ylabel('Sum of payments in network')
ax.set_xlim(0.01,0.1)

savepath = os.path.join('results', 'p-size-of-gcv-plot.png')
plt.savefig(savepath, bbox_inches='tight', dpi=300)


# Plot of number of defaults as a function of t
path_insolv = os.path.join('results', 't-no-of-insolvent-test.npy')
t_insolv = np.load(path_insolv)

fig, ax = plt.subplots(1, 1, figsize=(8, 4))

ys = t_insolv[1:, :]
y_avg = np.mean(ys, axis=0)

ax.plot(t_insolv[0], y_avg, color='darkmagenta')

plt.plot()
fig.suptitle('Number of insolvent banks as a function of $t$', fontsize=14)
ax.set_title('for $n=1000$, $p=0.05$, $\\alpha=0.5$, and $\\beta=0.5$', fontsize=9)
ax.set_xlabel('External asset coefficient ($t$)')
ax.set_ylabel('Number of defaults')
ax.vlines(13, 900,1050, linestyle='--', color='b', linewidth=1, label='$t=13$', alpha=0.5)
ax.legend()
ax.set_xlim(0,100)

savepath = os.path.join('results', 't-no-of-insolvent-plot.png')

plt.savefig(savepath, bbox_inches='tight', dpi=300)


# Plot of distribution of insolvency levels for different p values
path_insolv_lvls = os.path.join('results', 'p-insolvency-levels-test.npy')
p_insolv_lvls = np.load(path_insolv_lvls, allow_pickle='true')

#Inspired by: https://plotly.com/python/box-plots/

no_plots = len(p_insolv_lvls[0])

ps = list(np.around(p, decimals=2) for p in p_insolv_lvls[0]) 
data = []

#The test can only get the number of level-x insolvent banks, 
# so we use this information to simulate full datasets that can be used to make box plots. 
for i in range (0, no_plots):
    data_i = np.array([])
    no_insolvency_levels = len(p_insolv_lvls[1][i])
    
    for j in range(no_insolvency_levels):
        no_lvl_j_insolvent = p_insolv_lvls[1][i][j]
        
        lvl_j = np.full((1, no_lvl_j_insolvent), j)
        data_i = np.concatenate((data_i, lvl_j), axis=None)
        
    data.append(data_i)


# generate an array of rainbow colors by fixing the saturation and lightness of the HSL
# representation of colour and marching around the hue.
c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, no_plots)]


fig = go.Figure(data=[go.Box(
    y=data[i],
    marker_color=c[i], name=ps[i]
    ) for i in range(int(no_plots))])

# format the layout
fig.update_layout(
    #Plot title and subtitle
    title = go.layout.Title(text='Distribution of insolvency-levels <br><sup> for n=1000, t=20, &#945;=0.5, and &#946;=0.5 </sup>', x=0.5, y=0.97),
    xaxis_title='Probability of debt liability (p)',
    yaxis_title ='Insolvency-level',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=True),
    yaxis=dict(zeroline=False, gridcolor='white'),
    plot_bgcolor='#EAEAF2',
    width=800,
    height=450,
    margin=dict(l=50, r=50, b=50, t=50, pad=4),
    font = dict(color = '#051c2c')    
)

# Moves the y-axis to the left
fig.update_yaxes(ticksuffix = "  ")

#Remove trace boxes
fig.update_traces(showlegend=False, 
                  selector=dict(type='box'))

fig.show()

savepath = os.path.join('results', 'p-insolvency-levels-boxplot.png')
fig.write_image(savepath, scale=2)

