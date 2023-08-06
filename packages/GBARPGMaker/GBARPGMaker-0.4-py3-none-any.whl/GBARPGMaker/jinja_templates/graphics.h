#ifndef GRAPHICS_H
#define GRAPHICS_H

const int* currentMapSize;
const int* currentSpecials;
const unsigned short* currentBottomMap;
const int* currentBottomMapSize;
const unsigned short* currentMiddleMap;
const int* currentMiddleMapSize;
const unsigned short* currentTopMap;
const int* currentTopMapSize;

{% for map_name in maps.keys() %}
void loadMap{{ map_name }}();
{% endfor %}
{% for sprite_name in sprites.keys() %}
extern bool {{ sprite_name }}loaded;
extern void* {{ sprite_name }}PaletteLocation;
extern void* {{ sprite_name }}TilesetLocation;

void loadSprite{{ sprite_name }}();

void unloadSprite{{ sprite_name }}();
{% endfor %}

void moveScreen(int screenx, int screeny);

void forceMoveScreen(int screenx, int screeny);

void moveHero(int* herox, int* heroy);

#endif
