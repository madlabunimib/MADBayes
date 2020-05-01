import weighted_imputation as wi
from weighted_imputation.data import load_networks_from_disk
import weighted_imputation.utils.bds as bds 


if __name__ == "__main__":

    bn = load_networks_from_disk()["insurance"]
    print("score: ", bds.bds_score("insurance", bn, 1.0))

    bn = load_networks_from_disk()["asia"]
    print("score: ", bds.bds_score("asia", bn, 1.0))
