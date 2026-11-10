# SEAStheMoment — STAI-X Challenge 2026

Predictive model for nonfatal overdose emergency department visit rates across US jurisdictions, stratified by drug category. STAI-X Challenge 2026 competition submission.

## Task

**Regression problem**: Predict `rate_per_10000_ed_visits` for each combination of:
- 6 validation time periods
- 51 US jurisdictions (states + DC)
- 3 drug categories (all_drugs, all_opioids, all_stimulants)
- Total: 918 prediction rows

**Metric**: Mean Absolute Error (MAE)

## Data

### Training Data
- `train/dose_sys_train.csv` — labeled overdose rates (target)
- `train/covariates.csv` — panel of state-level features (time × jurisdiction)
- `train/images/mat_density/` — optional 256×256 PNG heatmaps of MAT clinic density per state-period

### Features
- Numeric: unemployment rate, labor force size, temperature, precipitation
- Text: state Department of Health press releases (TF-IDF encoded)
- Search trends: Google Trends indices for "overdose", "fentanyl", "naloxone", "opioid", "methamphetamine"
- Temporal: period identifiers (ordered by calendar)

### Validation Data
- `val/covariates.csv` — same features as train, no target (hidden)
- `val/images/mat_density/` — corresponding MAT density images

## Architecture

**Mixture of Experts ensemble** with 4 specialized expert pipelines + orchestrator:

1. **Feature engineering**: Median imputation, log transforms, frequency encoding, TF-IDF + SVD for text, datetime decomposition, temporal lags (past-only)
2. **Per-category training**: Separate model pipeline for each drug category
3. **Ensemble models**: LightGBM, XGBoost, CatBoost with 5-fold cross-validation
4. **Aggregation**: Per-group out-of-fold predictions averaged across models
5. **Fallback**: Baseline (group/global median) for any missing or invalid prediction

## Files

- `SEAStheMoment_STAIX26_submission.ipynb` — Kaggle pipeline for original overdose domain (hardcoded features and structure)
- `experts/` — Pretrained model artifacts (mpnet/EfficientNet pretrained weights from Kaggle)
- `CLAUDE.md` — Domain-agnostic Award B autonomous data-analysis agent specification
- `requirements.txt` — All package dependencies (LightGBM, XGBoost, CatBoost, scikit-learn, pandas, numpy, SciPy)

## Key Constraints (Competition Rules)

- **CPU-only**: No GPU acceleration
- **Local data only**: No external downloads (no pretrained models beyond provided files)
- **Wall-clock**: ≤ 2 hours execution time
- **Token budget**: ≤ 1,000,000 tokens for agent reasoning
- **Determinism**: Fixed `SEED = 42` throughout; results must reproduce
- **Schema compliance**: Exact submission template format with zero NaN values

## Running

```bash
pip install -q lightgbm xgboost catboost scikit-learn reportlab matplotlib pandas numpy scipy
python SEAStheMoment_STAIX26_submission.ipynb
```

Output: `submission.csv` (918 rows, validated against template schema)

## Approach

1. Load train/val data and sample submission template
2. Write baseline (per-category median) before any modeling
3. Feature engineering: imputation, encoding, TF-IDF, lags, datetime features
4. Train LightGBM → XGBoost → CatBoost per category with GroupKFold CV
5. Ensemble out-of-fold predictions; merge with test period data
6. Fallback missing rows to group baseline
7. Validate against template schema (row count, columns, dtype, zero NaN)
8. Generate report.pdf with EDA, CV results, and feature importance

