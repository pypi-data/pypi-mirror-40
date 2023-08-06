const unsigned short BGPalette[{{ BGpalette|length }}] __attribute__((aligned(4))) __attribute__((visibility("hidden")))=
{
    {% for i in range(BGpalette|length) -%}
    {{ "{0:#06x}".format(BGpalette[i]) }},
    {%- if loop.index is divisibleby 12 and not loop.last %}
    {% endif -%}
    {%- endfor %}
};

const unsigned int BGTileset[{{ BGtileset|length }}] __attribute__((aligned(4))) __attribute__((visibility("hidden")))=
{
    {% for i in range(BGtileset|length) -%}
    {{ "{0:#010x}".format(BGtileset[i]) }},
    {%- if loop.index is divisibleby 8 and not loop.last %}
    {% endif -%}
    {%- endfor %}
};

{% for i in range(BGtile_maps|length) %}
const int {{ BGtile_map_names[i] }}Size[2] = { {{ BGtile_map_sizes[i][0] }}, {{ BGtile_map_sizes[i][1] }} };
const unsigned short {{ BGtile_map_names[i] }}[{{ BGtile_maps[i]|length }}] __attribute__((aligned(4))) __attribute__((visibility("hidden")))=
{
    {% for o in range(BGtile_maps[i]|length) -%}
    {{ "{0:#06x}".format(BGtile_maps[i][o]) }},
    {%- if loop.index is divisibleby 12 and not loop.last %}
    {% endif -%}
    {%- endfor %}
};
{% endfor %}

{% for i in range(OBJpalettes|length) %}
const unsigned short {{ OBJnames[i] }}Palette[{{ OBJpalettes[i]|length }}] __attribute__((aligned(4))) __attribute__((visibility("hidden")))=
{
    {% for o in range(OBJpalettes[i]|length) -%}
    {{ "{0:#06x}".format(OBJpalettes[i][o]) }},
    {%- if loop.index is divisibleby 12 and not loop.last %}
    {% endif -%}
    {%- endfor %}
};

const unsigned int {{ OBJnames[i] }}Tileset[{{ OBJtilesets[i]|length }}] __attribute__((aligned(4))) __attribute__((visibility("hidden")))=
{
    {% for o in range(OBJtilesets[i]|length) -%}
    {{ "{0:#010x}".format(OBJtilesets[i][o]) }},
    {%- if loop.index is divisibleby 8 and not loop.last %}
    {% endif -%}
    {%- endfor %}
};
{% endfor %}
