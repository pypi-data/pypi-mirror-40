User defined parameters
=======================

The users may specify their own parameters to modules, registers and fields. The values are preserved in YAML
import/export and the types are consistent with the types accepted by the `pyyaml` package used by `registerMap`. An
incomplete list of such types includes `bool`, `int`, `str` and `float`.

More complex types may also be supported, but this should not be relied upon as support may change without notice as the
version of `pyyaml` package is updated.

The names of user defined parameters must not begin with underscore ('_') as this is a special character that is ignored
by register map YAML import.

.. code-block:: python

   import registerMap
   myMap = registerMap.RegisterMap()

   m1 = myMap.addModule( 'module1' )

   m1['bool-parameter'] = True
   m1['float-parameter'] = 3.14

   r1 = m1.addRegister( 'register1' )

   r1['int-parameter'] = 31
   r1['string-parameter'] = 'some value'
