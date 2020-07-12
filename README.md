<pre>
  __  __          _____  ____                        
 |  \/  |   /\   |  __ \|  _ \                       
 | \  / |  /  \  | |  | | |_) | __ _ _   _  ___  ___ 
 | |\/| | / /\ \ | |  | |  _ < / _` | | | |/ _ \/ __|
 | |  | |/ ____ \| |__| | |_) | (_| | |_| |  __/\__ \
 |_|  |_/_/    \_\_____/|____/ \__,_|\__, |\___||___/
                                      __/ |          
                                     |___/           
</pre>
[![Build Status](https://travis-ci.com/madlabunimib/MADBayes.svg?branch=master)](https://travis-ci.com/madlabunimib/MADBayes) [![CodeFactor](https://www.codefactor.io/repository/github/madlabunimib/madbayes/badge/master)](https://www.codefactor.io/repository/github/madlabunimib/madbayes/overview/master) [![codecov](https://codecov.io/gh/madlabunimib/MADBayes/branch/master/graph/badge.svg)](https://codecov.io/gh/madlabunimib/MADBayes)

# MADLab MADBayes

MADBayes is a Python library about Bayesian Networks.

## Introduction

## How to Install

Clone the repository including submodules:

  git clone --recurse-submodules -j8 https://github.com/madlabunimib/MADBayes.git

Install the required system libraries:

  sudo apt-get install libigraph0-dev libgraphviz-dev graphviz

Build the package with C++ backend and install:

  cd MADBayes && sudo python3 setup.py install

## Contents

### Legend

* *empty* - Not implemented
* :heavy_check_mark: - Already implemented
* :x: - Non-existent

### Structural Properties

| Name                 | Python | C/C++ |
| -------------------- |:------:|:-----:|
| Independence Map     |        |       |
| U-Separation         |        |       |
| D-Separation         |        |       |
| Markov Blanket       |        |       |
| Equivalence Classes  |        |       |
| Topological Ordering |        |       |

### Types of Bayesian Networks

| Name              |       Python       | C/C++ |
| ----------------- |:------------------:|:-----:|
| Discrete Networks | :heavy_check_mark: |       |
| Gaussian Networks |                    |       |
| CLG Networks      |                    |       |
| Mixed Networks    |                    |       |

### Classifiers

| Name                       | Python | C/C++ |
| -------------------------- |:------:|:-----:|
| Naive Bayes                |        |       |
| Tree-Augmented Naive Bayes |        |       |

### Exact Inference

| Type        | Name                          |       Python       | C/C++ |
| ----------- | ----------------------------- |:------------------:|:-----:|
| Exact       | Variable Elimination          |                    |       |
|             | Junction Tree                 | :heavy_check_mark: |       |
|             |                               |                    |       |
| Approximate | Prior Sampling                |                    |       |
|             | Rejection Sampling            |                    |       |
|             | Likelihood Weighting Sampling |                    |       |
|             | Monte Carlo Chain Sampling    |                    |       |

### Structural Learning

| Type            | Name                       |       Python       | C/C++ |
| --------------- |:-------------------------- |:------------------:|:-----:|
| Costraint-based | Inductive Causation        |                    |       |
|                 | Peter & Clark              |                    |       |
|                 | Grow-Shrink                |                    |       |
|                 | Incremental Association    |                    |       |
|                 | Max-Min Parents & Children |                    |       |
|                 | Hiton-PC                   |                    |       |
|                 |                            |                    |       |
| Score-based     | Hill-Climbing              | :heavy_check_mark: |       |
|                 | Greedy Equivalent Search   |                    |       |
|                 | Tabu Search                |                    |       |
|                 | Genetic Algorithms         |                    |       |
|                 | Simulated Annealing        |                    |       |
|                 |                            |                    |       |
| Hybrid          | Sparse Candidate Algorithm |                    |       |
|                 | MMHC                       |                    |       |

### Structure Score

| Name                                         |       Python       | C/C++ |
| -------------------------------------------- |:------------------:|:-----:|
| Bayesian Information Criterion (BIC)         |                    |       |
| Akaike’s Information Criterion (AIC)         |                    |       |
| Bayesian Dirichlet Equivalent Uniform (BDeu) |                    |       |
| Bayesian Dirichlet Sparse (BDs)              | :heavy_check_mark: |       |
| Bayesian Gaussian equivalent (BGe)           |                    |       |

### Missing Data

| Name                     |       Python       | C/C++ |
| ------------------------ |:------------------:|:-----:|
| Expectation-Maximisation | :heavy_check_mark: |       |
| Structural EM            | :heavy_check_mark: |       |
| Data Augmentation        |                    |       |
| Bootstrap Aggregation    |                    |       |

### Causal Models - Effects of Interventions

| Name                              | Python | C/C++ |
| --------------------------------- |:------:|:-----:|
| Interventions                     |        |       |
| Adjustement Formula               |        |       |
| Backdoor Criterion                |        |       |
| Front-Door Criterion              |        |       |
| Causal Infrence in Linear Systems |        |       |

### Causal Models - Counterfactuals

| Name                              | Python | C/C++ |
| --------------------------------- |:------:|:-----:|
| Counterfactuals                   |        |       |
| Probabilistic Counterfactuals     |        |       |
| Counterfactuals in Linear Systems |        |       |
