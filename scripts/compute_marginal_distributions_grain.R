library(bnlearn)
library(jsonlite)

write_json <- function(x, file, pretty = TRUE, na = FALSE, auto_unbox = FALSE) {
  if ("factor" %in% class(x)) x <- as.character(x)
  if (any(grepl("data.frame", class(x)))) {
    index_factor <- sapply(x, is.factor)
    x[index_factor] <- lapply(x[index_factor], as.character)
  }
  if (na) {
    json <- jsonlite::toJSON(
      x, 
      pretty = pretty, 
      na = "null", 
      null = "null",
      auto_unbox = auto_unbox
    )
  } else {
    json <- jsonlite::toJSON(x, pretty = pretty, auto_unbox = auto_unbox)
  }
  write(json, file)
}

BASE_PATH = "~/madlab_weighted_imputation/weighted_imputation/networks/"
files = list.files(BASE_PATH)
for (file in files) {
  if (endsWith(file, ".bif")) {
    fitted = read.bif(paste(BASE_PATH, file, sep=""))
    probs = gRain::querygrain(as.grain(fitted), nodes = names(fitted), type = "marginal")
    write_json(probs, paste(BASE_PATH, file, ".json", sep=""))
  }
}
