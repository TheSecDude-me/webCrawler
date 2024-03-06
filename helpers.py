import shutil, os
from urllib.parse import urlparse
from settings import mimes, files
import re
import json

def create_project(project_name):

    try:
        shutil.rmtree("./projects/")
    except:
        pass
    if os.path.exists("./projects") == False:
        os.mkdir("./projects")

    if os.path.exists("./projects/" + project_name) == False:
        print("[*] Creating project ...")
        os.mkdir("./projects/" + project_name)
        os.mkdir("./projects/" + project_name + "/requests_pickles")
        os.mkdir("./projects/" + project_name + "/origins")
        print("[+] Project created {}".format(project_name))
    else:
        while True:
            project_name = input("[*] Porject exists, Enter a new name for your project: [Not {}]".format(project_name))
            if os.path.exists("./projects/" + project_name) == False:
                os.mkdir("./projects/" + project_name)
                break
    
    if os.path.exists("./projects/" + project_name + "/just_one_no_more_patterns.txt") == False:
        with open("./projects/" + project_name + "/just_one_no_more_patterns.txt", "w") as f_:
            patterns = []
            while True:
                pattern = input("If there is any pattern of URL that you want to crawl once, please write it here as regex: [Blank to pass] ")
                if pattern == "":
                    break

                error = ""
                while True:
                    if error != "":
                        example = input(error + " - Enter an example for your regex pattern : [Enter to leave] ")
                    else:
                        example = input("Enter an example for your regex pattern : [Enter to leave] ")
                    if example == "":
                        break
                    try:
                        re.search(pattern, example).string
                        break
                    except AttributeError:
                        error = "[Not match]"
                        continue
                patterns.append({
                    'pattern': pattern,
                    'example': example
                })
            f_.write(json.dumps(patterns))
        

def is_file(name):
    try:
        ext = "." + name.split(".")[-1]
        fileType = [y['name'] for y in mimes if ext in y['fileTypes']]
        if len([y for y in files if y in fileType[0]]) != 0:
            return True
        return False
    except:
        return False
    

def add_link(links, link):
    if len([x for x in links if urlparse(url=link).scheme + "://" + urlparse(url=link).netloc + urlparse(url=link).path + urlparse(url=link).params + urlparse(url=link).query in x['link']]) == 0:
        links.append({
            "link": link,
            "checked": 0
        })
    return links