import sys, os, re, io
import docutils.writers.html5_polyglot as html_writer
#import docutils.writers.html4css1 as html_writer
import docutils.core, docutils.nodes
from docutils.parsers.rst import roles

import eclaircie

class MyTranslator(html_writer.HTMLTranslator):
  def __init__(self, document):
    super().__init__(document)
    
  def visit_image(self, node):
    super().visit_image(node)
    self.body[-1] = self.body[-1].replace('"/_images', '"__BLOG_HTML_ROOT__/_images', )
    
  def visit_title_reference(self, node):
    splitted = node.children[0].split("<", 1)
    if len(splitted) == 2:
      label, ref = splitted
      ref = ref.rsplit(">", 1)[0]
    else:
      label = ""
      ref = splitted[0]

    if "#" in ref:
      ref, anchor = ref.split("#", 1)
      anchor = "#%s" % anchor
    else:
      anchor = ""
      
    if ref.startswith("/"):
      src_filename = os.path.join(eclaircie.BLOG.blog_dir, ref[1:])
    else:
      src_filename = os.path.join(eclaircie.BLOG.blog_dir, CURRENT_PATH, ref)
    src_filename = os.path.abspath(src_filename)
    
    doc = eclaircie.BLOG.src_filename_2_doc.get(src_filename + ".rst")
    if not doc:
      doc = eclaircie.BLOG.src_filename_2_doc.get(src_filename + "/index.rst")
      if not doc:
        print(src_filename)
        raise ValueError
    ref = doc.doc_name
    
    if not label.strip():
      if len(eclaircie.BLOG.langs) == 1:
        lang = eclaircie.BLOG.langs[0].langs[0]
      else:
        lang = CURRENT_LANG_PREFIX[1:]
      label = doc.get_html_page(eclaircie.LANGS[lang]).get_title()
    
    node.children[0] = docutils.nodes.Text(label.strip())
    self.body.append(self.starttag(node, 'a', href = "__BLOG_HTML_ROOT__/%s%s.html%s" % (ref, CURRENT_LANG_PREFIX, anchor), CLASS = "reference internal"))
    
  def depart_title_reference(self, node):
    self.body.append('</a>')
    
  def visit_DownloadNode(self, node):
    splitted = node.children[0].split("<", 1)
    if len(splitted) == 2:
      label, ref = splitted
      ref = ref.rsplit(">", 1)[0]
    else:
      label = ""
      ref = splitted[0]
      
    node.children[0] = docutils.nodes.Text((label or ref.rsplit(os.sep, 1)[1]).strip())
    self.body.append(self.starttag(node, 'a', href = "__BLOG_HTML_ROOT__%s" % ref, CLASS = "download reference internal"))
    
  def depart_DownloadNode(self, node):
    self.body.append('</a>')
    
  def visit_literal_block(self, node):
    self.body.append(self.starttag(node, 'pre', '', CLASS = 'literal-block'))
    if 'code' in node.get('classes', []):
      self.body.append('<code>')
      
  def depart_literal_block(self, node):
    if 'code' in node.get('classes', []):
      self.body.append('</code>')
    self.body.append('</pre>\n')
    
  def visit_system_message(self, node):
    #print(" ".join(node.traverse(docutils.nodes.Text)))
    node.children = []
    
  def depart_system_message(self, node):
    pass
  
writer = html_writer.Writer()
writer.translator_class = MyTranslator

def doc_role(name, rawtext, text, lineno, inliner, options = {}, content = []):
  node = docutils.nodes.title_reference(rawtext, text, **options)
  return [node], []
roles.register_canonical_role("doc", doc_role)

class DownloadNode(docutils.nodes.Inline, docutils.nodes.TextElement): pass

def download_role(name, rawtext, text, lineno, inliner, options = {}, content = []):
  node = DownloadNode(rawtext, text, **options)
  return [node], []
roles.register_canonical_role("download", download_role)

CURRENT_LANG_PREFIX = ""
CURRENT_PATH = ""

title_regexp = re.compile(r"</?h[1-9]>")

def fix_titles(html):
  nb = 0
  def rep(match):
    nonlocal nb
    nb += 1
    if nb >= 2:
      h = match.group()
      level = int(h[-2])
      return "%s%s>" % (h[:-2], level + 1)
    return match.group()
  return title_regexp.sub(rep, html)

def shift_titles(html, offset = 1):
  def rep(match):
    h = match.group()
    level = int(h[-2])
    return "%s%s>" % (h[:-2], max(level + offset, 0))
  return title_regexp.sub(rep, html)
  
  
def rst_2_html(rst, lang, path, orig_file):
  global CURRENT_LANG_PREFIX, CURRENT_PATH
  if lang: CURRENT_LANG_PREFIX = "_%s" % lang
  else:    CURRENT_LANG_PREFIX = ""
  CURRENT_PATH = path
  
  ##html = docutils.core.publish_string(rst, writer = writer).decode("utf8")
  #parts = docutils.core.publish_parts(source = rst, writer_name = "html")
  
  sys.stderr = buf = io.StringIO()
  parts = docutils.core.publish_parts(source = rst, writer = writer)
  sys.stderr = sys.__stderr__
  err = buf.getvalue()
  if err:
    print("WARNING: RST error in:", orig_file)
    print(err)
  html = parts["body_pre_docinfo"] + parts["fragment"]
  return fix_titles(html)



if __name__ == "__main__":
  rst = """
Grand titre
===========

bla bla bla...

Petit titre
***********

bla bla bla...

Mini titre
----------

bla bla bla...

Mini titre
----------

bla bla bla...

"""
  print(rst_2_html(rst, "", "", ""))
  
