# Cleaning log

- Dropped 30 exact duplicate rows
- Dropped 23 rows with forecast outside [0,1]
- Filled 15 missing outcomes from the question's recorded outcome
- Clean file: 10484 rows, 300 forecasters, 40 questions

## Questions for data owner
- 15 rows exported with blank outcome although the question had resolved. Cause of the join gap? Confirm outcomes are recorded per question, not per forecaster.
- 23 forecasts recorded above 1 (values 1.5 to 99). Platform input scale (0-1 or 0-100)? Display bug or forecaster entry error? Dropped pending answer.
- 2 forecasts at exactly 0 or 1. Did the platform allow these? Kept.

## Method decisions
- Brier score computed per forecast, averaged within forecaster, then averaged across forecasters in each group. Selected because the unit of comparison is the forecaster, not the forecast; forecasters answered between 30 and 39 questions, so a pooled average would weight prolific forecasters more heavily. This is the standard in the forecasting literature (Tetlock and Mellers, Good Judgment Project).
- Uncertainty: 95% bootstrap confidence interval (5,000 resamples of forecasters within group), plus standard error. Selected because per-forecaster Brier scores are bounded and may not be normal; the bootstrap does not assume a distribution.

## Robustness checks
- Dropped rows by group: 0.36% to 0.57% of each group. Out-of-range forecasts skewed to general public (17 of 23) but immaterial in volume.
- Skipping: all groups skipped about 5 of 40 questions. Skipped questions were no harder than answered ones (mean difficulty 0.087 vs 0.088). No correlation between question response rate and difficulty (Spearman 0.21, p 0.19). Per-forecaster Brier not flattered by selective skipping.
- Wave: group mix similar across waves (about 60/40). Wave effect 0.002 Brier, p 0.56. Ignored.
- Question-level dependence: all forecasters answered the same 40 questions. Two-way bootstrap (forecasters and questions) widens CIs about 2x; group CIs still do not overlap. Mixed model with random intercepts for forecaster and question: first fit did not converge and gave misleading SEs (superforecaster vs expert p 0.14). Three converged refits and OLS with two-way clustered SEs all give p < 0.001 for every group contrast. Report two-way bootstrap CIs in the paper.
- Experience: Spearman within group rho 0.12 to 0.23, none p < 0.05. OLS brier ~ years + group: years 0.0008 per year, p 0.07; no group x years interaction (p 0.50). Group R2 0.52. Report as no association detected; narrow within-group experience ranges limit power.

## Limitations to state
- Observational design; group is a label, not a mechanism. No causal claim about experience.
- 40 questions; question-level variance dominates. More questions would tighten CIs.
- Domain of each expert unknown; cannot test in-domain vs out-of-domain expert accuracy. Question for data owner.
- Brier not decomposed into calibration and resolution; supplementary analysis recommended.
