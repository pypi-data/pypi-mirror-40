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

import sys, os, re, locale, datetime
from html import escape
from urllib.parse import urljoin

from eclaircie import Post, Category, Page, LANGS
from eclaircie.rst import rst_2_html
from eclaircie.email_obfuscator import email_link

h1 = re.compile("""<h1.*?>(.*?)</h1>\n?""")
h2 = re.compile("""<h2.*?>(.*?)</h2>\n?""")

script_regexp = re.compile("""<script.*?</script>""")
to_text = re.compile("""<.*?>""")

def split_lang(rst):
  lang_lines = []
  available_langs = set()
  for line in rst.split("\n"):
    if line.startswith(".. lang::"):
      lang = line[len(".. lang::"):].strip()
      available_langs.add(lang)
      lang_lines.append((lang, []))
    else:
      if not lang_lines: lang_lines.append(("all", []))
      lang_lines[-1][1].append(line)
      
  available_langs.discard("all")
  if not available_langs: available_langs = set(LANGS.keys())
  
  r = {}
  for lang in LANGS.values():
    for included_lang in lang.langs:
      if included_lang in available_langs:
        result_lines = []
        for l, lines in lang_lines:
          if (l == included_lang) or (l == "all"): result_lines.extend(lines)
        r[lang] = "\n".join(result_lines)
        break
      
  return r


class HTMLPage(object):
  def __init__(self, filename, docs, lang, rst, theme, **kargs):
    self.filename  = filename
    self.docs      = docs
    self.doc       = docs[-1]
    self.lang      = lang
    self.rst       = rst
    self.theme     = theme
    self.title     = None
    self.html      = None
    self.html_page = None
    self.has_two_part = False
    self.__dict__.update(kargs)

  def __repr__(self): return "<HTMLPage '%s'>" % self.filename

  def get_url(self):
    return os.path.relpath(self.filename, os.path.join(self.doc.blog.blog_dir, "html"))
  
  def get_hyperlink(self, label = ""):
    return """<a href="__BLOG_HTML_ROOT__/%s">%s</a>""" % (self.get_url(), label or self.get_title())
  
  def get_title(self):
    if self.title is None:
      if len(self.doc.blog.langs) == 1: lang = ""
      else:                             lang = self.lang.langs[0]
      
      path = os.path.relpath(os.path.dirname(self.filename), os.path.join(self.doc.blog.blog_dir, "html"))
      
      if "\n.. more::" in self.rst:
        self.has_two_part = True
        rst_first_part, rst_second_part = self.rst.split("\n.. more::", 1)
        self.html = rst_2_html("\n".join([rst_first_part, rst_second_part]), lang, path, self.filename)
        self.html_first_part = rst_2_html(rst_first_part, lang, path, self.filename)
      else:
        self.html = self.html_first_part = rst_2_html(self.rst, lang, path, self.filename)
        
      self.title = ""
      if isinstance(self.doc, Post):
        def rep(match):
          self.title = match.group(1)
          return "<h1>%s</h1> " % self.get_hyperlink()
        self.html            = h1.sub(rep, self.html)
        self.html_first_part = h1.sub(rep, self.html_first_part)
      else:
        def rep(match):
          self.title = match.group(1)
          return ""
        self.html = h1.sub(rep, self.html)
    return self.title
  
  def get_html(self):
    if self.html is None: self.get_title()
    if isinstance(self.doc, Post):
      if self.comments:
        if len(self.doc.blog.langs) == 1: lang = ""
        else:                             lang = self.lang.langs[0]
        path = os.path.relpath(os.path.dirname(self.filename), os.path.join(self.doc.blog.blog_dir, "html"))
        self.html += "%s\n" % rst_2_html(self.comments, lang, path, self.filename)
        self.html += "%s\n" % self.get_add_comment_link()
      else:
        self.html += "%s\n" % self.get_add_comment_link()
    return self.html
  
  def get_html_first_part(self):
    if self.html is None: self.get_title()
    if self.has_two_part:
      return self.html_first_part + "\n%s" % self.get_hyperlink(label = self.doc.blog.translate("more", self.lang))
    else:
      if self.comments:
        return self.html_first_part + "\n%s" % self.get_hyperlink(label = self.doc.blog.translate("comment", self.lang))
      else:
        return self.html_first_part + "\n%s" % self.get_add_comment_link()
      
  def get_add_comment_link(self):
    return email_link(self.doc.blog.author_email,
                      "%s /%s_%s" % (self.doc.blog.title.replace(" ", ""), self.doc.doc_name, self.lang.langs[0]),
                      self.doc.blog.translate("add_comment", self.lang),
                      localurl = "file://%s" % self.doc.blog.blog_dir,
                      url      = self.doc.blog.url)
  
  def get_html_page(self):
    if self.html_page is None:
      pages = [doc.get_html_pages()[self.lang] for doc in self.docs]
      self.html_page = self.theme.htmlize(pages, self, self.lang)
    return self.html_page
  
  def get_rss_page(self):
    root_category = self.doc.blog.categories_dict[""]
    title = root_category.get_html_page(self.lang).get_title()
    if not root_category is self.doc:
      title = "%s — %s" % (title, self.get_title())
      
    locale.setlocale(locale.LC_ALL, "C") # For strftime(); RSS need dates in english :-(
    date = datetime.date.today().strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    rss = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel>
<title>%s</title>
<link>%s</link>
<description></description>
<language>%s</language>
<pubDate>%s</pubDate>
""" % (title, urljoin(self.doc.blog.url, self.get_url()), self.lang.langs[0], date)
    
    for post in self.recent_posts:
      post_page = post.get_html_page(self.lang)
      url = urljoin(self.doc.blog.url, post_page.get_url())
      html = post_page.get_html_first_part()
      #html += """"""
      rss += """<item>\n"""
      rss += """  <link>%s</link>\n""" % url
      rss += """  <guid>%s</guid>\n""" % url
      rss += """  <title><![CDATA[%s]]></title>\n""" % post_page.get_title()
      rss += """  <description><![CDATA[%s]]></description>\n""" % html
      rss += """  <category><![CDATA[%s]]></category>\n""" % " ".join(category.doc_name for category in post.categories)
      rss += """  <pubDate>%s</pubDate>\n""" % post.date.strftime("%a, %d %b %Y %H:%M:%S +0000")
      rss += """</item>\n"""
      
    rss += """</channel></rss>"""
    return rss
  
  def get_text(self):
    html = self.get_html()
    text = script_regexp.sub(" ", html)
    return to_text.sub(" ", text)
  
