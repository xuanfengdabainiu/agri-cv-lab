suppressPackageStartupMessages(library(rrBLUP))

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: Rscript run_brix_2021_to_2022.R <data-root> <output-dir> [repeats] [seed]")
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
  "BIProject_LongPhenoType_ByYear.csv"
)
geno_path <- file.path(
  data_root,
  "genotype",
  "BIProject_compiled_variants_v2_Dosage_minDepth64_maxMiss.05_minMinor250.csv"
)

pheno <- read.csv(pheno_path, check.names = FALSE)
geno <- read.csv(geno_path, check.names = FALSE)

# Match the population filter used by the author before separating years.
pheno <- pheno[pheno$ORUSPopulationNumbers > 756, ]
train_2021 <- pheno[
  pheno$year == 2021 & !is.na(pheno$Brix),
  c("germplasmName", "Brix")
]
test_2022 <- pheno[
  pheno$year == 2022 & !is.na(pheno$Brix),
  c("germplasmName", "Brix")
]
train_2021 <- train_2021[!duplicated(train_2021$germplasmName), ]
test_2022 <- test_2022[!duplicated(test_2022$germplasmName), ]

metadata_columns <- c("Marker", "Chrom", "Position", "REF", "ALT")
genotype_ids <- setdiff(names(geno), metadata_columns)

# Explicit ID matching avoids the row-order ambiguity in the upstream script.
common_ids <- Reduce(
  intersect,
  list(train_2021$germplasmName, test_2022$germplasmName, genotype_ids)
)
sample_ids <- genotype_ids[genotype_ids %in% common_ids]

if (length(sample_ids) < 20) {
  stop("Too few matched 2021/2022 samples: ", length(sample_ids))
}

train_2021 <- train_2021[match(sample_ids, train_2021$germplasmName), ]
test_2022 <- test_2022[match(sample_ids, test_2022$germplasmName), ]
stopifnot(identical(train_2021$germplasmName, test_2022$germplasmName))

dosage <- as.matrix(geno[, sample_ids, drop = FALSE])
storage.mode(dosage) <- "numeric"
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
  test_size <- max(1L, round(0.2 * nrow(train_2021)))
  held_out_ids <- sample(sample_ids, size = test_size, replace = FALSE)

  model_data <- data.frame(
    germplasmName = sample_ids,
    Brix = train_2021$Brix
  )
  model_data$Brix[model_data$germplasmName %in% held_out_ids] <- NA_real_

  fit <- kin.blup(
    data = model_data,
    geno = "germplasmName",
    pheno = "Brix",
    K = kinship,
    PEV = TRUE
  )

  predicted <- fit$pred[held_out_ids]
  measured <- test_2022$Brix[match(held_out_ids, test_2022$germplasmName)]
  pearson <- cor(measured, predicted, use = "complete.obs", method = "pearson")
  spearman <- cor(measured, predicted, use = "complete.obs", method = "spearman")
  mse <- mean((predicted - measured)^2, na.rm = TRUE)
  heritability <- fit$Vg / (fit$Vg + fit$Ve)

  results[[run_index]] <- data.frame(
    Run = run_index,
    Seed = seed,
    TrainN = nrow(train_2021) - test_size,
    TestN = test_size,
    PredictiveAbility = pearson,
    Spearman = spearman,
    MSE = mse,
    Vg = fit$Vg,
    Ve = fit$Ve,
    Heritability = heritability
  )
  predictions[[run_index]] <- data.frame(
    Run = run_index,
    germplasmName = held_out_ids,
    Brix2021 = train_2021$Brix[match(held_out_ids, train_2021$germplasmName)],
    Brix2022 = measured,
    PredictedFrom2021 = predicted
  )
}

results <- do.call(rbind, results)
predictions <- do.call(rbind, predictions)
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
write.csv(results, file.path(output_dir, "brix-2021-to-2022-metrics.csv"), row.names = FALSE)
write.csv(predictions, file.path(output_dir, "brix-2021-to-2022-predictions.csv"), row.names = FALSE)

cat("Matched samples:", nrow(train_2021), "\n")
cat("Markers:", ncol(marker_matrix), "\n")
cat("Mean predictive ability:", mean(results$PredictiveAbility), "\n")
