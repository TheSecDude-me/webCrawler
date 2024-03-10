import os
from urllib.parse import urlparse
from settings import mimes, files, project_files, project_dirs
import re
import json
import pathlib
import sys

def init_settings(settings, project_name):
    print("init_settings ...")
    if settings['origin_contains']:
        if len(settings["origin_contains_list"]) == 0:
            while True:
                origin_contains_str = input("[*] Enter a string for origin contains: [Separate them with , like site,web,blog] ")
                if origin_contains_str != "":
                    break
            origin_contains_list = [y.replace(" ", "") for y in origin_contains_str.split(",")]
            settings["origin_contains_list"] = origin_contains_list
            with open("./projects/" + project_name + "/settings.json", "w") as f_:
                f_.write(json.dumps(settings))
    return settings

def init_origins_conf(settings, project_name):
    print("init origins_conf ...")
    with open("./projects/" + project_name + "/origins_conf.json", "r") as f_:
        origins_conf = json.loads(f_.read())
        if len(origins_conf) == 0:
            origins_conf["allowed"].append(urlparse(settings['url']).scheme + "://" + urlparse(settings['url']).netloc + "/")
            with open("./projects/" + project_name + "/origins_conf.json", "w") as f_:
                    f_.write(json.dumps(origins_conf))
    return origins_conf

def init_url_regex_patterns(project_name):
    print("init url_regex_patterns...")
    with open("./projects/" + project_name + "/url_regex_patterns.json", "r") as f_:
        url_regex_patterns = json.loads(f_.read())
        if len(url_regex_patterns) == 0:
            with open("./projects/" + project_name + "/url_regex_patterns.json", "w") as f_:
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
    return url_regex_patterns






def delete_folder(dst):
    pth = pathlib.Path(dst)
    for sub in pth.iterdir():
        if sub.is_dir():
            delete_folder(sub)
        else:
            sub.unlink()
    pth.rmdir()

def create_project(project_name, settings):
    if os.path.exists("./projects") == False:
        os.mkdir("./projects")

    if os.path.exists("./projects/" + project_name) == False:
        print("[*] Creating project ...")
        os.mkdir("./projects/" + project_name)

        for d in project_dirs: # Creating project directories
            os.mkdir("./projects/" + project_name + "/" + d)

        for f in project_files: # Creating project files
            with open("./projects/" + project_name + "/" + f['file_name'], "w") as f_:
                f_.write(json.dumps(f['content']))
        
        with open("./projects/" + project_name + "/settings.json", "w") as f_:
            f_.write(json.dumps(settings))

        init_settings(settings=settings, project_name=project_name)
        init_origins_conf(settings=settings, project_name=project_name)
        init_url_regex_patterns(project_name=project_name)

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


                        for d in project_dirs: # Creating project directories
                            os.mkdir("./projects/" + p + "/" + d)
                        for f in project_files:
                            with open("./projects/" + p + "/" + f['file_name'], "w") as f_:
                                f_.write(json.dumps(f['content']))

                        with open("./projects/" + project_name + "/settings.json", "w") as f_:
                            f_.write(json.dumps(settings))


                        project_name = p
                        init_settings(settings=settings, project_name=project_name)
                        init_origins_conf(settings=settings, project_name=project_name)
                        init_url_regex_patterns(project_name=project_name)
                        print("[+] Project created {}".format(p))
                        break
                    else:
                        print("[*] Enter a new name please ...")
            elif q == "D" or q == "d":
                print("[*] Delete previous project ...")
                delete_folder("./projects/" + project_name)
                print("[*] Creating project ...")
                os.mkdir("./projects/" + project_name)
                for d in project_dirs: # Creating project directories
                    os.mkdir("./projects/" + project_name + "/" + d)
                for f in project_files:
                    with open("./projects/" + project_name + "/" + f['file_name'], "w") as f_:
                        f_.write(json.dumps(f['content']))
        
                with open("./projects/" + project_name + "/settings.json", "w") as f_:
                    f_.write(json.dumps(settings))

                init_settings(settings=settings, project_name=project_name)
                init_origins_conf(settings=settings, project_name=project_name)
                init_url_regex_patterns(project_name=project_name)

                print("[+] Project created {}".format(project_name))
                break
            elif q == "C" or q == "c":
                print("[*] Ok, Continue the last project .")
                print("[*] Checking for last project files and folders ...")

                if os.path.exists("./projects/" + project_name): print("[+] Project folder exists .") 
                else: 
                    print("[-] Project structure is corupted .")
                    sys.exit(0)

                for d in project_dirs: # checking project directories
                    if os.path.exists("./projects/" + project_name + "/" + d): print("[+] {}/{} folder exists .".format(project_name, d))
                    else:
                        print("[-] {}/{} does not exist, Project is corrupted .".format(project_name, d))
                        sys.exit(0)


                for f in project_files:
                    if os.path.exists("./projects/" + project_name + "/" + f["file_name"]): print("[+] ./projects/" + project_name + "/" + f['file_name'] + " file exists .")
                    else:
                        print("[-] ./projects/" + project_name + "/" + f['file_name'] + "  does not exist .")
                        sys.exit(0)
                break
            else:
                continue
            break
    
    

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
    if len([x for x in links if x['link'] == link]) == 0:
        links.append({
            "link": link,
            "checked": 0
        })
    elif len([x for x in links if urlparse(url=link).scheme + "://" + urlparse(url=link).netloc + urlparse(url=link).path + urlparse(url=link).params + urlparse(url=link).query in x['link']]) == 0:
        links.append({
            "link": link,
            "checked": 0
        })
    return links

def load_files(project_name, url):
    """
        Load files from project folder .
    """
    files_dict = {}
    for f in project_files:
        with open("./projects/" + project_name + "/" + f['file_name'], "r") as f_:
            files_dict[f['file_name'].split(".")[0]] = (json.loads(f_.read()))

    return files_dict