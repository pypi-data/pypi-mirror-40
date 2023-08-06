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

#include <cstdint>

#include "{{ prefixPath }}/memory/memory.hpp"


{% set memoryPointerType = memory.sizeType~' volatile* const' -%}
namespace {{ registerMapName }}
{

#ifndef OFF_TARGET_MEMORY

  {{ memoryPointerType }}
    MemorySpace::base = reinterpret_cast<{{ memoryPointerType }}>( {{ memory.baseAddress }} );

#else

  constexpr std::uint_least32_t
    MemorySpace::allocated_memory_span;

  {{ memory.sizeType }} volatile
    MemorySpace::off_target_memory[];

  {{ memoryPointerType }}
    MemorySpace::base = MemorySpace::off_target_memory;

#endif

}
