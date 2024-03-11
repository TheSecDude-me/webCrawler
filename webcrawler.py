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
from helpers import create_project, is_file, add_link, load_files
from settings import mimes, link_xpaths, bad_links, schemes
from difflib import SequenceMatcher
import winsound
import re


try:
    url = sys.argv[1]
except:
    while True:
        url = input("[*] Enter URL: ")
        if url != "":
            break

origin_compare = False
origin_compare_ratio = 0.6
reqs_timeout = 25
origin_contains = True


settings = {
    "url": url,
    "reqs_timeout": reqs_timeout,
    "origin_compare": origin_compare,
    "origin_compare_ratio": origin_compare_ratio,
    "origin_contains": origin_contains,
    "origin_contains_list": [],
}



url_parsed = urlparse(settings['url'])
project_name = url_parsed.netloc.replace("www.", "").replace(".", "_")
create_project(project_name, settings)

# links, err_reqs, forms, inputs, origins_conf, url_regex_patterns, settings = load_files(project_name, url)
locals().update(load_files(project_name, url))
print("URL: {}".format(url))


requests = []

links_found = add_link(links_found, settings['url'])


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
                    global links_found
                    for link in jslinks:
                        if link.startswith("http://") == False and link.startswith("https://") == False:
                            if link.startswith("/"):
                                links_found = add_link(links_found, urlparse(request.url).scheme + "://" + urlparse(request.url).netloc + link)
                            elif link.startswith("./"):
                                links_found = add_link(links_found, urlparse(request.url).scheme + "://" + urlparse(request.url).netloc + link[1:])
                            else:
                                links_found = add_link(links_found, urlparse(request.url).scheme + "://" + urlparse(request.url).netloc + "/" + link)
                        else:
                            links_found = add_link(links_found, link)
        except Exception as e:
            pass


        global requests
        requests.append(request)
        links_found = add_link(links_found, request.url)
        if len(requests) > 100:
            pickled = pickle.dumps(requests)
            with open("./projects/" + project_name + "/requests_pickles/" + str(int(time.time())), "wb") as f_:
                f_.write(pickled)
                del requests
                requests = []



# Creates an instance of the chrome driver (browser)
print("[*] Lauching browser ...")
driver = webdriver.Firefox()
driver.set_page_load_timeout(settings['reqs_timeout'])
print("[+] Browser launched successfully ...")
driver.response_interceptor = response_interceptor

print("Get url: {}".format(url))
url_parsed = urlparse(url)


def origins_chk(link):
    link_origin = urlparse(link).scheme + "://" + urlparse(link).netloc + "/"
    if link_origin in origins_conf["allowed"]:
        return True
    elif link_origin not in origins_conf['allowed'] and link_origin not in origins_conf['disallowed']:
        if settings['origin_contains']:
            
            if len([y for y in settings['origin_contains_list'] if y in link_origin]):
                origins_conf["allowed"].append(link_origin)
                with open("./projects/" + project_name + "/origins_conf.json", "w") as f_:
                        f_.write(json.dumps(origins_conf))
                return True
            else:
                origins_conf["disallowed"].append(link_origin)
                with open("./projects/" + project_name + "/origins_conf.json", "w") as f_:
                    f_.write(json.dumps(origins_conf))
                return False
        if settings['origin_compare']:
            _tmp = [SequenceMatcher(None, y, link_origin).ratio() > settings['origin_compare_ratio'] for y in origins_conf['allowed']]
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



