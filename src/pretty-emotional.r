# =========================================================================== #
# Constants
# TODO: Add offline option.
googlesheets4::gs4_auth(
  path = "etc/emotional-piano-project-132a154939e0.json"
)
pretty_url <- paste0(
  "https://docs.google.com/spreadsheets/d/",
  "1Cg8zY-U-bIwfFYjgLS8gJOtqqPnVbydphTGHrE87i6w/edit#gid=1518267623"
)
albumID_meta <- googlesheets4::read_sheet(
  pretty_url,
  sheet = "PrettyAlbumID"
)
setCode_meta <- googlesheets4::read_sheet(
  pretty_url,
  sheet = "PrettySetCode"
)
pieceID_meta <- googlesheets4::read_sheet(
  pretty_url,
  sheet = "PrettyPieceID"
)
performer_meta <- googlesheets4::read_sheet(
  pretty_url,
  sheet = "PrettyPerformer"
)
composer_meta <- googlesheets4::read_sheet(
  pretty_url,
  sheet = "PrettyComposer"
)

# =========================================================================== #
#' Retrieve metadata from sheet
#'
#' For a given Emotional Piano Project identifier, returns all associated
#' metadata as a list. See PrettyEmotional google sheet for full list of
#' identifiers and metadata available.
#'
#' @param type Identifier type. Must be one of the following: albumID, pieceID,
#' composer, setCode, performer.
#' @param values Value of identifier for lookup. Must be a string value of an
#' identifier in PrettyEmotional google sheet, or vector containing pieceID and
#' setCode in the case of PieceID lookups.
#'
#' @return Named list containing all associated metadata.
#'
#' @export
#'
#' @examples
#' # Get metadata for albumID "alkanMartin1989"
#' get_metadata("albumID", "alkanMartin1989")
get_metadata <- function(
  type,
  values
) {
  #'
  flatten <- function(x) {
    if (is.data.frame(x)) {
      unlist(
        lapply(
          x,
          flatten
        ),
        use.names = FALSE
      )
    } else if (is.list(x)) {
      unlist(
        lapply(
          x,
          flatten
        )
      )
    } else {
      x
    }
  }
  if (type == "pieceID") {
    if (!is.character(values) || length(values) != 2) {
      stop("'values' must be passed as a vector including pieceID and setCode.")
    } else {
      metadata <- pieceID_meta[complete.cases(pieceID_meta$pieceID,
                                              pieceID_meta$setCode) &
                                 pieceID_meta$pieceID == values[1] &
                                 pieceID_meta$setCode == values[2], ]
    }
  } else {
    metadata <- switch(
      type,
      albumID = albumID_meta,
      composer = composer_meta,
      performer = performer_meta,
      setCode = setCode_meta,
      stop(paste0("Invalid type. Must be one of: ",
                  "albumID, composer, pieceID, performer, setCode"))
    )
  }
  metadata <- metadata[metadata[[type]] == values[1], ]
  metadata <- lapply(as.list(metadata), flatten)
  return(metadata)
}

# =========================================================================== #
#' Get names of metadata parameters available for a given identifier.
#'
#'
#'
#' @param type
#'
#' @return
#'
#' @export
#'
#' @examples
#' # get albumID metadata parameter names.
#' get_metadata_params("albumID")
get_metadata_params <- function(type) {
  # TODO: Return a list, with brief descriptions of each piece of metadata
  metadata <- switch(
    type,
    albumID = albumID_meta,
    composer = composer_meta,
    performer = performer_meta,
    pieceID = pieceID_meta,
    setCode = setCode_meta,
    stop(paste0("Invalid type. Must be one of: ",
                "albumID, composer, pieceID, performer, setCode"))
  )
  return(colnames(metadata))
}

# =========================================================================== #
#' Generate human readable identifier labels.
#'
#' Generic function for generating human readable, custom format labels.
#' Generally not useful on it's own, intended to be used with get_metadata.
#' See wrapper functions below.
#'
#' @param metadata
#' @param format
#'
#' @return
#'
#' @examples
#' #
#' pretty_labeller()
pretty_labeller <- function(metadata, format) {
  #'
  replace_substrings <- function(input_string, dictionary) {
    modified_string <- input_string
    for (substring in regmatches(input_string,
                                 gregexpr("%(.*?)%", input_string))[[1]]) {
      modified_string <- gsub(substring,
                              dictionary[gsub("%", "", substring)][[1]],
                              modified_string)
    }
    return(modified_string)
  }
  formatted_info <- replace_substrings(format, metadata)
  return(formatted_info)
}

# =========================================================================== #
#' Use correct accidental labels.
#'
#' Replaces all instances of "b" and "#" with correct unicode characters for
#' musical accidentals (flat and sharp) in a string. Note that the use of
#' lower-case "b" instead of "B" to refer to key chroma will return a flat.
#'
#' @param tonic A string containing key information (e.g., "C Major")
#'
#' @return A string with unicode symbols for accidentals
#'
#' @export
#'
#' @examples
#' # Flat accidental.
#' pretty_accidental("Bb Major")
#' # Sharp accidental.
#' pretty_accidental("C# Major")
pretty_accidental <- function(tonic) {
  # TODO: Make smart detection for lower-case chroma "b".
  tonic <- as.character(tonic)
  tonic <- gsub("b", "\u266d", tonic)
  tonic <- gsub("#", "\u266f", tonic)
  return(tonic)
}

# =========================================================================== #
#' Convert albumID to human readable format.
#'
#' Wrapper function for pretty_labeller(get_metadata())
#'
#' @param albumID
#' @param format
#'
#' @return
#'
#' @export
#'
#' @examples
#' # Default behaviour.
#' pretty_albumID("alkanMartin1989")
#' # Specify a different format including initials of composer and year.
#' pretty_albumID("bachAshkenazy2006", format = "%pfn%, %ci% %year%")
pretty_albumID <- function(albumID, format = "%perf_fullname%, %year%") {
  metadata <- get_metadata("albumID", albumID)
  pretty <- pretty_labeller(metadata, format)
  return(pretty)
}

# =========================================================================== #
#' Convert setCode to human readable format.
#'
#' Wrapper function for pretty_labeller(get_metadata())
#'
pretty_setCode <- function(setCode, format = "%title%") {
  metadata <- get_metadata("setCode", setCode)
  pretty <- pretty_labeller(metadata, format)
  return(pretty)
}

# =========================================================================== #
#' Convert pieceID to human readable format.
#'
#' Wrapper function for pretty_labeller(get_metadata())
#'
pretty_pieceID <- function(pieceID, setCode, format = "%tonic% %mode%") {
  metadata <- get_metadata("pieceID", c(pieceID, setCode))
  pretty <- pretty_labeller(metadata, format)
  pretty <- pretty_accidental(pretty)
  return(pretty)
}

# =========================================================================== #
#' Convert performer to human readable format.
#'
#' Wrapper function for pretty_labeller(get_metadata())
#'
pretty_performer <- function(performer, format = "%pfn%") {
  metadata <- get_metadata("performer", performer)
  pretty <- pretty_labeller(metadata, format)
  return(pretty)
}

# =========================================================================== #
#' Convert composer to human readable format.
#'
#' Wrapper function for pretty_labeller(get_metadata())
#'
pretty_composer <-  function(composer, format = "%cfn%") {
  metadata <- get_metadata("composer", composer)
  pretty <- pretty_labeller(metadata, format)
  return(pretty)
}

# =========================================================================== #
#' Wrapper for pretty_pieceID
prettyKeySig <- pretty_pieceID

# =========================================================================== #