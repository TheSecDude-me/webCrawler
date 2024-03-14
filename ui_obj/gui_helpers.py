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

                    "origins": {
                        "allowed": [],
                        "disallowed": []
                    },

                    "bad_links": ["resource://", "chrome://", "data:image", "wss://"],
                    "link_xpaths": [{
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
                    ],
                    "schemes": ["http://", "https://"],
                    "files": ["image", "font", "audio", "video", "javascript", "css"],
                    "search_for_tags": ['form', 'input', 'textarea', 'iframe'],
                    "url_regex_patterns": [],

                    "proxy": {
                        "address": "",
                        "port": 1080
                    },
                    "depth": 3,
                    "infinite_depth": False
                }
                f_.write(json.dumps(settings))
                pass
            return (True, "Successful", "Project created successfully")
        except Exception as e:
            return (False, "Error", str(e))
    
help_messages = {
    "origins_compare_ratio_help_label": {
        "title": "Origin Compare Ratio",
        "message": """
What is origin compare ratio settings ?
Of course you  do not want to check all URLs with any origin, so you should set some settings to crawl just some specific ones with certain origin . 
Compare Ratio will compare origin of an URL with allowed origins, If it was similare to them cralwer will crawl it too .
So you need to set sensitivity of the comparison with the slider element .

این واسه اینه که هر اوریجینی رو تست نکنه . فرض کنید که میخواید یک وب سایت به ادرس زیر رو تست کنید :
https://site.dm
توی این سایت ممکن هست که لینکهایی از اوریجین های مختلف وجود داشته باشه و شما نخواید که همه رو تست کنید .
با فعال کردن این گزینه میتونید یک درجه شباهت به اوریجین دامنه اصلی بهش بدید و اوریجین هایی که شباهت با 
اوریجین اصلی دارن رو تشخیص میده و براتون اونها رو هم کرال میکنه .
            """,
    },
    "origins_contain_help_label": {
        "title": "Origin Contain Settings",
        "message": """
What is origin contain settings ?
Of course you  do not want to check all URLs with any origin, so you should set some settings to crawl just some specific ones with certain origin . 
Origin contain settings will allow you to set some spicific words, Crawler will cralw URLs with an origin that contains at least one of these words .
For example, If you set site,blog,news, Cralwer will crawl site.com, news.com, blog,com, news.site.com, ... but it won't cralw airport.com

این مورد واسه اینه که شما یک کلمه کلیدی رو قرار بدید و اوریجینی که اون کلمه کلیدی رو داره رو واسه شما تست میکنه . 
حتی میتونید تعداد متعددی کلمه کلیدی رو تعریف کنید به شکل زیر :
site,blog,news
اوریجین های مختلف رو تشخیص میده و بررسی میکنه که ایا این کلمات کلیدی توش هست یا خیر . اگه باشه اونها رو هم کرال میکنه وگرنه نادیده گرفته میشه .
            """,
    },
    "regex_pattern_help_label": {
        "title": "Regex Patterns",
        "message": """
Why you need to set some regex pattern for better crawling ?
Imagine you target is a shop website . It has a lot of products by shop.com/products/[product_id] URL . 
All of products pages have same structure and you do not need to check all of them and checking all of them is wasting time and resources .
You can set some regex pattern for some specific URLs like shop.com/products/[product_id] to check one of them not any more . 
Regex pattern and it's example should be matched and if they are not matched you will receive some errors .
                                    
یک تارگت میتونه تعدادی لینک داشته باشه که محتوای اون صفحه ساختار یکسانی داشته باشه . مثلا سایت زیر رو در نظر بگیرید :
https://shop.dm
این فروشگاه صفحات مخصوص محصولات داره که عینا واسه هر محصول تکرار میشه به شکل زیر :
https://shop.dm/products/12
https://shop.dm/products/15
...
شما میتونید با تعریف ریجکس این ادرس ها رو تشخیص بدید و کرالر فقط یک بار اونها رو کرال میکنه و بار دیگر نادیده میگیره .
            """,
    },
    "bad_links_help_label": {
        "title": "Bad links",
        "message": """
What is a bad link ?
Sometimes crawler detects some strings that are not link but their structures are like links . 
You can filter them here to not to waist your time by crawling wrong links . 
For example: "resource://", "chrome://", "data:image" are some strings who are not a real link,
by adding them to this list you can ignore them .
                                    
ممکن هست برخی از ادرس ها توسط کرالر اشتباه شناسایی شوند که در حقیقت ادرس یو ار ال درست نیستند . میتونید اونها رو توی این لیست تعریف کنید و کافیه که پروتکل اونها رو بنویسید و کرالر اونها رو نادیده میگیره .مثلا :
resource://, chrome://, data:image, ...
""",
    },
    "links_xpath_help_label": {
        "title": "Links XPATH",
        "message": """
What is xpath link ?
In a HTML document we have some attributes that can have links in themselves .
By extracting them from a HTML page we can find the links .
For example, href attributes, src attributes and ...
You can add your attributes to this list .

توی یک صفحه اچ تی ام ال لینک ها توی خصیصه هایی قرار داده میشوند مثلا :
src, href, action, ...
توی این جدول میتونید اونها رو تعریف کنید و کرالر توی صفحه لینک هایی که توی انها قرار داره رو استخراج میکنه . دقت کنید که باید ایکس پت اونها رو هم بنویسید .
""",
    },
    "schemes_help_label": {
        "title": "Schemes",
        "message": """
What is scheme ?
If you want to search for links with specific scheme you can add that scheme here to search for .
For example links that start with https:// or http:// .

هر لینکی یک پروتکلی داره و شما میتونید با تعریف پروتکل هایی توی این لیست به کرالر بگید که لینک هایی رو تشخیص بده که این پروتکل رو دارند . مثلا : 
https://, http://, ...
""",
    },
    "tags_help_label": {
        "title": "Tags Table",
        "message": """
Why we should add some tags here ?
If you add some tags to this list, Crawler will search for them in crawled web pages and will add them to a file in project folder .
For example, by default input, form, textarea are some tags that crawler will search for them inside a HTML document .
                                    
ممکن هست که علاوه بر لینک های توی یک صفحه به دنبال تگ های مختلفی باشید . مثلا تگهای :
input, form, textarea, ...
میتونید اونها رو توی این لیست تعریف کنید و کرالر علاوه بر لینکها این تگها رو هم پیدا میکنه و توی یک فایل برای شما ذخیره خواهد کرد تا بعدا بتونید به راحتی بهشون دسترسی پیدا کنید .
""",
    },
    "files_help_label": {
        "title": "Files exclude table",
        "message": """
Why we should add files mime here ?
By default crawler will search in all files from a target . 
For example, Javascript files, CSS files, JPG files and ...
We know that some of them have no links inside and you can add their mime type to this list to not to crawl them . 
For example, JPG files are binary and crawling inside them is waisting time . 

برخی از فایل ها هستند که محتوایی حاوی لینک ندارند . مثلا فایل های :
jpeg, png, ...
میتونید با تعریف میم تایپ اونها توی این لیست به کرالر بگید که در صورتی که به این لینک ها رسید اونها رو نادیده بگیره و کرال نکنه .           
""",
    }
}



def add_link(links, link, depth=0):
    links.append({
            "link": link,
            "checked": 0,
            "depth": depth
        })
    return links
