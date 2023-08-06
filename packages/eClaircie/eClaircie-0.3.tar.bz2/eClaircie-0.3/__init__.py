# éClaircie
# Copyright (C) 2014-2018 Jean-Baptiste LAMY

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

import sys, os, locale
import PIL, PIL.Image
from datetime import date as Date
from collections import defaultdict

from eclaircie.email_obfuscator import *
import eclaircie.rst_ext

VERSION = "0.3"
EC_THEME_PATH = os.path.join(os.path.dirname(__file__), "themes")

def need_update(origs, deriveds):
  for i in range(len(deriveds)):
    if not os.path.lexists(deriveds[i]):
      deriveds[i] = "%s.empty" % os.path.splitext(deriveds[i])[0]
      if not os.path.lexists(deriveds[i]): return True
      
  orig_mtime    = max((os.path.getmtime(orig)    for orig    in origs if os.path.exists(orig)), default = float("inf"))
  derived_mtime = min((os.path.getmtime(derived) for derived in deriveds))
  return orig_mtime > derived_mtime

def write_file(filename, s, touch = False, touch_ref = ""):
  if isinstance(s, str): s = s.encode("utf8")
  if os.path.lexists(filename) and (len(s) == os.path.getsize(filename)):
    old_s = open(filename, "rb").read()
    if s == old_s:
      if touch:
        if os.path.getmtime(filename) < os.path.getmtime(touch_ref):
          print("touch    %s" % filename)
          os.utime(filename)
      return False
    
  print("write    %s" % filename)
  os.makedirs(os.path.dirname(filename), exist_ok = True)
  open(filename, "wb").write(s)
  return True

def reduce_image(filename, dest_filename, max_width = 200, max_height = 150, copy_if_already_small_enough = False):
  if need_update([filename], [dest_filename]):
    if not filename.endswith(".svg"):
      image = PIL.Image.open(filename)
      if (image.size[0] > max_width) or (image.size[1] > max_height):
        if image.size[0] * max_height  > image.size[1] * max_width:
          if int(image.size[0] * max_height / image.size[1]) > max_width * 1.4:
            image.thumbnail((max_width, int(image.size[1] * max_width / image.size[0])), 1)
          else:
            image.thumbnail((100000, max_height), 1)
        else:
          image.thumbnail((100000, max_height), 1)
        print("create   %s" % dest_filename)
        image.save(dest_filename)
        return
        
    if copy_if_already_small_enough:
      print("create   %s" % dest_filename)
      data = open(filename, "rb").read()
      open(dest_filename, "wb").write(data)
      


