# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -c docs
SPHINXBUILD   = sphinx-build
PAPER         =

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d docs/_build/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

.PHONY: help clean html web pickle htmlhelp latex changes linkcheck

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  pickle    to make pickle files (usable by e.g. sphinx-web)"
	@echo "  htmlhelp  to make HTML files and a HTML help project"
	@echo "  latex     to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  changes   to make an overview over all changed/added/deprecated items"
	@echo "  linkcheck to check all external links for integrity"

clean:
	-rm -rf docs/_build/*

html:
	mkdir -p docs/_build/html docs/_build/doctrees
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) docs/_build/html
	@echo
	@echo "Build finished. The HTML pages are in docs/_build/html."

pickle:
	mkdir -p docs/_build/pickle docs/_build/doctrees
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) docs/_build/pickle
	@echo
	@echo "Build finished; now you can process the pickle files or run"
	@echo "  sphinx-web docs/_build/pickle"
	@echo "to start the sphinx-web server."

web: pickle

htmlhelp:
	mkdir -p docs/_build/htmlhelp docs/_build/doctrees
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) docs/_build/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in docs/_build/htmlhelp."

latex:
	mkdir -p docs/_build/latex docs/_build/doctrees
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) docs/_build/latex
	@echo
	@echo "Build finished; the LaTeX files are in docs/_build/latex."
	@echo "Run \`make all-pdf' or \`make all-ps' in that directory to" \
	      "run these through (pdf)latex."

changes:
	mkdir -p docs/_build/changes docs/_build/doctrees
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) docs/_build/changes
	@echo
	@echo "The overview file is in docs/_build/changes."

linkcheck:
	mkdir -p docs/_build/linkcheck docs/_build/doctrees
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) docs/_build/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in docs/_build/linkcheck/output.txt."
