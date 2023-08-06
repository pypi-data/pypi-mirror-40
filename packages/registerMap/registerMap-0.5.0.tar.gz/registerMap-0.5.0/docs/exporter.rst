Exporting to other formats
==========================

When the Python wheel is installed a command line utility becomes available to facilitate converting a register map YAML
file to other formats.

.. code-block:: bash

   export-map <register map YAML file> --registermap-name <my register map name> <export language> <export location>

For the moment only C and C++ export languages are available. The optional register map name may be used to control the
naming convention of files and folders, enabling the simultaneous installation of multiple register maps into a single
source tree location. The export location is a directory into which the register map source files will be installed. In
C and C++ these would be the necessary `include` and `source` folders, for example.


C/C++ export
------------

C/C++ export includes the concept of "off target" vs "on target". On target means being compiled into the target
architecture, while off target means being compiled into architecture other than the target - usually a generic PC system
running Linux or Windows specifically for the purpose of running unit tests.

When compiling off target, the assumption is that the register map memory space is a contiguous series of addresses from
some start address up to an end address. The end address is the last used address of the last module; this
corresponds to the register map "span".

Use the define `-D OFF_TARGET_MEMORY` to compile off target.


C/C++ export options
^^^^^^^^^^^^^^^^^^^^

For the most part the C and C++ export options are the same. It will be noted in the text where any differences exist.

+-----------------------------+----------------------------------------------------------------------------------------+
| Command line option         | Description                                                                            |
+=============================+========================================================================================+
| output (mandatory)          | The directory to output generated headers and source files. The directory is created   |
|                             | if not present, along with any necessary subdirectories.                               |
|                             | By default the following directory/file tree is created (in C these are `.h` and `.c`  |
|                             | files instead of `.hpp` and `.cpp` files):                                             |
|                             | |defaultTree|                                                                          |
+-----------------------------+----------------------------------------------------------------------------------------+
| --pack <integer> (optional) | The memory alignment size specified using `#pragma pack`. The packing value is enabled |
|                             | only for the registermap.                                                              |
+-----------------------------+----------------------------------------------------------------------------------------+
| --include-prefix <value>    | A prefix path to be pre-pended to `#include` directives in the register map. The value |
|      (optional)             | is also used as a prefix in the structure of the register map file hierarchy.          |
|                             | The prefixed include tree looks like this:                                             |
|                             | |prefixedTree|
+-----------------------------+----------------------------------------------------------------------------------------+

.. |defaultTree| replace::
   .
   ├── include
   │   └── < register map name >
   │       ├── macro
   │       ├── memory
   │       ├── modules
   │       └── registerMap.hpp
   └── source
       ├── memory.cpp
       └── < register map name >.cpp


.. |prefixedTree| replace::
   .
   ├── include
   │   └── < prefix path >
   │       └── < register map name >
   │           ├── macro
   │           ├── memory
   │           ├── modules
   │           └── registerMap.hpp
   └── source
       └── < register map name >
           ├── memory.cpp
           └── < register map name >.cpp
