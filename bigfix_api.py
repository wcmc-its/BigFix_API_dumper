#!/usr/bin/env python3

# This script pulls from Bigfix API, and outputs All systems into csv format.
# Written by: Brian Whelan and Bryan Fisher
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
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)





# relevance query stuff

class RelevanceQueryDumper():
    """ class to handle interfacing with the BigFix relevance api """

    def __init__(self, relevance_api_url, relevance_api_username, relevance_api_password):
        self.relevance_api_session = requests.session(
            auth=(relevance_api_username,relevance_api_password),
            verify=False)
        self.relevance_api_url = relevance_api_url

    def build_relevance_query(self, fields):
        """ takes in a list of fields to query from BigFix,
        returns a relevance query to send to BigFix"""
        query = ""
        return query

    def query_relevance_api(self, query):
        """ takes in a query, returns its raw output """
        api_output = ""
        return api_output

    def parse_api_output(self, api_xml):
        """ take in raw output from the API, return a dictionary """
        return parsed_output

    def dump(self, fields):
        """ takes in a list of fields to query, returns a dictionary of the output """
        # build a query
        # query the api
        # parse the output
        return output 






# REST API stuff

# Initializes cache files
bigfix_new_asset_url_cache_file = '.bigfix_new_asset_url_list.cache'
bigfix_old_asset_url_cache_file = '.bigfix_old_asset_url_list.cache'
bigfix_diff_asset_url_cache_file = '.bigfix_temp_asset_url_list.cache'
bigfix_inv_asset_url_cache_file = '.bigfix_inv_asset_url_list.cache'
bigfix_asset_info_cache_file = '.bigfix_asset_info.cache'

def init_cache():
    # Intiallize Cache files.  This should only be run once perday
    if __debug__:
        print("Initializing cache")
    try:
        f = open(bigfix_new_asset_url_cache_file)
        f.close()
    except IOError as e:
        f = open(bigfix_new_asset_url_cache_file, 'w')
        f.close()


def get_asset_url(username, password):
    # Function expects the username and password
    # calls Bigfix to get the URL list of machines
    if __debug__:
        print("getting asset URLs")
    f = open(bigfix_new_asset_url_cache_file, 'w')
    f.close()
    response = requests.get(bigfix_url, verify=False,
                            auth=(username, password))
    # print(response.text)
    f = open(bigfix_new_asset_url_cache_file, 'a')
    f.write(response.text)
    f.close()


def update_history(update_hist):
    # creats inventory file if it does not exist, also copies it to History.  History is used for comparison New and Decom
    try:
        f = open(bigfix_inv_asset_url_cache_file)
        f.close()
    except IOError as e:
        f = open(bigfix_inv_asset_url_cache_file, 'w')
        f.close()
    if update_hist == 'true':
        # copies new cache to old
        copyfile(bigfix_inv_asset_url_cache_file,
                 bigfix_old_asset_url_cache_file)


def read_bigfix_url_file(update_hist):
    # Reads file containaing BigFix URL's and parses out the URL for that asset outputs to inventory file
    outfile = open(bigfix_inv_asset_url_cache_file,
                   'w')  # raw asset url output file
    cache_file = open(bigfix_new_asset_url_cache_file, 'r')  # raw BF output
    cache_soup = BeautifulSoup(cache_file, 'lxml')  # soupify raw BF output
    # extract the computer computer records
    computer_records = cache_soup.find_all('computer')
    if __debug__:
        print(f"extracted {len(computer_records)} computer records")
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
        null = ''
    #     break
    newf = open(search_for, 'r')
    for line_in_newf in newf:
        search_url_exsits = line_in_newf.rstrip()
        if search_url_exsits not in open(comp_against).read():
            output = open(delta_output, 'a')
            output.write(search_url_exsits + '\n')
            output.close()

    newf.close()


def find_new_assets():
    # compair two files and output
    search_for = '.bigfix_inv_asset_url_list.cache'
    comp_against = '.bigfix_old_asset_url_list.cache'
    delta_output = '.bigfix_temp_asset_url_list.cache'
    comp_assets(search_for, comp_against, delta_output)


def find_decom_assets():
    # compair two files and output
    search_for = '.bigfix_old_asset_url_list.cache'
    comp_against = '.bigfix_inv_asset_url_list.cache'
    delta_output = '.bigfix_temp_asset_url_list.cache'
    comp_assets(search_for, comp_against, delta_output)


def read_asset_info_file(report_on):
    # reads inforamtion from a file containing a list of BF asset URLs and extracts meaingful information,
    # then writes them to a delimeted report file
    bigfix_report = 'report_output.dem' # report output file
    report_output = open(bigfix_report, 'w')
    # header for report
    header = 'Computer Name;Operating System;IP Address;Asset Type;Last Report Time;Big_Fix_Asset URL\n'
    report_output.write(header)

    url_list = open(report_on, 'r')

    for raw_url in url_list:
        # remove trailing newline
        asset_url = raw_url.rstrip()
        # print(asset_url)
        # request asset from BigFix
        asset_info_request = requests.get(
            asset_url, verify=False, auth=(username, password))
            # print(get_asset_info.text)
        # make soup
        asset_soup = BeautifulSoup(asset_info_request.text, 'lxml')

        # extract relevant information
        computer_name = asset_soup.find_all('property', {'name': 'Computer Name'})[0].text
        operating_system = asset_soup.find_all('property', {'name': 'OS'})[0].text
        ip_addr = asset_soup.find_all('property', {'name': 'IP Address'})[0].text
        asset_type = asset_soup.find_all('property', {'name': 'License Type'})[0].text
        report_time = asset_soup.find_all('property', {'name': 'Last Report Time'})[0].text

        # compile a line to write, and write it to our report
        data = computer_name.rstrip() + ';' + operating_system.rstrip() + ';' + ip_addr.rstrip() + \
            ';' + asset_type.rstrip() + ';' + report_time.rstrip() + ';' + asset_url + '\n'
        if __debug__:
            print(data)
        report_output.write(data)
    report_output.close()


