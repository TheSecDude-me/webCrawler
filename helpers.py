import shutil, os
from urllib.parse import urlparse
from settings import mimes, files

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