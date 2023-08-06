{%- for map_name, map in maps.items() %}
const unsigned short {{ map_name }}Palette[{{ map.palette|length }}] __attribute__((aligned(4))) __attribute__((visibility("hidden")))=
{
    {% for i in range(map.palette|length) -%}
    {{ "{0:#06x}".format(map.palette[i]) }},
    {%- if loop.index is divisibleby 12 and not loop.last %}
    {% endif -%}
    {%- endfor %}
};

const unsigned int {{ map_name }}Tileset[{{ map.tileset|length }}] __attribute__((aligned(4))) __attribute__((visibility("hidden")))=
{
    {% for i in range(map.tileset|length) -%}
    {{ "{0:#010x}".format(map.tileset[i]) }},
    {%- if loop.index is divisibleby 8 and not loop.last %}
    {% endif -%}
    {%- endfor %}
};

const int {{ map_name }}Size[2] = { {{ map.size[0] }}, {{ map.size[1] }} };

const int {{ map_name }}Specials[{{ map.specials|length }}] =
{
    {% for i in map.specials -%}
    {{ "{0}".format(i) }},
    {%- if loop.index is divisibleby 24 and not loop.last %}
    {% endif -%}
    {%- endfor %}
};

{% for i in range(map.layer_tile_maps|length) %}
const int {{ map.layer_names[i] }}Size[2] = { {{ map.layer_sizes[i][0] }}, {{ map.layer_sizes[i][1] }} };
const unsigned short {{ map.layer_names[i] }}[{{ map.layer_tile_maps[i]|length }}] __attribute__((aligned(4))) __attribute__((visibility("hidden")))=
{
    {% for o in range(map.layer_tile_maps[i]|length) -%}
    {{ "{0:#06x}".format(map.layer_tile_maps[i][o]) }},
    {%- if loop.index is divisibleby 12 and not loop.last %}
    {% endif -%}
    {%- endfor %}
};
{% endfor -%}
{% endfor %}

{%- for sprite_name, sprite in sprites.items() %}

const unsigned short {{ sprite_name }}Size[2] = { {{sprite.size[0]}}, {{ sprite.size[1] }} };

const unsigned short {{ sprite_name }}Palette[{{ sprite.palette|length }}] __attribute__((aligned(4))) __attribute__((visibility("hidden")))=
{
    {% for o in range(sprite.palette|length) -%}
    {{ "{0:#06x}".format(sprite.palette[o]) }},
    {%- if loop.index is divisibleby 12 and not loop.last %}
    {% endif -%}
    {%- endfor %}
};

const unsigned int {{ sprite_name }}Tileset[{{ sprite.tileset|length }}] __attribute__((aligned(4))) __attribute__((visibility("hidden")))=
{
    {% for o in range(sprite.tileset|length) -%}
    {{ "{0:#010x}".format(sprite.tileset[o]) }},
    {%- if loop.index is divisibleby 8 and not loop.last %}
    {% endif -%}
    {%- endfor %}
};
{% endfor %}
