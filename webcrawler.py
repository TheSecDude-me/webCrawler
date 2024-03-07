from seleniumwire import webdriver 
from seleniumwire.utils import decode as sw_decode
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import os
import pickle
import time
import json
from linkfinder_js import js_link_finder
import random
import sys
from helpers import create_project, is_file, add_link
from settings import mimes, link_xpaths, bad_links, schemes
from difflib import SequenceMatcher
import winsound
import re


try:
    url = sys.argv[1]
except:
    url = "https://divar.ir/"

origin_compare = False
origin_compare_ratio = 0.6

origin_contains = True
origin_contains_str = "divar"

url_parsed = urlparse(url)
project_name = url_parsed.netloc.replace("www.", "").replace(".", "_")
create_project(project_name)


with open("./projects/" + project_name + "/links_found.json", "r") as f_:
    links = json.loads(f_.read())

with open("./projects/" + project_name + "/err_reqs.json", "r") as f_:
    err_reqs = json.loads(f_.read())

requests = []

# Create project and its configuations

links = add_link(links, url)


def response_interceptor(request, response):
    if ("firefox" not in request.host) and ("mozilla" not in request.host) and ("google-analytics" not in request.host) and ("google.com" not in request.host):
        if origins_chk(request.url):
            if str(request.response.status_code).startswith("4") or str(request.response.status_code).startswith("5"):
                err_reqs.append({
                    "url": request.url,
                    "status_code": request.response.status_code,
                    "method": request.method,
                    "request_headers": dict(request.headers),
                    "response_headers": dict(request.response.headers)
                })
                with open("./projects/" + project_name + "/err_reqs.json", "w") as f_:
                    f_.write(json.dumps(err_reqs))
        req_dir = "./projects/" + project_name + "/origins/" + urlparse(request.url).netloc.replace(".", "_")
        try:
            os.mkdir(req_dir)
        except:
            pass
        try:
            content_type = dict(request.response.headers)['content-type']
            mime = list(filter(lambda x:x["name"]==content_type or (content_type in x['links']['deprecates']),mimes))
            if mime:
                ext = mime[0]['fileTypes'][0]
                
                data = sw_decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                file_name = request.path.split("/")[-1] #.split(".")[0] + ext
                if ext not in file_name:
                    file_name = file_name + ext

                file_path = req_dir + "/".join(request.path.split("/")[0:-1])
                try:
                    os.makedirs(file_path)
                except:
                    pass
                with open(file_path + "/" + file_name, "wb") as f_:
                    f_.write(data)
                if "js" in ext:
                    jslinks = js_link_finder(file_path + "/" + file_name)
                    global links
                    for link in jslinks:
                        if link.startswith("http://") == False and link.startswith("https://") == False:
                            if link.startswith("/"):
                                links = add_link(links, urlparse(request.url).scheme + "://" + urlparse(request.url).netloc + link)
                            elif link.startswith("./"):
                                links = add_link(links, urlparse(request.url).scheme + "://" + urlparse(request.url).netloc + link[1:])
                            else:
                                links = add_link(links, urlparse(request.url).scheme + "://" + urlparse(request.url).netloc + "/" + link)
                        else:
                            links = add_link(links, link)
        except Exception as e:
            pass


        global requests
        requests.append(request)
        links = add_link(links, request.url)
        if len(requests) > 100:
            pickled = pickle.dumps(requests)
            with open("./projects/" + project_name + "/requests_pickles/" + str(int(time.time())), "wb") as f_:
                f_.write(pickled)
                del requests
                requests = []



# Creates an instance of the chrome driver (browser)
print("[*] Lauching browser ...")
driver = webdriver.Firefox()
print("[+] Browser launched successfully ...")
driver.response_interceptor = response_interceptor

print("Get url: {}".format(url))
url_parsed = urlparse(url)