class Doc(object):
  def __init__(self, blog, src_filename):
    self.blog           = blog
    self.src_filename   = src_filename
    self.categories     = []
    self.doc_name       = os.path.splitext(os.path.relpath(src_filename, blog.blog_dir))[0]
    self.empty_filename = "%s.empty" % os.path.join(blog.blog_dir, self.doc_name)
    self.empty          = os.path.exists(self.empty_filename) and (os.path.getsize(self.empty_filename) == 0)
    self.html_pages     = None
    self.changed        = False
    self.need_update    = False
    self.html_filenames = {}
    self.extra_html_pages = {}
    
    for path, theme in self.blog.ec_multiple_themes:
      if self.doc_name.startswith(path):
        self.theme = theme
        break
    
    if len(blog.langs) == 1:
      f = src_filename[len(blog.blog_dir):]
      if f.startswith(os.sep): f = f[1:]
      f = os.path.join(blog.blog_dir, "html", f)
      f = "%s.html" % os.path.splitext(f)[0]
      self.html_filenames[blog.langs[0]] = f
    else:
      for lang in blog.langs:
        f = src_filename[len(blog.blog_dir):]
        if f.startswith(os.sep): f = f[1:]
        f = os.path.join(blog.blog_dir, "html", f)
        f = "%s_%s.html" % (os.path.splitext(f)[0], lang.langs[0])
        self.html_filenames[lang] = f
        
    blog.docs.append(self)
    
  def __repr__(self):
    extra = ""
    if self.theme and (not self.theme is self.blog.ec_multiple_themes[-1][1]): extra += " theme=%s" % self.theme.name
    #extra += " theme=%s" % self.theme.name
    if self.need_update: extra += " NEED UPDATE"
    return "<%s '%s'%s>" % (self.__class__.__name__, self.src_filename, extra)
    
  def add_link(self, link_filename): raise ValueError("Symlink are supported only for posts.")
  
  def ready(self):
    if "/" in self.doc_name: self.categories = [self.blog.categories_dict[os.path.dirname(self.doc_name)]]
    else:                    self.categories = [self.blog.categories_dict[""]]
    
  def get_src_filenames(self): return [self.src_filename]

  def assert_need_update(self): self.need_update = True
  
  def check_update(self, force = False):
    if force:
      print("changed  %s (force)" % self.src_filename)
      self.changed = self.need_update = True
    else:
      html_filenames = [filename for filename in self.html_filenames.values() if os.path.exists(filename)]
      if (not html_filenames) or need_update(self.get_src_filenames(), html_filenames):
        self.changed = self.need_update = True
        print("changed  %s" % self.src_filename)
        
  #def update_sibling(self):
  #  for category in self.category:
  #    for doc in category.post, category.pages:
  #      doc.need_update = True
        
  def get_html_page(self, lang):
    html_pages = self.get_html_pages()
    for sublang in lang.langs:
      html_page = html_pages.get(LANGS[sublang])
      if html_page: return html_page
    return None
  
  def get_html_pages(self):
    if self.html_pages is None:
      self.html_pages = {}
      src = self.get_source()
      lang_2_rst = split_lang(src)
      
      docs = []
      doc = self
      while doc:
        docs.insert(0, doc)
        doc = doc.categories[0]
        
      for lang, rst in lang_2_rst.items():
        html_page = self.create_html_page(docs, lang, rst)
        self.html_pages[lang] = html_page
        
    return self.html_pages
  
  def create_html_page(self, docs, lang, rst):
    return HTMLPage(self.html_filenames[lang], docs, lang, rst, self.theme)
  
  def build(self):
    if self.need_update:
      print("build    %s as %s" % (self.src_filename, self.__class__.__name__))
      self.get_html_pages() # Generate HTML pages
      
  def get_source(self):
    print("read     %s" % self.src_filename)
    return open(self.src_filename).read()
  
  def save_html_pages(self):
    if self.need_update and self.html_pages:
      for html_page in self.html_pages.values():
        write_file(html_page.filename, html_page.get_html_page(), touch = True, touch_ref = self.src_filename)
      for html_pages in self.extra_html_pages.values():
        for html_page in html_pages:
          write_file(html_page.filename, html_page.get_html_page())
          
class Page(Doc):
  def ready(self):
    super().ready()
    for category in self.categories: category.pages.append(self)
    
class Archives(Page):
  def check_update(self, force = False):
    super().check_update(force)
    for category in self.categories:
      for doc in category.posts_rec: # Archives are placed at the end => ok
        if doc.changed: self.changed = self.need_update = True
        break
      
class Include(Doc):
  def ready(self):
    super().ready()
    for category in self.categories: category.includes.append(self)

class CommentsInclude(Include):
  def ready(self):
    self.post = self.blog.src_filename_2_doc.get(self.src_filename[:-13] + ".rst")
    if self.post:
      self.post.comments_include = self
    else:
      print("WARNING: comments include for unknown post: '%s'!" % self.src_filename)
      
  def assert_need_update(self): pass
  def check_update(self, force = False): pass
  
  def build(self): pass
  
  def get_html_pages(self): return {}
  
class Search(Page):
  def ready(self):
    super().ready()
    for category in self.categories: category.pages.append(self)
    self.blog.search_doc = self
    
class Post(Doc):
  def __init__(self, blog, src_filename, date):
    super().__init__(blog, src_filename)
    self.date = date
    self.link_filenames = []
    self.comments_include = None
    
  def formated_date(self): return self.date.strftime("%x")
  
  def add_link(self, link_filename):
    self.link_filenames.append(link_filename)
    
  def get_src_filenames(self): return [self.src_filename, "%s_comments.inc" % self.src_filename[:-4]]
    
  def ready(self):
    super().ready()
    
    for link_filename in self.link_filenames:
      link_doc_name = os.path.splitext(os.path.relpath(link_filename, self.blog.blog_dir))[0]
      if "/" in link_doc_name: self.categories.append(self.blog.categories_dict[os.path.dirname(link_doc_name)])
      else:                    self.categories.append(self.blog.categories_dict[""])
      
    ancestor_categories = set()
    for category in self.categories:
      category.posts.append(self)
      while category:
        ancestor_categories.add(category)
        if category.doc_name in self.blog.ec_dont_propagate_posts_for_categories: break
        category = category.categories[0]
        
    for ancestor_category in ancestor_categories: ancestor_category.posts_rec.append(self)
    
  def check_update(self, force = False):
    super().check_update(force)
    if self.comments_include:
      self.comments_include.check_update(force)
      if self.comments_include.need_update: self.need_update = True
    
  def create_html_page(self, docs, lang, rst):
    if self.comments_include:
      comments = self.comments_include.get_source()
      lang_2_comments = split_lang(comments)
      comments = lang_2_comments.get(lang, "")
    else:
      comments = ""
      
    return HTMLPage(self.html_filenames[lang], docs, lang, rst, self.theme, comments = comments)
      
  
