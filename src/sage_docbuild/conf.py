r"""
Sphinx build configuration

This file contains configuration needed to customize Sphinx input and output
behavior.
"""

# ****************************************************************************
#       Copyright (C) 2022 Kwankyu Lee <ekwankyu@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

# Load configuration shared with sage.misc.sphinxify
from sage.misc.sagedoc_conf import *

import importlib
import sys
import os
import sphinx
import sphinx.ext.intersphinx as intersphinx
import dateutil.parser
import sage.version

from sphinx import highlighting
from IPython.lib.lexers import IPythonConsoleLexer, IPyLexer

from sage.misc.sagedoc import extlinks
from sage.env import SAGE_DOC_SRC, SAGE_DOC, THEBE_DIR, PPLPY_DOCS, MATHJAX_DIR
from sage.misc.latex_macros import sage_mathjax_macros
from sage.features import PythonModule

# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sage_docbuild.ext.inventory_builder',
    'sage_docbuild.ext.multidocs',
    'sage_docbuild.ext.sage_autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.extlinks',
    'sphinx.ext.mathjax',
    'sphinx_copybutton',
    'IPython.sphinxext.ipython_directive',
    'matplotlib.sphinxext.plot_directive',
    'jupyter_sphinx',
]

jupyter_execute_default_kernel = 'sagemath'

jupyter_sphinx_thebelab_config = {
    'requestKernel': True,
    'binderOptions': {
        'repo': "sagemath/sage-binder-env",
    },
    'kernelOptions': {
        'name': "sagemath",
        'kernelName': "sagemath",
        'path': ".",
    },
}

# This code is executed before each ".. PLOT::" directive in the Sphinx
# documentation. It defines a 'sphinx_plot' function that displays a Sage object
# through matplotlib, so that it will be displayed in the HTML doc
plot_html_show_source_link = False
plot_pre_code = r"""
# Set locale to prevent having commas in decimal numbers
# in tachyon input (see https://github.com/sagemath/sage/issues/28971)
import locale
locale.setlocale(locale.LC_NUMERIC, 'C')
def sphinx_plot(graphics, **kwds):
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt
    from sage.misc.temporary_file import tmp_filename
    from sage.plot.graphics import _parse_figsize
    if os.environ.get('SAGE_SKIP_PLOT_DIRECTIVE', 'no') != 'yes':
        ## Option handling is taken from Graphics.save
        options = dict()
        if isinstance(graphics, sage.plot.graphics.Graphics):
            options.update(sage.plot.graphics.Graphics.SHOW_OPTIONS)
            options.update(graphics._extra_kwds)
            options.update(kwds)
        elif isinstance(graphics, sage.plot.multigraphics.MultiGraphics):
            options.update(kwds)
        else:
            graphics = graphics.plot(**kwds)
        dpi = options.pop('dpi', None)
        transparent = options.pop('transparent', None)
        fig_tight = options.pop('fig_tight', None)
        figsize = options.pop('figsize', None)
        if figsize is not None:
            figsize = _parse_figsize(figsize)
        plt.figure(figsize=figsize)
        figure = plt.gcf()
        if isinstance(graphics, (sage.plot.graphics.Graphics,
                                 sage.plot.multigraphics.MultiGraphics)):
            graphics.matplotlib(figure=figure, figsize=figsize, **options)
            if isinstance(graphics, (sage.plot.graphics.Graphics,
                                     sage.plot.multigraphics.GraphicsArray)):
                # for Graphics and GraphicsArray, tight_layout adjusts the
                # *subplot* parameters so ticks aren't cut off, etc.
                figure.tight_layout()
        else:
            # 3d graphics via png
            import matplotlib as mpl
            mpl.rcParams['image.interpolation'] = 'bilinear'
            mpl.rcParams['image.resample'] = False
            mpl.rcParams['figure.figsize'] = [8.0, 6.0]
            mpl.rcParams['figure.dpi'] = 80
            mpl.rcParams['savefig.dpi'] = 100
            fn = tmp_filename(ext=".png")
            graphics.save(fn)
            img = mpimg.imread(fn)
            plt.imshow(img)
            plt.axis("off")
        plt.margins(0)
        if not isinstance(graphics, sage.plot.multigraphics.MultiGraphics):
            plt.tight_layout(pad=0)

from sage.all_cmdline import *
"""

plot_html_show_formats = False
plot_formats = ['svg', 'pdf', 'png']

# We do *not* fully initialize intersphinx since we call it by hand
# in find_sage_dangling_links.
#, 'sphinx.ext.intersphinx']