with open("./projects/" + project_name + "/origins_conf.json", "r") as f_:
    origins_conf = json.loads(f_.read())
    if len(origins_conf) == 0:
        origins_conf = {
            "allowed": [urlparse(url).scheme + "://" + urlparse(url).netloc + "/"],
            "disallowed": []
        }

with open("./projects/" + project_name + "/origins_conf.json", "w") as f_:
    f_.write(json.dumps(origins_conf))


def origins_chk(link):
    link_origin = urlparse(link).scheme + "://" + urlparse(link).netloc + "/"
    if link_origin in origins_conf["allowed"]:
        return True
    elif link_origin not in origins_conf['allowed'] and link_origin not in origins_conf['disallowed']:
        if origin_contains:
            if origin_contains_str in link_origin:
                origins_conf["allowed"].append(link_origin)
                with open("./projects/" + project_name + "/origins_conf.json", "w") as f_:
                        f_.write(json.dumps(origins_conf))
                return True
            else:
                origins_conf["disallowed"].append(link_origin)
                with open("./projects/" + project_name + "/origins_conf.json", "w") as f_:
                    f_.write(json.dumps(origins_conf))
                return False
        if origin_compare:
            _tmp = [SequenceMatcher(None, y, link_origin).ratio() > origin_compare_ratio for y in origins_conf['allowed']]
            if len([y for y in _tmp if y == True]) > len([y for y in _tmp if y == False]):
                origins_conf["allowed"].append(link_origin)
                with open("./projects/" + project_name + "/origins_conf.json", "w") as f_:
                        f_.write(json.dumps(origins_conf))
                return True
            elif len([y for y in _tmp if y == True]) == 0:
                origins_conf["disallowed"].append(link_origin)
                with open("./projects/" + project_name + "/origins_conf.json", "w") as f_:
                    f_.write(json.dumps(origins_conf))
                return False
            

        while True:
            winsound.Beep(500, 500)
            add_it_to_allowed = input(link_origin + " -> Do you wanna add it to allowed origins ? [Y/[N]] ")
            if add_it_to_allowed == "Y" or add_it_to_allowed == "y":
                origins_conf["allowed"].append(link_origin)
                with open("./projects/" + project_name + "/origins_conf.json", "w") as f_:
                    f_.write(json.dumps(origins_conf))
                return True
            else:
                origins_conf["disallowed"].append(link_origin)
                with open("./projects/" + project_name + "/origins_conf.json", "w") as f_:
                    f_.write(json.dumps(origins_conf))
                return False
    else:
        return False
                

with open("./projects/" + project_name + "/just_one_no_more_patterns.txt", "r") as f_:
    just_one_no_more_patterns = json.loads(f_.read())
    just_one_no_more_patterns = [x['pattern'] for x in just_one_no_more_patterns]


while len([x for x in links if x["checked"] == 0]) != 0:
    for current_link in [x for x in links if x["checked"] == 0]:
        time.sleep(random.random() * 3)
        print(len(links) - len([x for x in links if x["checked"] == 0]), "/", len(links))
        del driver.requests
        try:
            if origins_chk(current_link['link']) == False:
                raise Exception("disallowed_origin")

            if is_file(urlparse(url=current_link['link']).path.split("/")[-1]) == True:
                raise Exception("is_file")

            if len([x for x in just_one_no_more_patterns if re.match(x, current_link['link'])]) != 0: # current_link['link'] is in patterns
                if len([y for y in links if y['checked'] == 1]) != 0: # link like current_link['link'] checked before .
                    raise Exception("just_one_no_more_patterns_caught")

            driver.get(url=current_link['link'])
        except Exception as e:
            links[links.index(current_link)]['checked'] = -1
            links[links.index(current_link)]['err_reason'] = str(e)
            continue

        # Where are links ?
        for xpath in link_xpaths:
            elms = driver.find_elements(By.XPATH, xpath['xpath'])
            for elm in elms:
                try:
                    link = elm.get_dom_attribute(xpath['attr'])
                    for bad in bad_links:
                        if bad in link:
                            raise Exception("Bad link detected .")
                except:
                    continue
                if len([y for y in schemes if y in link]) == 0:
                    current_url = urlparse(driver.current_url).scheme + "://" + urlparse(driver.current_url).netloc
                    if link.startswith("/"):
                        link = current_url + link
                    elif link.startswith("/") == False:
                        link = driver.current_url + "/" + link
                    links = add_link(links, link)


        links[links.index(current_link)]['checked'] = 1
        with open("./projects/" + project_name + "/links_found.json", "w") as f_:
            f_.write(json.dumps(links))



