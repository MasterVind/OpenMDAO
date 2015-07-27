# -*- coding: utf-8 -*-
#
# OpenMDAO documentation build configuration file, created by
# sphinx-quickstart on Thu May  7 15:52:54 2015.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.
from mock import Mock
import sys
import os

MOCK_MODULES = ['scipy.sparse.linalg', 'scipy.sparse', 'networkx', 'h5py',
                'petsc4py', 'mpi4py', 'pyoptsparse']
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

#------------------------begin monkeypatch-----------------------
#monkeypatch to make our docs say "Args" instead of "Parameters"
from numpydoc.docscrape_sphinx import SphinxDocString
from numpydoc.docscrape import NumpyDocString, Reader
import textwrap

import openmdao


def generate_docs():
    index_top = """.. _source_documentation:

=============================
OpenMDAO Source Documentation
=============================

.. toctree::
   :maxdepth: 3
   :glob:


"""

    package_top = """
.. toctree::
    :maxdepth: 3

"""

    package_bottom = """
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

    ref_sheet_bottom = """
   :members:
   :undoc-members:
   :show-inheritance:

.. toctree::
   :maxdepth: 2
"""


    # need to set up the srcdocs directory structure, relative to docs.
    dir = os.path.dirname(__file__)
    if os.path.isdir(os.path.join(dir, "srcdocs")):
        import shutil
        shutil.rmtree(os.path.join(dir, "srcdocs"))
    os.mkdir(os.path.join(dir, "srcdocs"))
    os.mkdir(os.path.join(dir, "srcdocs", "packages"))


    # look for directories in the openmdao level, one up from docs
    # those directories will be the openmdao packages
    # auto-generate the top-level index.rst file for srcdocs, based on openmdao packages:
    packages = []
    listings = os.listdir(os.path.join(dir, ".."))
    # Everything in listings that isn't discarded is appended as a source package.
    for listing in listings:
        if os.path.isdir(os.path.join("..", listing)):
            if listing != "docs" and listing != "test" and listing != "config" \
                    and listing != "devtools" and listing != "__pycache__":
                packages.append(listing)

    # begin writing the 'srcdocs/index.rst' file at top level.
    index_filename = os.path.join(dir, "srcdocs", "index.rst")
    index = open(index_filename, "w")
    index.write(index_top)

    # auto-generate package header files (e.g. 'openmdao.core.rst')
    for package in packages:
        # a package is e.g. openmdao.core, that contains source files
        # a sub_package, is a src file, e.g. openmdao.core.component
        sub_packages = []
        package_filename = os.path.join(dir, "srcdocs", "packages", "openmdao." + package + ".rst")
        package_name = "openmdao." + package
        sub_listings = os.listdir(os.path.join("..", package))

        # the sub_listing is going into each package dir and listing what's in it
        for sub_listing in sub_listings:
            # don't want to catalog files twice, nor use init files nor test dir
            if not sub_listing.endswith('.pyc') and not sub_listing.startswith('__init__.') \
                    and not sub_listing.endswith('.ini') and sub_listing != "test" \
                    and not "__pycache__" in sub_listing:
                # just want the name of e.g. dataxfer not dataxfer.py
                sub_packages.append(sub_listing.rsplit('.')[0])

        if len(sub_packages) > 0:
            # continue to write in the top-level index file.
            # only document non-empty packages to avoid errors
            # (e.g. at time of writing, doegenerators, drivers, are empty dirs)
            index.write("   packages/openmdao." + package + "\n")

            # make subpkg directory (e.g. srcdocs/packages/core) for ref sheets
            package_dirname = os.path.join(dir, "srcdocs", "packages", package)
            os.mkdir(package_dirname)

            # create/write a package index file: (e.g. "srcdocs/packages/openmdao.core.rst")
            package_file = open(package_filename, "w")
            package_file.write(package_name + "\n")
            package_file.write("-" * len(package_name) + "\n")
            package_file.write(package_top)

            for sub_package in sub_packages:
                # this line writes subpackage name e.g. "core/component.py"
                # into the corresponding package index file (e.g. "openmdao.core.rst")
                package_file.write("    " + os.path.join(package, sub_package) + "\n")

                # creates and writes out one reference sheet (e.g. core/component.rst)
                ref_sheet_filename = package_dirname + os.path.sep + sub_package + ".rst"
                ref_sheet = open(ref_sheet_filename, "w")
                # get the meat of the ref sheet code done
                filename = sub_package + ".py"
                ref_sheet.write(".. index:: " + filename + "\n\n")
                ref_sheet.write(".. _" + package_name + "." + filename + ":\n\n")
                ref_sheet.write(filename + "\n")
                ref_sheet.write("+" * len(filename) + "\n\n")
                ref_sheet.write(".. automodule:: " + package_name + "." + sub_package)
                # finish and close each reference sheet.
                ref_sheet.write(ref_sheet_bottom)
                ref_sheet.close()

            # finish and close each package file
            package_file.write(package_bottom)
            package_file.close()

    # finish and close top-level index file
    index.close()


generate_docs()


def _parse(self):
        self._doc.reset()
        self._parse_summary()

        for (section,content) in self._read_sections():
            if not section.startswith('..'):
                section = ' '.join([s.capitalize() for s in section.split(' ')])
            if section in ('Args', 'Returns', 'Raises', 'Warns',
                           'Other Args', 'Attributes', 'Methods'):
                self[section] = self._parse_param_list(content)
            elif section.startswith('.. index::'):
                self['index'] = self._parse_index(section, content)
            elif section == 'See Also':
                self['See Also'] = self._parse_see_also(content)
            else:
                self[section] = content


def __str__(self, indent=0, func_role="obj"):
        out = []
        out += self._str_signature()
        out += self._str_index() + ['']
        out += self._str_summary()
        out += self._str_extended_summary()
        out += self._str_param_list('Args')
        out += self._str_returns()
        for param_list in ('Other Args', 'Raises', 'Warns'):
            out += self._str_param_list(param_list)
        out += self._str_warnings()
        out += self._str_see_also(func_role)
        out += self._str_section('Notes')
        out += self._str_references()
        out += self._str_examples()
        for param_list in ('Attributes', 'Methods'):
            out += self._str_member_list(param_list)
        out = self._str_indent(out,indent)
        return '\n'.join(out)

def __init__(self, docstring, config={}):

        docstring = textwrap.dedent(docstring).split('\n')

        self._doc = Reader(docstring)
        self._parsed_data = {
            'Signature': '',
            'Summary': [''],
            'Extended Summary': [],
            'Args': [],
            'Returns': [],
            'Raises': [],
            'Warns': [],
            'Other Args': [],
            'Attributes': [],
            'Methods': [],
            'See Also': [],
            'Notes': [],
            'Warnings': [],
            'References': '',
            'Examples': '',
            'index': {}
            }

        self._parse()

#Do the actual patch switchover to these local versions
NumpyDocString.__init__ = __init__
SphinxDocString._parse = _parse
SphinxDocString.__str__ = __str__
#--------------end monkeypatch---------------------



# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../srcdocs'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'numpydoc'
]

numpydoc_show_class_members = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'OpenMDAO'
copyright = u'2015, openmdao.org'
author = u'openmdao.org'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = openmdao.__version__
# The full version, including alpha/beta/rc tags.
release = openmdao.__version__ + ' Alpha'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'theme'
#html_theme = 'sphinxdoc'

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ['.']

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/OpenMDAO_Logo.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/OpenMDAO_Favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr'
#html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
#html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
#html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'OpenMDAOdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',

# Latex figure (float) alignment
#'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  (master_doc, 'OpenMDAO.tex', u'OpenMDAO Documentation',
   u'openmdao.org', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'openmdao', u'OpenMDAO Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  (master_doc, 'OpenMDAO', u'OpenMDAO Documentation',
   author, 'OpenMDAO', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False
