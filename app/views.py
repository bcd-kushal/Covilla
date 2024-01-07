from django.shortcuts import render

import time
import threading

from django.views.decorators.cache import cache_page
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate as default_authenticate, login as LoginUser, logout as LogoutUser
from django.contrib.auth.models import User as RegisteredUsers
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .api_read import *
from .api_delete import *

# ================================================================================================================



# @/blog/<int:id>/
def blog(req,id):
    if req.method == "GET":

        id = "What is SlidesAI"
        tag = "Design"

        blog = get_whole_blog(id)

        

        return render(req,"src/blog.html",{
            "tab_title": "Bloggers",

            # blog details
            "title": blog["title"],
            "date": blog["date"],
            "author": blog["author"],
            "thumbnail": blog["thumbnail"],
            "tag": blog["tag"],
            "contents": blog["contents"],
            "header": blog["header"],
            "body": blog["body"],


            # more blogs
            "more_blogs": get_more_blogs(tag),


            # recents
            "recents": get_recent_blog_titles(),



            # statistics
            "statistics": get_site_stats()
        })
    

    elif req.method == "POST":

        if req.POST.get("comment"):
            blog_name = req.POST.get("blog_name")
            name = req.POST.get("author")
            email = req.POST.get("email")
            comment = req.POST.get("comment")


            print({
                "blog_name": blog_name,
                "name": name,
                "email": email,
                "comment": comment
            })

            # post_comment(blog=blog_name,name=name,email=email,comment=comment)


        return render(req,"src/success.html",{})


    else:
        return send_bad_request(req)














# @/
def homepage(req):
    if req.method == "GET":
        return render(req,"src/all_blogs.html",{
            "tab_title": "Covilla: Home",

            "page_title": "All Blogs",
            "page_brief": "Stay up to date with the most recent news and updates of our team happenings",

            "recents": get_recent_blog_titles(),

            "blogs": get_blogs(),

            "statistics": get_site_stats()
        })
    else:
        return send_bad_request(req)
    



# @/categories/
def categories(req):
    if req.method == "GET":
        return render(req,"src/categories.html",{
            "statistics": get_site_stats()
            
        })
    else:
        return send_bad_request(req)
    




# @/categories/design/
def design_blogs(req):
    if req.method == "GET":
        return render(req,"src/all_blogs.html",{
            "tab_title": "Design Blogs: Covilla",

            "page_title": "Design Blogs",
            "page_brief": "For the design-centric peeps out there",

            "recents": get_recent_blog_titles(),

            "blogs": get_blogs(),

            "statistics": get_site_stats()
        })
    else:
        return send_bad_request(req)


# @/categories/tech/
def tech_blogs(req):
    if req.method == "GET":
        return render(req,"src/all_blogs.html",{
            "tab_title": "Tech Blogs: Covilla",

            "page_title": "Technical Blogs",
            "page_brief": "Technology is the present, and future afterall",

            "recents": get_recent_blog_titles(),

            "blogs": get_blogs(),

            "statistics": get_site_stats()
        })
    else:
        return send_bad_request(req)


# @/categories/my-life/
def life_blogs(req):
    if req.method == "GET":
        return render(req,"src/all_blogs.html",{
            "tab_title": "Life Blogs: Covilla",

            "page_title": "Life Blogs",
            "page_brief": "The daily happenings jotted down",

            "recents": get_recent_blog_titles(),

            "blogs": get_blogs(),

            "statistics": get_site_stats()
        })
    else:
        return send_bad_request(req)


# @/categories/profession/
def profession_blogs(req):
    if req.method == "GET":
        return render(req,"src/all_blogs.html",{
            "tab_title": "Professional Blogs: Covilla",

            "page_title": "Profession Blogs",
            "page_brief": "Staying stern and sharp on the work sector with blogs",

            "recents": get_recent_blog_titles(),

            "blogs": get_blogs(),

            "statistics": get_site_stats()
        })
    else:
        return send_bad_request(req)





# @/categories/daily/
def daily_blogs(req):
    if req.method == "GET":
        return render(req,"src/all_blogs.html",{
            "tab_title": "Daily Blogs: Covilla",

            "page_title": "Daily Blogs",
            "page_brief": "A daily record into the life of us.",

            "recents": get_recent_blog_titles(),

            "blogs": get_blogs(),

            "statistics": get_site_stats()
        })
    else:
        return send_bad_request(req)





# @/categories/community/
def community_blogs(req):
    if req.method == "GET":
        return render(req,"src/all_blogs.html",{
            "tab_title": "Community Blogs: Covilla",

            "page_title": "Community Blogs",
            "page_brief": "For the readers, by the readers, to the readers",

            "recents": get_recent_blog_titles(),

            "blogs": get_blogs(),

            "statistics": get_site_stats()
        })
    else:
        return send_bad_request(req)







# @/recents/
def recents(req):
    if req.method == "GET":
        return render(req,"src/all_blogs.html",{
            "tab_title": "Recent Blogs: Covilla",

            "page_title": "Recent Blogs",
            "page_brief": "We add blogs on a weekly basis",

            "recents": get_recent_blog_titles(),

            "blogs": get_blogs(),

            "statistics": get_site_stats()
        })
    else:
        return send_bad_request(req)







# @/search?query=...
def search(req):
    if req.method == "GET":

        keyword = req.GET.get("keywords",None)
        blogs = get_searched_blogs(search_word=keyword)
        total = len(blogs)

        return render(req,"src/all_blogs.html",{
            "tab_title": "Search Results: Covilla",

            "page_title": f"Search results for '{keyword}'",
            "page_brief": f"Found a total of {total} related blogs",

            "recents": get_recent_blog_titles(),

            "blogs": blogs,

            "statistics": get_site_stats()
        })
    else:
        return send_bad_request(req)








# @/subscribe/
def subscribe(req):
    if req.method == "GET":
        return render(req,"src/subscribe.html",{})
    else:
        return send_bad_request(req)





# ===== error page =====================================

def send_bad_request(req):
    return render(req,"src/error/error.html",{})
