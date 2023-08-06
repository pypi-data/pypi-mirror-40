========================================================================
virtual network embdding

========================================================================
 run method
from VNE_SIM.VNR import *
from VNE_SIM.SN import *
import VNE_SIM.algorithm as alg
SNpath='topology\\sn\\sub100-570.txt'
vnrpath='topology\\newr-2000-0-20-0-25'
vnrnumber=2000
timeframe=2000
mysimulation=simulation(5,SNpath,vnrpath,vnrnumber)
mysimulation.init(timeframe)
def my_vne_alg():
    v2sindex=[[v1,s1]]
    ve2seindex=[[s1,s2,...]]
    return True|False,v2sindex,ve2seindex
mysimulation.simulation_run(EA_VNR.EA_VNR_alg,EA_VNR.EA_VNR_ALG_NAME)
mysimulation.draw()
 #####################################
zzu@1402


