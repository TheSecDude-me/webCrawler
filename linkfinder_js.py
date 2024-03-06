#!/usr/bin/env python
# By Gerben_Javado


# Import libraries
import re
import json

# Regex used
regex_str = r"""

  (?:"|')                               # Start newline delimiter

  (
    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path

    |

    ((?:/|\.\./|\./)                    # Start with /,../,./
    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
    [^"'><,;|()]{1,})                   # Rest of the characters can't be

    |

    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
    [a-zA-Z0-9_\-/]{1,}                 # Resource name
    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

    |

    ([a-zA-Z0-9_\-/]{1,}/               # REST API (no extension) with /
    [a-zA-Z0-9_\-/]{3,}                 # Proper REST endpoints usually have 3+ chars
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

    |

    ([a-zA-Z0-9_\-]{1,}                 # filename
    \.(?:php|asp|aspx|jsp|json|
         action|html|js|txt|xml)        # . + extension
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

  )

  (?:"|')                               # End newline delimiter

"""

with open("./mimeData.json", "r") as f_:
    mimes = f_.read()
mimes = json.loads(mimes)

def js_link_finder(file, regex_str=regex_str):
    with open(file, "r") as f_:
        content = f_.read()

    regex = re.compile(regex_str, re.VERBOSE)
    items = [{"link": m.group(1)} for m in re.finditer(regex, content)]

    # Remove duplication
    all_links = set()
    no_dup_items = []
    for item in items:
        if item["link"] not in all_links:
            all_links.add(item["link"])
            no_dup_items.append(item)
    items = no_dup_items

    
    all_links = list(all_links)
    links = []
    for link in all_links:
        if len([y for y in mimes if y['name'] == link]):
            continue
        links.append(link)

    return links