# Add any paths that contain templates here, relative to this directory.
templates_path = [os.path.join(SAGE_DOC_SRC, 'common', 'templates'), 'templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = ""
copyright = "2005--{}, The Sage Development Team".format(dateutil.parser.parse(sage.version.date).year)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
version = sage.version.version
release = sage.version.version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of glob-style patterns that should be excluded when looking for
# source files. [1] They are matched against the source file names
# relative to the source directory, using slashes as directory
# separators on all platforms.
exclude_patterns = ['.build']

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = True

# Default lexer to use when highlighting code blocks, using the IPython
# console lexers. 'ipycon' is the IPython console, which is what we want
# for most code blocks: anything with "sage:" prompts. For other IPython,
# like blocks which might appear in a notebook cell, use 'ipython'.
highlighting.lexers['ipycon'] = IPythonConsoleLexer(in1_regex=r'sage: ', in2_regex=r'[.][.][.][.]: ')
highlighting.lexers['ipython'] = IPyLexer()
highlight_language = 'ipycon'

# Create table of contents entries for domain objects (e.g. functions, classes,
# attributes, etc.). Default is True.
toc_object_entries = True

# A string that determines how domain objects (e.g. functions, classes,
# attributes, etc.) are displayed in their table of contents entry.
#
# Use "domain" to allow the domain to determine the appropriate number of parents
# to show. For example, the Python domain would show Class.method() and
# function(), leaving out the module. level of parents. This is the default
# setting.
#
# Use "hide" to only show the name of the element without any parents (i.e. method()).
#
# Use "all" to show the fully-qualified name for the object (i.e. module.Class.method()),
# displaying all parents.
toc_object_entries_show_parents = 'hide'

# Extension configuration
# -----------------------

# include the todos
todo_include_todos = True

# Cross-links to other project's online documentation.
python_version = sys.version_info.major


def set_intersphinx_mappings(app, config):
    """
    Add precompiled inventory (the objects.inv)
    """
    refpath = os.path.join(SAGE_DOC, "html", "en", "reference")
    invpath = os.path.join(SAGE_DOC, "inventory", "en", "reference")
    if app.config.multidoc_first_pass == 1 or \
            not (os.path.exists(refpath) and os.path.exists(invpath)):
        app.config.intersphinx_mapping = {}
        return

    app.config.intersphinx_mapping = {
    'python': ('https://docs.python.org/',
                os.path.join(SAGE_DOC_SRC, "common",
                             "python{}.inv".format(python_version))),
    }
    if PPLPY_DOCS and os.path.exists(os.path.join(PPLPY_DOCS, 'objects.inv')):
        app.config.intersphinx_mapping['pplpy'] = (PPLPY_DOCS, None)
    else:
        app.config.intersphinx_mapping['pplpy'] = ('https://www.labri.fr/perso/vdelecro/pplpy/latest/', None)

    # Add master intersphinx mapping
    dst = os.path.join(invpath, 'objects.inv')
    app.config.intersphinx_mapping['sagemath'] = (refpath, dst)

    # Add intersphinx mapping for subdirectories
    # We intentionally do not name these such that these get higher
    # priority in case of conflicts
    for directory in os.listdir(os.path.join(invpath)):
        if directory == 'jupyter_execute':
            # This directory is created by jupyter-sphinx extension for
            # internal use and should be ignored here. See trac #33507.
            continue
        if os.path.isdir(os.path.join(invpath, directory)):
            src = os.path.join(refpath, directory)
            dst = os.path.join(invpath, directory, 'objects.inv')
            app.config.intersphinx_mapping[src] = dst

    intersphinx.normalize_intersphinx_mapping(app, config)


# By default document are not master.
multidocs_is_master = True

# https://sphinx-copybutton.readthedocs.io/en/latest/use.html
copybutton_prompt_text = r"sage: |[.][.][.][.]: |\$ "
copybutton_prompt_is_regexp = True
copybutton_exclude = '.linenos, .c1'  # exclude single comments (in particular, # optional!)
copybutton_only_copy_prompt_lines = True

# Options for HTML output
# -----------------------

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [os.path.join(SAGE_DOC_SRC, "common", "themes")]

if PythonModule("furo").is_present():
    # Sphinx theme "furo" does not permit an extension. Do not attempt to make
    # a "sage-furo" theme.
    html_theme = "furo"

    # Theme options are theme-specific and customize the look and feel of
    # a theme further.  For a list of options available for each theme,
    # see the documentation.
    html_theme_options = {
        "light_css_variables": {
            "color-brand-primary": "#0f0fff",
            "color-brand-content": "#0f0fff",
        },
        "light_logo": "logo_sagemath_black.svg",
        "dark_logo": "logo_sagemath_white.svg",
    }

    # The name of the Pygments (syntax highlighting) style to use. This
    # overrides a HTML theme's corresponding setting.
    pygments_style = "sphinx"
    pygments_dark_style = "monokai"

    # Add siderbar/home.html to the default sidebar.
    html_sidebars = {
        "**": [
            "sidebar/scroll-start.html",
            "sidebar/brand.html",
            "sidebar/search.html",
            "sidebar/home.html",
            "sidebar/navigation.html",
            "sidebar/ethical-ads.html",
            "sidebar/scroll-end.html",
            "sidebar/variant-selector.html",
        ]
    }

    # These paths are either relative to html_static_path
    # or fully qualified paths (eg. https://...)
    html_css_files = [
        'custom-furo.css',
    ]
    # A list of paths that contain extra templates (or templates that overwrite
    # builtin/theme-specific templates). Relative paths are taken as relative
    # to the configuration directory.
    templates_path = [os.path.join(SAGE_DOC_SRC, 'common', 'templates-furo')] + templates_path

else:
    # Sage default Sphinx theme.
    #
    # See the directory doc/common/themes/sage-classic/ for files comprising
    # the custom theme.
    html_theme = "sage-classic"

    html_theme_options = {}

# HTML style sheet. This overrides a HTML theme's corresponding setting.
#html_style = 'default.css'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (within the static path) to place at the top of
# the sidebar.
#html_logo = 'sagelogo-word.ico'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = 'favicon.ico'

# html_static_path defined here and imported in the actual configuration file
# conf.py read by Sphinx was the cause of subtle bugs in builders (see #30418 for
# instance). Hence now html_common_static_path contains the common paths to static
# files, and is combined to html_static_path in each conf.py file read by Sphinx.
html_common_static_path = [os.path.join(SAGE_DOC_SRC, 'common', 'static'),
                           THEBE_DIR, 'static']

# Configure MathJax
# https://docs.mathjax.org/en/latest/options/input/tex.html
mathjax3_config = {
    "tex": {
        # Add custom sage macros
        # http://docs.mathjax.org/en/latest/input/tex/macros.html
        "macros": sage_mathjax_macros(),
        # Add $...$ as possible inline math
        # https://docs.mathjax.org/en/latest/input/tex/delimiters.html#tex-and-latex-math-delimiters
        "inlineMath": [["$", "$"], ["\\(", "\\)"]],
        # Increase the limit the size of the string to be processed
        # https://docs.mathjax.org/en/latest/options/input/tex.html#option-descriptions
        "maxBuffer": 50 * 1024,
        # Use colorv2 extension instead of built-in color extension
        # https://docs.mathjax.org/en/latest/input/tex/extensions/autoload.html#tex-autoload-options
        # https://docs.mathjax.org/en/latest/input/tex/extensions/colorv2.html#tex-colorv2
        "autoload": {"color": [], "colorv2": ["color"]},
    },
}

if os.environ.get('SAGE_USE_CDNS', 'no') == 'yes':
    mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"
else:
    mathjax_path = 'mathjax/tex-chtml.js'
    html_common_static_path += [MATHJAX_DIR]

# A list of glob-style patterns that should be excluded when looking for source
# files. They are matched against the source file names relative to the
# source directory, using slashes as directory separators on all platforms.
exclude_patterns = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_use_modindex = True

# A list of prefixes that are ignored for sorting the Python module index ( if
# this is set to ['foo.'], then foo.bar is shown under B, not F). Works only
# for the HTML builder currently.
modindex_common_prefix = ['sage.']

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = True

# If true, the reST sources are included in the HTML build as _sources/<name>.
#html_copy_source = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
#htmlhelp_basename = ''

# Options for LaTeX output
# ------------------------
# See http://sphinx-doc.org/config.html#confval-latex_elements
latex_elements = {}

# The paper size ('letterpaper' or 'a4paper').
#latex_elements['papersize'] = 'letterpaper'

# The font size ('10pt', '11pt' or '12pt').
#latex_elements['pointsize'] = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
latex_documents = []

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = 'sagelogo-word.png'

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
latex_elements['preamble'] = r"""
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{textcomp}
\usepackage{mathrsfs}
\usepackage{iftex}

% Only declare unicode characters when compiling with pdftex; E.g. japanese
% tutorial does not use pdftex
\ifPDFTeX
    \DeclareUnicodeCharacter{01CE}{\capitalcaron a}
    \DeclareUnicodeCharacter{0428}{cyrillic Sha}
    \DeclareUnicodeCharacter{250C}{+}
    \DeclareUnicodeCharacter{2510}{+}
    \DeclareUnicodeCharacter{2514}{+}
    \DeclareUnicodeCharacter{2518}{+}
    \DeclareUnicodeCharacter{253C}{+}

    \DeclareUnicodeCharacter{03B1}{\ensuremath{\alpha}}
    \DeclareUnicodeCharacter{03B2}{\ensuremath{\beta}}
    \DeclareUnicodeCharacter{03B3}{\ensuremath{\gamma}}
    \DeclareUnicodeCharacter{0393}{\ensuremath{\Gamma}}
    \DeclareUnicodeCharacter{03B4}{\ensuremath{\delta}}
    \DeclareUnicodeCharacter{0394}{\ensuremath{\Delta}}
    \DeclareUnicodeCharacter{03B5}{\ensuremath{\varepsilon}}
    \DeclareUnicodeCharacter{03B6}{\ensuremath{\zeta}}
    \DeclareUnicodeCharacter{03B7}{\ensuremath{\eta}}
    \DeclareUnicodeCharacter{03B8}{\ensuremath{\vartheta}}
    \DeclareUnicodeCharacter{0398}{\ensuremath{\Theta}}
    \DeclareUnicodeCharacter{03BA}{\ensuremath{\kappa}}
    \DeclareUnicodeCharacter{03BB}{\ensuremath{\lambda}}
    \DeclareUnicodeCharacter{039B}{\ensuremath{\Lambda}}
    \DeclareUnicodeCharacter{00B5}{\ensuremath{\mu}}      % micron sign
    \DeclareUnicodeCharacter{03BC}{\ensuremath{\mu}}
    \DeclareUnicodeCharacter{03BD}{\ensuremath{\nu}}
    \DeclareUnicodeCharacter{03BE}{\ensuremath{\xi}}
    \DeclareUnicodeCharacter{039E}{\ensuremath{\Xi}}
    \DeclareUnicodeCharacter{03B9}{\ensuremath{\iota}}
    \DeclareUnicodeCharacter{03C0}{\ensuremath{\pi}}
    \DeclareUnicodeCharacter{03A0}{\ensuremath{\Pi}}
    \DeclareUnicodeCharacter{03C1}{\ensuremath{\rho}}
    \DeclareUnicodeCharacter{03C3}{\ensuremath{\sigma}}
    \DeclareUnicodeCharacter{03A3}{\ensuremath{\Sigma}}
    \DeclareUnicodeCharacter{03C4}{\ensuremath{\tau}}
    \DeclareUnicodeCharacter{03C6}{\ensuremath{\varphi}}
    \DeclareUnicodeCharacter{03A6}{\ensuremath{\Phi}}
    \DeclareUnicodeCharacter{03C7}{\ensuremath{\chi}}
    \DeclareUnicodeCharacter{03C8}{\ensuremath{\psi}}
    \DeclareUnicodeCharacter{03A8}{\ensuremath{\Psi}}
    \DeclareUnicodeCharacter{03C9}{\ensuremath{\omega}}
    \DeclareUnicodeCharacter{03A9}{\ensuremath{\Omega}}
    \DeclareUnicodeCharacter{03C5}{\ensuremath{\upsilon}}
    \DeclareUnicodeCharacter{03A5}{\ensuremath{\Upsilon}}
    \DeclareUnicodeCharacter{2113}{\ell}

    \DeclareUnicodeCharacter{2148}{\ensuremath{\id}}
    \DeclareUnicodeCharacter{2202}{\ensuremath{\partial}}
    \DeclareUnicodeCharacter{2205}{\ensuremath{\emptyset}}
    \DeclareUnicodeCharacter{2208}{\ensuremath{\in}}
    \DeclareUnicodeCharacter{2209}{\ensuremath{\notin}}
    \DeclareUnicodeCharacter{2211}{\ensuremath{\sum}}
    \DeclareUnicodeCharacter{221A}{\ensuremath{\sqrt{}}}
    \DeclareUnicodeCharacter{221E}{\ensuremath{\infty}}
    \DeclareUnicodeCharacter{2227}{\ensuremath{\wedge}}
    \DeclareUnicodeCharacter{2228}{\ensuremath{\vee}}
    \DeclareUnicodeCharacter{2229}{\ensuremath{\cap}}
    \DeclareUnicodeCharacter{222A}{\ensuremath{\cup}}
    \DeclareUnicodeCharacter{222B}{\ensuremath{\int}}
    \DeclareUnicodeCharacter{2248}{\ensuremath{\approx}}
    \DeclareUnicodeCharacter{2260}{\ensuremath{\neq}}
    \DeclareUnicodeCharacter{2264}{\ensuremath{\leq}}
    \DeclareUnicodeCharacter{2265}{\ensuremath{\geq}}
    \DeclareUnicodeCharacter{2293}{\ensuremath{\sqcap}}
    \DeclareUnicodeCharacter{2294}{\ensuremath{\sqcup}}
    \DeclareUnicodeCharacter{22C0}{\ensuremath{\bigwedge}}
    \DeclareUnicodeCharacter{22C1}{\ensuremath{\bigvee}}
    \DeclareUnicodeCharacter{22C2}{\ensuremath{\bigcap}}
    \DeclareUnicodeCharacter{22C3}{\ensuremath{\bigcup}}
    \DeclareUnicodeCharacter{2323}{\ensuremath{\smile}}  % cup product
    \DeclareUnicodeCharacter{00B1}{\ensuremath{\pm}}
    \DeclareUnicodeCharacter{2A02}{\ensuremath{\bigotimes}}
    \DeclareUnicodeCharacter{2295}{\ensuremath{\oplus}}
    \DeclareUnicodeCharacter{2297}{\ensuremath{\otimes}}
    \DeclareUnicodeCharacter{2A01}{\ensuremath{\oplus}}
    \DeclareUnicodeCharacter{00BD}{\ensuremath{\nicefrac{1}{2}}}
    \DeclareUnicodeCharacter{00D7}{\ensuremath{\times}}
    \DeclareUnicodeCharacter{00B7}{\ensuremath{\cdot}}
    \DeclareUnicodeCharacter{230A}{\ensuremath{\lfloor}}
    \DeclareUnicodeCharacter{230B}{\ensuremath{\rfloor}}
    \DeclareUnicodeCharacter{2308}{\ensuremath{\lceil}}
    \DeclareUnicodeCharacter{2309}{\ensuremath{\rceil}}
    \DeclareUnicodeCharacter{22C5}{\ensuremath{\cdot}}
    \DeclareUnicodeCharacter{2227}{\ensuremath{\wedge}}
    \DeclareUnicodeCharacter{22C0}{\ensuremath{\bigwedge}}
    \DeclareUnicodeCharacter{2192}{\ensuremath{\to}}
    \DeclareUnicodeCharacter{21A6}{\ensuremath{\mapsto}}
    \DeclareUnicodeCharacter{2102}{\ensuremath{\mathbb{C}}}
    \DeclareUnicodeCharacter{211A}{\ensuremath{\mathbb{Q}}}
    \DeclareUnicodeCharacter{211D}{\ensuremath{\mathbb{R}}}
    \DeclareUnicodeCharacter{2124}{\ensuremath{\mathbb{Z}}}
    \DeclareUnicodeCharacter{2202}{\ensuremath{\partial}}

    \DeclareUnicodeCharacter{2070}{\ensuremath{{}^0}}
    \DeclareUnicodeCharacter{00B9}{\ensuremath{{}^1}}
    \DeclareUnicodeCharacter{00B2}{\ensuremath{{}^2}}
    \DeclareUnicodeCharacter{00B3}{\ensuremath{{}^3}}
    \DeclareUnicodeCharacter{2074}{\ensuremath{{}^4}}
    \DeclareUnicodeCharacter{2075}{\ensuremath{{}^5}}
    \DeclareUnicodeCharacter{2076}{\ensuremath{{}^6}}
    \DeclareUnicodeCharacter{2077}{\ensuremath{{}^7}}
    \DeclareUnicodeCharacter{2078}{\ensuremath{{}^8}}
    \DeclareUnicodeCharacter{2079}{\ensuremath{{}^9}}
    \DeclareUnicodeCharacter{207A}{\ensuremath{{}^+}}
    \DeclareUnicodeCharacter{207B}{\ensuremath{{}^-}}
    \DeclareUnicodeCharacter{141F}{\ensuremath{{}^/}}
    \DeclareUnicodeCharacter{2080}{\ensuremath{{}_0}}
    \DeclareUnicodeCharacter{2081}{\ensuremath{{}_1}}
    \DeclareUnicodeCharacter{2082}{\ensuremath{{}_2}}
    \DeclareUnicodeCharacter{2083}{\ensuremath{{}_3}}
    \DeclareUnicodeCharacter{2084}{\ensuremath{{}_4}}
    \DeclareUnicodeCharacter{2085}{\ensuremath{{}_5}}
    \DeclareUnicodeCharacter{2086}{\ensuremath{{}_6}}
    \DeclareUnicodeCharacter{2087}{\ensuremath{{}_7}}
    \DeclareUnicodeCharacter{2088}{\ensuremath{{}_8}}
    \DeclareUnicodeCharacter{2089}{\ensuremath{{}_9}}
    \DeclareUnicodeCharacter{208A}{\ensuremath{{}_+}}
    \DeclareUnicodeCharacter{208B}{\ensuremath{{}_-}}
    \DeclareUnicodeCharacter{1D62}{\ensuremath{{}_i}}
    \DeclareUnicodeCharacter{2C7C}{\ensuremath{{}_j}}

    \newcommand{\sageMexSymbol}[1]
    {{\fontencoding{OMX}\fontfamily{cmex}\selectfont\raisebox{0.75em}{\symbol{#1}}}}
    \DeclareUnicodeCharacter{239B}{\sageMexSymbol{"30}} % parenlefttp
    \DeclareUnicodeCharacter{239C}{\sageMexSymbol{"42}} % parenleftex
    \DeclareUnicodeCharacter{239D}{\sageMexSymbol{"40}} % parenleftbt
    \DeclareUnicodeCharacter{239E}{\sageMexSymbol{"31}} % parenrighttp
    \DeclareUnicodeCharacter{239F}{\sageMexSymbol{"43}} % parenrightex
    \DeclareUnicodeCharacter{23A0}{\sageMexSymbol{"41}} % parenrightbt
    \DeclareUnicodeCharacter{23A1}{\sageMexSymbol{"32}} % bracketlefttp
    \DeclareUnicodeCharacter{23A2}{\sageMexSymbol{"36}} % bracketleftex
    \DeclareUnicodeCharacter{23A3}{\sageMexSymbol{"34}} % bracketleftbt
    \DeclareUnicodeCharacter{23A4}{\sageMexSymbol{"33}} % bracketrighttp
    \DeclareUnicodeCharacter{23A5}{\sageMexSymbol{"37}} % bracketrightex
    \DeclareUnicodeCharacter{23A6}{\sageMexSymbol{"35}} % bracketrightbt

    \DeclareUnicodeCharacter{23A7}{\sageMexSymbol{"38}} % curly brace left top
    \DeclareUnicodeCharacter{23A8}{\sageMexSymbol{"3C}} % curly brace left middle
    \DeclareUnicodeCharacter{23A9}{\sageMexSymbol{"3A}} % curly brace left bottom
    \DeclareUnicodeCharacter{23AA}{\sageMexSymbol{"3E}} % curly brace extension
    \DeclareUnicodeCharacter{23AB}{\sageMexSymbol{"39}} % curly brace right top
    \DeclareUnicodeCharacter{23AC}{\sageMexSymbol{"3D}} % curly brace right middle
    \DeclareUnicodeCharacter{23AD}{\sageMexSymbol{"3B}} % curly brace right bottom
    \DeclareUnicodeCharacter{23B0}{\{} % 2-line curly brace left top half  (not in cmex)
    \DeclareUnicodeCharacter{23B1}{\}} % 2-line curly brace right top half (not in cmex)

    \DeclareUnicodeCharacter{2320}{\ensuremath{\int}} % top half integral
    \DeclareUnicodeCharacter{2321}{\ensuremath{\int}} % bottom half integral
    \DeclareUnicodeCharacter{23AE}{\ensuremath{\|}} % integral extenison

    % Box drawings light
    \DeclareUnicodeCharacter{2500}{-}  % h
    \DeclareUnicodeCharacter{2502}{|}  % v
    \DeclareUnicodeCharacter{250C}{+}  % dr
    \DeclareUnicodeCharacter{2510}{+}  % dl
    \DeclareUnicodeCharacter{2514}{+}  % ur
    \DeclareUnicodeCharacter{2518}{+}  % ul
    \DeclareUnicodeCharacter{251C}{+}  % vr
    \DeclareUnicodeCharacter{2524}{+}  % vl
    \DeclareUnicodeCharacter{252C}{+}  % dh
    \DeclareUnicodeCharacter{2534}{+}  % uh
    \DeclareUnicodeCharacter{253C}{+}  % vh
    \DeclareUnicodeCharacter{2571}{/}  % upper right to lower left
    \DeclareUnicodeCharacter{2571}{\setminus} % upper left to lower right

    \DeclareUnicodeCharacter{25CF}{\ensuremath{\bullet}}  % medium black circle
    \DeclareUnicodeCharacter{26AC}{\ensuremath{\circ}}  % medium small white circle
    \DeclareUnicodeCharacter{256D}{+}
    \DeclareUnicodeCharacter{256E}{+}
    \DeclareUnicodeCharacter{256F}{+}
    \DeclareUnicodeCharacter{2570}{+}
\fi

\let\textLaTeX\LaTeX
\AtBeginDocument{\renewcommand*{\LaTeX}{\hbox{\textLaTeX}}}

% Workaround for a LaTeX bug -- see trac #31397 and
% https://tex.stackexchange.com/questions/583391/mactex-2020-error-with-report-hyperref-mathbf-in-chapter.
\makeatletter
\pdfstringdefDisableCommands{%
  \let\mathbf\@firstofone
}
\makeatother
"""

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True

#####################################################
# add LaTeX macros for Sage

from sage.misc.latex_macros import sage_latex_macros

try:
    pngmath_latex_preamble  # check whether this is already defined
except NameError:
    pngmath_latex_preamble = ""

for macro in sage_latex_macros():
    # used when building latex and pdf versions
    latex_elements['preamble'] += macro + '\n'
    # used when building html version
    pngmath_latex_preamble += macro + '\n'

#####################################################
# add custom context variables for templates

def add_page_context(app, pagename, templatename, context, doctree):
    # # The template function
    # def template_function(arg):
    #     return "Your string is " + arg
    # # Add it to the page's context
    # context['template_function'] = template_function
    path1 = os.path.dirname(app.builder.get_outfilename(pagename))
    path2 = os.path.join(SAGE_DOC, 'html', 'en')
    relpath = os.path.relpath(path2, path1)
    context['release'] = release
    context['documentation_title'] = 'Sage {}'.format(release) + ' Documentation'
    context['documentation_root'] = os.path.join(relpath, 'index.html')
    if 'website' in path1:
        context['title'] = 'Documentation'
        context['website'] = True
        context['documentation_root'] = 'index.html'
    if 'reference' in path1 and not path1.endswith('reference'):
        path2 = os.path.join(SAGE_DOC, 'html', 'en', 'reference')
        relpath = os.path.relpath(path2, path1)
        context['reference_title'] = 'Sage {}'.format(release) + ' Reference Manual'
        context['reference_root'] = os.path.join(relpath, 'index.html')
        context['refsub'] = True

dangling_debug = False

def debug_inf(app, message):
    if dangling_debug:
        app.info(message)

def call_intersphinx(app, env, node, contnode):
    r"""
    Call intersphinx and make links between Sage manuals relative.

    TESTS:

    Check that the link from the thematic tutorials to the reference
    manual is relative, see :trac:`20118`::

        sage: from sage.env import SAGE_DOC
        sage: thematic_index = os.path.join(SAGE_DOC, "html", "en", "thematic_tutorials", "index.html")
        sage: for line in open(thematic_index).readlines():  # optional - sagemath_doc_html
        ....:     if "padics" in line:
        ....:         _ = sys.stdout.write(line)
        <li><p><a class="reference external" href="../reference/padics/sage/rings/padics/tutorial.html#sage-rings-padics-tutorial" title="(in $p$-adics v...)"><span>Introduction to the p-adics</span></a></p></li>
    """
    debug_inf(app, "???? Trying intersphinx for %s" % node['reftarget'])
    builder = app.builder
    res =  intersphinx.missing_reference(
        app, env, node, contnode)
    if res:
        # Replace absolute links to $SAGE_DOC by relative links: this
        # allows to copy the whole documentation tree somewhere else
        # without breaking links, see Issue #20118.
        if res['refuri'].startswith(SAGE_DOC):
            here = os.path.dirname(os.path.join(builder.outdir,
                                                node['refdoc']))
            res['refuri'] = os.path.relpath(res['refuri'], here)
            debug_inf(app, "++++ Found at %s" % res['refuri'])
    else:
        debug_inf(app, "---- Intersphinx: %s not Found" % node['reftarget'])
    return res

def find_sage_dangling_links(app, env, node, contnode):
    r"""
    Try to find dangling link in local module imports or all.py.
    """
    debug_inf(app, "==================== find_sage_dangling_links ")

    reftype = node['reftype']
    reftarget  = node['reftarget']
    try:
        doc = node['refdoc']
    except KeyError:
        debug_inf(app, "-- no refdoc in node %s" % node)
        return None

    debug_inf(app, "Searching %s from %s"%(reftarget, doc))

    # Workaround: in Python's doc 'object', 'list', ... are documented as a
    # function rather than a class
    if reftarget in base_class_as_func and reftype == 'class':
        node['reftype'] = 'func'

    res = call_intersphinx(app, env, node, contnode)
    if res:
        debug_inf(app, "++ DONE %s"%(res['refuri']))
        return res

    if node.get('refdomain') != 'py': # not a python file
        return None

    try:
        module = node['py:module']
        cls    = node['py:class']
    except KeyError:
        debug_inf(app, "-- no module or class for :%s:%s"%(reftype, reftarget))
        return None

    basename = reftarget.split(".")[0]
    try:
        target_module = getattr(sys.modules['sage.all'], basename).__module__
        debug_inf(app, "++ found %s using sage.all in %s" % (basename, target_module))
    except AttributeError:
        try:
            target_module = getattr(sys.modules[node['py:module']], basename).__module__
            debug_inf(app, "++ found %s in this module" % (basename,))
        except AttributeError:
            debug_inf(app, "-- %s not found in sage.all or this module" % (basename))
            return None
        except KeyError:
            target_module = None
    if target_module is None:
        target_module = ""
        debug_inf(app, "?? found in None !!!")

    newtarget = target_module+'.'+reftarget
    node['reftarget'] = newtarget

    # adapted  from sphinx/domains/python.py
    builder = app.builder
    searchmode = node.hasattr('refspecific') and 1 or 0
    matches =  builder.env.domains['py'].find_obj(
        builder.env, module, cls, newtarget, reftype, searchmode)
    if not matches:
        debug_inf(app, "?? no matching doc for %s"%newtarget)
        return call_intersphinx(app, env, node, contnode)
    elif len(matches) > 1:
        env.warn(target_module,
                 'more than one target found for cross-reference '
                 '%r: %s' % (newtarget,
                             ', '.join(match[0] for match in matches)),
                 node.line)
    name, obj = matches[0]
    debug_inf(app, "++ match = %s %s"%(name, obj))

    from docutils import nodes
    newnode = nodes.reference('', '', internal=True)
    if name == target_module:
        newnode['refid'] = name
    else:
        newnode['refuri'] = builder.get_relative_uri(node['refdoc'], obj[0])
        newnode['refuri'] += '#' + name
        debug_inf(app, "++ DONE at URI %s"%(newnode['refuri']))
    newnode['reftitle'] = name
    newnode.append(contnode)
    return newnode

# lists of basic Python class which are documented as functions
base_class_as_func = [
    'bool', 'complex', 'dict', 'file', 'float',
    'frozenset', 'int', 'list', 'long', 'object',
    'set', 'slice', 'str', 'tuple', 'type', 'unicode', 'xrange']

# Nit picky option configuration: Put here broken links we want to ignore. For
# link to the Python documentation several links where broken because there
# where class listed as functions. Expand the list 'base_class_as_func' above
# instead of marking the link as broken.
nitpick_ignore = [
    ('py:class', 'twisted.web2.resource.Resource'),
    ('py:class', 'twisted.web2.resource.PostableResource')]

def nitpick_patch_config(app):
    """
    Patch the default config for nitpicky

    Calling path_config ensure that nitpicky is not considered as a Sphinx
    environment variable but rather as a Sage environment variable. As a
    consequence, changing it doesn't force the recompilation of the entire
    documentation.
    """
    app.config.values['nitpicky'] = (False, 'sage')
    app.config.values['nitpick_ignore'] = ([], 'sage')

skip_picklability_check_modules = [
    #'sage.misc.test_nested_class', # for test only
    'sage.misc.latex',
    'sage.misc.explain_pickle',
    '__builtin__',
]


def check_nested_class_picklability(app, what, name, obj, skip, options):
    """
    Print a warning if pickling is broken for nested classes.
    """
    if hasattr(obj, '__dict__') and hasattr(obj, '__module__'):
        # Check picklability of nested classes.  Adapted from
        # sage.misc.nested_class.modify_for_nested_pickle.
        module = sys.modules[obj.__module__]
        for (nm, v) in obj.__dict__.items():
            if (isinstance(v, type) and
                v.__name__ == nm and
                v.__module__ == module.__name__ and
                getattr(module, nm, None) is not v and
                v.__module__ not in skip_picklability_check_modules):
                # OK, probably this is an *unpicklable* nested class.
                app.warn('Pickling of nested class %r is probably broken. '
                         'Please set the metaclass of the parent class to '
                         'sage.misc.nested_class.NestedClassMetaclass.' % (
                        v.__module__ + '.' + name + '.' + nm))

def skip_member(app, what, name, obj, skip, options):
    """
    To suppress Sphinx warnings / errors, we

    - Don't include [aliases of] builtins.

    - Don't include the docstring for any nested class which has been
      inserted into its module by
      :class:`sage.misc.NestedClassMetaclass` only for pickling.  The
      class will be properly documented inside its surrounding class.

    - Optionally, check whether pickling is broken for nested classes.

    - Optionally, include objects whose name begins with an underscore
      ('_'), i.e., "private" or "hidden" attributes, methods, etc.

    Otherwise, we abide by Sphinx's decision.  Note: The object
    ``obj`` is excluded (included) if this handler returns True
    (False).
    """
    if 'SAGE_CHECK_NESTED' in os.environ:
        check_nested_class_picklability(app, what, name, obj, skip, options)

    if getattr(obj, '__module__', None) == '__builtin__':
        return True

    objname = getattr(obj, "__name__", None)
    if objname is not None:
        # check if name was inserted to the module by NestedClassMetaclass
        if name.find('.') != -1 and objname.find('.') != -1:
            if objname.split('.')[-1] == name.split('.')[-1]:
                return True

    if 'SAGE_DOC_UNDERSCORE' in os.environ:
        if name.split('.')[-1].startswith('_'):
            return False

    return skip


# This replaces the setup() in sage.misc.sagedoc_conf
def setup(app):
    app.connect('autodoc-process-docstring', process_docstring_cython)
    app.connect('autodoc-process-docstring', process_directives)
    app.connect('autodoc-process-docstring', process_docstring_module_title)
    app.connect('autodoc-process-docstring', process_dollars)
    app.connect('autodoc-process-docstring', process_inherited)
    if os.environ.get('SAGE_SKIP_TESTS_BLOCKS', False):
        app.connect('autodoc-process-docstring', skip_TESTS_block)
    app.connect('autodoc-skip-member', skip_member)
    app.add_transform(SagemathTransform)

    # When building the standard docs, app.srcdir is set to SAGE_DOC_SRC +
    # 'LANGUAGE/DOCNAME'.
    if app.srcdir.startswith(SAGE_DOC_SRC):
        app.add_config_value('intersphinx_mapping', {}, False)
        app.add_config_value('intersphinx_cache_limit', 5, False)
        app.add_config_value('intersphinx_disabled_reftypes', [], False)
        app.add_config_value('intersphinx_timeout', None, False)
        app.connect('config-inited', set_intersphinx_mappings)
        app.connect('builder-inited', intersphinx.load_mappings)
        # We do *not* fully initialize intersphinx since we call it by hand
        # in find_sage_dangling_links.
        #   app.connect('missing-reference', missing_reference)
        app.connect('missing-reference', find_sage_dangling_links)
        app.connect('builder-inited', nitpick_patch_config)
        app.connect('html-page-context', add_page_context)
