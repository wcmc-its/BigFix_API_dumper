#!/opt/rh/rh-python36/root/usr/bin/python
# This script pulls from Bigfix API, and outputs All systems into csv format.
# Written by: Brian Whelan
# v1.0
import requests
import getpass
import xml.etree.ElementTree as ET
import urllib3
import os
from shutil import copyfile
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)




#Initializes cache files
bigfix_new_asset_url_cache_file = '.bigfix_new_asset_url_list.cache'
bigfix_old_asset_url_cache_file = '.bigfix_old_asset_url_list.cache'
bigfix_diff_asset_url_cache_file = '.bigfix_temp_asset_url_list.cache'


############ ENGINE ######

def write_assets_to_cache(asset_url, cache_file):
     f = open(cache_file, 'a')
     f.write(asset_url+'\n')
     f.close()

def get_asset_url(username, password):
#Function expects the username and password
#bigfix URL:
url='URL'
#calls Bigfix to get the URL list of machines
     os.remove(bigfix_new_asset_url_cache_file)
     response = requests.get(url, verify=False, auth=(username, password))
     root = ET.fromstring(response.text)
#pull the Asset URL from the bigix XML parse
     for xml_info in root.findall('Computer'):
           asset_url = xml_info.get('Resource')
           #print(asset_url)
           cache_file = bigfix_new_asset_url_cache_file
           write_assets_to_cache(asset_url, cache_file)



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
          search_url_exists = line_in_newf.rstrip()
          if search_url_exists not in open(comp_against).read():
               output = open(delta_output, 'a')
               output.write(search_url_exists)
               output.close()

     newf.close()

def report_engine(report_on):
     bigfix_report = 'report_output.csv'     
     try:
          f = open(bigfix_report)
          f.close()
          os.remove(bigfix_report)
     except IOError as e:
          null=''

     report_output = open(bigfix_report, 'a')
     header = 'Computer Name;Operating System;IP Address;Asset Type;Last Report Time\n'
     #print(header)
     report_output.write(header)
     report_output.close()
     newf = open(report_on, 'r')
     for line_in_newf in newf:
          asset_url = line_in_newf.rstrip()
         # print(asset_url)
          get_asset_info = requests.get(asset_url, verify=False, auth=(username, password))
          #Parse XML for meaningfull information
          bigfix_asset_info = ET.fromstring(get_asset_info.text)
          for asset_xml_output in bigfix_asset_info.findall('Computer'):
               for child in asset_xml_output:
                    # Pull out Asset information
                    name = child.get('Name')
                    if name == 'Computer Name':
                         computer_name = child.text
                    elif name == 'OS':
                         operating_system = child.text
                    elif name == 'IP Address':
                         ip_addr = child.text
                    elif name == 'License Type':
                         asset_type = child.text
                    elif name == 'Last Report Time':
                         report_time = child.text
          data = computer_name+';'+operating_system+';'+ip_addr+';'+asset_type+';'+report_time+'\n' 
         # print(data)
          report_output = open(bigfix_report, 'a')
          report_output.write(data)
          report_output.close()




###### ENGINE#################

######### API Function Calls #####
def init_cache(update_hist):
#Intiallize Cache files.  This should only be rin once perday and should be part of Chon
     #checks to see if new cache file exists, if not it creates it this is to avoid error if it is the first time running
     try:
         f = open(bigfix_new_asset_url_cache_file)
         f.close()
     except IOError as e:
         f = open(bigfix_new_asset_url_cache_file, 'w')
         f.close()
     if update_hist == 'true':
         #copies new cache to old
         copyfile(bigfix_new_asset_url_cache_file, bigfix_old_asset_url_cache_file)
     #deletes new cache file
     os.remove(bigfix_new_asset_url_cache_file)


def get_asset_url(username, password):
#Function expects the username and password
#calls Bigfix to get the URL list of machines
     update_hist = 'false'
     init_cache(update_hist)
     response = requests.get('***REMOVED***', verify=False, auth=(username, password))
     root = ET.fromstring(response.text)
#pull the Asset URL from the bigix XML parse
     for xml_info in root.findall('Computer'):
           asset_url = xml_info.get('Resource')
           #print(asset_url)
           cache_file = bigfix_new_asset_url_cache_file
           write_assets_to_cache(asset_url, cache_file)


def find_new_assets():
     search_for =  '.bigfix_new_asset_url_list.cache' 
     comp_against = '.bigfix_old_asset_url_list.cache' 
     delta_output = '.bigfix_temp_asset_url_list.cache'
     comp_assets(search_for, comp_against, delta_output)


def find_decom_assets():
     search_for =  '.bigfix_old_asset_url_list.cache'
     comp_against = '.bigfix_new_asset_url_list.cache'
     delta_output = '.bigfix_temp_asset_url_list.cache'
     comp_assets(search_for, comp_against, delta_output)


def gen_asset_report(rep_type):
    if rep_type == 'current':
       update_hist='false'
       init_cache(update_hist)
       get_asset_url(username, password)
       report_on =  '.bigfix_new_asset_url_list.cache'
       report_engine(report_on)
      # print("hello")
    elif rep_type == 'new':
       update_hist='false'
       init_cache(update_hist)
       get_asset_url(username, password)
       find_new_assets()
       report_on =  '.bigfix_temp_asset_url_list.cache'
       report_engine(report_on)
      # print("hello")
    elif rep_type == 'new_w_cache':
       update_hist='true'
       init_cache(update_hist)
       get_asset_url(username, password)
       find_new_assets()
       report_on =  '.bigfix_temp_asset_url_list.cache'
       report_engine(report_on)
      # print("hello")
    elif rep_type == 'decom':
       update_hist='false'
       init_cache(update_hist)
       get_asset_url(username, password)
       find_decom_assets()
       report_on =  '.bigfix_temp_asset_url_list.cache'
       report_engine(report_on)
      # print("hello")
    elif rep_type == 'decom_w_cache':
       update_hist='true'
       init_cache(update_hist)
       get_asset_url(username, password)
       find_new_assets()
       report_on =  '.bigfix_temp_asset_url_list.cache'
       report_engine(report_on)
       # print("hello")
    elif rep_type == 'history':
       report_on =  '.bigfix_old_asset_url_list.cache'
       report_engine(report_on)


#############API########


#########Order of Operations#####

username = input("Please Enter Username: ")
password = getpass.getpass()

update_hist='true'
init_cache(update_hist)
get_asset_url(username, password)
find_new_assets`()
find_decom_assets()
rep_type = 'current'
gen_asset_report(rep_type)
