/*
 *
 * Module: {{ module.name }}
 *
 {%- if licenseText is not none %}
 {%- for line in licenseText %}
 * {{ line }}
 {%- endfor %}
 {%- endif %}
 *
 */

#ifndef {{ registerMapName|upper }}_{{ module.name|upper }}_H
#define {{ registerMapName|upper }}_{{ module.name|upper }}_H

#include <stdint.h>

#include "{{ prefixPath }}/macro/extern.h"
#include "{{ prefixPath }}/memory/memory.h"
#include "{{ prefixPath }}/registerMap.h"

{% if module.registers|count != 0 %}
{{ registerMapName|upper }}_OPEN_EXTERN_C
{%- for thisRegister in module.registers %}
{%- set canonicalRegisterName = module.name~'_'~thisRegister.name %}
{%- set typeName = canonicalRegisterName~'_t' %}

struct {{ registerMapName }}_{{ typeName }}
{
{%- for bitField in thisRegister.fields %}
  {{ bitField.type }} volatile {{ bitField.name }}:{{ bitField.size }};
{%- endfor %}
};
{% endfor %}

#pragma pack( {{ registerMapMemoryAlignment }} )

struct {{ registerMapName }}_{{ module.name }}_t
{
{%- for thisRegister in module.registers %}
{%- if thisRegister.precedingGapBytes != 0 %}
  uint8_t gap_{{ thisRegister.name }}[{{ thisRegister.precedingGapBytes }}];
{%- endif %}
{%- set canonicalRegisterName = module.name~'_'~thisRegister.name %}
{%- set typeName = canonicalRegisterName~'_t volatile' %}
  struct {{ registerMapName }}_{{ typeName }} {{ thisRegister.name }};
{% endfor -%}
};

#pragma pack()


{{ registerMapName|upper }}_CLOSE_EXTERN_C
{%- else %}
// {{ registerMapName }}_{{ module.name }} is an empty module
{%- endif %}

#endif
