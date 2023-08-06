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

import sys, os, os.path, locale, urllib, urllib.request, re, codecs, glob
from datetime import date as Date
from html import escape as htmlescape
from docutils import nodes
from docutils.parsers.rst import Directive, directives


import eclaircie, eclaircie.rst, eclaircie.email_obfuscator

def register_directive(directive_class, directive_name = ""):
  directives.register_directive(directive_name or directive_class.__name__[:-9].lower(), directive_class)
  return directive_class

def register_node(node_class):
  setattr(eclaircie.rst.MyTranslator, "visit_%s" % node_class.__name__,  node_class.visit)
  setattr(eclaircie.rst.MyTranslator, "depart_%s" % node_class.__name__, node_class.depart)
  return node_class

  
@register_directive
class GalleryDirective(Directive):
  has_content = True
  
  def run(self):
    base_image_dir = os.path.join(eclaircie.BLOG.blog_dir, "_images")
    if not base_image_dir.endswith(os.path.sep): base_image_dir += os.path.sep
    
    images0 = (" ".join(self.content)).split()
    images = []
    for image0 in images0:
      if "*" in image0:
        filenames = sorted(glob.glob(os.path.join(eclaircie.BLOG.blog_dir, "_images", image0), recursive = True))
      else:
        filenames = [os.path.join(eclaircie.BLOG.blog_dir, "_images", image0)]
      for filename in filenames:
        if os.path.isdir(filename):
          images.extend(sorted(os.path.join(image0, f)
                               for f in os.listdir(filename)
                               if (not f.startswith("miniature_")) and (f.lower().endswith(".png") or f.lower().endswith(".jpeg") or f.lower().endswith(".jpg") or f.lower().endswith(".svg") or f.lower().endswith(".gif"))))
        else:
          images.append(filename[len(base_image_dir):])
    r = []
    next_id = 0
    for image in images:
      if   image.startswith("/"):
        pass
      elif image.startswith("http://") or image.startswith("."):
        r.append(GalleryImageNode(gallery_id = next_id, uri = image, mini = next_id, big = next_id)); next_id += 1
      else:
        dirname = os.path.dirname(image)
        if dirname: dirname = "%s/" % dirname
        big  = "__BLOG_HTML_ROOT__/_images/%s" % image
        mini = "__BLOG_HTML_ROOT__/_images/%sminiature_%s" % (dirname, os.path.basename(image))
        
        if image.endswith(".svg"):
          r.append(GalleryImageNode(gallery_id = next_id, uri = big,  mini = next_id, big = next_id)); next_id += 1
        else:
          r.append(GalleryImageNode(gallery_id = next_id, uri = mini, mini = next_id,     big = next_id + 1)); next_id += 1
          r.append(GalleryImageNode(gallery_id = next_id, uri = big,  mini = next_id - 1, big = next_id)); next_id += 1
    node = GalleryNode()
    node.extend(r)
    return [node]



@register_node
class GalleryNode(nodes.General, nodes.Element):
  @staticmethod
  def visit(self, node):
    self.body.append(self.starttag(node, 'div', CLASS = "gallery"))
    id_2_node = [child for child in node.children]
    
    big_images = []
    for image in id_2_node:
      if image.attributes["gallery_id"] == image.attributes["big"]:
        big = image.attributes["uri"]
        big_images.append("'%s'" % big)
    big_images = "[%s]" % ",".join(big_images)
    
    i = 0
    for image in id_2_node:
      if image.attributes["gallery_id"] == image.attributes["mini"]:
        mini = image.attributes["uri"]
        if mini.endswith(".svg"):
          extra = ' style="height:auto; width:auto; max-width:200px; max-height:150px;"'
        else:
          extra = ""
        self.body.append("""<img class="gallery-img" src="%s" onClick="show_imageviewer(%s, %s);"%s/>\n""" % (mini, big_images, i, extra))
        i += 1
        
  @staticmethod
  def depart(self, node):
    self.body.append('</div>')
    
@register_node
class GalleryImageNode(nodes.image):
  @staticmethod
  def visit (self, node): pass
  @staticmethod
  def depart(self, node): pass
  



@register_directive
class YoutubeDirective(Directive):
  has_content = True
  
  def run(self):
    node = YoutubeNode()
    node.attributes["youtube_id"] = " ".join(self.content).strip()
    return [node]

