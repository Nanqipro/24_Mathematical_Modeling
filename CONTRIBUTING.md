# Contributing

Contributions that improve reproducibility, documentation, tests, and data dictionaries are welcome.

## Before opening a pull request

1. Do not commit raw competition video, certificates, participant identifiers, database credentials, or machine-local paths.
2. Keep generated outputs under `outputs/` unless they are small, reviewed evidence intended for `results/`.
3. Preserve third-party license and attribution files.
4. Run:

   ```bash
   python -m compileall scripts Vehicle-tracking-main/application/main
   python scripts/evaluate_predictions.py
   python scripts/generate_readme_assets.py
   ```

5. Explain any change to formulas, units, filtering, random seeds, or evaluation splits.

For model or metric changes, include the command used and enough provenance to reproduce the result.
