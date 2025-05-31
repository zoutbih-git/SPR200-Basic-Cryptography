# Lab03.5 Configure and Run Your Own Tor Website
**name:** Zakariya Outbih   
**Student ID:** 100184233  
**Date:** 02/12/2025

## Table of contents
- [Introduction](##Introduction)  
- [VM configuration details](##VM-Configuration-Details)
- [Steps](##Steps)


## Introduction

This lab focuses on setting up and running a basic tor hidden service on ubuntu.

## VM configuration details

**VM name** zubuntu  
**RAM** 4GB   
**Disk Space** 25 GB   
**CPU cores** 4  
**Network Adapter** NAT && Internal



## Steps

### Step 1

1. Navigate to /usr/local/etc/tor/torrc_sample, copy the torrc_sample file as torrc

### Step 2

2. copy   
HiddenServiceDir /var/lib/tor/hidden_service/
HiddenServicePort 80 127.0.0.1:8082  
into the torrc file

### Step 3

3. Navigate to /var/lib/tor/hidden_service (or create it if it doesn't exist like in my case) and run 
echo "Hello, SPR200!" > /var/lib/tor/hidden_service/index.html

### Step 4

4. Now you have a index.html file, this will be used to format how your website looks like, now do sudo chmod 700 /var/lib/tor/hidden_service/ 
additionally you will want to change the owner of the directory and index.html file ex. sudo chown user:user /var/lib/tor/hidden_service (change the user parameter to reflect the name and group of the actual user)

### Step 5

5. in the directory run the command  
"sudo python3 -m http.server 8082 --bind 127.0.0.1"  
ensure that the tor directory is owned by the user ex. sudo chown user:user ~/tor  
run tor "tor"

### Step 6

6. If all steps are done appropriately you should have a file in the 
/var/lib/tor/hidden_service directory created called hostname, this hostname will
contain the onion address of the hidden service that you are running, it should look something like this ndrt2nb5gshz6gokgwrvguonkll5bklhyhieylx3ysukcbpu5vbyl5id.onion.



