import mistune
import os
import json
import datetime
from jinja2 import Template
from pygments import highlight
from pygments.lexer import  get_lexer_by_time
from pygments.formatters import HtmlFormatter

ARTICLE_DATA = []
TEMPLATES = {}

def load_templates():
    """
        Load the templates defined in templates dir in .tpl format
    """

    global TEMPLATES
    
    for filename in os.listdir("./templates"):
        with open('./templates/' + filename, 'r') as f:
            TEMPLATES.update({ filename.rstrip(".tpl"): Template(f.read()) })

class BlogContentRenderer(mistune.Renderer):
    
    def block_code(self, code, lang):
        
        global ARTICLE_DATA

        if not lang:
            return '\n<pre><code id="block_code">%s</code></pre>' % mistune.escape(code)

        if lang == "blogcfg":
            article_info = json.loads(code)
            print(article_info)
            ARTICLE_DATA.append(article_info)

            return "" 

        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(linenos=False, cssclass="source")
        return highlight(code, lexer, formatter)

def render_articles():
    """ 
        Renders the markdown content to raw html by mistune, then applied on a
        jinja template and exported to out/
    """
    for md_filename in os.listdir('./content'):
        
        # skip draft files from processing
        if "draft" in md_filename:
            continue

        with open("./content/" + md_filename, 'r') as f:
            
            article_name = md_filename.rstrip('.md')

            print('[+] Rendering Article ', article_name)

            # render the markdown to raw html
            renderer = BlogContentRenderer(escape=True)
            markdown = mistune.Markdown(renderer=renderer)
            raw_html = markdown(f.read())


        # apply the article jinja template to it
        with open("./out/article/" + article_name + '.html', 'w') as html_f:

            html_f.write(render_template('article', {'meta': ARTICLE_DATA[-1],
                'content': raw_html }))

def render_main_page():
    """
        Render the main page by updating with article list
    """
    with open('./out/index.html', 'w') as f:
        f.write(render_template('mainpage', 
            {'articles': ARTICLE_DATA}))
load_templates()
render_articles()
render_main_page()