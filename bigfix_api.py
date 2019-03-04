#!/opt/rh/rh-python36/root/usr/bin/python
# This script pulls from Bigfix API, and outputs All systems into csv format.
# Written by: Brian Whelan
# v1.0
import requests
import getpass
import re
from bs4 import BeautifulSoup
import lxml
import urllib3
import os
import sys
from shutil import copyfile
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#Initializes cache files
bigfix_new_asset_url_cache_file = '.bigfix_new_asset_url_list.cache'
bigfix_old_asset_url_cache_file = '.bigfix_old_asset_url_list.cache'
bigfix_diff_asset_url_cache_file = '.bigfix_temp_asset_url_list.cache'
bigfix_inv_asset_url_cache_file = '.bigfix_inv_asset_url_list.cache'
bigfix_asset_info_cache_file = '.bigfix_asset_info.cache'


#url
my_url = 'my_url'

def init_cache(update_hist):
    #Intiallize Cache files.  This should only be run once perday
    try:
        f = open(bigfix_new_asset_url_cache_file)
        f.close()
            except IOError as e:
                f = open(bigfix_new_asset_url_cache_file, 'w')
                f.close()
                    if update_hist == 'true':
                        #copies new cache to old
                        copyfile(bigfix_new_asset_url_cache_file, bigfix_old_asset_url_cache_file)
                            f = open(bigfix_new_asset_url_cache_file, 'w')
                            f.close()

def get_asset_url(username, password):
    #Function expects the username and password
    #calls Bigfix to get the URL list of machines
    f = open(bigfix_new_asset_url_cache_file, 'w')
    f.close()
    response = requests.get(my_url, verify=False, auth=(username, password))
    #print(response.text)
    f = open(bigfix_new_asset_url_cache_file, 'a')
        f.write(response.text)
        f.close()

def read_bigfix_url_file():
    #Reads file containaing BigFix URL's and parses out the URL for that asset outputs to inventory file
    #infile = 'big_fix_url.txt'
    infile = bigfix_new_asset_url_cache_file
        outfile = open(bigfix_inv_asset_url_cache_file, 'w')
        outfile.close()
        fileobj = open(infile, 'r')
        out= fileobj.readlines()
        for line in out:
            soup = BeautifulSoup(line, 'lxml')
            #print(soup.computer)
            if soup.computer != None:
                #    print(soup.computer)
                print(soup.computer.get('resource'))
                outfile = open(bigfix_inv_asset_url_cache_file, 'a')
                outfile.write(soup.computer.get('resource')+'\n')
                outfile.close()
                    # asset_url = soup.computer.get('resource')
                    fileobj.close()


def read_asset_info_file(report_on):
    #reads inforamtion from file and extracts meaingful information
    bigfix_report = 'report_output.dem'
        f = open(bigfix_report, 'w')
        report_output = open(bigfix_report, 'a')
        header = 'Computer Name;Operating System;IP Address;Asset Type;Last Report Time\n'
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
                                                                                    data =      computer_name.rstrip()+';'+operating_system.rstrip()+';'+ip_addr.rstrip()+';'+asset_type.rstrip()+';'+report_time.rstrip()+'\n'
                                                                                    print(data)
                                                                                    report_output = open(bigfix_report, 'a')
                                                                                    report_output.write(data)
                                                                                    report_output.close()




#########Order of Operations#####

username = input("Please Ent`er Username: ")
password = getpass.getpass()


update_hist = 'true'
init_cache(update_hist)
get_asset_url(username, password)
read_bigfix_url_file()
report_on = bigfix_inv_asset_url_cache_file
read_asset_info_file(report_on)
