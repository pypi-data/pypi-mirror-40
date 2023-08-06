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

#include "{{ prefixPath }}/registerMap.hpp"


namespace {{ registerMap.name }}
{

  {{ registerMap.name }}_t {{ registerMap.name }};

}
