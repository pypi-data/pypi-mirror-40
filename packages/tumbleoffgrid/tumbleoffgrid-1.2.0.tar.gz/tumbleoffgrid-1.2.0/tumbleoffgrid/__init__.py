from os import path
from zipfile import ZipFile
from pathlib import Path
import webbrowser

EXPORT_FOLDER_NAME = 'tumbleoffgrid'
INDEX_FILENAME = 'index.html'
export_path = path.join(path.expanduser('~'), EXPORT_FOLDER_NAME)
tumble_url = path.join(export_path, INDEX_FILENAME)

def make_link(target, name='', add_break=True):
    link = ''.join(['<a href="', target, '">', name, '</a>'])
    if add_break:
        link = link + '<br />'
    return link

def add_header():
    return "<h1>All your exported links</h1>"

def render(body='', include_header=True):
    DOCTYPE = '<!DOCTYPE html>'
    dom = ''.join([DOCTYPE, '<html><body>'])

    if add_header:
        dom = dom.join([add_header()])
    dom = dom + body + '</body></html>'
    return dom
         

# Get Export filename 
p = Path(export_path)
export_filename = list(p.glob('**/*.zip'))[0]

# Unzip tumblr export
with ZipFile(str(export_filename)) as myzip:
    myzip.extractall(path=export_path)

# Now extract posts.zip
posts_filename = path.join(export_path, 'posts.zip')
with ZipFile(str(posts_filename)) as myzip:
    myzip.extractall(path=export_path)

# all html pages
html_pages_path = Path(path.join(export_path, 'html'))
all_html_pages = list(html_pages_path.glob('**/*.html'))

# Build a page with links
page = ''

for html_page in all_html_pages:
    page = page + make_link(target=str(html_page), 
                            name=html_page.name.replace('.html',''))

render(body=page)
with open(path.join(export_path, INDEX_FILENAME), 'w') as tumbleoffgrid:
    tumbleoffgrid.write(render(body=page))
    
# Run web server
webbrowser.open(tumble_url)