class Category(Doc):
  def __init__(self, blog, src_filename):
    super().__init__(blog, src_filename)
    self.subcategories = []
    self.pages         = []
    self.includes      = []
    self.posts         = []
    self.posts_rec     = [] # Posts, including posts in subcategories
    if "/" in self.doc_name: self.category_name = self.doc_name.rsplit("/", 1)[0] # Remove "/index"
    else:                    self.category_name = "" # Root category
    if   "/" in self.category_name: self.categories = [blog.categories_dict[self.category_name.rsplit("/", 1)[0]]]
    elif self.category_name:        self.categories = [blog.categories_dict[""]]
    else:                           self.categories = [None]  # Root category
    if self.categories[0]: self.categories[0].subcategories.append(self)
    
    blog.categories_dict[self.category_name] = self
    
  def ready(self):
    pass # Disable Doc's behavior
    self.subcategories.sort(key = lambda category: category.doc_name)
    self.pages        .sort(key = lambda page:     page.doc_name)
    self.posts        .sort(key = lambda post:     post.date)
    self.posts_rec    .sort(key = lambda post:     post.date)
    
  def check_update(self, force = False):
    super().check_update(force)
    
    cascade_update = self.changed
    
    archives = []
    for doc in self.pages + self.includes + self.posts + self.subcategories:
      if isinstance(doc, Archives): archives.append(doc)
      else:
        doc.check_update(force)
        #if doc.need_update:
        if doc.changed:
          self.need_update = True
          if isinstance(doc, Page) or isinstance(doc, Category):
            cascade_update = True # Page/category title might have changed
            
    for doc in archives: # Archives page need to be checked AFTER the index, not before, because it depends on its posts.
      doc.check_update(force)
      if doc.need_update:
        self.need_update = True
        cascade_update = True
        
    if not self.need_update:
      for post in self.posts_rec:
        if post.changed:
          self.need_update = True
          break
        
    if cascade_update:
      for doc in self.pages + self.includes + self.posts + self.subcategories:
        doc.assert_need_update()
        
  def assert_need_update(self):
    super().assert_need_update()
    for doc in self.pages + self.includes + self.posts + self.subcategories: doc.assert_need_update()
    
  def get_posts_rec(self, lang):
    r = []
    for post in self.posts_rec:
      if post.get_html_page(lang): r.append(post)
    r.sort(key = lambda doc: doc.date)
    r.reverse()
    return r
  
  def create_html_page(self, docs, lang, rst):
    posts_rec = self.get_posts_rec(lang)
    if len(posts_rec) <= self.blog.number_of_recent_post:
      recents = posts_rec
    else:
      recentss = [[]]
      for post in posts_rec:
        if post.empty: continue
        recentss[-1].append(post)
        if len(recentss[-1]) >= self.blog.number_of_recent_post: recentss.append([])
      if not recentss[-1]: del recentss[-1]
      
      self.extra_html_pages[lang] = l = []
      i = 2
      filename = self.html_filenames[lang].rsplit(os.sep, 1)[0]
      if len(self.blog.langs) == 1:
        filename = os.path.join(filename, "ec_recent_posts%s.html")
      else:
        filename = os.path.join(filename, "ec_recent_posts%%s_%s.html" % lang.langs[0])
      for recents in recentss[1:]:
        l.append(HTMLPage(filename % i, docs, lang, "", self.theme, recent_posts = recents, number = i))
        i += 1
      recents = recentss[0]
      
    html_page = HTMLPage(self.html_filenames[lang], docs, lang, rst, self.theme, recent_posts = recents, number = 1)
    return html_page
  
  def build(self):
    archives = []
    for doc in self.pages + self.includes + self.posts + self.subcategories:
      if isinstance(doc, Archives): archives.append(doc)
      else:                         doc.build()
      
    super().build()
    
    for doc in archives: # Archives page need to be built AFTER the index, not before, because it depends on it.
      doc.build()
    
  def save_html_pages(self):
    super().save_html_pages()
    
    if self.need_update and self.html_pages:
      for html_page in self.html_pages.values():
        rss = html_page.get_rss_page()
        f1, f2 = html_page.filename.rsplit(os.sep, 1)
        f2 = "news%s.rss" % f2[5:-5]
        filename = os.path.join(f1, f2)
        write_file(filename, rss)
        

