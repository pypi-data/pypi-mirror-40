#include <gba.h>
#include <stdio.h>
#include <stdlib.h>

#include "imageData.h"
#include "specials.h"

const int* currentMapSize;
const int* currentSpecials;
const unsigned short* currentBottomMap;
const int* currentBottomMapSize;
const unsigned short* currentMiddleMap;
const int* currentMiddleMapSize;
const unsigned short* currentTopMap;
const int* currentTopMapSize;

void* spritePaletteIndex = (void*)SPRITE_PALETTE;
void* spriteTilesetIndex = (void*)OBJ_BASE_ADR;

{% for map_name, map in maps.items() %}
void loadMap{{ map_name }}() {
    currentMapSize = {{ map_name }}Size;
    currentSpecials = {{ map_name }}Specials;
    dmaCopy({{ map_name }}Palette, BG_PALETTE, {{ map_name }}PaletteLen);
    dmaCopy({{ map_name }}Tileset, TILE_BASE_ADR(0), {{ map_name }}TilesetLen);
    currentBottomMap = {{ map.bottom_layer_name }};
    currentBottomMapSize = {{ map.bottom_layer_name }}Size;
    currentMiddleMap = {{ map.middle_layer_name }};
    currentMiddleMapSize = {{ map.middle_layer_name }}Size;
    currentTopMap = {{ map.top_layer_name }};
    currentTopMapSize = {{ map.top_layer_name }}Size;
}
{% endfor %}
{% for sprite_name in sprites.keys() %}
bool {{ sprite_name }}loaded = false;
void* {{ sprite_name }}PaletteLocation;
void* {{ sprite_name }}TilesetLocation;

void loadSprite{{ sprite_name }}() {
    if ({{sprite_name}}loaded == true) {
        return;
    }
    dmaCopy({{ sprite_name }}Palette, spritePaletteIndex, {{ sprite_name }}PaletteLen);
    dmaCopy({{ sprite_name }}Tileset, spriteTilesetIndex, {{ sprite_name }}TilesetLen);
    {{ sprite_name }}PaletteLocation = spritePaletteIndex;
    {{ sprite_name }}TilesetLocation = spriteTilesetIndex;
    spritePaletteIndex += {{ sprite_name }}PaletteLen;
    spriteTilesetIndex += {{ sprite_name }}TilesetLen;
    {{ sprite_name }}loaded = true;
}

void unloadSprite{{ sprite_name }}() {
    dmaCopy({{ sprite_name }}PaletteLocation + {{ sprite_name }}PaletteLen, {{ sprite_name }}PaletteLocation, spritePaletteIndex - {{ sprite_name }}PaletteLocation);
    dmaCopy({{ sprite_name }}TilesetLocation + {{ sprite_name }}TilesetLen, {{ sprite_name }}TilesetLocation, spriteTilesetIndex - {{ sprite_name }}TilesetLocation);
    spritePaletteIndex -= {{ sprite_name }}PaletteLen;
    spriteTilesetIndex -= {{ sprite_name }}TilesetLen;
    {{ sprite_name }}loaded = false;
}
{% endfor %}

void moveScreen(int screenx, int screeny) {
    static int lastscreentx;
    static int lastscreenty;

    int screentx = (screenx) / 8;
    int screenty = (screeny) / 8;

    if (screentx != lastscreentx || screenty != lastscreenty) {
        for (int i = 0; i < 22; ++i) {
            dmaCopy(currentBottomMap + (i + screenty - 1) * currentBottomMapSize[0] + screentx - 1, MAP_BASE_ADR(24) + 32 * 2 * i, 32 * 2);
        }
        for (int i = 0; i < 22; ++i) {
            dmaCopy(currentMiddleMap + (i + screenty - 1) * currentTopMapSize[0] + screentx - 1, MAP_BASE_ADR(25) + 32 * 2 * i, 32 * 2);
        }
        for (int i = 0; i < 22; ++i) {
            dmaCopy(currentTopMap + (i + screenty - 1) * currentTopMapSize[0] + screentx - 1, MAP_BASE_ADR(26) + 32 * 2 * i, 32 * 2);
        }
    }

    REG_BG0HOFS = screenx % 8 + 8;
    REG_BG0VOFS = screeny % 8 + 8;
    REG_BG1HOFS = screenx % 8 + 8;
    REG_BG1VOFS = screeny % 8 + 8;
    REG_BG2HOFS = screenx % 8 + 8;
    REG_BG2VOFS = screeny % 8 + 8;

    lastscreentx = screentx;
    lastscreenty = screenty;
}

void forceMoveScreen(int screenx, int screeny) {
    moveScreen(-100, -100);
    moveScreen(screenx, screeny);
}

void moveHero(int* herox, int* heroy) {
    int screenx = 0;
    int screeny = 0;
    static int lastherox;
    static int lastheroy;

    if (*herox < 0) {
        *herox = 0;
    } else if (*herox > currentMapSize[0] * 8 - heroSize[0] * 8) {
        *herox = currentMapSize[0] * 8 - heroSize[0] * 8;
    }
    if (*heroy < 0) {
        *heroy = 0;
    } else if (*heroy > currentMapSize[1] * 8 - heroSize[1] * 8) {
        *heroy = currentMapSize[1] * 8 - heroSize[1] * 8;
    }

    int herotx = (*herox) / 8;
    int heroty = (*heroy) / 8;
    int herotex = (*herox - 1) / 8;
    int herotey = (*heroy - 1) / 8;

    for (int i = herotx; i <= herotex + heroSize[0]; ++i) {
        for (int o = heroty; o <= herotey + heroSize[1]; ++o) {
            if (currentSpecials[i + o * currentMapSize[0]] & 1) {
                *herox = lastherox;
                *heroy = lastheroy;
            }
            if (currentSpecials[i + o * currentMapSize[0]] & 2) {
                *herox = 0;
                *heroy = 0;
            }
        }
    }

    if (*herox <= 120 - heroSize[0] * 4) {
        screenx = 0;
        OAM[0].attr1 = ATTR1_SIZE_16 | OBJ_X(*herox);
    } else if (*herox >= currentMapSize[0] * 8 - 120 - heroSize[0] * 4) {
        screenx = currentMapSize[0] * 8 - 240;
        OAM[0].attr1 = ATTR1_SIZE_16 | OBJ_X(*herox - (currentMapSize[0] * 8 - 120 - heroSize[0] * 4) + 120 - heroSize[0] * 4);
    } else {
        screenx = *herox - (120 - heroSize[0] * 4);
    }
    if (*heroy <= 80 - heroSize[1] * 4) {
        screeny = 0;
        OAM[0].attr0 = OBJ_Y(*heroy) | OBJ_256_COLOR;
    } else if (*heroy >= currentMapSize[1] * 8 - 80 - heroSize[1] * 4) {
        screeny = currentMapSize[1] * 8 - 160;
        OAM[0].attr0 = OBJ_Y(*heroy - (currentMapSize[1] * 8 - 80 - heroSize[1] * 4) + 80 - heroSize[1] * 4) | OBJ_256_COLOR;
    } else {
        screeny = *heroy - (80 - heroSize[1] * 4);
    }
    moveScreen(screenx, screeny);
    lastherox = *herox;
    lastheroy = *heroy;
}
