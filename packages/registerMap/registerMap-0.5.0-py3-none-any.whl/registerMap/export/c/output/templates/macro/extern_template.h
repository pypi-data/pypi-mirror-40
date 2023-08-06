/*
 *
 {%- if licenseText is not none %}
 {%- for line in licenseText %}
 * {{ line }}
 {%- endfor %}
 {%- endif %}
 *
 */

#ifndef {{ registerMapName|upper }}_EXTERN_H
#define {{ registerMapName|upper }}_EXTERN_H

#ifdef __cplusplus

#define {{ registerMapName|upper }}_OPEN_EXTERN_C extern "C" {
#define {{ registerMapName|upper }}_CLOSE_EXTERN_C }

#else

/* Empty macro to disable extern C */
#define {{ registerMapName|upper }}_OPEN_EXTERN_C
#define {{ registerMapName|upper }}_CLOSE_EXTERN_C

#endif

#endif
