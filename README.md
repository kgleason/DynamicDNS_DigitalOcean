# Dyanmic DNS for Digital Ocean

by Kirk Gleason (<kgleason@gmail.com>) 
5/30/2015

This code and associated documentation are released into the Public Domain.

The following script is inspired by [Snorp's Python Linode update script](https://github.com/snorp/linode), but has been heavily modified.

This script has been tested against Python 3.4 on Antergos Linux. It has not been tested on other platforms, but should work on most versions of Python 3.

## What this script does
This script will read the dictionary in the config. Each key in the dictionary should be a domain whose DNS is located at Digital Ocean. The value of the keys should be a list of hostnames. 

You can scale this to work with as many domains as you want, but it is relatively slow with the 12 records that I have it updating. I'm sure that there is a way to fix it.

This script does the follwoing things:

   + determine your public IP address
   + loop through your domains
   + loop through all of the hostnames
       + Check the existing A record at Digital Ocean
       + if the existing vaue is different from your public IP, the A record is updated

## What this script should do better

Error handling in it sucks right now. In fact, it doesn't really exist, which really sucks. 

It could also probably be better about logging what it is doing.

## Using this script

As it is, this won't work for you. You'll need to do some tweaking.

  + Rename config.py.sample to config.py
  + Start by visiting Digital Ocean to get your API Key. Unless things have changed, you will find it in [your Digital Ocean dashboard](https://cloud.digitalocean.com/api_access). 
  + Set up the domainData dictionary. This dictionary has a couple of elements in it:
    + The name of the domain to be updated. Hopefully you know what this should be.
    + A list of the hostnames to be checked.
  + The service that you want to use to get your public IP. By default, the script uses [bot.whatismyipaddress.com](bot.whatismyipaddress.com). You can change this, but the script will expect that the site will return notinng but a plain IP address. If you use a proper API, then a little jiggering will be needed.
  
Once all of those values are set, you should be able to set it up in cron and run it.

My crontab entry looks like this:

`15 * * * * python /usr/local/bin/DynamicDNS.py`

which will check every hour at quarter past.