"""
# Where are inputs ?
input_elms = driver.find_elements(By.XPATH, "//input")
textarea_elms = driver.find_elements(By.XPATH, "//textarea")

# Where are forms ?
form_elms = driver.find_elements(By.XPATH, "//form")



def is_href(el):
    try:
        xpath = "."
        el = el.find_element(By.XPATH, xpath)
        while True:
            xpath = xpath + "/.."
            el = el.find_element(By.XPATH, xpath)
            if el.get_attribute("href") != None:
                return True
    except:
        return False

# Where are clickable elements ?
button_elms = driver.find_elements(By.XPATH, "//button")
# 2. Elements with onclick attribute
onclick_elms = driver.find_elements(By.XPATH, "//*[@onclick]")
pointer_elms = []
print("[+] Finding pointer elements in page .")
elms = driver.find_elements(By.XPATH, "//*")
for el in elms:
    if el.value_of_css_property("cursor") == "pointer":
        pointer_elms.append(el)
print("[+] Finding pointer elmenets in page done .")
clickables = []
clickables = list(set(clickables + button_elms + onclick_elms + pointer_elms))
clickables_dict = []
counter = 0
for el in clickables:
    # if is_href(el) == False:
    print(counter)
    clickables_dict.append({
        "element": el,
        "is_displayed": el.is_displayed(),
        "is_enabled": el.is_enabled(),
        "location": el.location,
        "rect": el.rect,
        "size": el.size,
        "clicked_before": False,
        "is_href": False
    })
    counter += 1

infinite = 1
counter = 0
bad_buttons = []
while infinite:
    print("[*] Calculating displayed and clicked elements")
    my_list = []
    for i in clickables_dict:
        if i['is_displayed'] == True and i['clicked_before'] == False and i['is_href'] == False:
            my_list.append(i)
    print("[+] Calculating displayed and clicked elements done .")
    print(len(my_list), "/", len(clickables_dict))
    if (len(my_list) == 0):
        break
    
    for i in clickables_dict:
        print("A")
        el = i['element']
        if i['is_displayed'] == True and i['clicked_before'] == False:
            print("b")
            time.sleep(0.5)
            try:
                print("C")
                el.click()
                if (driver.current_url != url):
                    print("D")
                    button_elms = []
                    onclick_elms = []
                    clickables = []
                    clickables_dict = []
                    driver.get(url)
            except ElementClickInterceptedException:
                continue
            except StaleElementReferenceException:
                try:
                    clickables_dict.remove(i)
                except ValueError:
                    continue
                continue
            i['clicked_before'] = True
            # Where are clickable elements ?
            button_elms = driver.find_elements(By.XPATH, "//button")
            # 2. Elements with onclick attribute
            onclick_elms = driver.find_elements(By.XPATH, "//*[@onclick]")
            clickables = list(set(clickables + button_elms + onclick_elms))
            for el in clickables:
                try:
                    el.is_displayed()
                except StaleElementReferenceException:
                    continue
                if el not in [i['element'] for i in clickables_dict]:
                    if is_href(el) == False:
                        clickables_dict.append({
                            "element": el,
                            "is_displayed": el.is_displayed(),
                            "is_enabled": el.is_enabled(),
                            "location": el.location,
                            "rect": el.rect,
                            "size": el.size,
                            "clicked_before": False,
                            "is_href": False
                        })
# driver.quit()
"""