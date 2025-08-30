# Author: @dare_devil_ex

import json

with open("config.json", "r") as f:
    config = json.load(f)
token = config["token"]

class Wkaie:
    def wkaie():
        print(token)


if __name__=="__main__":
    Wkaie.wkaie()