def gen_asset_report(rep_type):
    if rep_type == 'new':
     # updates everything and gives you entire inventory
        update_hist = 'true'
        init_cache()
        get_asset_url(username, password)
        read_bigfix_url_file(update_hist)
        report_on = '.bigfix_inv_asset_url_list.cache'
        read_asset_info_file(report_on)
    elif rep_type == 'last':
        # nothing is updated runs off last inventory cache file
        update_hist = 'false'
        report_on = '.bigfix_inv_asset_url_list.cache'
        read_asset_info_file(report_on)
    elif rep_type == 'current':
        # pulls new inventory list from bigfix and reports on it.  History file is not updated
        update_hist = 'false'
        init_cache()
        get_asset_url(username, password)
        read_bigfix_url_file(update_hist)
        report_on = '.bigfix_inv_asset_url_list.cache'
        read_asset_info_file(report_on)
    elif rep_type == 'new_servers':
        # pulls new inventory list from bigfix and compares against history file
        update_hist = 'false'
        init_cache()
        get_asset_url(username, password)
        read_bigfix_url_file(update_hist)
        find_new_assets()
        report_on = '.bigfix_temp_asset_url_list.cache'
        read_asset_info_file(report_on)
    elif rep_type == 'new_servers_hist_upd':
        # pulls new inventory list from bigfix and compares  against an updated history file
        update_hist = 'true'
        init_cache()
        get_asset_url(username, password)
        read_bigfix_url_file(update_hist)
        find_new_assets()
        report_on = '.bigfix_temp_asset_url_list.cache'
        read_asset_info_file(report_on)
    elif rep_type == 'decom_servers':
        # pulls Decom from bigfix history file and compares against new inventory file
        update_hist = 'false'
        init_cache()
        get_asset_url(username, password)
        read_bigfix_url_file(update_hist)
        find_decom_assets()
        report_on = '.bigfix_temp_asset_url_list.cache'
        read_asset_info_file(report_on)
    elif rep_type == 'decom_servers_hist_upd':
        # pulls Decom from updated bigfix history file and compares against new inventory file
        update_hist = 'true'
        init_cache()
        get_asset_url(username, password)
        read_bigfix_url_file(update_hist)
        find_decom_assets()
        report_on = '.bigfix_temp_asset_url_list.cache'
        read_asset_info_file(report_on)
    elif rep_type == 'history':
        # pulls new inventory list from bigfix and compares against an updated history file
        # currently if you run with out a history file this will crash
        report_on = '.bigfix_old_asset_url_list.cache'
        read_asset_info_file(report_on)


#########Order of Operations#####
if __name__ == "__main__":
    import argparse
    import configparser
    # init_cache()
    #get_asset_url(username, password)
    #update_hist = 'true'
    # update_history(update_hist)
    # find_new_assets()
    # find_decom_assets()
    # read_bigfix_url_file(update_hist)
    #report_on = bigfix_inv_asset_url_cache_file
    # read_asset_info_file(report_on)

    # default values before getting user input
    username = None
    password = None
    bigfix_url = None

    # get some info from the user about what we should be doing
    parser = argparse.ArgumentParser(
        description = "Get a bunch of stuff from BigFix",
        epilog = """
        By default, this script will attempt to input default
        values from a config file named "bigfix_config.conf."
        If this file is missing and none is specified via the
        argument, the script will ask for input on the CLI.
        If a config file is present and other arguments are
        specified, the values specified in the arguments will
        be used.
        """
    )
    parser.add_argument('-c', '--config', help="config file.")
    parser.add_argument('-u', '--user', help="API username")
    parser.add_argument('-p', '--password', help="API password. If not specified here or in \
                        the config file, it will be requested on the CLI")
    parser.add_argument('-s', help="Force asking for password securely on CLI", action="store_true")
    parser.add_argument('-r', '--rep_type',
                        help="Report Type",
                        default='new',
                        choices=['new', 'last', 'current', 'new_servers', 'new_server_hist_upd',
                        'decom_servers', 'decom_server_hist_upd', 'history'])
    args = parser.parse_args()

    # try to read in values from an assumed config file
    try:
        config = configparser.ConfigParser()
        config.read('bigfix_config.conf')
        try:
            bigfix_url = config["DEFAULT"]["bigfix_api_url"]
        except:
            pass
        try:
            username = config["DEFAULT"]["username"]
        except:
            pass
        try:
            password = config["DEFAULT"]["password"]
        except:
            pass
    except:
        config = None

    # read a config file specified by the user
    if args.config:
        config = configparser.ConfigParser()
        config.read(args.config)
        try:
            bigfix_url = config["DEFAULT"]["bigfix_api_url"]
        except:
            pass
        try:
            username = config["DEFAULT"]["username"]
        except:
            pass
        try:
            password = config["DEFAULT"]["password"]
        except:
            pass

    # did we get a username from the user?
    if args.user:
        username = args.user
    # same for password, with secure input handling
    if args.s:
        password = getpass.getpass()
    elif args.password:
        password = args.password

    # fall back to requesting input directly from the user
    if not username:
        username = input("Please Enter Username: ")
    if not password:
        password = getpass.getpass()

    # finally do the things
    gen_asset_report(args.rep_type)
