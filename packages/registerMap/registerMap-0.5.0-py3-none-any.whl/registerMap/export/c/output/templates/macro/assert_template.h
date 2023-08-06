/*
 *
 {%- if licenseText is not none %}
 {%- for line in licenseText %}
 * {{ line }}
 {%- endfor %}
 {%- endif %}
 *
 */

#ifndef {{ registerMapName|upper }}_ASSERT_H
#define {{ registerMapName|upper }}_ASSERT_H


#ifndef DISABLE_RUNTIME_ASSERT

#include <assert.h>
#define RUNTIME_ASSERT(expression) \
  assert(expression)

#else

#define RUNTIME_ASSERT()

#endif


#ifndef DISABLE_COMPILETIME_ASSERT

#define COMPILETIME_ASSERT(expression) \
#if !(expression) \
#error "ASSERTION FAILED: " #expression \
#endif

#else

#define COMPILETIME_ASSERT(expression)

#endif


#endif
