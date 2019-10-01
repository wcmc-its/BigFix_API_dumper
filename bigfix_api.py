#!/usr/bin/env python3

# This script pulls from Bigfix API, and outputs All systems into csv format.
# Written by: Brian Whelan
# v2.5
import requests
import getpass
import re
from bs4 import BeautifulSoup
import lxml
import urllib3
import os
import sys
from shutil import copyfile
import configparser
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#get bigfix URL from config file
config = configparser.ConfigParser()
config.read('bigfix_config.conf')
bigfix_url = config["DEFAULT"]["bigfix_api_url"]


#Initializes cache files
bigfix_new_asset_url_cache_file = '.bigfix_new_asset_url_list.cache'
bigfix_old_asset_url_cache_file = '.bigfix_old_asset_url_list.cache'
bigfix_diff_asset_url_cache_file = '.bigfix_temp_asset_url_list.cache'
bigfix_inv_asset_url_cache_file = '.bigfix_inv_asset_url_list.cache'
bigfix_asset_info_cache_file = '.bigfix_asset_info.cache'


def init_cache():
#Intiallize Cache files.  This should only be run once perday
     if __debug__: print("Initializing cache")
     try:
         f = open(bigfix_new_asset_url_cache_file)
         f.close()
     except IOError as e:
         f = open(bigfix_new_asset_url_cache_file, 'w')
         f.close()

def get_asset_url(username, password):
#Function expects the username and password
#calls Bigfix to get the URL list of machines
     if __debug__: print("getting asset URLs")
     f = open(bigfix_new_asset_url_cache_file, 'w')
     f.close()
     response = requests.get(bigfix_url, verify=False, auth=(username, password))
     #print(response.text)
     f = open(bigfix_new_asset_url_cache_file, 'a')
     f.write(response.text)
     f.close()


def update_history(update_hist):
#creats inventory file if it does not exist, also copies it to History.  History is used for comparison New and Decom
     try:
         f = open(bigfix_inv_asset_url_cache_file)
         f.close()
     except IOError as e:
         f = open(bigfix_inv_asset_url_cache_file, 'w')
         f.close()
     if update_hist == 'true':
         #copies new cache to old
         copyfile(bigfix_inv_asset_url_cache_file, bigfix_old_asset_url_cache_file)


def read_bigfix_url_file(update_hist):
     #Reads file containaing BigFix URL's and parses out the URL for that asset outputs to inventory file
     outfile = open(bigfix_inv_asset_url_cache_file, 'w') # raw asset url output file
     cache_file = open(bigfix_new_asset_url_cache_file, 'r') # raw BF output
     cache_soup = BeautifulSoup(cache_file, 'lxml') # soupify raw BF output
     computer_records = cache_soup.find_all('computer') # extract the computer computer records
     if __debug__: print(f"extracted {len(computer_records)} computer records")
     # get the resource URL from each computer record and write to URL file
     for computer in computer_records:
         outfile.write(computer['resource'] + '\n')
     outfile.close()


def comp_assets(search_for, comp_against, delta_output):
     try:
          f = open(delta_output)
          f.close()
          os.remove(delta_output)
     except IOError as e:
          null=''
     #     break
     newf = open(search_for, 'r')
     for line_in_newf in newf:
          search_url_exsits = line_in_newf.rstrip()
          if search_url_exsits not in open(comp_against).read():
               output = open(delta_output, 'a')
               output.write(search_url_exsits+'\n')
               output.close()

     newf.close()



def find_new_assets():
#compair two files and output
     search_for =  '.bigfix_inv_asset_url_list.cache'
     comp_against = '.bigfix_old_asset_url_list.cache'
     delta_output = '.bigfix_temp_asset_url_list.cache'
     comp_assets(search_for, comp_against, delta_output)


def find_decom_assets():
#compair two files and output
     search_for =  '.bigfix_old_asset_url_list.cache'
     comp_against = '.bigfix_inv_asset_url_list.cache'
     delta_output = '.bigfix_temp_asset_url_list.cache'
     comp_assets(search_for, comp_against, delta_output)



