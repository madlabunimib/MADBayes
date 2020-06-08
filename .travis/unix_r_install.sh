#!/bin/sh
sudo R -e 'install.packages("BiocManager", repos = "https://cloud.r-project.org/")'
sudo R -e 'BiocManager::install(c("bnlearn", "gRain"))'
