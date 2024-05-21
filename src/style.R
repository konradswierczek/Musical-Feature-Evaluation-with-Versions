# Set colours for nominal model.
mode_cols <- c(
  "Major" = "#f0373a",
  "Minor" = "#5269af",
  "No Nominal Mode" = "#7f857f"
)

# Set colours for extraction tools.
tool_cols <- c(
  "Essentia" = "#90253F",
  "Librosa" = "#FBBC86",
  "MIRtoolbox" = "#268234"
)

# Custom theme.
theme_maple <- function() {
  theme(
    panel.grid = element_blank(),
    panel.background = element_rect(
      fill = "white",
      color = NA
    ),
    panel.border = element_rect(
      fill = NA,
      color = "black",
      size = 1
    ),
strip.background = element_rect(fill = "white", color = "black", size = 1),
    strip.text = element_text(color = "black")
  )
}