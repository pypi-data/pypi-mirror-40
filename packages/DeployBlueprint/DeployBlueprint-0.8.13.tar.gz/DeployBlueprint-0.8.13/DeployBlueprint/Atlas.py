# https://docs.atlas.mongodb.com/reference/api/clusters-create-one/
from enum import Enum
import requests
from requests.auth import HTTPDigestAuth
import json
import re
import time

class AtlasSize(Enum):
    M2 = "M2"	    # 2GB	Shared
    M5 = "M5"	    # 5GB	Shared
    M10 = "M10"	    # 10GB	2GB
    M20 = "M20"	    # 20GB	4GB
    M30 = "M30"	    # 40GB	8GB
    M40 = "M40"     # or R40	80GB	16GB
    M50 = "M50"     # or R50	160GB	32GB
    M60 = "M60"     # or R60	320GB	64GB
    R80 = "R80"	    # 750GB	122GB
    M100 = "M100"	# 1TB	160GB
    M140 = "M140 "	# 1TB	192GB
    M200 = "M200"   # or R200	1.5TB	256GB
    M300 = "M300"   # 2TB	384GB
    R400 = "R400"	# 3TB	488GB

class Atlas:
    username = ""
    apikey = ""
    uid = ""
    group = ""
    names = []

    def __init__(self, username, apikey, uid):
        self.username = username
        self.apikey = apikey
        self.uid = uid
    def createCluster(self, name, group, region, type, version, cloud, size, rscount, shards, disksize=16, iops=100, backup=False, bi=False, encrypted=False):
        self.group = group
        data = {}
        data["name"] = s = re.sub('[^0-9a-zA-Z]+', '', name) + "-" + self.uid
        data["diskSizeGB"] = int(disksize)
        data["numShards"] = int(shards)
        ps = {}
        ps["providerName"] = cloud
        ps["diskIOPS"] = int(iops)
        ps["encryptEBSVolume"] = encrypted
        ps["instanceSizeName"] = size
        ps["regionName"] = region
        data["providerSettings"] = ps
        data["replicationFactor"] = int(rscount)
        data["backupEnabled"] = backup
        if encrypted:
            data["encryptionAtRestProvider"] = cloud
        data["autoScaling"] = {"diskGBEnabled": False}

        url = "https://cloud.mongodb.com/api/atlas/v1.0/groups/"+group+"/clusters"
        headers = {"Content-Type":"application/json"}
        result = requests.post(url, auth=HTTPDigestAuth(self.username, self.apikey), headers=headers, data=json.dumps(data))
        
        if ((int(result.status_code) > 199) and (int(result.status_code) < 300)):
            return True, result.text
            self.names.append(data["name"])
        else:
            return False, result.text
    def clusterStatus(self, name):
        url = "https://cloud.mongodb.com/api/atlas/v1.0/groups/"+self.group+"/clusters/"+name
        headers = {"Content-Type":"application/json"}
        result = requests.get(url, auth=HTTPDigestAuth(self.username, self.apikey), headers=headers)
        return result.text

    def r_waitForCluster(self):
        up = True
        retval = []
        for name in self.names:
            result = self.clusterStatus(name)
            rd = json.loads(result)
            if rd["stateName"] != "IDLE":
                up = False
            else:
                retval.append(result)
        if up:
            return retval
        else:
            time.sleep(10)
            sys.stdout.write(".")
            sys.stdout.flush()
            self.r_waitForCluster()
