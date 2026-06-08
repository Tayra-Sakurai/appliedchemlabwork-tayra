# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'AppliedChemLabWork-tayra'
copyright = '2026, Tayra Sakurai'
author = 'Tayra Sakurai'
release = '0.0.34'

import sys
from pathlib import Path
sys.path.insert(0, str(Path('..', '..', 'src').resolve()))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "numpydoc",
    "sphinx.ext.githubpages",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.apidoc",
    "sphinx.ext.viewcode",
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
