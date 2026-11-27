suppressPackageStartupMessages(library(rrBLUP))

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 6) {
  stop(paste(
    "Usage: Rscript run_trait_gblup.R <data-root> <output-dir>",
    "<long-trait> <2022-trait> <trait-slug>",
    "<within-2022|cross-year|3year-fixed|3year-average> [repeats] [seed]"
  ))
}

data_root <- normalizePath(args[[1]], mustWork = TRUE)
output_dir <- args[[2]]
long_trait <- args[[3]]
trait_2022 <- args[[4]]
trait_slug <- args[[5]]
mode <- args[[6]]
repeats <- if (length(args) >= 7) as.integer(args[[7]]) else 10L
seed <- if (length(args) >= 8) as.integer(args[[8]]) else 42L

valid_modes <- c("within-2022", "cross-year", "3year-fixed", "3year-average")
if (!mode %in% valid_modes) stop("Unsupported mode: ", mode)
if (is.na(repeats) || repeats < 1) stop("repeats must be a positive integer")
if (is.na(seed)) stop("seed must be an integer")

short_path <- file.path(
  data_root,
  "phenotype",
  "BIProject_2022Pheno_WithParentsandNoOutliers.csv"
)
long_path <- file.path(
  data_root,
  "phenotype",
  "BIProject_LongPhenoType_ByYear.csv"
)
geno_path <- file.path(
  data_root,
  "genotype",
  "BIProject_compiled_variants_v2_Dosage_minDepth64_maxMiss.05_minMinor250.csv"
)

short_pheno <- read.csv(short_path, check.names = FALSE)
long_pheno <- read.csv(long_path, check.names = FALSE)
geno <- read.csv(geno_path, check.names = FALSE)

if (!trait_2022 %in% names(short_pheno)) {
  stop("Missing 2022 trait column: ", trait_2022)
}
if (!long_trait %in% names(long_pheno)) {
  stop("Missing long trait column: ", long_trait)
}

metadata_columns <- c("Marker", "Chrom", "Position", "REF", "ALT")
genotype_ids <- setdiff(names(geno), metadata_columns)

short_pheno <- short_pheno[
  short_pheno$ORUSPopulationNumbers > 756,
]
long_pheno <- long_pheno[
  long_pheno$ORUSPopulationNumbers > 756 &
    long_pheno$year %in% c(2020, 2021, 2022),
]

fixed_effect <- NULL
training_lookup <- NULL

if (mode == "within-2022") {
  phenotype <- short_pheno[
    !is.na(short_pheno[[trait_2022]]),
    c("germplasmName", trait_2022)
  ]
  phenotype <- phenotype[!duplicated(phenotype$germplasmName), ]
  names(phenotype)[2] <- "TraitValue"
  sample_ids <- genotype_ids[genotype_ids %in% phenotype$germplasmName]
  phenotype <- phenotype[match(sample_ids, phenotype$germplasmName), ]
  model_ids <- sample_ids
  evaluation_ids <- sample_ids
  evaluation_values <- setNames(phenotype$TraitValue, phenotype$germplasmName)
  training_lookup <- evaluation_values
  base_model_data <- phenotype
}

if (mode == "cross-year") {
  train_data <- long_pheno[
    long_pheno$year == 2021 & !is.na(long_pheno[[long_trait]]),
    c("germplasmName", long_trait)
  ]
  test_data <- long_pheno[
    long_pheno$year == 2022 & !is.na(long_pheno[[long_trait]]),
    c("germplasmName", long_trait)
  ]
  train_data <- train_data[!duplicated(train_data$germplasmName), ]
  test_data <- test_data[!duplicated(test_data$germplasmName), ]
  common_ids <- Reduce(
    intersect,
    list(train_data$germplasmName, test_data$germplasmName, genotype_ids)
  )
  sample_ids <- genotype_ids[genotype_ids %in% common_ids]
  train_data <- train_data[match(sample_ids, train_data$germplasmName), ]
  test_data <- test_data[match(sample_ids, test_data$germplasmName), ]
  stopifnot(identical(train_data$germplasmName, test_data$germplasmName))
  base_model_data <- data.frame(
    germplasmName = sample_ids,
    TraitValue = train_data[[long_trait]]
  )
  model_ids <- sample_ids
  evaluation_ids <- sample_ids
  evaluation_values <- setNames(test_data[[long_trait]], sample_ids)
  training_lookup <- setNames(train_data[[long_trait]], sample_ids)
}

