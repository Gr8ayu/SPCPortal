# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "spcportal"
copyright = "2021, Ayush Kumar"
author = "Ayush Kumar"

# The full version, including alpha/beta/rc tags
release = "1.0.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"


extensions = [
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.httpdomain",
    # 'sphinx_tabs.tabs',
    "sphinx-prompt",
    "notfound.extension",
    "hoverxref.extension",
    "sphinx_search.extension",
    "sphinxemoji.sphinxemoji",
    "myst_parser",
    "sphinx_copybutton",
]

# html_theme_options = {
#     # 'analytics_id': 'UA-XXXXXXX-1',  #  Provided by Google in your dashboard
#     # 'analytics_anonymize_ip': False,
#     'logo_only': False,
#     'display_version': False,
#     # 'prev_next_buttons_location': 'bottom',
#     'style_external_links': False,
#     # 'vcs_pageview_mode': '',
#     # 'style_nav_header_background': 'white',
#     # # Toc options
#     'collapse_navigation': True,
#     # 'sticky_navigation': True,
#     'navigation_depth': 4,
#     'includehidden': True,
#     'titles_only': False
# }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
