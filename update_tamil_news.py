import requests
import xml.etree.ElementTree as ET

RSS_URL = "https://www.dinamani.com/rss/tamil-news.xml"

response = requests.get(RSS_URL)
response.raise_for_status()

root = ET.fromstring(response.content)
items = root.findall('.//item')

news_list = []
for item in items[:10]:  # Get top 10 news
    title = item.find('title').text
    link = item.find('link').text
    description = item.find('description').text
    news_list.append({'title': title, 'link': link, 'description': description})

html_news = """
<ul>
"""
for news in news_list:
    html_news += f'<li><a href="{news["link"]}" target="_blank">{news["title"]}</a><br><small>{news["description"]}</small></li>\n'
html_news += "</ul>"

with open("/workspaces/amazetime/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Insert news into a div with id="tamil-news" or at the end if not found
if '<div id="tamil-news">' in html:
    html = html.split('<div id="tamil-news">')[0] + '<div id="tamil-news">' + html_news + '</div>'
else:
    html += f'\n<div id="tamil-news">{html_news}</div>'

with open("/workspaces/amazetime/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Tamil news updated in index.html.")
