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
    "image", "font", "audio", "video"
]