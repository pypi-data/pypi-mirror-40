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

"""
Test ``BitsMemoryELement``.
"""

import unittest.mock

from ..configuration import MemoryConfiguration
from ..element import BitsMemoryElement


class TestBitsMemoryElementConstructor( unittest.TestCase ) :
    """
    Test ``BitsMemoryElement`` constructor.
    """


    def setUp( self ) :
        self.memoryConfiguration = MemoryConfiguration()


    def testDefaultArguments( self ) :
        testElement = BitsMemoryElement()

        self.assertIsNone( testElement.sizeBits )


    def testConstructSize( self ) :
        expectedSize = 10
        testElement = BitsMemoryElement( expectedSize )

        self.assertEqual( expectedSize, testElement.sizeBits )


class TestBitsMemoryElementSizeProperties( unittest.TestCase ) :
    """
    Test ``BitsMemoryElement`` size properties.
    """


    def setUp( self ) :
        self.memoryConfiguration = MemoryConfiguration()
        self.mockObserver = unittest.mock.MagicMock()

        self.elementUnderTest = BitsMemoryElement()
        self.elementUnderTest.addObserver( self.mockObserver )


    def testAssignSizeObserverNotified( self ) :
        self.assertIsNone( self.elementUnderTest.sizeBits )
        expectedSize = 1
        self.elementUnderTest.sizeBits = expectedSize

        self.assertEqual( expectedSize, self.elementUnderTest.sizeBits )
        self.mockObserver.update.assert_called_once()


    def testAssignSizeObserverNotNotified( self ) :
        self.assertIsNone( self.elementUnderTest.sizeBits )
        expectedSize = 1
        self.elementUnderTest.sizeBitsNoNotify = expectedSize

        self.assertEqual( expectedSize, self.elementUnderTest.sizeBits )
        self.mockObserver.update.assert_not_called()


if __name__ == '__main__' :
    unittest.main()
