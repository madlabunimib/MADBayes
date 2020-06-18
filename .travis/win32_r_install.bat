@ECHO ON
R.exe -e 'install.packages("BiocManager", repos = "https://cloud.r-project.org/")'
R.exe -e 'BiocManager::install(c("bnlearn", "graph", "RBGL", "Rgraphviz"))'
R.exe -e 'install.packages("gRain", dependencies = TRUE, repos = "https://cloud.r-project.org/")'
