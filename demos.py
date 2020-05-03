from .util import *
from .util import Psr_query
from .snr import process
process_snr = process
#%%
process_snr = process
testfilename = "GBT_57438_42346_J1239+2453_mid.h5"
testfilepath = "/mnt_blpd13/datax/cal_and_psrs/"
servername ="shufanl@blpl1.ssl.berkeley.edu"
testfil = "spliced_blc7071727374757677_guppi_58845_40114_PSR_B1133+16_0009.gpuspec.0002.fil"
#%%
h = Psr_query()
#%%
h.read_score(testfilename)
#%%
h.write_score(testfilename,0.7232)
#%%
servername+":"+h.latest_psr(testfilename)
#%%
h.get_closest_observations(h.data,58000)
#%%
snrs=process_snr(testfil)
#%%
if snrs["SNR"]==float("nan"):
    snrs["SNR"]=0
score = (snrs["expSNR"]-max(0,snrs["SNR"]))/snrs["expSNR"]
print(score)

h.write_score(testfilename,score)
#%%
h.read_score(testfilename)
#%%
