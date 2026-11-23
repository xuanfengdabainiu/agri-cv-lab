args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 2) {
  stop("Usage: Rscript inspect_data.R <data-root> <output-csv>")
}

data_root <- normalizePath(args[[1]], mustWork = TRUE)
output_csv <- args[[2]]

pheno_2022_path <- file.path(
  data_root,
  "phenotype",
  "BIProject_2022Pheno_WithParentsandNoOutliers.csv"
)
pheno_long_path <- file.path(
  data_root,
  "phenotype",
  "BIProject_LongPhenoType_ByYear.csv"
)
geno_path <- file.path(
  data_root,
  "genotype",
  "BIProject_compiled_variants_v2_Dosage_minDepth64_maxMiss.05_minMinor250.csv"
)

required_files <- c(pheno_2022_path, pheno_long_path, geno_path)
missing_files <- required_files[!file.exists(required_files)]
if (length(missing_files) > 0) {
  stop("Missing required files: ", paste(missing_files, collapse = ", "))
}

pheno_2022 <- read.csv(pheno_2022_path, check.names = FALSE)
pheno_long <- read.csv(pheno_long_path, check.names = FALSE)
geno <- read.csv(geno_path, check.names = FALSE)

required_pheno_columns <- c("germplasmName", "Brix_2022")
if (!all(required_pheno_columns %in% names(pheno_2022))) {
  stop("2022 phenotype table is missing required columns")
}

required_geno_columns <- c("Marker", "Chrom", "Position", "REF", "ALT")
if (!all(required_geno_columns %in% names(geno))) {
  stop("Genotype table is missing required columns")
}

geno_samples <- setdiff(names(geno), required_geno_columns)
brix_rows <- !is.na(pheno_2022$Brix_2022)
brix_ids <- unique(pheno_2022$germplasmName[brix_rows])
overlap_ids <- intersect(brix_ids, geno_samples)

summary_table <- data.frame(
  Metric = c(
    "phenotype_2022_rows",
    "phenotype_long_rows",
    "brix_2022_nonmissing_rows",
    "brix_2022_unique_genotypes",
    "genotype_markers",
    "genotype_samples",
    "brix_genotype_overlap",
    "brix_min",
    "brix_mean",
    "brix_max"
  ),
  Value = c(
    nrow(pheno_2022),
    nrow(pheno_long),
    sum(brix_rows),
    length(brix_ids),
    nrow(geno),
    length(geno_samples),
    length(overlap_ids),
    min(pheno_2022$Brix_2022, na.rm = TRUE),
    mean(pheno_2022$Brix_2022, na.rm = TRUE),
    max(pheno_2022$Brix_2022, na.rm = TRUE)
  )
)

dir.create(dirname(output_csv), recursive = TRUE, showWarnings = FALSE)
write.csv(summary_table, output_csv, row.names = FALSE)
print(summary_table, row.names = FALSE)
