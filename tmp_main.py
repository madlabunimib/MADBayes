import weighted_imputation as wi
from weighted_imputation.data import load_networks_from_disk
import weighted_imputation.utils.bds as bds 


if __name__ == "__main__":

    bn = load_networks_from_disk()["survey"]


    bds.bds_score("survey", bn, 1.0)
