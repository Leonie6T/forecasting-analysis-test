import pandas as pd, numpy as np
import statsmodels.formula.api as smf
f = pd.read_csv('../output/forecasts_clean.csv'); f['brier'] = (f.forecast-f.outcome)**2
out = ["CHECK 1: wave"]
out.append("Rows by group x wave:\n" + pd.crosstab(f.group, f.wave).to_string())
out.append("Mean Brier by group x wave:\n" + f.groupby(['group','wave']).brier.mean().unstack().round(4).to_string())
m = smf.ols('brier ~ C(group) + C(wave)', data=f).fit(cov_type='cluster', cov_kwds={'groups': f.forecaster_id})
out.append(f"Wave effect (forecast-level OLS, SE clustered by forecaster): coef={m.params['C(wave)[T.2]']:.4f}, p={m.pvalues['C(wave)[T.2]']:.3f}")
out.append("\nCHECK 2: question-level dependence")
# two-way cluster bootstrap: resample forecasters and questions
rng = np.random.default_rng(0)
F = f.forecaster_id.unique(); Q = f.question_id.unique()
res = {g: [] for g in f.group.unique()}
piv = f.pivot_table(index='forecaster_id', columns='question_id', values='brier')
gmap = f.drop_duplicates('forecaster_id').set_index('forecaster_id').group
for _ in range(2000):
    fs = rng.choice(F, len(F)); qs = rng.choice(Q, len(Q))
    sub = piv.loc[fs, qs]
    per = sub.mean(axis=1)
    for g in res: res[g].append(per[gmap.loc[fs].values == g].mean())
old = pd.read_csv('../output/brier_by_group.csv').set_index('group')
rows = []
for g in old.index:
    lo, hi = np.percentile(res[g], [2.5, 97.5])
    rows.append(dict(group=g, mean=old.loc[g,'mean_brier'], ci_forecaster_only=f"{old.loc[g,'ci_low']:.4f}-{old.loc[g,'ci_high']:.4f}", ci_two_way=f"{lo:.4f}-{hi:.4f}"))
out.append(pd.DataFrame(rows).round(4).to_string(index=False))
# mixed model: random intercepts for forecaster and question (question as variance component)
mm = smf.mixedlm('brier ~ C(group)', f, groups=f.forecaster_id, re_formula='1', vc_formula={'question': '0 + C(question_id)'}).fit(reml=True)
out.append("\nMixed model brier ~ group, random intercepts forecaster + question:")
out.append(mm.summary().tables[1].to_string())
txt = "\n".join(out); print(txt); open('../output/robustness_output.txt','w').write(txt)
