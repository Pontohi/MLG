import requests
import json
from tqdm import tqdm
import os
import shutil
import io
from PIL import Image
for walkdat in os.walk("Data/jmappers"):
    for loadset in walkdat[2]:
        if (".json" in loadset):
            linkset = json.load(open("Data/jmappers/"+loadset,"rb"))
            print("\nLoading up " + linkset["SetName"])
            try:
                os.mkdir("Data/"+linkset["SetName"])
            except:
                print("Finding was that the dir already exists.")
            for set in tqdm(linkset["URLs"]):
                if (linkset["DatFold"] == "Internet"):
                    try:
                        endpath = set.split('/')[-1]
                        gifFile = ".gif" in endpath
                        r = requests.get(set, allow_redirects=True,stream=False)
                        if r.status_code == 200:
                            if (gifFile):
                                i = Image.open(io.BytesIO(r.content))
                                i.convert("RGB").save("Data/"+linkset["SetName"]+"/"+endpath+".png", quality=90)
                            else:
                                open("Data/"+linkset["SetName"]+"/"+endpath,"wb").write(r.content)
                    except Exception as e:
                        print(e)
                else:
                    try:
                        os.mkdir("Data/validated_"+linkset["SetName"])
                    except:
                        print("Finding was that the valdir already exists.")
                    for file in linkset["URLs"]:
                        try:
                            shutil.copy("Data/"+linkset["SetName"]+"/"+file,"Data/validated_"+linkset["SetName"]+"/"+file)
                        except Exception as e:
                            print("Copy failed for "+file+" with error "+e)