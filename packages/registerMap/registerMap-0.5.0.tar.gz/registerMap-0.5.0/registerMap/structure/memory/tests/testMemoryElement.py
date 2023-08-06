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

import logging
import unittest

from ..element import \
    MemoryUnitMemoryElement, \
    SizeValue


log = logging.getLogger( __name__ )


class TestMemoryUnitsMemoryElementDefaultConstructor( unittest.TestCase ) :

    def setUp( self ) :
        self.memoryUnitBits = SizeValue( 8 )


    def testDefaultArguments( self ) :
        testElement = MemoryUnitMemoryElement( self.memoryUnitBits )

        self.assertIsNone( testElement.sizeBits )
        self.assertIsNone( testElement.sizeMemoryUnits )


    def testAssignSizeBits( self ) :
        testElement = MemoryUnitMemoryElement( self.memoryUnitBits )

        testElement.sizeBits = 16

        self.assertEqual( 16, testElement.sizeBits )
        self.assertEqual( 2, testElement.sizeMemoryUnits )


    def testAssignSizeMemoryUnits( self ) :
        testElement = MemoryUnitMemoryElement( self.memoryUnitBits )

        testElement.sizeMemoryUnits = 4

        self.assertEqual( 32, testElement.sizeBits )
        self.assertEqual( 4, testElement.sizeMemoryUnits )


    def testAssignSizeBitsRaises( self ) :
        """
        Assigning a non integer multiple of memoryUnitBits raises an exception
        """
        testElement = MemoryUnitMemoryElement( self.memoryUnitBits )

        with self.assertRaisesRegex( RuntimeError, '^Cannot assign bits a non integer multiple of memory units' ) :
            testElement.sizeBits = 15


if __name__ == '__main__' :
    unittest.main()