if (mode == "3year-fixed") {
  phenotype <- long_pheno[
    !is.na(long_pheno[[long_trait]]) &
      long_pheno$germplasmName %in% genotype_ids,
    c("germplasmName", long_trait, "year")
  ]
  phenotype <- phenotype[!duplicated(phenotype[, c("germplasmName", "year")]), ]
  names(phenotype)[2] <- "TraitValue"
  phenotype$year <- factor(phenotype$year, levels = c(2020, 2021, 2022))
  evaluation <- phenotype[phenotype$year == 2022, c("germplasmName", "TraitValue")]
  evaluation <- evaluation[!duplicated(evaluation$germplasmName), ]
  model_ids <- genotype_ids[genotype_ids %in% unique(phenotype$germplasmName)]
  evaluation_ids <- model_ids[model_ids %in% evaluation$germplasmName]
  evaluation <- evaluation[match(evaluation_ids, evaluation$germplasmName), ]
  evaluation_values <- setNames(evaluation$TraitValue, evaluation_ids)
  base_model_data <- phenotype
  fixed_effect <- "year"
}

if (mode == "3year-average") {
  phenotype <- long_pheno[
    !is.na(long_pheno[[long_trait]]) &
      long_pheno$germplasmName %in% genotype_ids,
    c("germplasmName", long_trait, "year")
  ]
  phenotype <- phenotype[!duplicated(phenotype[, c("germplasmName", "year")]), ]
  mean_trait <- aggregate(
    phenotype[[long_trait]],
    by = list(germplasmName = phenotype$germplasmName),
    FUN = mean
  )
  names(mean_trait)[2] <- "TraitValue"
  model_ids <- genotype_ids[genotype_ids %in% mean_trait$germplasmName]
  mean_trait <- mean_trait[match(model_ids, mean_trait$germplasmName), ]
  evaluation_ids <- model_ids
  evaluation_values <- setNames(mean_trait$TraitValue, model_ids)
  training_lookup <- evaluation_values
  base_model_data <- mean_trait
}

if (length(evaluation_ids) < 20) {
  stop("Too few evaluation samples: ", length(evaluation_ids))
}

dosage <- as.matrix(geno[, model_ids, drop = FALSE])
storage.mode(dosage) <- "numeric"
dosage[dosage == 0] <- -1
dosage[dosage %in% c(1, 2, 3)] <- 0
dosage[dosage == 4] <- 1
marker_matrix <- t(dosage)

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
  test_size <- max(1L, round(0.2 * length(evaluation_ids)))
  held_out_ids <- sample(evaluation_ids, size = test_size, replace = FALSE)
  model_data <- base_model_data

  if (mode == "3year-fixed") {
    held_out_rows <-
      model_data$year == 2022 & model_data$germplasmName %in% held_out_ids
  } else {
    held_out_rows <- model_data$germplasmName %in% held_out_ids
  }
  model_data$TraitValue[held_out_rows] <- NA_real_

  fit_args <- list(
    data = model_data,
    geno = "germplasmName",
    pheno = "TraitValue",
    K = kinship,
    PEV = TRUE
  )
  if (!is.null(fixed_effect)) fit_args$fixed <- fixed_effect
  fit <- do.call(kin.blup, fit_args)

  predicted <- fit$pred[held_out_ids]
  measured <- evaluation_values[held_out_ids]
  pearson <- cor(measured, predicted, use = "complete.obs", method = "pearson")
  spearman <- cor(measured, predicted, use = "complete.obs", method = "spearman")
  mse <- mean((predicted - measured)^2, na.rm = TRUE)
  heritability <- fit$Vg / (fit$Vg + fit$Ve)

  results[[run_index]] <- data.frame(
    Run = run_index,
    Trait = long_trait,
    Mode = mode,
    Seed = seed,
    ModelGenotypes = length(model_ids),
    TrainingRecords = sum(!is.na(model_data$TraitValue)),
    EvaluationN = length(evaluation_ids),
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
    TrainingValue = if (is.null(training_lookup)) NA_real_ else training_lookup[held_out_ids],
    ObservedValue = measured,
    PredictedValue = predicted
  )
  assignments[[run_index]] <- data.frame(
    Run = run_index,
    germplasmName = evaluation_ids,
    SetAssignment = ifelse(evaluation_ids %in% held_out_ids, "Test", "Train")
  )
}

prefix <- paste(trait_slug, mode, sep = "-")
results <- do.call(rbind, results)
predictions <- do.call(rbind, predictions)
assignments <- do.call(rbind, assignments)
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
write.csv(results, file.path(output_dir, paste0(prefix, "-metrics.csv")), row.names = FALSE)
write.csv(predictions, file.path(output_dir, paste0(prefix, "-predictions.csv")), row.names = FALSE)
write.csv(assignments, file.path(output_dir, paste0(prefix, "-assignments.csv")), row.names = FALSE)

cat("Trait:", long_trait, "\n")
cat("Mode:", mode, "\n")
cat("Model genotypes:", length(model_ids), "\n")
cat("Evaluation samples:", length(evaluation_ids), "\n")
cat("Markers:", ncol(marker_matrix), "\n")
cat("Mean predictive ability:", mean(results$PredictiveAbility), "\n")
