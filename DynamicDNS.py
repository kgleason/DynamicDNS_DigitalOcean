# Python Dynamic DNS for Digital Ocean
# By Kirk Gleason <kirk@kirkg.us> 5/30/2015
# This code and associated documentation is released into the public domain.
#
# Read the readme to figure out how to set this all up.

import requests
import json, os
import config

apiHeaders = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {0}".format(config.doAuthBearer)
    }

def findDomainRecord(record):
    foundRecord = None
    pageNum = 1

    while not foundRecord:
        # Get all of the domain records
        url = "{0}/{1}/records?page={2}".format(config.apiURL, domain, pageNum)
        response = requests.get("{0}".format(url),headers=apiHeaders)
        domainRecords = json.loads(response.text)

        for rec in domainRecords['domain_records']:
            if rec["name"] == record and rec["type"] == "A":
                foundRecord = {}
                foundRecord["id"] = rec["id"]
                foundRecord["ip"] = rec["data"]
                break

        pageNum = pageNum + 1

        if not foundRecord:
            try:
                if not domainRecords['links']['pages']['next']:
                    # We've reached the end of the data.
                    foundRecord = -1
            except:
                    foundRecord = -1

    return foundRecord

def updateDNS(record, IP):
    url = "{0}/{1}/records/{2}/".format(config.apiURL, domain, record["id"])
    d = { "data" : IP }
    data = json.dumps(d)
    response = requests.put("{0}".format(url),data=data,headers=apiHeaders)
    result = json.loads(response.text)
    print(result)

# Start by grabbibg the current IP
resp = requests.get(config.Url_IP)
myIP = resp.text

if config.debug:
    print("Current IP ==> {0}".format(myIP))

# Iterate over all of the domains in the dict
for domain in config.domainData.keys():
    if config.debug:
        print("Starting ==> {0}".format(domain))

    # Iterate over all of the hostnames we want to check
    for record in config.domainData[domain]:
        if config.debug:
            print("Searching for {0}.{1}".format(record,domain))

        foundRecord = findDomainRecord(record)

        if type(foundRecord) is int:
            if config.debug:
                print("Unable to locate DNS record for {0}".format(record))
            continue

        if config.debug:
            print("Found ID: {0} and IP: {3} for {1}.{2}".format(foundRecord["id"],record,domain,foundRecord["ip"]))

        # Check to see if the record needs to be updated
        if foundRecord["ip"] != myIP:
            if config.debug:
                print("Updating {0}.{1} from {2} => {3}".format(record,domain,foundRecord["ip"],myIP))
            updateDNS(foundRecord,myIP)