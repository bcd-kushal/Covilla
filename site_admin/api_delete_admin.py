from datetime import datetime, timedelta

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

ATLAS_URI = "ATLAS_SECRET"


#==================================================================
#==================================================================

def delete_blog(blog):
    if blog is None or blog == "":
        return False
    
    val = True


    mongo_client = MongoClient(ATLAS_URI,server_api = ServerApi('1'))
    
    atlas_db = mongo_client.get_database("blogs")


    # delete whole blog first
    data = atlas_db.blog
    result = data.delete_one({ "title": blog })

    if result.deleted_count == 1:
        val &= True
    else: 
        val &= False



    # delete blog brief
    data = atlas_db.blog_brief
    result = data.delete_one({ "title": blog })

    if result.deleted_count == 1:
        val &= True
    else: 
        val &= False




    # delete comment on that blog
    data = atlas_db.comments
    result = data.delete_one({ "title": blog })

    if result.deleted_count == 1:
        val &= True
    else: 
        val &= False




    # delete total blog count
    data = atlas_db.statistics
    result = data.find_one({ "total_blogs": { "$exists": True } })

    new_val = int(result["total_blogs"]) - 1

    data.update_one({ "total_blogs": { "$exists": True } }, { "$set": { "total_blogs": new_val } })

    val &= True

    return val

    










def do_comment_delete(blog:str, name:str, comment:str):
    if blog=="" or blog==None:
        return False
    if name=="" or name==None:
        return False
    if comment=="" or comment==None:
        return False

    
    mongo_client = MongoClient(ATLAS_URI,server_api = ServerApi('1'))
    
    atlas_db = mongo_client.get_database("blogs")


    # firstly delete the comment in actuality
    data = atlas_db.comments
    result = data.find_one({ "title": blog })

    comments = result["comments"]

    new_obj = []

    for x in comments:
        if x["name"] == name and x["comment"] == comment:
            continue
        new_obj.append({
            "name": x["name"],
            "email": x["email"],
            "comment": x["comment"]
        })


    result = data.update_one({ "title": blog }, { "$set": { "comments": new_obj } })







    # update total comment count
    data = atlas_db.statistics
    result = data.find_one({ "total_comments": { "$exists": True } })

    new_val = int(result["total_comments"]) - 1

    data.update_one({ "total_comments": { "$exists": True } }, { "$set": { "total_comments": new_val } })



    return True
    

