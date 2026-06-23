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
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_copy_source = False
html_sourcelink_suffix = ""

# Notebooks are pre-executed by the docs runner; Sphinx must never re-execute them.
nbsphinx_execute = "never"
