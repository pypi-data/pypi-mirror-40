def render_markdown(path, template=""):
    pass

def render_template():
    pass

def markdown_to_html(text):
    pass

def url_for(path):
    pass

def static(location):
    pass

def wrap_html(content):
    WRAPPER = """
    <html>
    <head></head>
    <body>{}</body>
    </html>
    """
    return WRAPPER.format(content)
