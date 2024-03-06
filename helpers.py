import shutil, os
from urllib.parse import urlparse
from settings import mimes, files
import re
import json
import pathlib
import sys


def delete_folder(dst):
    pth = pathlib.Path(dst)
    for sub in pth.iterdir():
        if sub.is_dir():
            delete_folder(sub)
        else:
            sub.unlink()
    pth.rmdir()

def create_project(project_name):

    # try:
    #     shutil.rmtree("./projects/")
    # except:
    #     pass
    if os.path.exists("./projects") == False:
        os.mkdir("./projects")

    if os.path.exists("./projects/" + project_name) == False:
        print("[*] Creating project ...")
        os.mkdir("./projects/" + project_name)
        os.mkdir("./projects/" + project_name + "/requests_pickles")
        os.mkdir("./projects/" + project_name + "/origins")
        f = open("./projects/" + project_name + "/origins_conf.json", "w")
        f.write(json.dumps({}))
        f.close()
        f = open("./projects/" + project_name + "/just_one_no_more_patterns.txt", "w")
        f.write(json.dumps([]))
        f.close()
        f = open("./projects/" + project_name + "/links_found.json", "w")
        f.write(json.dumps([]))
        f.close()
        print("[+] Project created {}".format(project_name))
    else:
        while True:
            q = input("[*] Porject exists, What do you wanna do ? [N]ew name, [D]elete previous project, [C]ontinue last project ")
            if q == "n" or q == "N":
                while True:
                    p = input("[*] Enter new project name: [Not {}] ".format(project_name))
                    if p != project_name and os.path.exists("./projects/" + p) == False:
                        print("[*] Creating project ...")
                        os.mkdir("./projects/" + p)
                        os.mkdir("./projects/" + p + "/requests_pickles")
                        os.mkdir("./projects/" + p + "/origins")
                        f = open("./projects/" + p + "/origins_conf.json", "w")
                        f.write(json.dumps({}))
                        f.close()
                        f = open("./projects/" + p + "/just_one_no_more_patterns.txt", "w")
                        f.write(json.dumps([]))
                        f.close()
                        f = open("./projects/" + p + "/links_found.json", "w")
                        f.write(json.dumps([]))
                        f.close()
                        print("[+] Project created {}".format(p))
                        project_name = p
                        break
                    else:
                        print("[*] Enter a new name please ...")
            elif q == "D" or q == "d":
                print("[*] Delete previous project ...")
                delete_folder("./projects/" + project_name)
                print("[*] Creating project ...")
                os.mkdir("./projects/" + project_name)
                os.mkdir("./projects/" + project_name + "/requests_pickles")
                os.mkdir("./projects/" + project_name + "/origins")
                f = open("./projects/" + project_name + "/origins_conf.json", "w")
                f.write(json.dumps({}))
                f.close()
                f = open("./projects/" + project_name + "/just_one_no_more_patterns.txt", "w")
                f.write(json.dumps([]))
                f.close()
                f = open("./projects/" + project_name + "/links_found.json", "w")
                f.write(json.dumps([]))
                f.close()
                print("[+] Project created {}".format(project_name))
                break
            elif q == "C" or q == "c":
                print("[*] Ok, Continue the last project .")
                print("[*] Checking for last project files and folders ...")
                if os.path.exists("./projects/" + project_name): print("[+] Project folder exists .") 
                else: 
                    print("[-] Project structure is corupted .")
                    sys.exit(0)
                if os.path.exists("./projects/" + project_name + "/origins"): print("[+] {}/origins folder exists .".format(project_name))
                else:
                    print("[-] {}/origins does not exists, Project is corrupted .")
                    sys.exit(0)
                if os.path.exists("./projects/" + project_name + "/requests_pickles"): print("[+] ./projects/" + project_name + "/requests_pickles folder exists .")
                else:
                    print("[-] ./projects/" + project_name + "/requests_pickles does not exists, Project is corrupted .")
                    sys.exit(0)
                if os.path.exists("./projects/" + project_name + "/origins_conf.json"): print("[+] ./projects/" + project_name + "/origins_conf.json file exists .")
                else:
                    print("[-] ./projects/" + project_name + "/origins_conf.json does not exists, project is corrupted .")
                    sys.exit(0)
                if os.path.exists("./projects/" + project_name + "/just_one_no_more_patterns.txt"): print("[+] ./projects/" + project_name + "/just_one_no_more_patterns.txt exists .")
                else:
                    print("[-] ./projects/" + project_name + "/just_one_no_more_patterns.txt does not exists . Project is corrupted .")
                    sys.exit(0)
                if os.path.exists("./projects/" + project_name + "/links_found.json"): print("[+]./projects/" + project_name + "/links_found.json exists .")
                else:
                    print("[-] ./projects/" + project_name + "/links_found.json does not exists . Project is corrupted .")
                    sys.exit(0)
                break
            else:
                continue
            break
    
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