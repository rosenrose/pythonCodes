from bs4 import BeautifulSoup
from mitmproxy import ctx

with open('content.js') as f:
    content_js = f.read()

def response(flow):
    if flow.response.headers['Content-Type'] != 'text/html':
        return
    if not flow.response.status_code == 200:
        return

    html = BeautifulSoup(flow.response.text, 'lxml')
    container = html.head or html.body
    if container:
        script = html.new_tag('script', type='text/javascript')
        script.string = content_js
        cpontainer.insert(0,script)
        flow.response.text = str(html)
        ctx.log.info('Successfully injected the content.js script.')