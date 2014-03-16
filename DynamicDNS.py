# Python Dynamic DNS for Linode
# By Kirk Gleason <kirk@gleasons.info> 1/14/2014
# This code and associated documentation is released into the public domain.
#
# Read the readme to figure out how to set this all up.

from urllib2 import Request,urlopen
from urllib import urlencode
import json

# Set the next variable to True to do some extra debugging
debug = False

# Put yout API Key here
apiKey = "APIKEY000000APIKEY111111APIKEY222222APIKEY333333APIKEY444444APIK"

# Enter your domain information here
domainData = {
    "domain1.com" : {   # This is the friendly domain name. Only used for human readability.
        "domainID" : "000000",    # The Domain ID according to Linode. See README to find this.
        "resources" : ["#######", "#######"]   # The resource IDs that represent a specific record in this domain
    },
    "domain1.co" : {
        "domainID" : "111111",
        "resources" : ["#######", "#######"]
    },
    "domain1.org" : {
        "domainID" : "222222",
        "resources" : ["#######", "#######"]
    },
    "domain1.net" : {
        "domainID" : "333333",
        "resources" : ["#######", "#######"]
    },
    "domain1.us" : {
        "domainID" : "444444",
        "resources" : ["#######", "#######"]
    },
    "domain2.com" : {
        "domainID" : "555555",
        "resources" : ["#######", "#######"]
    },
}

# The URL of a Web service that returns your IP address as plaintext. 
#
myIpUrl = "http://bot.whatismyipaddress.com"

#
# If for some reason the API URI changes, or you wish to send requests to a
# different URI for debugging reasons, edit this.  {0} will be replaced with the
# API key set above, and & will be added automatically for parameters.
#
url = "https://api.linode.com/api/?api_key={0}".format(apiKey)

# Start by grabbibg the current IP
sock = urlopen(myIpUrl)
myIP = sock.read()
sock.close()

if debug:
    print "Current IP ==> {0}".format(myIP)


# Iterate over all of the domains in the dict
for domain in domainData.keys():
    if debug:
        print "Starting ==> {0}".format(domain)
    domainID = domainData[domain]["domainID"]
    
    # Iterate over all of the specific resources to be checked.    
    for resource in domainData[domain]["resources"]:
        urlParams = "&resultFormat=JSON&action=domainResourceGet&ResourceID={0}&DomainID={1}".format(resource,domainID)
        req = Request("{0}{1}".format(url,urlParams))
        res = json.load(urlopen(req,timeout=10))
        
        if debug:
            print "Linode returned ==> {0}".format(res)
        
        curDNS = res['DATA'][0]['TARGET']
        
        if debug:
            print "Existing DNS record ==> {0}".format(curDNS)
        
        # Check to see if the record needs to be updated    
        if curDNS != myIP:
            if debug:
                subdomain = res['DATA'][0]['NAME']
                if subdomain and len(subdomain) >= 1:
                    fqdn = "{0}.{1}".format(subdomain,domain)
                else:
                    fqdn = domain
                
                print "Updating {} from {} => {}".format(fqdn,curDNS,myIP)
                
            # We need to make an update
            requestParams = {
                "ResourceID" : resource,
                "DomainID" : domainData[domain]["domainID"],
                "Name" : res['DATA'][0]['NAME'],
                "Type" : res['DATA'][0]['TYPE'],
                "Target" : myIP,
                "TTL_SEC" : res['DATA'][0]['TTL_SEC']
            }
            
            newUrl = "{0}&{1}&{2}".format(url,"api_action=domain.resource.update",urlencode(requestParams))
            
            if debug:
                print "The update URL ==> {0}".format(newUrl)    
            
            req = Request(newUrl)
            res = json.load(urlopen(req,timeout=10))
            
            if debug:
                print "Linode returned ==> {0}".format(res)
            
