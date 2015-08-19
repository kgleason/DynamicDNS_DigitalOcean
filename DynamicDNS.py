# Python Dynamic DNS for CloudFlare
# By Kirk Gleason <kirk@kirkg.us> 8/17/2015
# This code and associated documentation is released into the public domain.
#
# Read the readme to figure out how to set this all up.

import requests
import json, os
import sys
import config

apiHeaders = {
    "Content-Type": "application/json",
    "X-Auth-Key": "{0}".format(config.cfgAuthBearer),
    "X-Auth-Email": "{0}".format(config.cfgAuthEmail)
    }

def getDomainID(d):
    pageNum = 1
    foundDomain = ""

    while not foundDomain:
        #Get all domain records
        url = "{0}zones&page={1}".format(config.apiURL, pageNum)

        response = requests.get("{0}".format(url),
            headers = apiHeaders)
        domains = json.loads(response.text)

        for domain in domains['result']:
            if domain["name"] == d:
                foundDomain = str(domain["id"])
                break

        if not foundDomain:
            if pageNum <= int(domains["result_info"]["total_pages"]):
                pageNum = pageNum + 1
            else:
                break

    return foundDomain

def findDomainRecord(dID, d, record, dns_rec_type):
    pageNum = 1
    foundRecord = {}

    while not foundRecord:
        # Get all of the domain records
        url = "{0}zones/{1}/dns_records?page={2}".format(config.apiURL, dID, pageNum)

        response = requests.get("{0}".format(url),
            headers=apiHeaders)
        domainRecords = json.loads(response.text)

        for rec in domainRecords['result']:
            if rec["name"] == '{0}.{1}'.format(record,d) and rec["type"] == dns_rec_type:
                foundRecord = rec
                break

        pageNum = pageNum + 1

        if not foundRecord:
            if pageNum <= int(domainRecords["result_info"]["total_pages"]):
                # We've reached the end of the data.
                pageNum = pageNum + 1
            else:
                break

    return foundRecord

def updateDNS(record, domainID):
    url = "{0}zones/{1}/dns_records/{2}/".format(config.apiURL, domainID, record["id"])
    data = json.dumps(record)
    response = requests.put("{0}".format(url),data=data,headers=apiHeaders)
    result = json.loads(response.text)
    print(result),


for ip_version in config.cfgDict.keys():
    if config.debug:
        print("Updating {0}".format(ip_version))

    cfg = config.cfgDict[ip_version]
    if cfg["check"]:

        # Start by grabbibg the current IP
        resp = requests.get(cfg["url_ip"])
        myIP = resp.text

        if config.debug:
            print("Current IP ==> {0}".format(myIP))

        # Iterate over all of the domains in the dict
        for domain in cfg["domainData"].keys():
            if config.debug:
                print("Starting ==> {0}".format(domain))

        # Get the domain ID
        domainID = getDomainID(domain)

        if not domainID:
            print("Error locating domain {0}".format(domain))
            sys.exit(1)
        else:
            if config.debug:
                print("DomainID ==> {0}".format(domainID))

        # Iterate over all of the hostnames we want to check
        for hostname in cfg["domainData"][domain]:
            if config.debug:
                print("Searching ==> {0}.{1}".format(hostname, domain))

            foundRecord = findDomainRecord(domainID, domain, hostname, cfg["rec_type"])

            if not foundRecord:
                print("Unable to locate DNS record for {0}".format(hostname))
            else:
                if config.debug:
                    print("RecordID ==> {0}".format(foundRecord["id"]))

                # Check to see if the record needs to be updated
                if foundRecord["content"] != myIP:
                    if config.debug:
                        print("Updating {0}.{1} from {2} => {3}".format(hostname,domain,foundRecord["content"],myIP))
                    foundRecord["content"] = myIP
                    updateDNS(foundRecord,domainID)