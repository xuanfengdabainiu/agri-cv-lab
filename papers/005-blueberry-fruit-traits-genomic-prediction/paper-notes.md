# Paper Notes

## 1. One-Sentence Summary

The paper uses blueberry SNP data to predict fruit quality, plant architecture, bloom timing, and ripening traits.

## 2. Problem Solved

Measuring fruit quality and ripening traits requires mature plants, repeated field work, and post-harvest measurements. The paper tests whether DNA markers can predict these traits earlier in a breeding program.

## 3. Core Method / Workflow

```text
SNP genotype data + measured fruit or ripening trait
  -> genotype filtering and relationship matrix
  -> GBLUP genomic prediction
  -> predicted trait values
  -> correlation between predicted and measured values
```

- SNP: a single DNA position that differs among plants.
- Brix: soluble solids measured in fruit juice; commonly used as a sweetness proxy.
- GBLUP: a model that uses genome-wide similarity to predict a trait.

## 4. Experiment Setup

- Crop: northern highbush blueberry.
- Genotype source: a 3K DArTag marker panel processed into SNP calls.
- Completed trait phase: Brix.
- Completed trait phases: Brix, titratable acidity, pH, and Brix-to-acidity ratio.
- Completed trait phases include fruit mass.
- Next trait phase: plant height.
- Main paper split: training data from 2021, 2022, or combined years; evaluation against 2022 observations.
- Main metric: predictive ability, calculated as the correlation between observed and predicted values.
- Paper reference range for Brix predictive ability: approximately 0.46 to 0.64, depending on the training set.
- Reproduced 2022-only baseline: mean predictive ability 0.4024 across 10 fixed-seed splits, close to the paper's approximately 0.41 value for the 2022 training set.
- Reproduced 2021-to-2022 prediction after matching samples by ID: mean predictive ability 0.3327, close to the paper's approximately 0.35 value.
- Corrected three-year model with year fixed effect: predictive ability 0.4201 versus the paper's approximately 0.59; heritability 0.4927 versus approximately 0.49.
- Three-year averaged phenotype: predictive ability 0.4558 versus author public mean 0.4555 and paper rounded value 0.46; heritability 0.5073 versus approximately 0.51.
- Acidity phase: 2022-only 0.4613, cross-year 0.3749, ID-safe three-year fixed 0.5044, and three-year average 0.5462.
- pH phase: 2022-only 0.4568, cross-year 0.3809, ID-safe three-year fixed 0.4824, and three-year average 0.5596.
- Ratio phase: 2022-only 0.4634, cross-year 0.3713, ID-safe three-year fixed 0.4993, and three-year average 0.5725.
- Fruit-mass phase: 2022-only 0.5973, cross-year 0.5612, ID-safe three-year fixed 0.6317, and three-year average 0.6666.

## 5. Limitations

- Brix is a proxy and does not equal perceived sweetness by itself; acidity also affects taste.
- The public repository is about 5.3 GB and contains many old and intermediate files.
- The main R script contains a hard-coded author path and many analyses beyond Brix.
- The random seed is commented out, so the unmodified script does not guarantee identical train-test splits.
- The upstream cross-year code compares separately built yearly tables by row position; explicit ID matching is required to prevent different plants from being compared.
- The upstream three-year split samples phenotype rows across years. In the public first design matrix, 196 test-labelled plant IDs retain their 2022 target in training.
- The acidity design audit finds the same issue: 201 test-labelled plant IDs retain their 2022 acidity target in training.
- The pH design audit finds the same issue: 209 test-labelled plant IDs retain their 2022 pH target in training.
- The ratio design audit finds the same issue: 191 test-labelled plant IDs retain their 2022 ratio target in training.
- The fruit-mass design audit finds the same issue: 197 test-labelled plant IDs retain their 2022 fruit-mass target in training.
- Results mainly apply to the studied breeding population.

## 6. What I Can Change

- Generalize the clean Brix scripts into a reusable per-trait prediction pipeline.
- Fix the random seed and record every split.
- Compare GBLUP with a simple machine-learning baseline later.
- Reproduce plant height with the same saved-split discipline.
