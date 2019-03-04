# BigFix API
BigFix has an API that is pretty useful. However, to get meaningful data I programed this interpreter.  This is very much still in development, with new features to follow.

## requirements
- python3
  - BeautifulSoup
  - lxml
  - os
  - sys
  - requests
  - getpass
  - urllib3
- BigFix
  - An account on BigFix that has proper role to query API
 
## Install
Download the program
#### Make the follolwing Modifcations:
    update python3 path
    Install requirements
    update my_url Variable to be your bigfix agent url
chmod 755
./bigfix_api.py


## Retool
I retooled this API using BeautifulSoup and RE as etree was breaking down when I ran it.   Right now, there are no controls other than re-initializing the cache.   There are many redundancies in this code, and I am using files, more than running in memory due to the issues I encountered in etree.  I do plan on adding back some controls so this can be executed with a single function call.  I also tried and failed to reduce my match calls to a single function.  This code has been tested and it works.  So, I will probably leave this all as is unless my OCD starts up.
