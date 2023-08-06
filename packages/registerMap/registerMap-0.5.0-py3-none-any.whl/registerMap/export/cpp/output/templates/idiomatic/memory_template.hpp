/*
 *
 * {{ registerMapName }}
 *
 {%- if licenseText is not none %}
 {%- for line in licenseText %}
 * {{ line }}
 {%- endfor %}
 {%- endif %}
 *
 */

#ifndef {{ registerMapName|upper }}_MEMORY_HPP
#define {{ registerMapName|upper }}_MEMORY_HPP

#include <cstdint>


namespace {{ registerMapName }}
{

{% set memoryPointerType = memory.sizeType~' volatile* const' -%}
  class MemorySpace
  {
  public:

    static {{ memoryPointerType }}
      base;

#ifdef OFF_TARGET_MEMORY

    static constexpr std::uint_least32_t
      allocated_memory_span = {{ memory.size }};

    static {{ memory.sizeType }} volatile
      off_target_memory[ allocated_memory_span ];

#endif

  };

}

#endif
