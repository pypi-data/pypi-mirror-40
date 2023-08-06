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


IDIOMATIC_REGISTERMAP_FILES := \
  memory.cpp \
  $(REGISTERMAP_NAME).cpp

IDIOMATIC_PREFIXED_REGISTERMAP_FILES := $(addprefix source/$(REGISTERMAP_NAME)/,$(IDIOMATIC_REGISTERMAP_FILES))

IDIOMATIC_TEST_FILES := \
  field.cpp \
  memory.cpp \
  register.cpp

IDIOMATIC_TEST_SOURCE := \
  $(IDIOMATIC_PREFIXED_REGISTERMAP_FILES) \
  $(addprefix tests/idiomatic/,$(IDIOMATIC_TEST_FILES))
