from bson.json_util import dumps
import pymongo
import flag
import re
import os
import json

def init(competition_name:str, mongo_link:str, teams_json:str, flags_json:str):
    # Plain text flag
    with open(flags_json) as flags:
        flags_data = json.loads(flags.read())

    flag_texts = {}

    # Generate formatted flag text
    for text in flags_data:
        fl = flag.generate_text(flags_data.get(text), 0)
        flag_texts[text] = fl

    # Connect to MongoDB
    try:
        client = pymongo.MongoClient(mongo_link)
    except:
        print("!!! Cannot connect to MongoDB !!!")
        quit()

    # Create DB
    db = client[competition_name]

    db.drop_collection("flags") # Reset existing collection
    flag_col = db["flags"] # Create collection containing the flag texts

    for title in flags_data:
        doc = {
            "chall_name" : title,
            "flag_text" : flag_texts[title]
        }

        flag_col.insert_one(doc) # Insert flag texts to collection

    db.drop_collection("teams") # Reset existing collection
    team_col = db["teams"] # Create collection containing flag checksums for each team

    with open("example_teams.json") as tm:
        tm = json.loads(tm.read())

    for teams in tm["teams"]: # Test team name
        flag_checksums = {}
        for chall in flag_texts:
            flag_checksums[chall] = flag.random_hex(10) # Generate checksum

        doc = {
            "team" : teams,
            "flag_checksums" : flag_checksums
        }
        
        team_col.insert_one(doc) # Insert checksums to collection
    return db

def check(team_name:str, chall_name:str, flag:str, db):
    chall_text = db["flags"].find_one({"chall_name":chall_name})["flag_text"]
    team_chall_checksum = db["teams"].find_one({"team" : team_name})["flag_checksums"][chall_name]
    flag_split = re.split("{|}|_", flag)[:-1]

    if flag == db.name + "{" + chall_text + "_" + team_chall_checksum + "}":
        return True
    else:
        return False

def dump_flags(db, filename):
    out = []
    for x in db["teams"].find({}):
        flags = {}
        for y in db["flags"].find({}, {"_id":0}):
            team = x["team"]
            chall = y["chall_name"]
            checksum = db["teams"].find_one({"team":team})["flag_checksums"][chall]
            flag_text = db["flags"].find_one({"chall_name":chall})["flag_text"]

            flags[chall] = db.name + "{" + flag_text + f"_{checksum}" + "}"
        doc = {
            "team":team,
            "flags":flags
        }
        out.append(doc)
    with open(filename, "w") as file:
        json.dump(out, file, indent=4)

def main():
    mdb = init("CTF2022", "mongodb+srv://" + os.environ["MONGODB_USER"] + ":" + os.environ["MONGODB_PASS"] + "@cluster0.bzrnt7o.mongodb.net/?retryWrites=true&w=majority", "example_teams.json", "example_flags.json")

    with open('flag_text.json', 'w') as file:
        json.dump(json.loads(dumps(mdb["flags"].find({}))), file, indent=4)

    with open('teams_checksum.json', 'w') as file:
        json.dump(json.loads(dumps(mdb["teams"].find({}))), file, indent=4)

    dump_flags(mdb, "team_flags.json")

    team_name = input("Enter your team name: ")
    chall = input("Enter challenge name: ")
    inp_flag = input("Enter your flag: ")

    chall_text = mdb["flags"].find_one({"chall_name":chall})["flag_text"]
    team_chall_checksum = mdb["teams"].find_one({"team" : team_name})["flag_checksums"][chall]
    inp_flag_split = re.split("{|}|_", inp_flag)[:-1]

    if inp_flag == mdb.name + "{" + chall_text + "_" + team_chall_checksum + "}":
        print("Solved")
    else:
        try:
            if inp_flag_split[0] == mdb.name and "_".join(inp_flag_split[1:-1]) == chall_text and inp_flag_split[-1] != team_chall_checksum:
                print("This flag is not for your team")
            else:
                print("Wrong flag")
        except:
            print("Wrong flag")

if __name__ == "__main__":
    main()