SPECIAL_DOCS = {}
BLOG = None
class Blog(object):
  def __init__(self, blog_dir, langs, number_of_recent_post, ec_multiple_themes, ec_translations, title, author, author_email, url, ec_dont_propagate_posts_for_categories):
    global BLOG
    BLOG                       = self
    self.blog_dir              = blog_dir
    self.langs                 = langs
    self.number_of_recent_post = number_of_recent_post
    self.ec_multiple_themes    = ec_multiple_themes
    self.ec_translations       = ec_translations
    self.docs                  = []
    self.categories_dict       = {}
    self.changed_categories    = []
    self.title                 = title
    self.author                = author
    self.author_email          = author_email
    self.url                   = url
    self.src_filename_2_doc    = {}
    self.pending_links         = defaultdict(list)
    self.ec_dont_propagate_posts_for_categories = ec_dont_propagate_posts_for_categories
    self.search_doc            = None

  def translate(self, txt, lang):
    if isinstance(lang, str):
      return self.ec_translations[(lang, txt)]
    else:
      for l in lang.langs:
        if (l, txt) in self.ec_translations: return self.ec_translations[l, txt]
    
  def scan_files(self, ignored_dirs = set()):
    config_file = os.path.join(self.blog_dir, "conf.py")
    
    for dirpath, dirnames, filenames in os.walk(self.blog_dir):
      if dirpath in ignored_dirs: dirnames[:] = []; continue
      
      for filename in filenames:
        if filename in SPECIAL_DOCS: continue
        full_filename = os.path.join(dirpath, filename)
        if filename.endswith(".rst") or filename.endswith(".inc"): self.create_doc(full_filename)
        
    # Put archives at the end
    archives = [doc for doc in self.docs if isinstance(doc, Archives)]
    for doc in archives: self.docs.remove(doc)
    self.docs.extend(archives)
    
  def create_doc(self, src_filename):
    if os.path.islink(src_filename):
      link_target = os.readlink(src_filename)
      if link_target.startswith("."): link_target = os.path.join(os.path.dirname(src_filename), link_target)
      link_target = os.path.normpath(link_target)
      if link_target in self.src_filename_2_doc: self.src_filename_2_doc[link_target].add_link(src_filename)
      else:                                      self.pending_links[link_target].append(src_filename)
      return
    
    date = is_post(src_filename)
    doc  = None
    if   src_filename.endswith("_comments.inc"): doc = CommentsInclude(self, src_filename)
    elif src_filename.endswith(".inc"):          doc = Include        (self, src_filename) # Must be checked before posts, for comments includes
    elif date:                                   doc = Post           (self, src_filename, date)
    elif src_filename.endswith("archives.rst"):  doc = Archives       (self, src_filename)
    elif src_filename.endswith("search.rst"):    doc = Search         (self, src_filename)
    elif src_filename.endswith("index.rst"):     doc = Category       (self, src_filename)
    else:                                        doc = Page           (self, src_filename)
    if doc: self.src_filename_2_doc[src_filename] = doc
    
    if src_filename in self.pending_links:
      for pending_link in self.pending_links[src_filename]: doc.add_link(pending_link)
      del self.pending_links[src_filename]
    
  def ready(self):
    for doc in self.docs: doc.ready()
    themes = set()
    for doc in self.docs:
      theme = doc.theme
      while theme:
        themes.add(theme)
        theme = theme.parent
    for theme in themes: theme.symlink_files(self.blog_dir)

  def check_update(self, force = False):
    self.categories_dict[""].check_update(force)
    
  def build(self):
    self.categories_dict[""].build()
    
  def save_html_pages(self):
    for doc in self.docs: doc.save_html_pages()
    
  def build_search(self, force = False):
    start_char = len(self.blog_dir) + 5 # 5 is for /html
    if not self.blog_dir.endswith(os.sep): start_char += 1
    
    # Use 2 db because Sqlite does not accept to remove/update from content-less table
    
    import sqlite3
    for lang in self.langs:
      db_filename0 = os.path.join(self.blog_dir, "searchdb%s.sqlite3"    % lang.get_suffix())
      if force:
        try: os.unlink(db_filename0)
        except: pass
        new_db = True
      else:
        new_db = not os.path.exists(db_filename0)
        
      db0 = sqlite3.connect(db_filename0)
      cursor0 = db0.cursor()
      if new_db:
        cursor0.execute("""CREATE TABLE page(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, title TEXT, text TEXT)""")
      for doc in self.docs:
        if not doc.need_update: continue
        page = doc.get_html_page(lang)
        if page:
          title = page.get_title()
          text = page.get_text()
          text = " ".join(text.split())
          text = "%s %s" % (title, text)
          page_name = page.filename[start_char:]
          if new_db:
            page_id = None
          else:
            page_id = cursor0.execute("""SELECT id FROM page WHERE name=?""", (page_name,)).fetchone()
            if not page_id is None:
              page_id = page_id[0]
              cursor0.execute("""UPDATE page SET title=?, text=? WHERE id=?""", (title, text, page_id,))
          if page_id is None:
            cursor0.execute("""INSERT INTO page VALUES (NULL, ?, ?, ?)""", (page_name, title, text))
            #page_id = cursor.lastrowid
      db0.commit()
      data = list(cursor0.execute("""SELECT id, name, title, text FROM page"""))
      
      db_filename = os.path.join(self.blog_dir, "html", "searchindex%s.sqlite3" % lang.get_suffix())
      try: os.unlink(db_filename)
      except: pass
      db  = sqlite3.connect(db_filename)
      cursor      = db.cursor()
      cursor.execute("""PRAGMA page_size=1024""")
      cursor.execute("""CREATE TABLE page(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, title TEXT)""")
      cursor.execute("""CREATE VIRTUAL TABLE fts USING fts4(content="", text, matchinfo=fts3)""")
      db.executemany("INSERT INTO page VALUES (?,?,?)", [(page_id, page_name, title) for (page_id, page_name, title, text) in data])
      db.executemany("INSERT INTO fts(docid, text) VALUES (?,?)", [(page_id, text) for (page_id, page_name, title, text) in data])
      cursor.execute("""INSERT INTO fts(fts) VALUES('optimize')""")
      db.commit()
      cursor0.close()
      cursor.close()
      db.execute("""VACUUM;""")
      db0.close()
      db.close()
      
      
