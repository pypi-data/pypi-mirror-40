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

#ifndef {{ registerMapName|upper }}_{{ module.name|upper }}_HPP
#define {{ registerMapName|upper }}_{{ module.name|upper }}_HPP

#include <cstdint>

#include "{{ prefixPath }}/memory/memory.hpp"

{% if  module.registers|count != 0 %}
namespace {{ registerMapName }}
{

  namespace {{ module.name }}
  {
    {%- for thisRegister in module.registers %}

    class {{ thisRegister.name }}_t
    {
      public:
      {%- for bitField in thisRegister.fields %}
        {{ bitField.type }} volatile {{ bitField.name }}:{{ bitField.size }};
      {%- endfor %}
    };

    {%- endfor %}

  }


#pragma pack( {{ registerMapMemoryAlignment }} )

  class {{ module.name }}_t
  {
    public:
{% for thisRegister in module.registers %}
{%- if thisRegister.precedingGapBytes != 0 %}
      uint8_t gap_{{ thisRegister.name }}[{{ thisRegister.precedingGapBytes }}];
{%- endif %}
      {{ module.name }}::{{ thisRegister.name }}_t volatile {{ thisRegister.name }};
{%- endfor %}
  };


#pragma pack()

}
{% else %}
// {{ registerMapName }}::{{ module.name }} is an empty module
{%- endif %}

#endif
