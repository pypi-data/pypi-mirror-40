#!/usr/bin/env python3

import sys, os, datetime
from eclaircie import *

langs = [
    Language("Français", "fr_FR.utf8", "fr", "en"),
    Language("English",  "en_US.utf8", "en"),
]


# The number of recent posts displayed per page

number_of_recent_post = 5

# The default theme.
# Per-category themes can be specified in themes.conf

html_theme = 'green_roses'

# This list allows to specify per-category/document themes (overriding the default theme above).

ec_multiple_themes = {
  "themes/champi" : "champi",
  "themes/green_roses" : "green_roses",
  "themes/balazar" : "balazar",
# "category/subcategory" : "theme",
}


# General information about the project.
# Note: you can use '.. lang::' directive here if you want a language-dependent website's title

project      = 'éClaircie' # This is the website's title
author       = 'Jean-Baptiste "Jiba" Lamy'
author_email = "your@email.here"
copyright    = '2014, %s' % author
url          = "http://xxx.org" # This is the final address of the website, online

# Translation strings ; you may want to personalize them or to add additional languages.

year = datetime.date.today().year

ec_translations = {
  ("fr", "older_posts") : "messages plus anciens >",
  ("en", "older_posts") : "older entries >",
  ("fr", "newer_posts") : "< messages plus récents",
  ("en", "newer_posts") : "< newer entries",
  ("fr", "in_category") : "dans",
  ("en", "in_category") : "in",
  ("fr", "more") : "(Suite et commentaires...)",
  ("en", "more") : "(More and comments...)",
  ("fr", "comment") : "(Voir les commentaires...)",
  ("en", "comment") : "(View comments...)",
  ("fr", "comment_title") : "Commentaires",
  ("en", "comment_title") : "Comments",
  ("fr", "add_comment") : "(Ajouter un commentaire - par mail, protège votre vie privée !)",
  ("en", "add_comment") : "(Add a comment - by mail, protect your privacy!)",
  ("fr", "comment_by") : "**Commentaire de %s** (%s)",
  ("en", "comment_by") : "**Comment by %s** (%s)",
  ("fr", "search") : "Recherche",
  ("en", "search") : "Search",
  ("fr", "search_result") : "Résultat de la recherche",
  ("en", "search_result") : "Search results for",
  ("fr", "search_no_result") : "Pas de résultat.",
  ("en", "search_no_result") : "No result.",
  ("fr", "bottom") : """© Copyright %s, Jean-Baptiste "Jiba" Lamy. Propulsé par <a href="http://www.lesfleursdunormal.fr/static/informatique/eclaircie/index_fr.html">éClaircie</a>, le moteur de blog statique et sans nuage !""" % year,
  ("en", "bottom") : """© Copyright %s, Jean-Baptiste "Jiba" Lamy. Powered by <a href="http://www.lesfleursdunormal.fr/static/informatique/eclaircie/index_fr.html">éClaircie</a>, the static cloud-less blog engine!""" % year,
}

# The mail directory where comments mails are located.
# When receiving mails, comment mails can be detected with their "To" header (which starts with the
# website name, i.e. the value of the 'project' option above). They should be moved into a specific folder.
# 
# Set to None to disable comments by mail.

comments_mail_dir = "/home/jiba/mail/blog_comments"
#comments_mail_dir = None

# Maximum size for miniature in image gallery

gallery_miniature_width  = 200
gallery_miniature_height = 150

# Maximum size when importing images in an image gallery (i.e. for images not already located in /_images/)
# Bigger image will be reduced

gallery_import_width     = 1400
gallery_import_height    = 1050


# The following set can be used to tag some categories as "special" and make then not propagate
# their post to the parent caegory.
# Note: the values must be "full" category name, including "/index" at the end,
# for example: "informatique/eclaircie/example_site/index"

ec_dont_propagate_posts_for_categories = set()




