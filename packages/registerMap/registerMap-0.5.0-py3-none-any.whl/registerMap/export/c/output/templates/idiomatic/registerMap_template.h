/*
 *
 * {{ registerMap.name }}
 *
 {%- if licenseText is not none %}
 {%- for line in licenseText %}
 * {{ line }}
 {%- endfor %}
 {%- endif %}
 *
 */

#ifndef {{ registerMap.name|upper }}_H
#define {{ registerMap.name|upper }}_H

#include "{{ prefixPath }}/macro/extern.h"
#include "{{ prefixPath }}/memory/memory.h"

{% for thisModule in registerMap.modules -%}
#include "{{ prefixPath }}/modules/{{ thisModule.name }}.h"
{% endfor %}

{{ registerMap.name|upper }}_OPEN_EXTERN_C
{%- set registerMapType = registerMap.name~'_t' %}
{%- if registerMap.modules|count != 0 %}

#pragma pack( {{ registerMap.memory.alignment }} )

struct {{ registerMapType }}
{
{%- for thisModule in registerMap.modules %}
{%- set pointerType = thisModule.name~'_t volatile* const' %}
  struct {{ registerMap.name }}_{{ pointerType }} {{ thisModule.name }};
{%- endfor %}
};

#pragma pack()


// Declare the register map instance for users.
extern struct {{ registerMap.name }}_MemorySpace_t {{ registerMap.name }}_memory;
extern struct {{ registerMap.name }}_t {{ registerMap.name }};
{%- endif %}

{{ registerMap.name|upper }}_CLOSE_EXTERN_C

#endif
