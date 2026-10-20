import pandas as pd, numpy as np
from scipy import stats
import statsmodels.formula.api as smf
per = pd.read_csv('../output/brier_per_forecaster.csv')
g = {k: v.brier.values for k, v in per.groupby('group')}
out = []
H, p = stats.kruskal(*g.values()); out.append(f"Kruskal-Wallis: H={H:.1f}, p={p:.2e}")
pairs = [('superforecaster','domain_expert'),('superforecaster','general_public'),('domain_expert','general_public')]
ps = [stats.mannwhitneyu(g[a], g[b], alternative='two-sided').pvalue for a, b in pairs]
from statsmodels.stats.multitest import multipletests
adj = multipletests(ps, method='holm')[1]
for (a, b), p0, p1 in zip(pairs, ps, adj):
    d = (g[a].mean()-g[b].mean())/np.sqrt((g[a].var(ddof=1)+g[b].var(ddof=1))/2)
    out.append(f"  {a} vs {b}: Mann-Whitney p={p0:.2e}, Holm-adjusted p={p1:.2e}, Cohen's d={d:.2f}")
out.append("\nSpearman (years_experience vs Brier) within group:")
for k, v in per.groupby('group'):
    r, p = stats.spearmanr(v.years, v.brier)
    out.append(f"  {k}: rho={r:.3f}, p={p:.3f}, n={len(v)}, years range {v.years.min()}-{v.years.max()}")
out.append("\nOLS: brier ~ years + group (reference = domain_expert), HC3 robust SE")
m = smf.ols('brier ~ years + C(group)', data=per).fit(cov_type='HC3')
out.append(m.summary2().tables[1].round(4).to_string())
out.append(f"R2={m.rsquared:.3f}")
m2 = smf.ols('brier ~ years * C(group)', data=per).fit(cov_type='HC3')
out.append(f"\nInteraction model (years x group): slopes differ by group? F-test p={m2.compare_f_test(m)[1]:.3f}")
txt = "\n".join(out); print(txt); open('../output/tests_output.txt','w').write(txt)
