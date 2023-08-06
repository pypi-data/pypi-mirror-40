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

import unittest

from ..address import AddressQueryResult


class TestAddressQueryResult( unittest.TestCase ) :

    def setUp( self ) :
        self.elementUnderTest = AddressQueryResult()


    def testDefault( self ) :
        self.assertIsNone( self.elementUnderTest.address )

        self.assertIsNone( self.elementUnderTest.module )
        self.assertIsNone( self.elementUnderTest.register )

        # fields must be an empty list
        self.assertTrue( not self.elementUnderTest.fields )


if __name__ == '__main__' :
    unittest.main()
