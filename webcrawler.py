from seleniumwire import webdriver 
from seleniumwire.utils import decode as sw_decode
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import os
import shutil
import pickle
import time
import json
from linkfinder_js import js_link_finder
import random
import sys

try:
    url = sys.argv[1]
except:
    url = "https://target.com/"

def request_interceptor(request):
    if "firefox" not in request.url and "mozilla" not  in request.url:
        pass
        # print("REQ:", request)

def response_interceptor(request, response):
    if ("firefox" not in request.host) and ("mozilla" not in request.host) and ("google-analytics" not in request.host) and ("google.com" not in request.host):
        req_tld = urlparse(request.url).netloc.replace(".", "_")
        req_dir = "./projects/" + project_name + "/origins/" + req_tld
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
                file_name = request.path.split("/")[-1].split(".")[0] + ext
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



requests = []


with open("./mimeData.json", "r") as f_:
    mimes = f_.read()
mimes = json.loads(mimes)

# Creates an instance of the chrome driver (browser)
driver = webdriver.Firefox()
driver.request_interceptor = request_interceptor
driver.response_interceptor = response_interceptor

print("Get url: {}".format(url))
url_parsed = urlparse(url)

# Create project and its configuations
try:
    shutil.rmtree("./projects/")
except:
    pass
if os.path.exists("./projects") == False:
    os.mkdir("./projects")

project_name = url_parsed.netloc.replace("www.", "").replace(".", "_")
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
        if "image" in fileType[0] or "font" in fileType[0] or "audio" in fileType[0] or "video" in fileType[0]:
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

links = []
links = add_link(links, url)





while len([x for x in links if x["checked"] == 0]) != 0:
    for current_link in [x for x in links if x["checked"] == 0]:
        time.sleep(random.random() * 3)
        print(len(links) - len([x for x in links if x["checked"] == 0]), "/", len(links))
        del driver.requests
        try:
            if is_file(urlparse(url=current_link['link']).path.split("/")[-1]) == False:
                driver.get(url=current_link['link'])
            else:
                links[links.index(current_link)]['checked'] = -1    
                links[links.index(current_link)]['err_reason'] = "is_file"
        except Exception as e:
            links[links.index(current_link)]['checked'] = -1
            links[links.index(current_link)]['err_reason'] = str(e)
            continue

        # Where are links ?
        href_elms = driver.find_elements(By.XPATH, "//*[@href]")
        for elm in href_elms:
            try:
                link = elm.get_dom_attribute("href")
                if link.startswith("resource://") or link.startswith("chrome://"):
                    continue
            except:
                continue
            if link.startswith("http://") == False and link.startswith("https://") == False:
                current_url = urlparse(driver.current_url).scheme + "://" + urlparse(driver.current_url).netloc
                if link.startswith("/"):
                    link = current_url + link
                elif link.startswith("/") == False:
                    link = driver.current_url + "/" + link
                links = add_link(links, link)
            
        src_elms = driver.find_elements(By.XPATH, "//*[@src]")
        for elm in src_elms:
            try:
                link = elm.get_dom_attribute("src")
                if link.startswith("resource://") or link.startswith("chrome://"):
                    continue
                if link.startswith("data:image"):
                    continue
            except:
                continue
            if link.startswith("http://") == False and link.startswith("https://") == False:
                current_url = urlparse(driver.current_url).scheme + "://" + urlparse(driver.current_url).netloc
                if link.startswith("/"):
                    link = current_url + link
                elif link.startswith("/") == False:
                    link = driver.current_url + "/" + link
                links = add_link(links, link)


        action_elms = driver.find_elements(By.XPATH, "//*[@action]")
        for elm in action_elms:
            try:
                link = elm.get_dom_attribute("action")
                if link.startswith("resource://") or link.startswith("chrome://"):
                    continue
            except:
                continue
            if link.startswith("http://") == False and link.startswith("https://") == False:
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