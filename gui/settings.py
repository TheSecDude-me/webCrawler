import json

with open("./mimeData.json", "r") as f_:
    mimes = f_.read()
mimes = json.loads(mimes)


bad_links = [
    "resource://", "chrome://", "data:image", "wss://"
]

link_xpaths = [
    {
        "xpath": "//*[@href]",
        "attr": "href"
    },
    {
        "xpath": "//*[@src]",
        "attr": "src"
    },
    {
        "xpath": "//*[@action]",
        "attr": "action"
    }
]

schemes = [
    "http://", "https://"
]

files = [
    "image", "font", "audio", "video", "javascript", "css"
]

search_for_tags = [
    'form', 'input', 'textarea', 'iframe'
]


project_files = [
    {
        "file_name": "origins_conf.json",
        "content": {
            "allowed": [],
            "disallowed": []
        }
    },
    {
        "file_name": "url_regex_patterns.json",
        "content": []
    },
    {
        "file_name": "err_reqs.json",
        "content": []
    },
    {
        "file_name": "links_found.json",
        "content": []
    },
    {
        "file_name": "forms_found.json",
        "content": []
    },
    {
        "file_name": "inputs_found.json",
        "content": []
    },
    {
        "file_name": "settings.json",
        "content": {}
    }

]

project_dirs = [
    "origins", "requests_pickles"
]

paths = {
    "python_path" : ".venv/Scripts/python.exe",
    "crawler_path" : "gui/crawler.py",
}