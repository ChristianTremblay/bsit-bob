# -- Sphinx configuration for si-builder docs ---------------------------------

import os
from datetime import datetime
from pathlib import Path


# Optionally sync ASHRAE 223 publication figures into doc/figures at build time
def _sync_s223_figures():
    try:
        from dotenv import load_dotenv  # optional

        load_dotenv()
    except Exception:
        pass
    try:
        repo_root = Path(__file__).resolve().parents[1]
        figures_dst = Path(__file__).parent / "figures"
        figures_dst.mkdir(parents=True, exist_ok=True)

        s223_folder = os.getenv("S223_FOLDER") or os.getenv("S223_DIRECTORY")
        roots = [Path(s223_folder)] if s223_folder else []
        guess = repo_root.parent / "223standard"
        roots += [guess, guess / "Standard_223"]

        patterns = ("Figure_*.svg", "Figure_*.png")
        copied = 0
        for root in roots:
            if not root or not root.exists():
                continue
            for sub in (
                "publication/figures",
                "Publication/figures",
                "figures",
                "Figures",
                ".",
            ):
                base = root / sub
                if not base.exists():
                    continue
                for pat in patterns:
                    for src in base.rglob(pat):
                        dst = figures_dst / src.name
                        try:
                            if not dst.exists():
                                import shutil

                                shutil.copy2(src, dst)
                                copied += 1
                        except Exception:
                            pass
        if copied:
            print(f"[s223] Copied {copied} figure(s) into {figures_dst}")
    except Exception:
        # Never fail the build because of figures
        pass


def setup(app):
    # Run before reading sources
    app.connect("builder-inited", lambda *_: _sync_s223_figures())


# -- Project information
project = "si-builder"
author = "ASHRAE 223P contributors"
copyright = f"{datetime.now():%Y}, {author}"
release = ""  # set to package version if desired

# -- General configuration
extensions = [
    "myst_parser",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
]

# Recognize Markdown (MyST) and reStructuredText
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# Root document (MyST toctree is in index.md)
root_doc = "index"

# Exclude build and archives from the tree
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "archive/**"]

# Templates/static directories (fallback to [] if missing)
_here = Path(__file__).parent
_templates = _here / "_templates"
_static = _here / "_static"
templates_path = ["_templates"] if _templates.is_dir() else []
html_static_path = ["_static"] if _static.is_dir() else []

# -- MyST configuration
myst_enable_extensions = [
    "deflist",
    "substitution",
    "attrs",
    "tasklist",
]
myst_heading_anchors = 3  # create anchors for H1–H3

# -- External links (Open223)
extlinks = {
    # Usage: :open223:`Equipment` -> https://explore.open223.info/s223/Equipment
    "open223": ("https://explore.open223.info/s223/%s", "s223:%s"),
}

# -- Intersphinx (standard lib cross-links)
# Second tuple element must be None or path to objects.inv (not an empty dict)
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- HTML output
html_theme = "furo"
html_title = "si-builder Documentation"
