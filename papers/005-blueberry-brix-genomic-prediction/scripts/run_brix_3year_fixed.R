suppressPackageStartupMessages(library(rrBLUP))

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: Rscript run_brix_3year_fixed.R <data-root> <output-dir> [repeats] [seed]")
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

metadata_columns <- c("Marker", "Chrom", "Position", "REF", "ALT")
genotype_ids <- setdiff(names(geno), metadata_columns)

pheno <- pheno[
  pheno$ORUSPopulationNumbers > 756 &
    pheno$year %in% c(2020, 2021, 2022) &
    !is.na(pheno$Brix) &
    pheno$germplasmName %in% genotype_ids,
  c("germplasmName", "Brix", "year")
]
pheno <- pheno[!duplicated(pheno[, c("germplasmName", "year")]), ]
pheno$year <- factor(pheno$year, levels = c(2020, 2021, 2022))

evaluation_2022 <- pheno[pheno$year == 2022, c("germplasmName", "Brix")]
evaluation_2022 <- evaluation_2022[!duplicated(evaluation_2022$germplasmName), ]
model_ids <- genotype_ids[genotype_ids %in% unique(pheno$germplasmName)]
evaluation_ids <- model_ids[model_ids %in% evaluation_2022$germplasmName]

if (length(evaluation_ids) < 20) {
  stop("Too few 2022 evaluation samples: ", length(evaluation_ids))
}

evaluation_2022 <- evaluation_2022[
  match(evaluation_ids, evaluation_2022$germplasmName),
]

dosage <- as.matrix(geno[, model_ids, drop = FALSE])
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

wide_brix <- reshape(
  pheno,
  idvar = "germplasmName",
  timevar = "year",
  direction = "wide"
)

set.seed(seed)
results <- vector("list", repeats)
predictions <- vector("list", repeats)
assignments <- vector("list", repeats)

for (run_index in seq_len(repeats)) {
  test_size <- max(1L, round(0.2 * length(evaluation_ids)))
  held_out_ids <- sample(evaluation_ids, size = test_size, replace = FALSE)

  model_data <- pheno
  held_out_2022 <-
    model_data$year == 2022 & model_data$germplasmName %in% held_out_ids
  model_data$Brix[held_out_2022] <- NA_real_

  fit <- kin.blup(
    data = model_data,
    geno = "germplasmName",
    pheno = "Brix",
    fixed = "year",
    K = kinship,
    PEV = TRUE
  )

  predicted <- fit$pred[held_out_ids]
  measured <- evaluation_2022$Brix[
    match(held_out_ids, evaluation_2022$germplasmName)
  ]
  pearson <- cor(measured, predicted, use = "complete.obs", method = "pearson")
  spearman <- cor(measured, predicted, use = "complete.obs", method = "spearman")
  mse <- mean((predicted - measured)^2, na.rm = TRUE)
  heritability <- fit$Vg / (fit$Vg + fit$Ve)

  results[[run_index]] <- data.frame(
    Run = run_index,
    Seed = seed,
    TrainingRecords = sum(!is.na(model_data$Brix)),
    EvaluationN = length(evaluation_ids),
    TestN = test_size,
    PredictiveAbility = pearson,
    Spearman = spearman,
    MSE = mse,
    Vg = fit$Vg,
    Ve = fit$Ve,
    Heritability = heritability
  )

  history_rows <- wide_brix[
    match(held_out_ids, wide_brix$germplasmName),
  ]
  predictions[[run_index]] <- data.frame(
    Run = run_index,
    germplasmName = held_out_ids,
    Brix2020 = history_rows$Brix.2020,
    Brix2021 = history_rows$Brix.2021,
    Brix2022 = measured,
    PredictedBrix = predicted
  )

  assignments[[run_index]] <- data.frame(
    Run = run_index,
    germplasmName = evaluation_ids,
    SetAssignment = ifelse(evaluation_ids %in% held_out_ids, "Test", "Train")
  )
}

results <- do.call(rbind, results)
predictions <- do.call(rbind, predictions)
assignments <- do.call(rbind, assignments)
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
write.csv(results, file.path(output_dir, "brix-3year-fixed-metrics.csv"), row.names = FALSE)
write.csv(predictions, file.path(output_dir, "brix-3year-fixed-predictions.csv"), row.names = FALSE)
write.csv(assignments, file.path(output_dir, "brix-3year-fixed-assignments.csv"), row.names = FALSE)

cat("Phenotype records:", nrow(pheno), "\n")
cat("Model genotypes:", length(model_ids), "\n")
cat("2022 evaluation samples:", length(evaluation_ids), "\n")
cat("Markers:", ncol(marker_matrix), "\n")
cat("Mean predictive ability:", mean(results$PredictiveAbility), "\n")
