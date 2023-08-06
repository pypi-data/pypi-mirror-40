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

#ifndef {{ registerMapName|upper }}_MEMORY_H
#define {{ registerMapName|upper }}_MEMORY_H

#include <stdint.h>

#include "{{ prefixPath }}/macro/extern.h"


{{ registerMapName|upper }}_OPEN_EXTERN_C

{% set memoryPointerType = memory.sizeType~' volatile* const' -%}
struct {{ registerMapName }}_MemorySpace_t
{
#ifdef OFF_TARGET_MEMORY

  uint_least32_t const allocated_memory_span;

  {{ memory.sizeType }} volatile base[ {{ memory.size }} ];

#else

  {{ memoryPointerType }} base;

#endif
};

{{ registerMapName|upper }}_CLOSE_EXTERN_C

#endif