def is_post(src_filename):  
  try:
    year, month, day, title = os.path.basename(src_filename).split("_", 3)
    return Date(int(year), int(month), int(day))
  except: return None

def symlink(src, dest):
  if os.path.lexists(dest):
    if os.path.islink(dest):
      dest_link = os.path.join(os.path.dirname(dest), os.readlink(dest))
      if os.path.samefile(dest_link, src): return
    os.unlink(dest)
  print("link  %s" % dest)
  os.symlink(src, dest)

def do(s):
  print("\n%s" % s)
  if os.system(s) != 0:
    print("\nÉCHEC!")
    sys.exit()

LANGS = {}
class _Language(object):
  def __init__(self, name, locale, *langs):
    self.name     = name
    self.locale   = locale
    self.langs    = langs
    self.priority = len(LANGS) + 1
    LANGS[langs[0]] = self
    
  def __repr__(self): return "<Language '%s'>" % self.langs[0]
  
  def set_locale_current(self):
    locale.setlocale(locale.LC_ALL, self.locale)
    
  def get_suffix(self):
    if len(LANGS) == 1: return ""
    return "_%s" % self.langs[0]
  
def Language(name, locale, *langs):
  if langs[0] in LANGS: return LANGS[langs[0]]
  return _Language(name, locale, *langs)

AVAILABLES_DOC_LANGS = {}
def get_available_doc_langs(doc_name):
  if not doc_name in AVAILABLES_DOC_LANGS:
    langs = set()
    src_filename = os.path.join(BLOG.blog_dir, "%s.rst" % doc_name)
    if os.path.exists(src_filename):
      print("readlang %s" % src_filename)
      s = open(src_filename).read()
      for line in s.split("\n"):
        if line.startswith(".. lang::"):
          lang = LANGS.get(line[len(".. lang::"):].strip())
          if lang: langs.add(lang)
    else: langs = LANGS.values() # Search page, etc
    AVAILABLES_DOC_LANGS[doc_name] = sorted(langs, key = lambda x: x.priority)
  return AVAILABLES_DOC_LANGS[doc_name]


from eclaircie.rst   import *
from eclaircie.theme import *
from eclaircie.page  import *