@register_node
class YoutubeNode(nodes.General, nodes.Element):
  @staticmethod
  def visit(self, node):
    youtube_id = node.attributes["youtube_id"]
    preview_filename = os.path.join(eclaircie.BLOG.blog_dir, "_images", "youtube_preview_%s.jpeg" % youtube_id)
    if not os.path.exists(preview_filename):
      s = urllib.request.urlopen("http://www.youtube.com/embed/%s" % youtube_id).read()
      s = s.decode("utf8")
      preview_url = re.findall('"iurlsd"\s*:\s*"(.*?)"', s)[0].replace("\\", "")
      s = urllib.request.urlopen(preview_url).read()
      open(preview_filename, "wb").write(s)
      
    self.body.append(self.starttag(node, 'div',
                                   style = """background-image: url("__BLOG_HTML_ROOT__/_images/youtube_preview_%s.jpeg");""" % youtube_id,
                                   onclick="""this.innerHTML="<iframe width='640' height='480' src='http://www.youtube.com/embed/%s?autoplay=1' frameborder='0' allowfullscreen='1'></iframe>";""" % youtube_id,
                                   CLASS = "video"))
    self.body.append(self.starttag(node, 'div', CLASS = "video-read"))
    self.body.append(' &gt; ')
    self.body.append('</div>')
    
  @staticmethod
  def depart(self, node):
    self.body.append('</div>')




@register_directive
class AudioDirective(Directive):
  has_content = True
  
  def run(self):
    node = AudioNode()
    node.attributes["filenames"] = [filename.strip() for filename in " ".join(self.content).split()]
    return [node]

EXT_2_MIME = { "ogg" : "audio/ogg", "mp3" : "audio/mpeg" }

@register_node
class AudioNode(nodes.General, nodes.Element):
  @staticmethod
  def visit(self, node):
    filenames = node.attributes["filenames"]
    
    self.body.append(self.starttag(node, 'audio', controls = "1"))
    for filename in filenames:
      self.body.append(self.starttag(node, 'source',
                                     src = "__BLOG_HTML_ROOT__/_downloads/%s" % filename,
                                     type = EXT_2_MIME[filename.rsplit(".")[-1].lower()]))
      self.body.append('</source>')
    self.body.append('Please update your browser for HTML5 audio support.')
    self.body.append('</audio>')
    
    for filename in filenames:
      self.body.append(self.starttag(node, 'p'))
      self.body.append(self.starttag(node, 'a', href = "__BLOG_HTML_ROOT__/_downloads/%s" % filename, CLASS = "reference download internal"))
      self.body.append(self.starttag(node, 'tt', CLASS = "xref download docutils literal"))
      self.body.append(self.starttag(node, 'span', CLASS = "pre"))
      self.body.append('%s</span></tt></a></p>' % filename)
  
  @staticmethod
  def depart(self, node): pass



@register_directive
class RedirectDirective(Directive):
  has_content = True
  
  def run(self):
    node = RedirectNode()
    node.attributes["redirect_url"] = " ".join(self.content).strip()
    return [node]

@register_node
class RedirectNode(nodes.General, nodes.Element):
  @staticmethod
  def visit(self, node):
    self.body.append(self.starttag(node, 'script'))
    self.body.append('window.location="%s";</script>' % node.attributes["redirect_url"])
    
  @staticmethod
  def depart(self, node): pass


@register_directive
class NabbleDirective(Directive):
  has_content = True
  
  def run(self):
    node = NabbleNode()
    contents = (" ".join(self.content)).split()
    node.attributes["nabble_name"] = contents[0]
    node.attributes["nabble_url"]  = contents[1]
    node.attributes["ids"].insert(0, "nabblelink")
    return [node]
  
@register_node
class NabbleNode(nodes.General, nodes.Element):
  @staticmethod
  def visit(self, node):
    self.body.append(self.starttag(node, "a", href = node.attributes["nabble_url"]))
    self.body.append(node.attributes["nabble_name"])
    self.body.append("</a>")
    self.body.append(self.starttag(node, "script", src = "%s/embed/f1" % node.attributes["nabble_url"]))
    self.body.append("</script>")
    
  @staticmethod
  def depart(self, node): pass
