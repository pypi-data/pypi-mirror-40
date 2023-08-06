# éClaircie
# Copyright (C) 2018 Jean-Baptiste LAMY

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, os, re, locale
from html import escape

from eclaircie import Post, Category, Page, Archives, Search
from eclaircie.email_obfuscator import email_link
from eclaircie.rst import shift_titles

h1 = re.compile('''<h1.*?>(.*?)</h1>\n?''')

THEMES = {}
def parse_theme_dir(dir):
  for subdir in os.listdir(dir):
    filename = os.path.join(dir, subdir, "theme.conf")
    if os.path.exists(filename):
      theme = THEMES.get(subdir) or Theme(subdir)
      theme.load(filename)

_CACHE = {}

class Theme(object):
  def __init__(self, name):
    self.name = name
    self.filename = ""
    self.parent = None
    self.stylesheets = []
    self.javascripts = []
    self.pygments_style = "sphinx"
    THEMES[self.name] = self
    
  def __repr__(self): return "<Theme '%s'>" % self.name
    
  def load(self, filename):
    self.filename = filename
    for line in open(filename).read().split("\n"):
      if (not line) or (line[0] == "#") or (line[0] == "["): continue
      option, value = line.split("=", 1)
      option = option.strip()
      value  = value .strip()
      if   option == "inherit": self.parent = THEMES.get(value) or Theme(value)
      elif option == "pygments_style": self.pygments_style = value
      elif option == "stylesheet": self.stylesheets.append(value)
      elif option == "javascript": self.javascripts.append(value)
      else:
        raise ValueError("Unknown option in theme config file: '%s' in '%s'!" % (line, filename))
      
  def get_stylesheets(self):
    if self.parent: return self.parent.get_stylesheets() + self.stylesheets
    else:           return self.stylesheets
    
  def get_javascripts(self):
    if self.parent: return self.parent.get_javascripts() + self.javascripts
    else:           return self.javascripts
    
  def symlink_files(self, blog_dir):
    if not self.filename: return
    from eclaircie import symlink
    static_dir = os.path.join(os.path.dirname(self.filename), "static")
    for filename in os.listdir(static_dir):
      full_filename = os.path.join(static_dir, filename)
      symlink(full_filename, os.path.join(blog_dir, "_static", filename))
      
  def perspective_title(self, pages, page):
    html = ""
    is_post = isinstance(pages[-1].doc, Post)
    if is_post: pages2 = pages[:-1]
    else:       pages2 = pages
    for i in range(len(pages2) - 1):
      html += """<span style="font-size: smaller;">"""
    for page2 in pages2:
      if page2 is pages2[-1]:
        if (not is_post) and (page2 is page):
          html += """%s""" % page2.get_title()
        else:
          html += """%s&nbsp;/""" % page2.get_hyperlink()
      else:
        html += """%s&nbsp;/</span> """ % page2.get_hyperlink()
        
    html = """<div class="related1 related"><div class="related1wrapper">%s</div></div>""" % html
    return html
  
  def side_bar(self, pages, lang):
    icons = ["""<div class="links"><span class="link-lang">"""]
    html_pages = pages[-1].doc.get_html_pages()
    for lang2 in sorted(pages[0].doc.blog.langs, key = lambda l: l.priority):
      page = html_pages.get(lang2)
      if page:
        filename = os.path.abspath(pages[-1].filename)[:-7].rsplit(os.sep, 1)[-1]
        icons.append("""<a class="link-lang" href="%s%s.html" title="%s"><img src="__BLOG_HTML_ROOT__/_static/lang_%s.svg"></a>""" % (filename, lang2.langs[0], lang2.name, lang2.langs[0]))
    if len(pages[0].doc.blog.langs) == 1:
      rss_lang = ""
    else:
      rss_lang = "_%s" % pages[-1].lang.langs[0]
    icons.append("""<a class="link-rss" href="news%s.rss" title="RSS"><img src="__BLOG_HTML_ROOT__/_static/rss.svg"></a>""" % rss_lang)
    icons.append("""</span></div>""")
    
    htmls = ["""<h3>%s</h3>""" % pages[0].get_hyperlink()]
    
    doc_2_status = {}
    for page in pages: doc_2_status[page] = 1 # expanded
    if isinstance(pages[-1].doc, Post): doc_2_status[pages[-2]] = 2 # current
    else:                               doc_2_status[pages[-1]] = 2 # current
    
    self._side_bar_category(htmls, pages[0], doc_2_status, lang)
    
    if pages[0].doc.blog.search_doc:
      search_doc  = pages[0].doc.blog.search_doc
      search_page = search_doc.get_html_page(lang)
      search = """<div id="searchbox">
  <h3>%s</h3>
    <form class="search" action="__BLOG_HTML_ROOT__/%s" method="get">
      <input type="text" name="q"/>
    </form>
</div>
""" % (search_page.get_hyperlink(), search_page.get_url())
    else:
      search = ""
    
    html = """%s
<div class="sphinxsidebar" role="navigation" aria-label="main navigation"><div class="sphinxsidebarwrapper">
%s
%s
<h3>eMail</h3>
%s
</div></div>""" % ("\n".join(icons),
                   "\n".join(htmls),
                   search,
                   email_link(pages[0].doc.blog.author_email))
    return html
  
  def _side_bar_category(self, htmls, page_category, doc_2_status, lang):
    htmls.append("<ul>")
    subs = [doc.get_html_page(lang) for doc in page_category.doc.subcategories + page_category.doc.pages]
    subs = [page for page in subs if page]
    subs.sort(key = lambda page: locale.strxfrm(page.get_title().lower()))
    for page in subs:
      if isinstance(page.doc, Search): continue
      status = doc_2_status.get(page, 0)
      if status == 2: 
        htmls.append("""<li class="toctree-l1 current">%s</li>""" % page.get_hyperlink())
      else:
        htmls.append("""<li class="toctree-l1">%s</li>""" % page.get_hyperlink())
      if status and isinstance(page.doc, Category):
        self._side_bar_category(htmls, page, doc_2_status, lang)
    htmls.append("</ul>")
    
  def nav_bar(self, pages, page):
    items = []
    
    if page.lang in page.doc.extra_html_pages:
      pages = [page.doc.get_html_page(page.lang)]
      pages.extend(page.doc.extra_html_pages[page.lang])

      if not page is pages[0]:
        items.append(pages[page.number - 2].get_hyperlink(page.doc.blog.ec_translations[(page.lang.langs[0], "newer_posts")]))
        
      for p in pages:
        if p is page:
          items.append(str(p.number))
        else:
          items.append(p.get_hyperlink(str(p.number)))

      if not page is pages[-1]:
        items.append(pages[page.number].get_hyperlink(page.doc.blog.ec_translations[(page.lang.langs[0], "older_posts")]))
        
    archives_filename = os.path.join(os.path.dirname(page.doc.src_filename), "archives.rst")
    archives = page.doc.blog.src_filename_2_doc.get(archives_filename)
    if archives:
      items.append(archives.get_html_page(page.lang).get_hyperlink())
      
    if not items: return ""
    return """<div class="nav_bar">\n%s\n</div>\n""" % " | ".join(items)
  
  def archives(self, pages, lang):
    doc = pages[-1].doc
    html = ""
    posts = [post.get_html_page(lang) for post in doc.blog.docs if isinstance(post, Post)]
    posts = [post for post in posts if post]
    posts.sort(key = lambda post: post.doc.date)
    
    year  = None
    month = None
    
    for post in posts:
      if post.doc.date.year != year:
        if month: html += """</ul>\n"""
        year  = post.doc.date.year
        month = None
        html += """<h2>%s</h2>\n""" % year
      if post.doc.date.month != month:
        if month: html += """</ul>\n"""
        month = post.doc.date.month
        html += """<h3>%s %s</h3>\n""" % (post.doc.date.strftime("%B"), year)
        html += """<ul>\n"""
        
      html += """<li>%s %s</li>\n""" % (post.doc.date.strftime("%x"), post.get_hyperlink())
      
    if month: html += """</ul>\n"""
    return html
  
  def search(self, pages, lang):
    html = r"""
<br/>
<input type="text" name="q" id="search_input"/><input type="submit" value="Ok" onclick="on_search();"/>
<div id="search_results" class="search_results"></div>
<script>
var q = decodeURIComponent(window.location.search.substring(3));

var db;
var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function(){
  if(xmlhttp.status == 200 && xmlhttp.readyState == 4) {
    var data = new Uint8Array(this.response);
    db = new SQL.Database(data);
    if (q != "") { search(q); }
  }
};
xmlhttp.open("GET", "searchindex_%s.sqlite3", true);
xmlhttp.responseType = "arraybuffer";
xmlhttp.send();

function search(query) {
  query = query.replace("+", " ");
  var keywords = query.split(" ");
  var keywords2 = "";
  for (k in keywords) { keywords2 = keywords2 + keywords[k] + "* "; }
  
  var input = document.getElementById("search_input");
  if (input.value != query) input.value = query;
  
  var results_div = document.getElementById("search_results");
  results_div.innerHTML = "...";
  var rs = db.exec("SELECT page.name, page.title FROM page, fts WHERE fts.text MATCH '" + keywords2 + "' AND page.id = fts.docid;");
  var html = '<h2>%s "' + query + '"</h2><br/><br/>';
  if (rs.length == 0) {
    results_div.innerHTML = html + "<br/>%s";
    return;
  }
  rs = rs[0]["values"];
  for(i in rs) {
    r = rs[i];
    html = html + "<div class='search_result'><b><a href='" + r[0] + "'>" + r[1] + "</a></b><div class='search_excerpt' id='search_excerpt" + i + "'>...</div></div>\n";
  }
  results_div.innerHTML = html;
  for(i in rs) {
    r = rs[i];
    excerpts(r[0], keywords, i);
  }
}

var remove_tag_regexp = new RegExp('<[^>]*>', "g");

function excerpts(name, keywords, excerpt_id) {
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", name, true);
  xmlhttp.responseType = "text";
  xmlhttp.onreadystatechange = function(){
    if(xmlhttp.status == 200 && xmlhttp.readyState == 4) {
      var page_html = xmlhttp.responseText;
      page_html = page_html.substring(page_html.search('<!-- DOCSTART -->') + 17);
      page_html = page_html.substring(0, page_html.search('<!-- DOCEND -->'));
      page_html = page_html.replace(remove_tag_regexp, "");
      page_html = " " + page_html + " ";
      
      var excerpts = "";
      for(i in keywords) {
        var keyword = keywords[i];
        var regexp = new RegExp(keyword, "gi");
        var p = page_html.search(regexp);
        var excerpt = page_html.substring(p - 50, p + 80);
        excerpt = excerpt.substring(excerpt.search(" "));
        excerpt = excerpt.substring(0, excerpt.lastIndexOf(" "));
        excerpt = excerpt.replace(regexp, "<span class='highlighted'>" + keyword + "</span>");
        if (!excerpt.endsWith(".")) { excerpt = excerpt + "..."; }
        excerpts = excerpts + "<div>" + excerpt + "</div>";
      }
      
      var excerpt_div = document.getElementById("search_excerpt" + excerpt_id);
      excerpt_div.innerHTML = excerpts;
    }
  };
  xmlhttp.send();
}
function on_search() {
  var input = document.getElementById("search_input");
  search(input.value);
}

var input = document.getElementById("search_input");
input.addEventListener("keyup", function(event) {
  event.preventDefault();
  if (event.keyCode === 13) on_search();
});
</script>
""" % (pages[-1].lang.langs[0],
       pages[-1].doc.blog.translate("search_result", pages[-1].lang),
       pages[-1].doc.blog.translate("search_no_result", pages[-1].lang))
    
    return html
    
  def htmlize(self, pages, page, lang):
    doc = page.doc
    lang.set_locale_current()

    javascripts = self.get_javascripts()
    if isinstance(page.doc, Search):
      javascripts.append("sql.js")
    styles  = "\n".join("""<link rel="stylesheet" href="__BLOG_HTML_ROOT__/_static/%s" type="text/css"/>""" % (stylesheet) for stylesheet in self.get_stylesheets())
    scripts = "\n".join("""<script type="text/javascript" src="__BLOG_HTML_ROOT__/_static/%s"></script>""" % (script) for script in javascripts)
    
    html = page.get_html()
    
    html = """<!-- DOCSTART -->
%s
<!-- DOCEND -->""" % html
    
    if   isinstance(doc, Post):
      html = """<div class="post-box section">
<div class="post-date container">%s</div>
%s
</div>""" % (page.doc.date.strftime("%x"), html)
    elif isinstance(doc, Archives):
      html = """<div class="section">
%s
%s
</div>""" % (html, self.archives(pages, lang))
    elif isinstance(doc, Search):
      html = """<div class="section">
%s
%s
</div>""" % (html, self.search(pages, lang))
    else:
      if html.strip():
        html = """<div class="section">
%s
</div>""" % html
      else:
        html = """<div>
%s
</div>""" % html
      
    if isinstance(doc, Category):
      nav_bar = self.nav_bar(pages, page)
      html += nav_bar
      
      posts = page.recent_posts
      if posts:
        html += """\n<div class="section" id="commentaires">"""
        for post in posts:
          post_html = shift_titles(post.get_html_pages()[lang].get_html_first_part())
          html += """<div class="post-box section">
<div class="post-date container">%s</div>
<div class="in-category container">%s %s</div>
%s
</div>
""" %  (post.date.strftime("%x"),
        doc.blog.ec_translations[(lang.langs[0], "in_category")],
        " ".join(category.get_html_page(lang).get_hyperlink() for category in post.categories),
        post_html)
        
        html += """\n</div>"""
        
      
    if len(pages) == 1:
      title = escape(pages[0].get_title())
    else:
      title = "%s — %s" % (escape(page.get_title()), escape(pages[0].get_title()))

    end = ""
    if isinstance(doc, Category):
      end = nav_bar
      
    html = """<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
%s
%s
<title>%s</title>
</head>
<body>
%s
%s
<div class="documentwrapper"><div class="bodywrapper"><div class="body" role="main">
%s
</div></div></div>
%s
<script>create_imageviewer();</script>
<div class="bottom">%s</div>
</body></html>""" % (styles, scripts,
                     title,
                     self.side_bar(pages, lang),
                     self.perspective_title(pages, page),
                     html,
                     end,
                     doc.blog.translate("bottom", page.lang),
)
    root = "../" * page.doc.doc_name.count("/")
    #if len(doc.blog.langs) == 1: current_lang = ""
    #else:                        current_lang = "_%s" % lang.langs[0]
    return html.replace("__BLOG_HTML_ROOT__/", root) #.replace("__BLOG_CURRENT_LANG__", current_lang)
  


