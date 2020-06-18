#!/bin/sh
sudo R -e 'install.packages("BiocManager", repos = "https://cloud.r-project.org/")'
sudo R -e 'BiocManager::install(c("bnlearn", "graph", "RBGL", "Rgraphviz"))'
sudo R -e 'install.packages("gRain", dependencies = TRUE, repos = "https://cloud.r-project.org/")'
