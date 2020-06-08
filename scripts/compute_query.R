library(bnlearn, gRain)
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

BASE_PATH = "~/madlab_madbayes/madbayes/networks"
file = "asia.bif"
fitted = read.bif(paste(BASE_PATH, file, sep="/"))
fitted = mutilated(fitted, evidence = list('lung' = 'yes'))
probs = gRain::querygrain(as.grain(fitted), nodes = c('asia', 'xray', 'tub'), type = 'joint', result='data.frame')
