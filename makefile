.PHONY: \
	prepare_commit \
	update_readme_py_files \
	update_readme_md_files \
	init_project \
	create_readme_notebook_files \
	clean \
	clean_papermill \
	clean_readme_notebook_files

EXISTING_README_NOTEBOOK_FILES := $(shell find . -name README.ipynb)
EXPECTED_README_PYTHON_FILES := $(EXISTING_README_NOTEBOOK_FILES:.ipynb=.py)
EXPECTED_README_MARKDOWN_FILES := $(EXISTING_README_NOTEBOOK_FILES:.ipynb=.md)
PAPERMILL_OUTPUT_DIR := .papermill
PAPERMILL_OUTPUT_DIRS := \
	$(patsubst %/, $(PAPERMILL_OUTPUT_DIR)/%, \
	$(dir $(EXISTING_README_NOTEBOOK_FILES)))
$(info $(PAPERMILL_OUTPUT_DIRS))

EXISTING_README_PYTHON_FILES := $(shell find . -name README.py)
EXPECTED_README_NOTEBOOK_FILES := $(EXISTING_README_PYTHON_FILES:.py=.ipynb)

prepare_commit: update_readme_py_files update_readme_md_files

update_readme_py_files: $(EXPECTED_README_PYTHON_FILES)

update_readme_md_files: $(EXPECTED_README_MARKDOWN_FILES)

init_project: create_readme_notebook_files

create_readme_notebook_files: $(EXPECTED_README_NOTEBOOK_FILES)

%/README.py: %/README.ipynb
	jupytext --output $@ $<

%/README.md: $(PAPERMILL_OUTPUT_DIR)/%/README.md
	cp -f $< $@

$(PAPERMILL_OUTPUT_DIR)/%/README.md: $(PAPERMILL_OUTPUT_DIR)/%/README.ipynb
	jupyter nbconvert --to markdown $<

$(PAPERMILL_OUTPUT_DIR)/%/README.ipynb: %/README.ipynb | $(PAPERMILL_OUTPUT_DIRS)
	-papermill --cwd . $< $@

$(PAPERMILL_OUTPUT_DIRS):
	mkdir -p $@

%/README.ipynb: %/README.py
	jupytext --output $@ $<

clean: clean_papermill clean_readme_notebook_files

clean_papermill:
	rm -rf $(PAPERMILL_OUTPUT_DIR)

clean_readme_notebook_files:
	rm $(EXISTING_README_NOTEBOOK_FILES)
