suppressPackageStartupMessages(library(rrBLUP))

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: Rscript run_brix_3year_average.R <data-root> <output-dir> [repeats] [seed]")
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

mean_brix <- aggregate(Brix ~ germplasmName, data = pheno, FUN = mean)
names(mean_brix)[names(mean_brix) == "Brix"] <- "MeanBrix"
year_counts <- aggregate(year ~ germplasmName, data = pheno, FUN = length)
names(year_counts)[names(year_counts) == "year"] <- "YearsMeasured"
mean_brix <- merge(mean_brix, year_counts, by = "germplasmName", sort = FALSE)

sample_ids <- genotype_ids[genotype_ids %in% mean_brix$germplasmName]
mean_brix <- mean_brix[match(sample_ids, mean_brix$germplasmName), ]
if (length(sample_ids) < 20) {
  stop("Too few averaged Brix samples: ", length(sample_ids))
}

dosage <- as.matrix(geno[, sample_ids, drop = FALSE])
storage.mode(dosage) <- "numeric"
dosage[dosage == 0] <- -1
dosage[dosage %in% c(1, 2, 3)] <- 0
dosage[dosage == 4] <- 1
marker_matrix <- t(dosage)

# EM fell back to mean imputation in every earlier run because rows are linearly dependent.
kinship <- A.mat(
  X = marker_matrix,
  impute.method = "mean",
  max.missing = 0.8,
  return.imputed = FALSE,
  n.core = min(4L, parallel::detectCores())
)

set.seed(seed)
results <- vector("list", repeats)
predictions <- vector("list", repeats)
assignments <- vector("list", repeats)

for (run_index in seq_len(repeats)) {
  test_size <- max(1L, round(0.2 * nrow(mean_brix)))
  held_out_ids <- sample(sample_ids, size = test_size, replace = FALSE)

  model_data <- mean_brix[, c("germplasmName", "MeanBrix")]
  model_data$MeanBrix[model_data$germplasmName %in% held_out_ids] <- NA_real_

  fit <- kin.blup(
    data = model_data,
    geno = "germplasmName",
    pheno = "MeanBrix",
    K = kinship,
    PEV = TRUE
  )

  predicted <- fit$pred[held_out_ids]
  measured <- mean_brix$MeanBrix[
    match(held_out_ids, mean_brix$germplasmName)
  ]
  pearson <- cor(measured, predicted, use = "complete.obs", method = "pearson")
  spearman <- cor(measured, predicted, use = "complete.obs", method = "spearman")
  mse <- mean((predicted - measured)^2, na.rm = TRUE)
  heritability <- fit$Vg / (fit$Vg + fit$Ve)

  results[[run_index]] <- data.frame(
    Run = run_index,
    Seed = seed,
    TrainN = nrow(mean_brix) - test_size,
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
    YearsMeasured = mean_brix$YearsMeasured[
      match(held_out_ids, mean_brix$germplasmName)
    ],
    MeanBrix = measured,
    PredictedMeanBrix = predicted
  )
  assignments[[run_index]] <- data.frame(
    Run = run_index,
    germplasmName = sample_ids,
    SetAssignment = ifelse(sample_ids %in% held_out_ids, "Test", "Train")
  )
}

results <- do.call(rbind, results)
predictions <- do.call(rbind, predictions)
assignments <- do.call(rbind, assignments)
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
write.csv(results, file.path(output_dir, "brix-3year-average-metrics.csv"), row.names = FALSE)
write.csv(predictions, file.path(output_dir, "brix-3year-average-predictions.csv"), row.names = FALSE)
write.csv(assignments, file.path(output_dir, "brix-3year-average-assignments.csv"), row.names = FALSE)

cat("Phenotype records:", nrow(pheno), "\n")
cat("Averaged genotypes:", nrow(mean_brix), "\n")
cat("Markers:", ncol(marker_matrix), "\n")
cat("Mean predictive ability:", mean(results$PredictiveAbility), "\n")
