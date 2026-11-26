args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: Rscript audit_author_3year_design.R <design-csv> <output-csv>")
}

design_path <- normalizePath(args[[1]], mustWork = TRUE)
output_path <- args[[2]]
design <- read.csv(design_path, check.names = FALSE)

required <- c(
  "germplasmName",
  "SetAssignment",
  "PhenotypeFedToModel",
  "year_fixedEffect"
)
if (!all(required %in% names(design))) {
  stop("Author design matrix is missing required columns")
}

test_rows <- design[design$SetAssignment == "Test", ]
train_rows <- design[design$SetAssignment == "Train", ]
test_ids <- unique(test_rows$germplasmName)

has_other_train_record <- vapply(
  test_ids,
  function(id) any(train_rows$germplasmName == id),
  logical(1)
)
has_2022_value_in_train <- vapply(
  test_ids,
  function(id) {
    any(
      train_rows$germplasmName == id &
        train_rows$year_fixedEffect == 2022 &
        !is.na(train_rows$PhenotypeFedToModel)
    )
  },
  logical(1)
)

summary_table <- data.frame(
  Metric = c(
    "total_rows",
    "unique_genotypes",
    "test_rows",
    "test_unique_genotypes",
    "test_rows_2020",
    "test_rows_2021",
    "test_rows_2022",
    "test_ids_with_other_training_record",
    "test_ids_with_2022_value_still_in_training"
  ),
  Value = c(
    nrow(design),
    length(unique(design$germplasmName)),
    nrow(test_rows),
    length(test_ids),
    sum(test_rows$year_fixedEffect == 2020),
    sum(test_rows$year_fixedEffect == 2021),
    sum(test_rows$year_fixedEffect == 2022),
    sum(has_other_train_record),
    sum(has_2022_value_in_train)
  )
)

dir.create(dirname(output_path), recursive = TRUE, showWarnings = FALSE)
write.csv(summary_table, output_path, row.names = FALSE)
print(summary_table, row.names = FALSE)
