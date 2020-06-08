@ECHO ON
R.exe -e 'install.packages("BiocManager")'
R.exe -e 'BiocManager::install(c("bnlearn", "gRain"))'
