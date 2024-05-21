# =========================================================================== #
#'
label_dotplot <- function(data, val, groups, breaks = "Sturges") {
    df <- data
    if (nrow(df) == 1) {
        # For a single observation, define breaks around the value
        single_val <- df[[val]]
        breaks = c(single_val - 1, single_val, single_val + 1)
    }
    
    # Create histogram, now safe for single observation
    d_hist <- hist(df[[val]], plot = FALSE, breaks = breaks)
    
    # If breaks have only one interval, force at least one bin
    if (length(d_hist$counts) == 0) {
        d_hist$counts <- 1
        d_hist$mids <- df[[val]]
    }
    
    df$x_bin <- cut(df[[val]], breaks = d_hist$breaks, labels = FALSE, include.lowest = TRUE)
    df$x_mid <- d_hist$mids[df$x_bin]
    df$y <- 1
    
    # Group by the specified groups and 'x_bin', then compute the cumulative sum 'y'
    df <- df %>% group_by(across(all_of(c(groups, "x_bin")))) %>%
        mutate(y = cumsum(y)) %>%
        ungroup()  # Ungroup to avoid accidental grouping effects later

    return(df)
}
# =========================================================================== #