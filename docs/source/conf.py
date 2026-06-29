"""Sphinx configuration for the pysampling documentation.

Notebooks are executed out-of-band by the docs runner (jupyter-cache); Sphinx
itself never executes them (``nbsphinx_execute = 'never'``) — it only renders the
already-hydrated ``.ipynb`` files.
"""

import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

import pysampling  # noqa: E402

project = "pysampling"
copyright = "2026, Julian Blank"
author = "Julian Blank"
release = pysampling.__version__

extensions = ["nbsphinx"]

exclude_patterns = ["build", "**.ipynb_checkpoints"]

html_theme = "sphinx_book_theme"
html_logo = "_static/pysampling.png"
html_title = "pysampling"
html_baseurl = "https://anyoptimization.com/projects/pysampling/"
# Mirrors pymoo's book-theme setup (minimal, stock knobs — no bespoke CSS/JS):
# light mode, GitHub repo/issue/source buttons in the navbar, and no left
# sidebar (single-page doc — avoids an empty bar; logo + content reflow).
html_theme_options = {
    "default_mode": "light",
    "repository_url": "https://github.com/anyoptimization/pysampling",
    "repository_branch": "master",
    "path_to_docs": "docs/source",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_source_button": True,
    "use_download_button": False,
    # Single-page doc: no right sidebar — the in-page TOC is moved to the left.
    "secondary_sidebar_items": [],
}
# Put the in-page "Contents" (page-toc) into the LEFT sidebar instead of the
# right, alongside the logo and search. One page, no splitting into many .md.
html_sidebars = {
    "**": [
        "navbar-logo.html",
        "icon-links.html",
        "search-button-field.html",
        "page-toc.html",
    ]
}
html_static_path = ["_static"]
html_css_files = ["custom.css"]
templates_path = ["_templates"]
# Shipped to the site root: /llms.txt (LLM-readable project summary).
html_extra_path = ["llms.txt"]
html_copy_source = False
html_sourcelink_suffix = ""

# Notebooks are pre-executed by the docs runner; Sphinx must never re-execute them.
nbsphinx_execute = "never"
