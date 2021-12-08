# This Makefile knows how to build a web site, mostly by converting Markdown
# files to HTML. It can also do some other helpful tasks, like create a site
# skeleton and serve the site locally for testing.

# -------------
# Configuration
# -------------

SITE_TITLE := webpage
FAVICON := media/favicon.png

INDEX := index.md
HEADER := includes/document-head.html
PREFIX := includes/page-header.html
SUFFIX := includes/page-footer.html
STYLES := media/styles.css

PANDOC := pandoc -s -c ${STYLES} -H ${HEADER} -B ${PREFIX} -A ${SUFFIX}

INPUTS := $(shell find . -type f ! -name README.md -name '*.md')
OUTPUTS := $(INPUTS:.md=.html)

# ------------
# User Targets
# ------------

.PHONY: help
help:
	@echo "init   - create a site skeleton"
	@echo "site   - build the site"
	@echo "clean  - remove generated HTML files"
	@echo "reset  - remove skeleton and generated HTML files"
	@echo "serve  - serve the site locally"
	@echo "upload - upload the site to a server"

.PHONY: init
init: ${INDEX} ${HEADER} ${PREFIX} ${SUFFIX} ${STYLES}

.PHONY: site
site: ${OUTPUTS} favicon.ico

.PHONY: clean
clean:
	@rm -f ${OUTPUTS}
	@rm -f favicon.ico

.PHONY: reset
reset: clean
	@echo "resetting"
	@rm -f "${INDEX}"
	@rm -f "${HEADER}"
	@rm -f "${PREFIX}"
	@rm -f "${SUFFIX}"
	@rm -f "${STYLES}"

.PHONY: serve
serve:
	@echo "Serving at http://localhost:8080"
	@echo "Use ctrl-c to terminate the server"
	@python3 -m http.server 8080

# ------------------
# Production targets
# ------------------

index.md:
	@echo "creating $@"
	@echo "# Webpage\n\nAwesome content goes here." > index.md

favicon.ico:
	@echo "creating $@"
	@cp "${FAVICON}" favicon.ico

%.html: %.md ${HEADER} ${PREFIX} ${SUFFIX} ${STYLES}
	@echo "building $<"
	@${PANDOC} -M pagetitle:"/$(@D) ${SITE_TITLE}" -o "$@" "$<"
	@ln -fs "$$(realpath --relative-to=$(@D) media)" "$$(dirname $@)" || true

includes/%:
	@echo "creating $@"
	@mkdir -p includes/
	@touch "$@"

media/%:
	@echo "creating $@"
	@mkdir -p media/
	@touch "$@"

