#
# Copyright 2017 Russell Smiley
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

import typing

from registerMap.exceptions import ConfigurationError
from registerMap.utility.observer import \
    Observable, \
    SizeChangeObserver

from .interface import AddressableElementInterface
from .configuration import MemoryConfiguration


SizeValue = typing.NewType( 'SizeValue', int )


class BitsMemoryElement( Observable ) :
    """
    Fundamental object of a memory space expresses the objects size in bits.

    The `BitsMemoryElement` is `Observable` so that the user can receive notification of a size change if needed.
    """


    def __init__( self,
                  sizeBits: SizeValue = None ) :
        super().__init__()

        self.__sizeObserver = SizeChangeObserver( self )

        self.__sizeBits = SizeValue( sizeBits )


    @property
    def sizeBits( self ) -> SizeValue :
        """
        Number of bits spanned by the element.
        """
        return self.__sizeBits


    @sizeBits.setter
    def sizeBits( self, v: SizeValue ) :
        self.__sizeBits = v
        self.notifyObservers()


    def __setattr__( self, key, value ) :
        """
        Create a "set only" property for ``sizeBitsNoNotify``.

        :param key:
        :param value:
        """
        if key == 'sizeBitsNoNotify' :
            # assign the bits and don't notify
            self.__sizeBits = value
        else:
            super().__setattr__( key, value )


class MemoryUnitMemoryElement( BitsMemoryElement ) :

    def __init__( self,
                  memoryUnitBits: SizeValue,
                  sizeMemoryUnits: SizeValue = None ) :
        sizeBits = None
        if sizeMemoryUnits is not None :
            sizeBits = sizeMemoryUnits * memoryUnitBits

        super().__init__( sizeBits = sizeBits )

        self.__memoryUnitBits = memoryUnitBits


    @BitsMemoryElement.sizeBits.setter
    def sizeBits( self, v: SizeValue ) :
        """
        Overload the BitMemoryElement sizeBits property setter to check that the assigned bits are an integer
        multiple of the memory unit bits.

        :param v:

        :return:
        """
        if (v % self.__memoryUnitBits) != 0 :
            raise RuntimeError( 'Cannot assign bits a non integer multiple of memory units, {0}'.format( v ) )

        BitsMemoryElement.sizeBits.fset( self, v )


    @property
    def sizeMemoryUnits( self ) -> SizeValue :
        """
        Number of memory units spanned by the element.
        """
        if self.sizeBits is not None :
            assert (self.sizeBits % self.__memoryUnitBits) == 0

            value = SizeValue( int( self.sizeBits / self.__memoryUnitBits ) )
        else :
            value = self.sizeBits

        return value


    @sizeMemoryUnits.setter
    def sizeMemoryUnits( self, v: SizeValue ) :
        self.sizeBits = v * self.__memoryUnitBits


    def __setattr__( self, key, value ) :
        if key == 'sizeMemoryUnitsNoNotify' :
            pass

        super().__setattr__( key, value )


AddressValue = typing.NewType( 'AddressValue', int )