while len([x for x in links_found if x["checked"] == 0]) != 0:
    for current_link in [x for x in links_found if x["checked"] == 0]:
        del driver.requests
        try:
            if origins_chk(current_link['link']) == False:
                raise Exception("disallowed_origin")

            if is_file(urlparse(url=current_link['link']).path.split("/")[-1]) == True:
                raise Exception("is_file")
            

            for pattern in url_regex_patterns:
                if re.match(pattern['pattern'], current_link['link']):
                    for l in [y for y in links_found if y['checked'] == 1]:
                        if re.match(pattern['pattern'], l['link']):
                            raise Exception("url_regex_patterns_caught")
                
            time.sleep(random.random()* 2)
            print(current_link['link'], len(links_found) - len([x for x in links_found if x["checked"] == 0]), "/", len(links_found))
            driver.get(url=current_link['link'])

        except KeyboardInterrupt:
            while True:
                cmd = input("> ")
                if cmd == "help":
                    print("""Table of commands :
    help        Show this menu
    get         Get settings 
    set         Set new setting
    continue    Continue crawling with new settings
    exit        Exit
""")
                elif cmd == "get":
                    while True:
                        getCMD = input("Get> ")
                        if getCMD == "help":
                            print("""Get table of commands:
    help        Show this menue
    origins     Show all allowed and disallowed origins
    patterns    Show all just one no more patterns and their exmaples 
    exit        Exit from this menu
""")
                        elif getCMD == "origins":
                            with open("./projects/" + project_name + "/origins_conf.json", "r") as f_:
                                print(json.dumps(json.loads(f_.read()), indent=1))
                        elif getCMD == "patterns":
                            with open("./projects/" + project_name + "/url_regex_patterns.json", "r") as f_:
                                print(json.dumps(json.loads(f_.read()), indent=1))
                        elif getCMD == "exit":
                            break
                        else:
                            continue
                elif cmd == "set":
                    while True:
                        setCMD = input("Set> ")
                        if setCMD == "help":
                            print("""Get table of commands:
    help                Show this menue
    origin allowed      Set new allowed origin
    origin disallowed
    pattern             Set new just one no more patterns and an exmaples 
    exit                Exit from this menu
""")
                        elif setCMD == "origin allowed":
                            allowed_origin = input("[*] Enter URL of allowed origin: ")
                            origins_conf["allowed"].append(allowed_origin)
                            with open("./projects/" + project_name + "/origins_conf.json", "w") as f_:
                                f_.write(json.dumps(origins_conf))
                            print(allowed_origin, "has been added to allowed origin list .")
                        elif setCMD == "origin disallowed":
                            disallowed_origin = input("[*] Enter URL of disallowed origin: ")
                            origins_conf["disallowed"].append(disallowed_origin)
                            with open("./projects/" + project_name + "/origins_conf.json", "w") as f_:
                                f_.write(json.dumps(origins_conf))
                            print(allowed_origin, "has been added to disallowed origin list .")
                        elif setCMD == "pattern":
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
                            url_regex_patterns.append({
                                'pattern': pattern,
                                'example': example
                            })
                            with open("./projects/" + project_name + "/url_regex_patterns.json", "w") as f_:
                                f_.write(json.dumps(url_regex_patterns))
                                # here

                        elif setCMD == "exit":
                            break
                        else:
                            continue
                elif cmd == "continue":
                    break
                elif cmd == "exit":
                    time.sleep(2)
                    print("[+] Good Bye .")
                    sys.exit()
                else:
                    continue
            print("[*] Continue crawling .")
            
        except Exception as e:
            print(current_link['link'], str(e), len(links_found) - len([x for x in links_found if x["checked"] == 0]), "/", len(links_found))
            links_found[links_found.index(current_link)]['checked'] = -1
            links_found[links_found.index(current_link)]['err_reason'] = str(e)
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
                    links_found = add_link(links_found, link)
        form_elms = driver.find_elements(By.XPATH, "//form")
        if len(form_elms):
            forms_found.append({
                'url': current_link['link'],
                'forms_count': len(form_elms)
            })
            
            with open("./projects/" + project_name + "/forms_found.json", "w") as f_:
                f_.write(json.dumps(forms_found))


        input_elms = driver.find_elements(By.XPATH, "//input")
        # textarea_elms = driver.find_elements(By.XPATH, "//textarea")
        inputs_elms_all = input_elms
        if len(inputs_elms_all):
                    inputs_found.append({
                        'url': current_link['link'],
                        'inputs_count': len(inputs_elms_all)
                    })
                    
                    with open("./projects/" + project_name + "/inputs_found.json", "w") as f_:
                        f_.write(json.dumps(inputs_found))


        # Where are forms ?
        
        links_found[links_found.index(current_link)]['checked'] = 1
        with open("./projects/" + project_name + "/links_found.json", "w") as f_:
            f_.write(json.dumps(links_found))



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