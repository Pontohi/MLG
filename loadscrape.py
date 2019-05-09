import requests
import json
from tqdm import tqdm
import os
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
                try:
                    gifFile = ".gif" in set[0]
                    r = requests.get(set[1], allow_redirects=True,stream=False)
                    if r.status_code == 200:
                        if (gifFile):
                            i = Image.open(io.BytesIO(r.content))
                            i.convert("RGB").save("Data/"+linkset["SetName"]+"/"+set[0]+".png", quality=90)
                        else:
                            open("Data/"+linkset["SetName"]+"/"+set[0],"wb").write(r.content)
                except Exception as e:
                    print(e)