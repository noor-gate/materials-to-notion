# materials-to-notion

## Description
Creates a Notion page for each course with all the course materials on it, organised into a table with to-dos, links, and tags. 

## Requirements
  - Be a student in DoC at Imperial College
  - cURL
  - Notion
  
## Usage
  - Clone the repo
  - Create a new Notion page
  - Get the token_v2 cookie from your browser
    - If you are using Chrome, click the padlock to the left of the url, then cookies, then the dropdown titled "www.notion.so", then the cookies folder, then copy the content from token_v2.
    - If you are using Safari, go to Safari -> Preferences -> Advance and tick 'Show Develop menu in menu bar', then go to Develop -> Show Web Inspector. Then click on the Storage tab of the inspector window, click on the Cookies dropdown on the left, click on "www.notion.so", double click the cookie named "token_v2" and copy the value.
  - Run `python3 main.py`
 
 