BLOG = None
EC_TRANSLATIONS = None
EC_HAS_COMMENTS = False
def run(conf_filename, force = False):
  global EC_TRANSLATIONS, EC_HAS_COMMENTS, BLOG
  d = {}
  s = open(conf_filename).read().split("\n")
  s = "\n".join(l for l in s if not l.startswith(".. lang::"))
  exec(s, d)
  blog_dir                 = os.path.dirname(conf_filename)
  number_of_recent_post    = d["number_of_recent_post"]
  EC_TRANSLATIONS          = d["ec_translations"]
  title                    = d["project"]
  author                   = d["author"]
  author_email             = d["author_email"]
  url                      = d["url"]
  comments_mail_dir        = d["comments_mail_dir"]
  gallery_miniature_width  = d["gallery_miniature_width"]
  gallery_miniature_height = d["gallery_miniature_height"]
  gallery_import_width     = d["gallery_import_width"]
  gallery_import_height    = d["gallery_import_height"]
  ec_translations          = d["ec_translations"]
  ec_dont_propagate_posts_for_categories = d["ec_dont_propagate_posts_for_categories"]
  
  os.makedirs(os.path.join(blog_dir, "html"), exist_ok = True)
  
  parse_theme_dir(os.path.join(os.path.dirname(__file__), "themes"))
  
  ec_multiple_themes = d.get("ec_multiple_themes") or {}
  ec_multiple_themes[""] = d.get("html_theme", "ec_base")
  ec_multiple_themes = [ (path, THEMES[theme_name]) for path, theme_name in ec_multiple_themes.items() ]
  ec_multiple_themes.sort(key = lambda category_theme: len(category_theme[0]), reverse = True)
  
  if comments_mail_dir:
    EC_HAS_COMMENTS = True
    import eclaircie.comments
    comments_changed_doc_names = eclaircie.comments.update_comments(blog_dir, title, EC_TRANSLATIONS, comments_mail_dir, force)
    
  symlink(os.path.join(blog_dir, "_static"),    os.path.join(blog_dir, "html", "_static"))
  symlink(os.path.join(blog_dir, "_images"),    os.path.join(blog_dir, "html", "_images"))
  symlink(os.path.join(blog_dir, "_downloads"), os.path.join(blog_dir, "html", "_downloads"))
  
  for dirpath, dirnames, filenames in os.walk(os.path.join(blog_dir, "_images")):
    for filename in filenames:
      if filename.startswith("miniature_"): continue
      if filename.startswith("youtube_preview_"): continue
      reduce_image(os.path.join(dirpath, filename), os.path.join(dirpath, "miniature_%s" % filename), gallery_miniature_width, gallery_miniature_height)
      
  langs = sorted(LANGS.values(), key = lambda lang: 0 if lang.langs[0] == "en" else 1) # Start by English
  BLOG = Blog(blog_dir, langs, number_of_recent_post, ec_multiple_themes, ec_translations, title, author, author_email, url, ec_dont_propagate_posts_for_categories)
    
  ignored_dirs = {
    os.path.join(blog_dir, "html"), os.path.join(blog_dir, "_static"),
    os.path.join(blog_dir, "_images"), os.path.join(blog_dir, "_downloads")
  }
  
  for dirpath, dirnames, filenames in os.walk(os.path.join(blog_dir)):
    if dirpath in ignored_dirs: dirnames[:] = []; continue
    for filename in filenames:
      if filename.endswith(".py") and (filename != "conf.py"):
        filename = os.path.join(dirpath, filename)
        print("running  %s..." % filename)
        py = open(filename).read()
        exec(py, { "__file__" : filename } )
        
  BLOG.scan_files(ignored_dirs)
  BLOG.ready()
  BLOG.check_update(force)
  BLOG.build()
  BLOG.save_html_pages()
  BLOG.build_search(force)
  
  if len(LANGS) > 1:
    index_filename = os.path.join(blog_dir, "html", "index.html")
    if not os.path.exists(index_filename):
      s = """<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<body>

<script language="javascript"><!--
var language = window.navigator.userLanguage || window.navigator.language;
language = language.slice(0,2);
"""
      for lang in LANGS.values():
        s += """if (language == "%s") document.location.href="index_%s.html";\n""" % (lang.langs[0], lang.langs[0])
      s += """else document.location.href="index_en.html";
//--></script>
<p>This site is available in several languages:</p>\n"""
      for lang in LANGS.values():
        s += """<a href="index_%s.html">%s</a><br/>\n""" % (lang.langs[0], lang.name)
      s += """</body></html>"""
      open(index_filename, "w").write(s)
    
