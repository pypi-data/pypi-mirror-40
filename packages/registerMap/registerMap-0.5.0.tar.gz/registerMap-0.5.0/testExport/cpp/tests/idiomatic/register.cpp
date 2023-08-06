/*
 *
 * Copyright 2018 Russell Smiley
 *
 * This file is part of registerMap.
 *
 * registerMap is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * registerMap is distributed in the hope that it will be useful
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with registerMap.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#include "catch.hpp"
#include "myRegisterMap/registerMap.hpp"


SCENARIO( "register offsets", "[register]" )
{

  GIVEN( "Registers in a register map" )
  {

    WHEN( "the register offset is acquired" )
    {
      std::uintptr_t const baseAddress = reinterpret_cast<std::uintptr_t>( myRegisterMap::myRegisterMap.memory.base );

      std::uintptr_t const r1_offset =
        reinterpret_cast<std::uintptr_t>( &myRegisterMap::myRegisterMap.m1->r1 ) - baseAddress;
      std::uintptr_t const r2_offset =
        reinterpret_cast<std::uintptr_t>( &myRegisterMap::myRegisterMap.m2->r2 ) - baseAddress;
      std::uintptr_t const r3_offset =
        reinterpret_cast<std::uintptr_t>( &myRegisterMap::myRegisterMap.m2->r3 ) - baseAddress;

      THEN( "the register offsets are as expected" )
      {
        REQUIRE( 0 == r1_offset );
        REQUIRE( 2 == r2_offset );
        REQUIRE( 3 == r3_offset );
      }
    }
  }


  GIVEN( "Registers with an unused gap between them" )
  {

    WHEN( "the register offset is acquired" )
    {
      std::uintptr_t const baseAddress = reinterpret_cast<std::uintptr_t>( myRegisterMap::myRegisterMap.memory.base );

      std::uintptr_t const r2_offset =
        reinterpret_cast<std::uintptr_t>( &myRegisterMap::myRegisterMap.m3->r2 ) - baseAddress;
      std::uintptr_t const r4_offset =
        reinterpret_cast<std::uintptr_t>( &myRegisterMap::myRegisterMap.m3->r4 ) - baseAddress;

      THEN( "the register offsets are as expected" )
      {
        std::uintptr_t const expectedOffset_r2 = 0x4;
        std::uintptr_t const expectedOffset_r4 = 0x21;

        REQUIRE( expectedOffset_r2 == r2_offset );
        REQUIRE( expectedOffset_r4 == r4_offset );
      }
    }
  }
}
