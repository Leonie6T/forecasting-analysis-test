import pandas as pd, numpy as np
f = pd.read_csv('../output/forecasts_clean.csv')
f['brier'] = (f.forecast - f.outcome)**2
per = f.groupby(['forecaster_id','group']).agg(brier=('brier','mean'), n_q=('brier','size'), years=('years_experience','first')).reset_index()
per.to_csv('../output/brier_per_forecaster.csv', index=False)
rng = np.random.default_rng(0)
out = []
for g, d in per.groupby('group'):
    b = d.brier.values
    boot = [rng.choice(b, len(b)).mean() for _ in range(5000)]
    out.append(dict(group=g, n_forecasters=len(b), mean_brier=b.mean(), sd=b.std(ddof=1),
                    se=b.std(ddof=1)/np.sqrt(len(b)), ci_low=np.percentile(boot,2.5), ci_high=np.percentile(boot,97.5)))
res = pd.DataFrame(out).sort_values('mean_brier')
res.to_csv('../output/brier_by_group.csv', index=False)
print(res.round(4).to_string(index=False))
