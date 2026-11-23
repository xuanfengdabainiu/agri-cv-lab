suppressPackageStartupMessages(library(rrBLUP))

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: Rscript run_brix_gblup.R <data-root> <output-dir> [repeats] [seed]")
}

data_root <- normalizePath(args[[1]], mustWork = TRUE)
output_dir <- args[[2]]
repeats <- if (length(args) >= 3) as.integer(args[[3]]) else 10L
seed <- if (length(args) >= 4) as.integer(args[[4]]) else 42L

if (is.na(repeats) || repeats < 1) stop("repeats must be a positive integer")
if (is.na(seed)) stop("seed must be an integer")

pheno_path <- file.path(
  data_root,
  "phenotype",
  "BIProject_2022Pheno_WithParentsandNoOutliers.csv"
)
geno_path <- file.path(
  data_root,
  "genotype",
  "BIProject_compiled_variants_v2_Dosage_minDepth64_maxMiss.05_minMinor250.csv"
)

pheno <- read.csv(pheno_path, check.names = FALSE)
geno <- read.csv(geno_path, check.names = FALSE)

# Match the author's population filter and use only samples with measured 2022 Brix.
pheno <- pheno[
  pheno$ORUSPopulationNumbers > 756 & !is.na(pheno$Brix_2022),
  c("germplasmName", "Brix_2022")
]
pheno <- pheno[!duplicated(pheno$germplasmName), ]

metadata_columns <- c("Marker", "Chrom", "Position", "REF", "ALT")
sample_columns <- setdiff(names(geno), metadata_columns)
sample_ids <- intersect(pheno$germplasmName, sample_columns)

if (length(sample_ids) < 20) {
  stop("Too few matched samples for train-test prediction: ", length(sample_ids))
}

pheno <- pheno[match(sample_ids, pheno$germplasmName), ]
dosage <- as.matrix(geno[, sample_ids, drop = FALSE])
storage.mode(dosage) <- "numeric"

# Reproduce the author's diploidized coding: 0 -> -1, 1/2/3 -> 0, 4 -> 1.
dosage[dosage == 0] <- -1
dosage[dosage %in% c(1, 2, 3)] <- 0
dosage[dosage == 4] <- 1
marker_matrix <- t(dosage)

kinship <- A.mat(
  X = marker_matrix,
  impute.method = "EM",
  max.missing = 0.8,
  return.imputed = FALSE,
  n.core = min(4L, parallel::detectCores())
)

set.seed(seed)
results <- vector("list", repeats)
predictions <- vector("list", repeats)

for (run_index in seq_len(repeats)) {
  test_size <- max(1L, floor(0.2 * nrow(pheno)))
  test_ids <- sample(pheno$germplasmName, size = test_size, replace = FALSE)

  model_data <- pheno
  observed <- model_data$Brix_2022
  model_data$Brix_2022[model_data$germplasmName %in% test_ids] <- NA_real_

  fit <- kin.blup(
    data = model_data,
    geno = "germplasmName",
    pheno = "Brix_2022",
    K = kinship,
    PEV = TRUE
  )

  predicted <- fit$pred[test_ids]
  measured <- observed[match(test_ids, pheno$germplasmName)]
  predictive_ability <- cor(measured, predicted, use = "complete.obs")

  results[[run_index]] <- data.frame(
    Run = run_index,
    Seed = seed,
    TrainN = nrow(pheno) - test_size,
    TestN = test_size,
    PredictiveAbility = predictive_ability
  )
  predictions[[run_index]] <- data.frame(
    Run = run_index,
    germplasmName = test_ids,
    MeasuredBrix = measured,
    PredictedBrix = predicted
  )
}

results <- do.call(rbind, results)
predictions <- do.call(rbind, predictions)
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
write.csv(results, file.path(output_dir, "brix-gblup-metrics.csv"), row.names = FALSE)
write.csv(predictions, file.path(output_dir, "brix-gblup-predictions.csv"), row.names = FALSE)

cat("Matched samples:", nrow(pheno), "\n")
cat("Markers:", ncol(marker_matrix), "\n")
cat("Mean predictive ability:", mean(results$PredictiveAbility), "\n")
