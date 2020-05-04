#! /usr/bin/env python3.7
import weighted_imputation as wi
from weighted_imputation.data import load_networks_from_disk
from weighted_imputation.utils.bds import bds_score 


if __name__ == "__main__":

    bn = load_networks_from_disk()["asia"]
    print("score: ", bds_score("asia", bn, 1.0, True))

    bn = load_networks_from_disk()["insurance"]
    print("score: ", bds_score("insurance", bn, 1.0, True))
