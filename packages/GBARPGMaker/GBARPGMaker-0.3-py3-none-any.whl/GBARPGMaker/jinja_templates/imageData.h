#ifndef IMAGE_DATA_H
#define IMAGE_DATA_H

// Background stuff

#define BGPaletteLen {{ 2 * BGpalette|length }}
extern const unsigned short BGPalette[{{ BGpalette|length }}];

#define BGTilesetLen {{ 4 * BGtileset|length }}
extern const unsigned int BGTileset[{{ BGtileset|length }}];

{%- for i in range(BGtile_maps|length) %}

#define {{ BGtile_map_names[i] }}Len {{ 2 * BGtile_maps[i]|length }}
extern const int {{ BGtile_map_names[i] }}Size[2];
extern const unsigned short {{ BGtile_map_names[i] }}[{{ BGtile_maps[i]|length }}];
{%- endfor %}

// Sprite stuff

{%- for i in range(OBJpalettes|length) %}

#define {{ OBJnames[i] }}PaletteLen {{ 2 * OBJpalettes[i]|length }}
extern const unsigned short {{ OBJnames[i] }}Palette[{{ OBJpalettes[i]|length }}];

#define {{ OBJnames[i] }}TilesetLen {{ 4 * OBJtilesets[i]|length }}
extern const unsigned {{ OBJnames[i] }}Tileset[{{ OBJtilesets[i]|length }}];
{% endfor %}

#endif
