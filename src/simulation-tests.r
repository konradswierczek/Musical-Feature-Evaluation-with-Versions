permutation_test <- function(
  df,
  groups,
  vals,
  n = 1000,
  type = "two-tailed"
) {
  if (!groups %in% names(df)) {
    stop("Group variable not found in the dataframe.")
  }
  if (length(unique(df[[groups]])) != 2) {
    stop("Group variable must have exactly two levels.")
  }
  observed_statistic <- diff(by(df[[vals]], df[[groups]], mean))
  permutations <- as.vector(replicate(n, diff(by(df[[vals]], sample(df[[groups]], size = dim(df)[1], FALSE), mean))))
  if (type == "one-tailed") {
    p_value <- sum(permutations > observed_statistic)/n
  }
  else if (type == "two-tailed") {
    p_value <- sum(
      abs(permutations) > abs(observed_statistic)) / n
  }
  confidence <- quantile(
    abs(permutations),
    c(
      0.025,
      0.975
    )
  )
  return(
    list(
      p_value,
      permutations,
      abs(observed_statistic),
      confidence
    )
  )
}

# =========================================================================== #
#'
pairwise_permutation_tests <- function(
  df,
  group,
  vals,
  n = 1000,
  type = "two_tailed"
) {
  get_subset <- function(df, col, pair) {
    return(df[df[[col]] %in% pair, , drop = FALSE])
  }

  # Generate all pairwise combinations of unique values in the "groups" column
  comparisons <- combn(unique(df[[group]]), 2)

  # Perform permutation test for each pairwise combination
  results <- apply(comparisons, 2, function(pair) {
    subset_data <- get_subset(df, group, pair)
    permutation_test(subset_data, group, vals)
  })

  return(
    tibble(
      group1 = comparisons[1, ],
      group2 = comparisons[2, ],
      p_value = sapply(results, function(x) x[[1]]),
      observed_statistic = sapply(results, function(x) x[[3]]),
      ci_low = sapply(results, function(x) x[[4]][1]),
      ci_high = sapply(results, function(x) x[[4]][2])
    )
  )
}

# =========================================================================== #