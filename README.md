# BigFix API
BigFix has an API that is pretty useful. However, to get meaningful data I programed this interpreter.  This is very much still in development, with new features to follow.

## requirements
- python3
  - ElementTree
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
    update def get_asset_url Function url Variable to be your bigfix agent url
chmod 755
./bigfix_api.py


## Important Functions

### init_cache(update_hist)
Initialize Cache files.  This should only be run once per day and should be part of Cron, as when it is run the cache file library that any of the delta reports are based off are updated, thereby eliminated the usefulness of them.
#### Expects: 
update_hist = true (Will update last run Cache  .bigfix_old_asset_url_list.cache )
update_hist = false (Will not update run Cache  .bigfix_old_asset_url_list.cache)

### get_asset_url(username, password)
It is a good idea to run this before doing other calls as it allows you to rerun BigFix API query to get newest list of Assets.  Running this will not update older Cache.  To do this rerun init_chache()
#### Expects: username and password 

### find_new_assets()
Finds new asset url list from Bigfix since last cache initialization

### find_decom_assets()
Generates an asset report to ~/report_output.csv

#### Expects:
    rep_type (Types of reports:)
    current (Current Bigfix Assets)
    new  (New Bigfix Assets)
    new_w_cache (New Bigfix Assets with updated_cache)
    decom (decom Bigfix Assets)
    decom_w_cache (Decom Bigfix Assets with updated_cache)
    History (report of last cache update history


## Version 2.5 To-Do's
For reports search on Os
For reports search on type

Add as e-mail
Add to splunk
Run as service account
learn pip3 install
call as bigfix_api.function(params)
add help
add error control

