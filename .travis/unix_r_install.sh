#!/bin/sh
sudo R -e 'install.packages("BiocManager", version = "3.10", repos = "https://cloud.r-project.org/")'
sudo R -e 'BiocManager::install(version = "3.10", c("bnlearn", "graph", "RBGL", "Rgraphviz"))'
sudo R -e 'install.packages("gRain", dependencies = TRUE, repos = "https://cloud.r-project.org/")'
