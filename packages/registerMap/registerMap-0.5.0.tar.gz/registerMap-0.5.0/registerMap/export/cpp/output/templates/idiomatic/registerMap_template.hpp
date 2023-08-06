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

#ifndef {{ registerMap.name|upper }}_HPP
#define {{ registerMap.name|upper }}_HPP

{% for thisModule in registerMap.modules -%}
#include "{{ prefixPath }}/modules/{{ thisModule.name }}.hpp"
{% endfor %}

{% set registerMapType = registerMap.name~'_t' -%}
namespace {{ registerMap.name }}
{
  {%- if registerMap.modules|count != 0 %}

#pragma pack( {{ registerMap.memory.alignment }} )

  class {{ registerMapType }}
  {
    public:
      MemorySpace memory;

      {{ registerMapType }}() :
      {%- for thisModule in registerMap.modules %}
      {%- set pointerType = thisModule.name~'_t volatile* const' %}
          {{ thisModule.name }}( reinterpret_cast<{{ pointerType }}>( memory.base + {{ thisModule.offset }} ) ){{ "," if not loop.last }}
      {%- endfor %}
        {};
{% for thisModule in registerMap.modules %}
      {%- set pointerType = thisModule.name~'_t volatile* const' %}
      {{ pointerType }} {{ thisModule.name }};
{%- endfor %}
  };

#pragma pack()


  // Declare the register map instance for users.
  extern {{ registerMap.name }}_t {{ registerMap.name }};
  {%- endif %}

}

#endif
