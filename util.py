from blimpy import Waterfall
import pandas as pd
import h5py
PSR_DATA = pd.read_csv("object_GBT_pulsars.csv")
PSR_LST = list(PSR_DATA["NAME"])
PSR_LST = PSR_LST # + list(map(lambda x: "DIAG_"+x,PSR_LST))
QUERY_API = "http://seti.berkeley.edu/opendata//api/query-files"
DATA = pd.read_csv("psrdata.csv")
Rpath = "/mnt_blpd13/datax/cal_and_psrs/"
servername ="shufanl@blpl1.ssl.berkeley.edu"


import requests
class Psr_query:
    psr_observations = None
    @staticmethod
    def write_score(filename, score):
        f = h5py.File(filename)
        f['data'].attrs['quality'] = score
        f.close()

    @staticmethod
    def read_score(filename):
        f = h5py.File(filename)
        result = f['data'].attrs.get('quality')
        f.close()
        return result

    def __init__(self):
        self.data = DATA
        pass
    @staticmethod
    def get_observation_time(file):
        f = Waterfall(file)
        header = f.header
        return header[b'tstart']

    @property
    def get_psr_observations(self):
        if self.psr_observations:
            return self.psr_observations
        payload = {"file-types":"filterbank"}

        rst = []
        visited = set()
        for i in PSR_LST:
            payload["target"] = i
            r = requests.get(QUERY_API,payload)
            js = r.json()
            print(len(js.get("data",[])).__str__()+" obserivations for "+ i)
            for entry in js.get("data",[]):
                md5 = entry["md5sum"]
                if md5 not in visited:
                    visited.add(md5)
                    rst.append(entry)
                    #print(entry)
            #break

        rst.sort(key = lambda x:x['size'],reverse = True)
        rst.sort(key = lambda x:x['mjd'],reverse = True)
        self.psr_observations = rst
        return rst

    def latest_psr(self,file):
        t_start = self.get_observation_time(file)
        return Rpath+self.get_closest_observations(self.data,t_start)

    def calculate_SNR(self):
        pass

    def get_closest_observations(self,df, mjd):
        df["time_delta"] = 0
        for index in df.index:
            df.loc[index, "time_delta"] = abs(df.loc[index, "tstart"] - mjd)
        k = df.sort_values("time_delta").loc[0]
        print(k["time_delta"])
        return k["fname"]
