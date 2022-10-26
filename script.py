#!/usr/bin/env python3

"""
Github repository cloner
"""

import requests
import json
import os
import urllib.request

USERNAME = "jxmked"

FOLDER = "zipball"
GH_AUTH_TOKEN = ""

def mkdirs(path):
    os.makedirs(path, exist_ok=True)

api_left = 0 # Api remaining

def fetch(url):
    global api_left
    
    # Fetch json file from Github REST api
    
    if GH_AUTH_TOKEN:
        headers = {
            "Authorization": "token %s" % GH_AUTH_TOKEN
        }
    else:
        headers = {}
    
    response = requests.get(url, headers)
    
    # Restricted / ratelimit exceeded - 403
    
    if not response.status_code == 200:
        return {}
    
    api_left = response.headers.get("x-ratelimit-remaining")
    
    return json.loads(response.text)


class ZipballRepositories:
    
    def __init__(self, username, outdir):
        self.username = username
        self.outdir = outdir
        
        self.repositories = []
        
        self.per_page = 100
        self.get_all_repos()
        self.start_download()
        
    
    def start_download(self):
        print("Repositories count %d" % len(self.repositories))
        
        for repo in self.repositories:
            self.download(repo.get("html_url"), repo.get("default_branch"), repo.get("name"))
    
    def get_all_repos(self):
        print("Getting all Repositories...")
        
        base_url = "https://api.github.com/users/%s/repos?per_page=%s" % (self.username, self.per_page)
        
        page = 1
        repos = []
        
        while True:
            req_url = "%s&page=%s" % (base_url, page)
            
            res_repo = fetch(req_url)
        
            repos += res_repo
            
            if len(res_repo) < self.per_page:
                self.repositories = repos
                break
            
            page += 1
        
    
    def download(self, repo, branch, name):
        print("Downloading... {}".format(repo))
        
        url = "{}/zipball/{}".format(repo, branch)
        out = "{}/{}/{}.zip".format(self.username, self.outdir, name)
        
        urllib.request.urlretrieve(url, out)


if __name__ == "__main__":
    
    print("Starting...")
    
    mkdirs(FOLDER)
    
    mkdirs("{}/{}".format(FOLDER, USERNAME))
    
    ZipballRepositories(USERNAME, FOLDER)
    

# # # # # # # # # # # # # #
# Github Username: jxmked #
# # # & # # # # # # # # # #
