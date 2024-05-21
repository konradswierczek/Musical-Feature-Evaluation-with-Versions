# =========================================================================== #
#' @examples
#' # Classic usage in original experiment.
#' relative_variability(df, "pieceID", c("tool", "algo", "feature"), "val")
relative_variability <- function(
  df,
  version_var,
  grouping_vars,
  val_var,
  variability_metric = sd
) {
  # Version-wise variability
  version_var_df <- df %>%
    group_by(
      !!!syms(
        c(
          grouping_vars,
          version_var
        )
      )
    ) %>%
    summarize(
      var_version = variability_metric(
        !!sym(val_var),
        na.rm = TRUE
      )
    )

  # Total variability
  total_var_df <- df %>%
    group_by(!!!syms(grouping_vars)) %>%
    summarize(
      var_total = variability_metric(
        !!sym(val_var),
        na.rm = TRUE
      )
    )

  # Join data frames
  new_df <- left_join(
    version_var_df,
    total_var_df,
    by = grouping_vars
  ) %>%
    mutate(
      ratio = var_version / var_total
    ) %>%
    ungroup()

  return(new_df)
}

# =========================================================================== #