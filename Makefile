

TOPTARGETS := clean build s3 clean-s3 ckan clean-ckan info list wp

SUBDIRS := datasets


$(TOPTARGETS): $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

.PHONY: $(TOPTARGETS) $(SUBDIRS) clean-build docker
	
install:
	pip install -r requirements.txt

	
REPO_ROOT=$(shell git rev-parse --show-toplevel)

PACK_DIR=$(REPO_ROOT)/_build
	
clean-build:
	rm -f $(PACK_DIR)/*.build
	

