# Dyanmic DNS for Linode

by Kirk Gleason (<kgleason@gmail.com>) 
3/15/2014

This code and associated documentation are released into the Public Domain.

The following script is inspired by [Snorp's Python Linode update script](https://github.com/snorp/linode), but has been heavily modified.

This script has been tested against Python 2.7.6 on OS X and Debian PowerPC linux. It does not work well with Python 2.7.5+ on linux (probably my fault).

To see what version you are using, run this:

`python --version`

I would expect that it will run on versions of Python that are newer than 2.7.6, but I doubt that it will work in Python 3 without some tweaking.

## What this script does
The original version of this script would update a single record of a single domain. I have a few domains, and right now they all have their DNS at Linode. For the time being, I want the SOA and the WWW 'A' records to point to the same dynamic IP.

The specific records that are being updated are all stored in a python list called resources.

You can scale this to work with as many domains as you want, but it is relatively slow with the 12 records that I have it updating. I'm sure that there is a way to fix it.

This script does the follwoing things:

   + determine your public IP address
   + loop through your domains
   + loop through all of the resources (aka DNS record)
       + Check the existing value at Linode
       + if the existing vaue is different from your public IP, then Linode is updated

## What this script should do better

Error handling in it sucks right now. In fact, it doesn't really exist, which really sucks. 

It could also probably be better about logging what it is doing.

## Using this script

As it is, this won't work for you. You'll need to do some tweaking.

  + Start by visiting Digital Ocean to get your API Key. Unless things have changed, you will find it in [your Digital Ocean dashboard](https://cloud.digitalocean.com/api_access). 
  + Create an environemnt variable for your API Key ($DIGITALOCEANAPI) and your Client Key ($DIGITALOCEANCLIENT)
  + Set up the domainData dictionary starting on line 18. This dictionary has a few elements in it:
    + The name of the domain to be updated. Hopefully you know what this should be.
    + The domain ID from Digital Ocean. 
      + You can find this by running this command after you have your environment variables in place: 
	  + `curl https://api.digitalocean.com/domains?client_id=${DIGITALOCEANCLIENT}&api_key=${DIGITALOCEANAPI}`    
      + That should return some JSON that will have a list of all of your domains, and their DomainIDs.
    + The resource ID for the DNS records that you want to update. 
      + You can find them by running this command, replacing 000000 with the domain ID that you are interested in.
	  + `DOMAINID=000000 curl https://api.digitalocean.com/domains/${DOMAINID}/records?client_id=${DIGITALOCEANCLIENT}&api_key=${DIGITALOCEANAPI}`
  + The service that you want to use to get your public IP. By default, the script uses [bot.whatismyipaddress.com](bot.whatismyipaddress.com). You can change this, but the script will expect that the site will return notinng but a plain IP address. If you use a proper API, then a little jiggering will be needed.
  
Once all of those values are set, you should be able to set it up in cron and run it.

My crontab entry looks like this:

`15 * * * * python /usr/local/bin/DynamicDNS_Linode.py`

which will check every hour at quarter past.