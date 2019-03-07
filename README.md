# BigFix API v. 2.5
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


## 2.5 Update
Everything is ran from gen_asset_report(rep_type)

### allows:
- new = updates everything and gives you entire inventory
- last = nothing is updated runs off last inventory cache file
- current = pulls new inventory list from bigfix and reports on it.  History file is not updated
- new_servers = pulls new inventory list from bigfix and compares against history file 
- new_servers_hist_upd = pulls new inventory list from bigfix and compares against an updated history file 
- decom_servers = pulls Decom from bigfix history file and compares against new inventory file 
- decom_servers_hist_upd = pulls Decom from updated bigfix history file and compares against new inventory file 
- history= pulls new inventory list from bigfix and compares against an updated history file currently if you run with out a history file this will crash