class AddressableMemoryElement( AddressableElementInterface ) :
    """
    Basic address properties of a memory element. The assumption is that an addressable memory element prefers to
    express size in terms of memory units rather than bits.

    For the purpose of enabling the separation of instances from the element object (say, `Register` and
    `RegisterInstance`) the MemoryElement to use for size related calculations can be supplied in the constructor.

    `AddressableMemoryElement` composites `MemoryElement` so that memory element instances such as `RegisterInstance`
    can refer to an independent object for size.
    """
    __DEFAULT_SIZE_MEMORY_UNITS = 1


    def __init__( self, memoryConfiguration: MemoryConfiguration,
                  startAddress: AddressValue = None,
                  endAddress: AddressValue = None,
                  sizeMemoryUnits: SizeValue = None,
                  sizeObject: typing.Type[ BitsMemoryElement ] = None ) :

        super().__init__()

        self.memoryConfiguration = memoryConfiguration

        if (endAddress is not None) and (sizeMemoryUnits is not None) :
            raise ConfigurationError(
                'Cannot specify both endAddress and sizeMemoryUnits, {0}, {1}'.format(
                    endAddress, sizeMemoryUnits ) )

        self.__sizeObserver = SizeChangeObserver( self )

        if sizeObject is not None :
            self.__size = sizeObject
        elif sizeMemoryUnits is not None :
            sizeBits = self.__calculateSizeBits( sizeMemoryUnits )
            self.__size = BitsMemoryElement( sizeBits )
        else :
            sizeBits = self.__calculateSizeBits( self.__DEFAULT_SIZE_MEMORY_UNITS )
            self.__size = BitsMemoryElement( sizeBits )

        self.__size.addObserver( self.__sizeObserver )

        self.__startAddress = startAddress
        if startAddress is None :
            self.__endAddress = None
        else :
            assert startAddress is not None

            # Assume the start address is numerical
            # If a sizeObject is specified, assume that it's size is valid.
            if endAddress is not None :
                self.__evaluateSizeFromEndAddressChange( endAddress )
            elif sizeMemoryUnits is not None :
                self.__evaluateEndAddressFromSizeChange( sizeMemoryUnits )
            elif sizeObject is None :
                self.__endAddress = self.__startAddress


    def __evaluateEndAddressFromSizeChange( self, newSizeMemoryUnits: SizeValue ) :
        """
        Adjust end address assuming the start address is constant.

        :param newSizeMemoryUnits:
        """
        if newSizeMemoryUnits is None :
            self.__endAddress = None
        elif self.__startAddress is not None :
            self.__endAddress = self.__startAddress + newSizeMemoryUnits - 1

        self.__updateSizeBits( newSizeMemoryUnits )


    def __updateSizeBits( self, newSizeMemoryUnits: SizeValue ) :
        if newSizeMemoryUnits is not None :
            self.__size.sizeBitsNoNotify = newSizeMemoryUnits * self.memoryConfiguration.memoryUnitBits
        else :
            self.__size.sizeBitsNoNotify = None


    def __evaluateEndAddressFromStartAddressChange( self, newAddress: AddressValue ) :
        """
        Adjust end address assuming the size is constant.

        :param newAddress:
        """
        if newAddress is None :
            self.__endAddress = None
        elif self.__size.sizeBits is not None :
            self.__endAddress = newAddress + self.sizeMemoryUnits - 1

        self.__startAddress = newAddress


    def __evaluateStartAddressFromSizeChange( self, newSizeMemoryUnits: SizeValue ) :
        """
        Adjust start address assuming the end address is constant.

        :param newSizeMemoryUnits:
        """
        if newSizeMemoryUnits is None :
            self.__startAddress = None
        elif self.__endAddress is not None :
            self.__startAddress = self.__endAddress - newSizeMemoryUnits + 1

        self.__updateSizeBits( newSizeMemoryUnits )


    def __evaluateStartAddressFromEndAddressChange( self, newAddress: AddressValue ) :
        """
        Adjust start address assuming the size is constant.

        :param newAddress:
        """
        if newAddress is None :
            self.__endAddress = None
        elif self.__size.sizeBits is not None :
            self.__startAddress = newAddress - self.sizeMemoryUnits + 1

        self.__endAddress = newAddress


    def __evaluateSizeFromStartAddressChange( self, newAddress: AddressValue ) :
        """
        Adjust size assuming the end address is constant.

        :param newAddress:
        """
        if newAddress is None :
            self.__startAddress = None
        elif self.__endAddress is not None :
            self.__updateSizeBits( SizeValue( self.__endAddress - newAddress + 1 ) )

        self.__startAddress = newAddress


    def __evaluateSizeFromEndAddressChange( self, newAddress: AddressValue ) :
        """
        Adjust size assuming the start address is constant.

        :param newAddress:
        """
        if newAddress is None :
            self.__startAddress = None
        elif self.__startAddress is not None :
            self.__updateSizeBits( newAddress - self.__startAddress + 1 )

        self.__endAddress = newAddress


    @property
    def offset( self ) :
        """
        Address offset relative to the memory space base address.
        """
        if self.__startAddress is None :
            offset = None
        else :
            offset = self.__startAddress - self.memoryConfiguration.baseAddress

        return offset


    def __calculateSizeBits( self, sizeMemoryUnits: SizeValue ) -> SizeValue :
        sizeBits = None
        if sizeMemoryUnits is not None :
            sizeBits = sizeMemoryUnits * self.memoryConfiguration.memoryUnitBits

        return sizeBits


    @property
    def sizeMemoryUnits( self ) -> SizeValue :
        if self.__size.sizeBits is None :
            value = None
        else :
            assert isinstance( self.__size.sizeBits, int )
            assert (self.__size.sizeBits % self.memoryConfiguration.memoryUnitBits) == 0

            value = SizeValue( int( self.__size.sizeBits / self.memoryConfiguration.memoryUnitBits ) )

        return value


    @sizeMemoryUnits.setter
    def sizeMemoryUnits( self, value: SizeValue ) :
        # Assume the start address is fixed and adjust the end address.
        self.__evaluateEndAddressFromSizeChange( value )


    @property
    def startAddress( self ) -> AddressValue :
        """
        The start address of the element, corresponding to the lowest numerical value of the addresses spanned by the
        element.
        """
        return self.__startAddress


    @startAddress.setter
    def startAddress( self, value: AddressValue ) :
        # Assume the size is fixed and adjust the end address.
        self.__evaluateEndAddressFromStartAddressChange( value )


    @property
    def endAddress( self ) -> AddressValue :
        """
        The end address of the element, corresponding to the highest numerical value of the addresses spanned by the
        element.
        """
        return self.__endAddress


    @endAddress.setter
    def endAddress( self, value: AddressValue ) :
        if self.__startAddress is None :
            raise ConfigurationError( 'Must define start address before attempting to define end address' )
        else :
            # Assume the start address is fixed and adjust the size.
            self.__evaluateSizeFromEndAddressChange( value )


    def reviewSizeChange( self ) :
        if self.__size.sizeBits is not None :
            assert (self.__size.sizeBits % self.memoryConfiguration.memoryUnitBits) == 0

        self.__evaluateEndAddressFromSizeChange( self.sizeMemoryUnits )
