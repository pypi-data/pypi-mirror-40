Introduction
============

In this framework a register map is an ordered list of modules. A module is an ordered list of registers and a register
is made up of fields.

A memory space defines the fundamental properties of the register map such as the number of bits in addresses, the base
address of the register map and the number of bits in memory units. This is also where memory paging can be defined.

    *   All memory units are the same size.
    *   Each memory unit has an address, so the maximum address minus the base address of the memory space is the
        maximum number of memory units.

The order of the modules defines how module addresses are generated. So the first module in the list would probably get
assigned the base address of the register map memory space and the next module might get the next available address.
The words 'probably' and 'might' are used here because there are other factors such as the total span of the module,
page registers and constraints applied to modules and registers that can change what addresses are available for
assignment. More on that later.

A module is a way of grouping registers together. When there is more than one module, the groups will probably have
some functional association of the registers, for example, a set of registers associated with a particular output, or a
set of read only registers for reporting status.

A register is made up of fields. The order of fields is not defined because the register bits to which each field
is assigned must be explicitly defined. A register, or perhaps more accurately, the total span of the bit width of its
fields may also span multiple memory units. This enables support for data that is larger than the bit size of a single
memory unit;
eg. If the memory unit size is 8 bits, then it may still be desirable to store a 16, 32 or 64 bit number for the
function of the integrated circuit.

The primary source format of the register map is YAML, so one way to get started is by `defining your register map
directly in a YAML text file`_. The other way is to import the Python library and start `working on the register map
dataset directly in a Python`_ terminal or script.

.. _`defining your register map directly in a YAML text file`: `Getting started using a YAML file`_
.. _`working on the register map dataset directly in a Python`: `Getting started using Python`_


Register map elements
---------------------

Memory space
    The memory space defines some basic properties of the register map memory such as the number of bits in addresses,
    the base address of the register map and the number of bits in memory units. This is also where memory paging can
    be defined.

    #.  Base address: The first address in the memory space.

        Default: 0x0
    #.  Address size: the number of bits in an address, ultimately defining the maximum number of addressable memory
        units when combined with the base address.

        eg. Common computer systems have 32 or 64 bit address busses, but maybe your custom digital system has 12 bits?

        Default: 32 bits
    #.  Memory unit size: the number of bits in a memory unit.

        Default: 8 bits

Register
    A register is defined as an integer number of memory units and is comprised of zero or more fields that are
    allocated to the individual bits of the memory units allocated to the register. When empty a register consumes one
    memory unit.

    Register names must be unique within a module.

Field
    A field is a set of bits that define a numerical value. The exact meaning of the numerical value (signed, unsigned,
    BCD, floating point, etc) is up to the users interpretation. By default a field is *local* to a register, meaning
    that all the field bits are allocated to a single register.

    In some cases it may be necessary to spread field bits across multiple registers and in this case a field may be
    declared *global*. A global field name must be unique across the entire register map.

Module
    A module is a collection of zero or more registers and when empty consumes one memory unit. Module names must be
    unique within the register map.

