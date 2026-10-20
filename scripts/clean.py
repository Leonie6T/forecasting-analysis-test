import pandas as pd
f = pd.read_csv('../data/forecasts.csv')
log = []
n0 = len(f)
f = f.drop_duplicates(); log.append(f"Dropped {n0-len(f)} exact duplicate rows")
n1 = len(f)
f = f[f.forecast.between(0, 1)]; log.append(f"Dropped {n1-len(f)} rows with forecast outside [0,1]")
known = f.dropna(subset=['outcome']).groupby('question_id').outcome.first()
nfill = f.outcome.isna().sum()
f['outcome'] = f.outcome.fillna(f.question_id.map(known)); log.append(f"Filled {nfill} missing outcomes from the question's recorded outcome")
f['outcome'] = f.outcome.astype(int)
assert f.outcome.isna().sum() == 0 and f.duplicated(['forecaster_id','question_id']).sum() == 0
f.to_csv('../output/forecasts_clean.csv', index=False)
log.append(f"Clean file: {len(f)} rows, {f.forecaster_id.nunique()} forecasters, {f.question_id.nunique()} questions")
open('../output/cleaning_log.md','w').write("# Cleaning log\n\n" + "\n".join(f"- {l}" for l in log) +
"\n\n## Questions for data owner\n- 15 rows exported with blank outcome although the question had resolved. Cause of the join gap? Confirm outcomes are recorded per question, not per forecaster.\n- 23 forecasts recorded above 1 (values 1.5 to 99). Platform input scale (0-1 or 0-100)? Display bug or forecaster entry error? Dropped pending answer.\n- 2 forecasts at exactly 0 or 1. Did the platform allow these? Kept.\n")
print("\n".join(log))
