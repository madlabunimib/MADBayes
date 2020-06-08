#!/bin/sh
sudo R -e 'install.packages("BiocManager")'
sudo R -e 'BiocManager::install(c("bnlearn", "gRain"))'
