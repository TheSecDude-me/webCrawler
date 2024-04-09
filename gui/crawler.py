from seleniumwire import webdriver 
from selenium.webdriver.common.by import By
from gui_helpers import add_link
from PyQt6.QtCore import *
import json
import time
import re
from urllib.parse import urlparse
import random
from difflib import SequenceMatcher
import sys

with open("mimeData.json", "r") as f_:
    mimes = f_.read()
mimes = json.loads(mimes)

class Crawler():
    def __init__(self, project_name):
        super(Crawler, self).__init__()
        self.project_name = project_name
        with open("projects/" + self.project_name + "/settings.json", "r") as f_:
            self.settings = json.loads(f_.read())
        with open("projects/" + self.project_name + "/links_found.json", "r") as f_:
            self.links = add_link(json.loads(f_.read()), self.settings['url'], project_name=self.project_name, add_to_file=True)

    def link_absolute_maker(self, link, current_url):
        if len([y for y in self.settings['schemes'] if y in link]) == 0:
            current_url = urlparse(current_url).scheme + "://" + urlparse(current_url).netloc
            if link.startswith("/"):
                link = current_url + link
            elif link.startswith("/") == False:
                link = current_url + "/" + link
        return link

    def link_validation_chk(self, links, link, depth):
        # Bad links check
        for bad in self.settings['bad_links']:
            if bad in link:
                return (False, "Bad_link_detected")

        # Not be duplicate
        if len([y for y in links if y['link'] == link]) > 0:
            return (False, "Duplicated")
        
        # Not be in url patterns
        for pattern in self.settings['url_regex_patterns']:
            if re.match(pattern['pattern'], link):
                for l in [y for y in links]:
                    if re.match(pattern['pattern'], l['link']):
                        return (False, "url_regex_patterns_matched")
            

        # Not be file
        name = urlparse(url=link).path.split("/")[-1]
        try:
            ext = "." + name.split(".")[-1]
            fileType = [y['name'] for y in mimes if ext in y['fileTypes']]
            if len([y for y in self.settings['files'] if y in fileType[0]]) != 0:
                return (False, "is_file")
        except:
            pass

        # Not be in disallowed origins
        link_origin = urlparse(link).scheme + "://" + urlparse(link).netloc + "/"
        if link_origin in self.settings['origins']["disallowed"]:
                return (False, "disallowed_origin")
        elif link_origin not in self.settings['origins']['allowed'] and link_origin not in self.settings['origins']['disallowed']:
            if self.settings['origin_contains']:
                if len([y for y in self.settings['origin_contains_list'] if y in link_origin]):
                    self.settings['origins']["allowed"].append(link_origin)
                    with open("./projects/" + self.project_name + "/settings.json", "w") as f_:
                            f_.write(json.dumps(self.settings))
                else:
                    self.settings['origins']["disallowed"].append(link_origin)
                    with open("./projects/" + self.project_name + "/settings.json", "w") as f_:
                        f_.write(json.dumps(self.settings))
                    return (False, "disallowed_origin")
            if self.settings['origin_compare']:
                _tmp = [SequenceMatcher(None, y, link_origin).ratio() > self.settings['origin_compare_ratio'] for y in self.settings['origins']['allowed']]
                if len([y for y in _tmp if y == True]) > len([y for y in _tmp if y == False]):
                    self.settings['origins']["allowed"].append(link_origin)
                    with open("./projects/" + self.project_name + "/settings.json", "w") as f_:
                            f_.write(json.dumps(self.settings))
                elif len([y for y in _tmp if y == True]) == 0:
                    self.settings['origins']["disallowed"].append(link_origin)
                    with open("./projects/" + self.project_name + "/settings.json", "w") as f_:
                        f_.write(json.dumps(self.settings))
                    return (False, "disallowed_origin")
        return (True, "is_valid")
    
    
    def run(self):
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(self.settings['reqs_timeout'])

        # self.interceptor = Interceptor()
        # self.interceptor.driver = self.driver
        # self.interceptor.requests_tableWidget = self.requests_tableWidget
        # self.interceptor.start()
        while True:
            while len([x for x in self.links if x["checked"] == 0]) != 0:
                for link in [x for x in self.links if x["checked"] == 0]:

                    try:
                        print("Current link:", link['link'])
                        self.driver.get(url=link['link'])
                        if self.settings['random_reqs_delay']:
                            time.sleep(random.randrange(self.settings['random_reqs_delay_from'], self.settings['random_reqs_delay_to']))
                        else:
                            time.sleep(self.settings['reqs_delay'])
                    except Exception as e:
                        continue
                    
                    self.links[self.links.index(link)]['checked'] = 1
                    for xpath in self.settings['link_xpaths']:
                        elms = self.driver.find_elements(By.XPATH, xpath['xpath'])
                        for elm in elms:
                            try:
                                lnk = elm.get_dom_attribute(xpath['attr'])
                                lnk = self.link_absolute_maker(link=lnk, current_url=self.driver.current_url)
                                try:
                                    depth = [y['depth'] for y in self.links if y['link'] == self.driver.current_url][0] + 1
                                except:
                                    depth = 0
                                validation = self.link_validation_chk(self.links, lnk, depth)
                                if validation[0] == True:
                                    self.links = add_link(self.links, lnk, depth=depth, project_name=self.project_name, add_to_file=True)
                                    print(self.links[-1])
                            except Exception as e:
                                print(e)
                                continue
                
                


crawler = Crawler(project_name=sys.argv[1])
crawler.run()