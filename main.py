from notion.client import * 
from notion.block import * 
import os
import getpass
import requests
from concurrent.futures import ThreadPoolExecutor

# Get access token from API
def get_access_token():
    USER = os.getenv('IC_USER')
    PASSWORD = os.getenv('IC_PASSWORD')
    response = requests.post('https://api-materials.doc.ic.ac.uk/auth/login', json={'username':USER, 'password':PASSWORD})
    return response.json()['access_token']

def get_page_and_client():
    token_v2 = input("Enter token_v2: ")
    url = input("Enter Notion page URL: ")
    client = NotionClient(token_v2=token_v2)
    page = client.get_block(url)
    return page, client     

# Set details in environment
def set_details():
    os.environ['IC_USER'] = input("Imperial Shortcode: ");
    os.environ['IC_PASSWORD'] = getpass.getpass("Password: ");

def get_courses(access_token):
    url = "https://api-materials.doc.ic.ac.uk/courses/2021"
    headers = {}
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + access_token
    return requests.get(url, headers=headers).json()

def get_materials(code, access_token):
    url = "https://api-materials.doc.ic.ac.uk/resources?year=2021&course=" + code
    headers = {}
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + access_token
    return requests.get(url, headers=headers).json()

def get_collection_schema():
    return {
        "%9:q": {"name": "Finished", "type": "checkbox"},
        "=d{|": {
            "name": "Category",
            "type": "multi_select",
            "options": [
                {
                    "color": "orange",
                    "id": "79560dab-c776-43d1-9420-27f4011fcaec",
                    "value": "Lecture",
                },
                {
                    "color": "red",
                    "id": "002c7016-ac57-413a-90a6-64afadfb0c44",
                    "value": "Tutorial",
                },
                {
                    "color": "yellow",
                    "id": "002c7016-ac57-413a-90a6-64afadfb0c45",
                    "value": "Notes",
                },
                {
                    "color": "green",
                    "id": "002c7016-ac57-413a-90a6-64afadfb0c46",
                    "value": "Video",
                },
                {
                    "color": "blue",
                    "id": "002c7016-ac57-413a-90a6-64afadfb0c47",
                    "value": "Lab",
                },
                 {
                    "color": "purple",
                    "id": "002c7016-ac57-413a-90a6-64afadfb0c48",
                    "value": "Answers",
                },
                {
                    "color": "grey",
                    "id": "002c7016-ac57-413a-90a6-64afadfb0c49",
                    "value": "Other",
                },
                {
                    "color": "pink",
                    "id": "002c7016-ac57-413a-90a6-64afadfb0c4a",
                    "value": "Code",
                },

                
                ],
       },
        
        "OBcJ": {"name": "Link", "type": "url"},
        "title": {"name": "Name", "type": "title"},
    }

def add_course(course):
    cvb = page.children.add_new(CollectionViewPageBlock, icon="x")
    cvb.collection = client.get_collection(
    client.create_record("collection", parent=cvb, schema=get_collection_schema()))
    cvb.title = course['title']
    view = cvb.views.add_new(view_type="table") 
    add_materials(cvb, course['code'], access_token)

def add_materials(cvb, code, access_token):
    materials = get_materials(code, access_token)
    for material in materials:
        row = cvb.collection.add_row()
        title = material['title']
        row.name = title
        tags = material['tags']
        path = material['path']
        options = []
        schema = get_collection_schema()
        for option in (schema["=d{|"])['options']:            
            options.append(option['value'])

        if tags != []:            
            valid_tags = []
            for tag in tags:
                if tag.title() in options:
                    valid_tags.append(tag)
            tags = valid_tags        
        else:            
            if "panopto" in path:
                tags.append("Lecture")
                tags.append("Video")
            if "slides" in title.lower() or "notes" in title.lower():
                tags.append("Lecture")
                tags.append("Notes")
            if "tutorial" in title.lower():
               tags.append("Tutorial")
            if "answers" in title.lower():
                tags.append("Answers")
            if "lecture" in title.lower():
                tags.append("Lecture")
        if not tags:
            tags.append("Other")
        row.category = tags 
        category = material['category']
        index = material['index']
        start = material['path'][:4] 
        if start != "http":
            row.link = ("https://materials.doc.ic.ac.uk/view/2021/" + code + "/" + category + "/" + str(index)).replace(" ", "%20")
        else:
            row.link = material['path'] 

# Enter details
set_details()
# Load Notion API
page, client = get_page_and_client()
access_token = get_access_token()
# Load courses
courses = get_courses(access_token)
# Using threads
with ThreadPoolExecutor(max_workers=20) as pool: 
    pool.map(add_course, courses)
