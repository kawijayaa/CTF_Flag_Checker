from bson.json_util import dumps
import pymongo
import flag
import re
import os
import json

def connect(mongo_link:str):
    # Connect to MongoDB
    try:
        client = pymongo.MongoClient(mongo_link)
        print("Connection Successful. \n")
    except:
        print("!!! Cannot connect to MongoDB !!!")
        quit()
    return client

def init_db(client, competition_name:str, flags_json:str, teams_json:str, reset=True):
    # Plain text flag
    with open(flags_json) as flags:
        flags_data = json.loads(flags.read())

    flag_texts = {}

    # Generate formatted flag text
    for text in flags_data:
        fl = flag.generate_text(flags_data.get(text), 0)
        flag_texts[text] = fl

    # Create DB
    db = client[competition_name]

    if reset:
        db.drop_collection("flags") # Reset existing collection

    flag_col = db["flags"] # Create collection containing the flag texts

    for title in flags_data:
        doc = {
            "chall_name" : title,
            "flag_text" : flag_texts[title]
        }

        flag_col.insert_one(doc) # Insert flag texts to collection

    if reset:
        db.drop_collection("teams") # Reset existing collection

    team_col = db["teams"] # Create collection containing flag checksums for each team

    with open(teams_json) as tm:
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

def check(team_name:str, chall_name:str, flagg:str, db):
    chall_text = db["flags"].find_one({"chall_name":chall_name})["flag_text"]
    team_chall_checksum = db["teams"].find_one({"team" : team_name})["flag_checksums"][chall_name]

    if flagg == flag.format_flag(db.name, chall_text, team_chall_checksum):
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

            flags[chall] = flag.format_flag(db.name, flag_text, checksum)
        doc = {
            "team":team,
            "flags":flags
        }
        out.append(doc)
    with open(filename, "w") as file:
        json.dump(out, file, indent=4)

def dump_flag_text(db, filename:str, id=False):
    with open(filename, 'w') as file:
        if id:
            json.dump(json.loads(dumps(db["flags"].find({}))), file, indent=4)
        else:
            json.dump(json.loads(dumps(db["flags"].find({}, {"_id":0}))), file, indent=4)

def dump_team_checksum(db, filename:str, id=False):
    with open(filename, 'w') as file:
        if id:
            json.dump(json.loads(dumps(db["teams"].find({}))), file, indent=4)
        else:
            json.dump(json.loads(dumps(db["teams"].find({}, {"_id":0}))), file, indent=4)

def main():
    mongo_link = input("Enter MongoDB server link: ")
    client = connect(mongo_link)
    mdb = init_db(client, "CTF2022", "example_flags.json", "example_teams.json")

    dump_flag_text(mdb, "flag_text.json")
    dump_team_checksum(mdb, "teams_checksum.json")
    dump_flags(mdb, "team_flags.json")

    team_name = input("Enter your team name: ")
    chall = input("Enter challenge name: ")
    inp_flag = input("Enter your flag: ")

    if check(team_name, chall, inp_flag, mdb):
        print("Solved")
    else:
        print("Wrong flag") 

if __name__ == "__main__":
    main()