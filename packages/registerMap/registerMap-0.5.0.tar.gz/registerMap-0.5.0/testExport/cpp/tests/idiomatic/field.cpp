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


SCENARIO( "field values", "[field]" )
{

  GIVEN( "A field in a multi memory unit register" )
  {
    std::uint_least16_t volatile* memoryValue =
      reinterpret_cast<std::uint_least16_t volatile*>( myRegisterMap::myRegisterMap.memory.off_target_memory );
    *(memoryValue) = static_cast<std::uint_least16_t>( 0x18e5 );

    auto f1 = static_cast<std::uint_least32_t>( myRegisterMap::myRegisterMap.m1->r1.f1 );

    REQUIRE( 0xe5 == f1 );

    WHEN( "the field is written to " )
    {
      myRegisterMap::myRegisterMap.m1->r1.f1 = 0x2ac;

      THEN( "the register map contains the new values" )
      {
        REQUIRE( static_cast<std::uint_least16_t>( 0x1aac ) == *(memoryValue) );
      }
    }
  }
}


SCENARIO( "field values can be read from", "[field]" )
{

  GIVEN( "A field in a register with a non-zero value " )
  {
    std::uint_least16_t volatile* memoryValue =
      reinterpret_cast<std::uint_least16_t volatile*>( myRegisterMap::myRegisterMap.memory.off_target_memory );
    *(memoryValue) = static_cast<std::uint_least16_t>( 0x1aac );

    std::uint_least16_t const expectedValue = 0x2ac;
    auto f1 = static_cast<std::uint_least32_t>( myRegisterMap::myRegisterMap.m1->r1.f1 );

    REQUIRE( expectedValue == f1 );

    WHEN( "the field is read from" ) {
      std::uint_least16_t const actualValue = myRegisterMap::myRegisterMap.m1->r1.f1;

      THEN( "the read value is the expected value" )
      {
        REQUIRE( expectedValue == actualValue );
      }
    }
  }
}


SCENARIO( "Non contiguous fields", "[field]" )
{

  GIVEN( "Non contiguous fields in a multi memory unit register" )
  {
    std::uint_least8_t constexpr r3_offset = 3;

    std::uint_least8_t f4_mask = 0x0c;
    std::uint_least8_t f5_mask = 0xe0;

    std::uint_least8_t volatile* memoryValue =
      reinterpret_cast<std::uint_least8_t volatile*>( &(myRegisterMap::myRegisterMap.memory.off_target_memory[r3_offset]) );
    *(memoryValue) = static_cast<std::uint_least8_t>( 0xb8 );


    WHEN( "the fields are read from " )
    {

      THEN( "the fields contain the new values" )
      {
        auto f4 = static_cast<std::uint_least32_t>( myRegisterMap::myRegisterMap.m2->r3.f4 );
        auto f5 = static_cast<std::uint_least32_t>( myRegisterMap::myRegisterMap.m2->r3.f5 );

        REQUIRE( 0x2 == f4 );
        REQUIRE( 0x5 == f5 );
      }
    }

    WHEN( "the field is written to " )
    {
      myRegisterMap::myRegisterMap.m2->r3.f4 = 0x1;
      myRegisterMap::myRegisterMap.m2->r3.f5 = 0x3;

      THEN( "the register map contains the new values" )
      {
        REQUIRE( static_cast<std::uint_least8_t>( 0x74 ) == *(memoryValue) );
      }
    }
  }
}
