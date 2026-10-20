import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
per = pd.read_csv('../output/brier_per_forecaster.csv'); grp = pd.read_csv('../output/brier_by_group.csv')
tw={'superforecaster':(0.0390,0.0514),'domain_expert':(0.0580,0.0749),'general_public':(0.1045,0.1250)}
for g,(lo,hi) in tw.items(): grp.loc[grp.group==g,['ci_low','ci_high']]=[lo,hi]
order = ['superforecaster','domain_expert','general_public']
labels = ['Superforecasters\n(n=60)','Domain experts\n(n=80)','General public\n(n=160)']
rng = np.random.default_rng(1)
fig, ax = plt.subplots(figsize=(6.5,4.2), dpi=200)
for i, g in enumerate(order):
    y = per[per.group==g].brier
    ax.scatter(i + rng.uniform(-0.18,0.18,len(y)), y, s=12, color='#9aa5b1', alpha=0.55, linewidths=0)
    r = grp[grp.group==g].iloc[0]
    ax.errorbar(i, r.mean_brier, yerr=[[r.mean_brier-r.ci_low],[r.ci_high-r.mean_brier]], fmt='o', color='#1f3864', ms=7, capsize=4, lw=1.6, zorder=3)
    ax.text(i+0.24, r.mean_brier, f"{r.mean_brier:.3f}", va='center', fontsize=9, color='#1f3864')
ax.set_xticks(range(3)); ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel('Mean Brier score per forecaster\n(lower = more accurate)', fontsize=9)
ax.axhline(0.25, color='#b91c1c', lw=1, ls='--'); ax.text(2.42, 0.252, 'Chance (always 50%) = 0.25', fontsize=7.5, color='#b91c1c', ha='right', va='bottom')
ax.set_ylim(0, 0.27)
ax.set_title('Forecast accuracy by group', fontsize=11, loc='left', fontweight='bold', pad=18)
ax.text(0, 1.015, 'Points: individual forecasters. Markers: group mean with 95% CI (bootstrap over forecasters and questions).', transform=ax.transAxes, fontsize=7.5, color='#555')
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.grid(axis='y', color='#e5e7eb', lw=0.6); ax.set_axisbelow(True)
plt.tight_layout(); plt.savefig('../output/fig1_brier_by_group.png'); print('saved')
