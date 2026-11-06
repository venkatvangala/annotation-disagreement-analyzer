# Annotation Disagreement Analyzer

SQL + Python analysis of annotator disagreement and rater quality on the
GoEmotions dataset (Reddit comments labeled with 28 emotion categories).

## Question
Where do human annotators disagree, and which raters are driving low
agreement? This is the kind of check a data quality team runs before
trusting labels for model training or evaluation.

## Data
GoEmotions raw annotations (Google Research, Demszky et al., 2020):
one row per rater per comment. I sampled 3,000 comments (random seed 1)
and kept every rater's labels for each: 10,931 annotations from 80 raters.

## Method
1. `src/load_data.py` downloads the raw files and samples comments.
2. `src/load_to_sqlite.py` loads the sample into a SQLite database.
3. SQL queries (`sql/`) find the most disputed comments and compare
   raters' labeling habits.
4. `src/rater_agreement.py` scores each rater by the average overlap
   (Jaccard similarity) between their labels and the other raters' labels
   on the same comments.
5. `src/make_charts.py` produces the charts below.

## Findings
- Overall agreement is low: **0.28** on a 0-1 scale. On average, two raters
  share about a quarter of their labels on the same comment.
- **Over-labelers.** Rater 31 chose 2.92 labels per comment (26 annotations)
  and rater 79 chose 1.88 (33 annotations). Their agreement was 0.13 and
  0.11, among the lowest.
- **A second type of low-agreement rater.** Rater 11 chose about 1 label per
  comment (1.03, over 95 annotations) yet agreed with others only 0.12 of
  the time. My hypothesis is that this rater reads the emotion categories
  differently, not that they label too much. I have not tested this yet.
- Raters with many annotations tend to sit at higher agreement. This could
  reflect experience or just less noise in larger samples.

![Rater behavior vs agreement](images/rater_scatter.png)
![Distribution of rater agreement](images/agreement_hist.png)

## Limitations
- The score penalizes raters who choose many labels: if one rater gives 1
  label and another gives 3, the best possible overlap is 0.33. Part of the
  low score for raters 31 and 79 comes from the measure itself.
- Raters with fewer than about 30 annotations give noisy scores.
- My first disagreement ranking (counting emotions that raters split on)
  was inflated by heavy labelers, which is why I added the per-rater view.

## How to run
```
pip install -r requirements.txt
python src/load_data.py
python src/load_to_sqlite.py
python src/run_sql.py sql/02_disagreement.sql
python src/rater_agreement.py
python src/make_charts.py
```

## Next steps
- Look at why raters split on the most disputed comments (sarcasm, missing
  context, overlapping categories).
- Try a measure that is not biased by label count.