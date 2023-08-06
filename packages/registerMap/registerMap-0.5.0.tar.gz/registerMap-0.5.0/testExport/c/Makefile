#
# Copyright 2018 Russell Smiley
#
# This file is part of registerMap.
#
# registerMap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# registerMap is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with registerMap.  If not, see <http://www.gnu.org/licenses/>.
#

VENV_PATH := /venv/bin
YAML_DIR := ../yaml

REGISTERMAP_YAML_FILE := $(YAML_DIR)/test-export.yml
REGISTERMAP_NAME := myRegisterMap

include tests/idiomatic/idiomatic.mk


all: clean idiomatic-tests


.PHONY: idiomatic-tests
idiomatic-tests: OUTPUT_FILE=c-idiomatic-tests
idiomatic-tests: TEST_SOURCE=$(IDIOMATIC_TEST_SOURCE) main.cpp
idiomatic-tests: clean export build-tests run-tests


.PHONY: export
export:
	$(VENV_PATH)/python3 $(YAML_DIR)/defineSimpleRegisterMap.py \
	  $(YAML_DIR)
	$(VENV_PATH)/export-map \
	  $(REGISTERMAP_YAML_FILE) \
	  --registermap-name $(REGISTERMAP_NAME) \
	  c \
	  . \
	  --pack 1 \
	  --include-prefix some/path


.PHONY: build-tests
build-tests:
	g++ \
	-std=c++17 \
	-D OFF_TARGET_MEMORY \
	-I ./include \
	-o $(OUTPUT_FILE) \
	$(TEST_SOURCE)


.PHONY: run-tests
run-tests:
	./$(OUTPUT_FILE)


.PHONY: clean
clean:
	@rm -rf ./include/$(REGISTERMAP_NAME)
	@rm -rf ./source/*
	@rm -f ./c-idiomatic-tests