def read_asset_info_file(report_on):
#reads inforamtion from file and extracts meaingful information
     bigfix_report = 'report_output.dem'
     f = open(bigfix_report, 'w')
     report_output = open(bigfix_report, 'a')
     header = 'Computer Name;Operating System;IP Address;Asset Type;Last Report Time;Big_Fix_Asset URL\n'
     report_output.write(header)
     report_output.close()

     newf = open(report_on, 'r')
     for line_in_newf in newf:
          asset_url = line_in_newf.rstrip()
        #  print(asset_url)
          get_asset_info = requests.get(asset_url, verify=False, auth=(username, password))
       #   print(get_asset_info.text)
          asset_info = open(bigfix_asset_info_cache_file, 'w')
          asset_info.write(get_asset_info.text)
          asset_info.close()
          infile = bigfix_asset_info_cache_file
          #infile = 'asset_info.txt'
          fileobj = open(infile, 'r')
          out= fileobj.readlines()
          for line in out:
               match =re.match("(.*<Property Name=\"Computer Name\".*>)", str(line))
               if match != None:
                  #  print(match.group(0))
                    soup = BeautifulSoup(line, 'lxml')
                 #   print(soup.text)
                    computer_name = soup.text
               match =re.match("(.*<Property Name=\"OS\".*>)", str(line))
               if match != None:
                #    print(match.group(0))
                    soup = BeautifulSoup(line, 'lxml')
                #    print(soup.text)
                    operating_system  = soup.text
               match =re.match("(.*<Property Name=\"IP Address\".*>)", str(line))
               if match != None:
                #    print(match.group(0))
                    soup = BeautifulSoup(line, 'lxml')
                 #   print(soup.text)
                    ip_addr  = soup.text
               match =re.match("(.*<Property Name=\"License Type\".*>)", str(line))
               if match != None:
                 #   print(match.group(0))
                    soup = BeautifulSoup(line, 'lxml')
                 #   print(soup.text)
                    asset_type  = soup.text
               match =re.match("(.*<Property Name=\"Last Report Time\".*>)", str(line))
               if match != None:
                  #  print(match.group(0))
                    soup = BeautifulSoup(line, 'lxml')
                  #  print(soup.text)
                    report_time  = soup.text
          fileobj.close()
          data =      computer_name.rstrip()+';'+operating_system.rstrip()+';'+ip_addr.rstrip()+';'+asset_type.rstrip()+';'+report_time.rstrip()+';'+asset_url+'\n'
          print(data)
          report_output = open(bigfix_report, 'a')
          report_output.write(data)
          report_output.close()



def gen_asset_report(rep_type):
    if rep_type == 'new':
       #updates everything and gives you entire inventory
       update_hist='true'
       init_cache()
       get_asset_url(username, password)
       read_bigfix_url_file(update_hist)
       report_on = '.bigfix_inv_asset_url_list.cache'
       read_asset_info_file(report_on)
    elif rep_type == 'last':
       #nothing is updated runs off last inventory cache file
       update_hist='false'
       report_on = '.bigfix_inv_asset_url_list.cache'
       read_asset_info_file(report_on)
    elif rep_type == 'current':
       #pulls new inventory list from bigfix and reports on it.  History file is not updated
       update_hist='false'
       init_cache()
       get_asset_url(username, password)
       read_bigfix_url_file(update_hist)
       report_on = '.bigfix_inv_asset_url_list.cache'
       read_asset_info_file(report_on)
    elif rep_type == 'new_servers':
       #pulls new inventory list from bigfix and compares against history file
       update_hist='false'
       init_cache()
       get_asset_url(username, password)
       read_bigfix_url_file(update_hist)
       find_new_assets()
       report_on = '.bigfix_temp_asset_url_list.cache'
       read_asset_info_file(report_on)
    elif rep_type == 'new_servers_hist_upd':
       #pulls new inventory list from bigfix and compares  against an updated history file
       update_hist='true'
       init_cache()
       get_asset_url(username, password)
       read_bigfix_url_file(update_hist)
       find_new_assets()
       report_on = '.bigfix_temp_asset_url_list.cache'
       read_asset_info_file(report_on)
    elif rep_type == 'decom_servers':
       #pulls Decom from bigfix history file and compares against new inventory file
       update_hist='false'
       init_cache()
       get_asset_url(username, password)
       read_bigfix_url_file(update_hist)
       find_decom_assets()
       report_on = '.bigfix_temp_asset_url_list.cache'
       read_asset_info_file(report_on)
    elif rep_type == 'decom_servers_hist_upd':
       #pulls Decom from updated bigfix history file and compares against new inventory file
       update_hist='true'
       init_cache()
       get_asset_url(username, password)
       read_bigfix_url_file(update_hist)
       find_decom_assets()
       report_on = '.bigfix_temp_asset_url_list.cache'
       read_asset_info_file(report_on)
    elif rep_type == 'history':
       #pulls new inventory list from bigfix and compares against an updated history file
       #currently if you run with out a history file this will crash
       report_on = '.bigfix_old_asset_url_list.cache'
       read_asset_info_file(report_on)




#########Order of Operations#####

username = input("Please Enter Username: ")
password = getpass.getpass()

#init_cache()
#get_asset_url(username, password)
#update_hist = 'true'
#update_history(update_hist)
#find_new_assets()
#find_decom_assets()
#read_bigfix_url_file(update_hist)
#report_on = bigfix_inv_asset_url_cache_file
#read_asset_info_file(report_on)

rep_type = 'new'
gen_asset_report(rep_type)
