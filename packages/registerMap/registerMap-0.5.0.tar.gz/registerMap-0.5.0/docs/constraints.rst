Constraints
===========

Constraints are a user specified limitation to the normal behaviour of modules and registers.

The current constraints are:

* **Memory alignment**: Specify a memory or register to align to a number of memory units.
* **Fixed address**: Specify the base address of a module or register.
* **Fixed size**: Specify a module or register as occupying a fixed size in memory.

In relation to these constraints, the normal behaviour of registers and modules is described below. The assumption is
that most of the time the user is not interested in specifying the size, alignment or base address of register and
modules and simply wants the modules and registers in order and the addresses to be known at specific times such as
export to C or C++ headers for use by software, for example.

1. Registers and modules are *ordered* such that the order of elements is preserved in the register map memory space.

#. In increasing order, the next available memory unit (address) in the memory space is allocated to the next register or module.

   eg. memory base address = 0x2000

       implies, first module base address = 0x2000

       in turn implies, first register of first module = 0x2000

#. At the end of a register or module the next available memory unit is allocated to the next register or module

   eg. memory base address = 0x2000

       first module has one or more registers spanning 16 bytes

       implies, next module base address = 0x2010

       in turn implies, first register of next module base address = 0x2010

       If first register of next module spans 4 bytes, then

       second register of next module base address = 0x2014

#. A register size will grow in increments of memory units depending on the bit fields that are allocated within the
   register. Implicitly the register will always be the minimum necessary size to span its bit fields.

#. A module size will grow in increments of memory units depending on how many registers are allocated within the
   module. Implicitly the module will always be the minimum necessary size to span its registers.


Memory alignment constraint
---------------------------

The memory alignment constraint enables the user to specify a register or module to align its base address with an integer
multiple of memory units.

For example, in a memory space with 8 bit memory units, the memory alignment constraint could align to 16, 32 or 64 bit
word boundaries (2, 4, 8 memory units respectively).

.. code-block:: python

   import registerMap
   myMap = registerMap.RegisterMap()

   myMap.memory.baseAddress = 0x1

   module1 = myMap.addModule( 'module1' )
   # with no constraint module1 base address is the register map base address
   assert module1.baseAddress == myMap.memory.baseAddress

   module1[ 'constraints' ][ 'alignmentMemoryUnits' ] = 4

   # memory space base address set to a non-aligned address
   assert myMap.memory.baseAddress == 0x1
   # module1 aligned base address
   assert module1.baseAddress == 0x4


Fixed address constraint
------------------------

The fixed address constraint enables the user to specify the base address of a register or module.

.. code-block:: python

   import registerMap
   myMap = registerMap.RegisterMap()
   # default memory space base address
   assert myMap.memory.baseAddress == 0x0

   module1 = myMap.addModule( 'module1' )
   # with no constraint module1 base address is the register map base address
   assert module1.baseAddress == myMap.memory.baseAddress

   module1[ 'constraints' ][ 'fixedAddress' ] = 0x2000

   # default memory space base address is retained
   assert myMap.memory.baseAddress == 0x0
   # specified module1 base address
   assert module1.baseAddress == 0x2000


Fixed size constraint
---------------------

The fixed size constraint enables the user to specify the size of a register or module. If bit fields are allocated to
a register, or register are allocated to a module, that exceed the fixed size, then an exception will be thrown.

.. code-block:: python

   import registerMap
   myMap = registerMap.RegisterMap()

   module1 = myMap.addModule( 'module1' )
   module1[ 'constraints' ][ 'fixedSizeMemoryUnits' ] = 6

   module2 = myMap.addModule( 'module2' )

   # default memory space base address
   assert myMap.memory.baseAddress == 0x0
   # module1 base address is memory space base address
   assert module1.baseAddress == myMap.memory.baseAddress
   # module1 spans 6 memory units so the next available address for module2 is 0x6
   assert module2.baseAddress == 0x6
