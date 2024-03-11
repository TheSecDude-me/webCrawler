import pathlib
import os
import json
from settings import project_dirs, project_files

def delete_folder(dst):
    pth = pathlib.Path(dst)
    for sub in pth.iterdir():
        if sub.is_dir():
            delete_folder(sub)
        else:
            sub.unlink()
    pth.rmdir()

def create_new_project_next(project_name):
    # Check for existance of new project
    if os.path.exists("./projects/" + project_name):
        return (False, "Error", "Project exists .")
    else:
        try:
            os.mkdir("./projects/" + project_name)
            for d in project_dirs: # Creating project directories
                os.mkdir("./projects/" + project_name + "/" + d)
            for f in project_files: # Creating project files
                with open("./projects/" + project_name + "/" + f['file_name'], "w") as f_:
                    f_.write(json.dumps(f['content']))

            with open("projects/" + project_name + "/settings.json", "w") as f_:
                settings = {
                    "url": "",
                    "reqs_timeout": 25,
                    "reqs_delay": 1,
                    "random_reqs_delay": True,
                    "random_reqs_delay_from": 1,
                    "random_reqs_delay_to": 99,

                    "origin_compare": True,
                    "origin_compare_ratio": 0.8,

                    "origin_contains": False,
                    "origin_contains_list": [],

                    "bad_links": [],
                    "link_xpaths": [],
                    "schemes": [],
                    "files": [],
                    "search_for_tags": [],
                    "url_regex_patterns": []
                }
                f_.write(json.dumps(settings))
                pass
            return (True, "Successful", "Project created successfully")
        except Exception as e:
            return (False, "Error", str(e))