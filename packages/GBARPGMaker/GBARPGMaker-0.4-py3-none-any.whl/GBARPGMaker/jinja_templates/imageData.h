#ifndef IMAGE_DATA_H
#define IMAGE_DATA_H

// Background stuff

{% for map_name, map in maps.items() %}
#define {{ map_name }}PaletteLen {{ 2 * map.palette|length }}
extern const unsigned short {{ map_name }}Palette[{{ map.palette|length }}];

#define {{ map_name }}TilesetLen {{ 4 * map.tileset|length }}
extern const unsigned int {{ map_name }}Tileset[{{ map.tileset|length }}];

extern const int {{ map_name }}Size[2];

extern const int {{ map_name }}Specials[{{ map.specials|length }}];

{%- for i in range(map.layer_tile_maps|length) %}

#define {{ map.layer_names[i] }}Len {{ 2 * map.layer_tile_maps[i]|length }}
extern const int {{ map.layer_names[i] }}Size[2];
extern const unsigned short {{ map.layer_names[i] }}[{{ map.layer_tile_maps[i]|length }}];
{%- endfor %}
{% endfor %}

// Sprite stuff

{%- for sprite_name, sprite in sprites.items() %}

extern const unsigned short {{ sprite_name }}Size[2];

#define {{ sprite_name }}PaletteLen {{ 2 * sprite.palette|length }}
extern const unsigned short {{ sprite_name }}Palette[{{ sprite.palette|length }}];

#define {{ sprite_name }}TilesetLen {{ 4 * sprite.tileset|length }}
extern const unsigned {{ sprite_name }}Tileset[{{ sprite.tileset|length }}];
{% endfor %}

#endif
