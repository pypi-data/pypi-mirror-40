#include <gba.h>
#include <stdio.h>
#include <stdlib.h>

#include "out.h"

int heroSize[2] = { 16, 16 };

int walls[5][2] = {
    {5, 5},
    {6, 5},
    {7, 5},
    {8, 5},
    {9, 5},
};

void moveMap(int* mapx, int* mapy) {
    static int lastmaptx;
    static int lastmapty;
    static int lastmapx;
    static int lastmapy;

    int maptx = (*mapx) / 8;
    int mapty = (*mapy) / 8;

    // Check for walls
    for (int i = 0; i < 5; ++i) {
        if (maptx == walls[i][0] && mapty == walls[i][1]) {
            *mapx = lastmapx;
            *mapy = lastmapy;
            return;
        }
    }

    // Check for map boundries
    if (*mapx < 0) {
        *mapx = 0;
        maptx = 0;
    } else if (*mapy < 0) {
        *mapy = 0;
        mapty = 0;
    } else if (*mapx > (FloorSize[0] - 30) * 8) {
        *mapx = (FloorSize[0] - 30) * 8;
        maptx = (*mapx) / 8;
    } else if (*mapy > (FloorSize[1] - 20) * 8) {
        *mapy = (FloorSize[1] - 20) * 8;
        mapty = (*mapy) / 8;
    }

    // Update MAP_BASe if necessary
    if (maptx != lastmaptx || mapty != lastmapty) {
        for (int i = 0; i < 22; ++i) {
            dmaCopy(Floor + (i + mapty - 1) * FloorSize[0] + maptx - 1, MAP_BASE_ADR(24) + 32 * 2 * i, 32 * 2);
        }
    }

    // Update display offsets
    REG_BG0HOFS = (*mapx) % 8 + 8;
    REG_BG0VOFS = (*mapy) % 8 + 8;

    lastmaptx = maptx;
    lastmapty = mapty;
    lastmapx = *mapx;
    lastmapy = *mapy;
}

// low level function that does no checks but just "efficiently" moves the screen
void moveScreen(int screenx, int screeny) {
    static int lastscreentx;
    static int lastscreenty;

    int screentx = (screenx) / 8;
    int screenty = (screeny) / 8;

    if (screentx != lastscreentx || screenty != lastscreenty) {
        for (int i = 0; i < 22; ++i) {
            dmaCopy(Floor + (i + screenty - 1) * FloorSize[0] + screentx - 1, MAP_BASE_ADR(24) + 32 * 2 * i, 32 * 2);
        }
    }

    // Update display offsets
    REG_BG0HOFS = screenx % 8 + 8;
    REG_BG0VOFS = screeny % 8 + 8;

    lastscreentx = screentx;
    lastscreenty = screenty;
}

void moveHero(int* herox, int* heroy, int* mapx, int* mapy) {
    if (*herox < 0) {
        *herox = 0;
    } else if (*herox > FloorSize[0] * 8 - heroSize[0]) {
        *herox = FloorSize[0] * 8 - heroSize[0];
    }
    if (*heroy < 0) {
        *heroy = 0;
    } else if (*heroy > FloorSize[1] * 8 - heroSize[1]) {
        *heroy = FloorSize[1] * 8 - heroSize[1];
    }

    if (*herox < 120 - heroSize[0] / 2) {
        *mapx = 0;
        OAM[0].attr1 = ATTR1_SIZE_16 | OBJ_X(*herox);
    } else if (*herox > FloorSize[0] * 8 - 120 - heroSize[0] / 2) {
        *mapx = FloorSize[0] * 8 - 240;
        OAM[0].attr1 = ATTR1_SIZE_16 | OBJ_X(*herox - (FloorSize[0] * 8 - 120 - heroSize[0] / 2) + 120 - heroSize[0] / 2);
    } else {
        *mapx = *herox - (120 - heroSize[0] / 2);
    }
    if (*heroy < 80 - heroSize[1] / 2) {
        *mapy = 0;
        OAM[0].attr0 = OBJ_Y(*heroy) | OBJ_256_COLOR;
    } else if (*heroy > FloorSize[1] * 8 - 80 - heroSize[1] / 2) {
        *mapy = FloorSize[1] * 8 - 160;
        OAM[0].attr0 = OBJ_Y(*heroy - (FloorSize[1] * 8 - 80 - heroSize[1] / 2) + 80 - heroSize[1] / 2) | OBJ_256_COLOR;
    } else {
        *mapy = *heroy - (80 - heroSize[1] / 2);
    }
    moveScreen(*mapx, *mapy);
}

int main(void) {
    irqInit();
    irqEnable(IRQ_VBLANK);
    SetMode(BG0_ON | OBJ_ENABLE | OBJ_1D_MAP);

    REG_BG0CNT = TILE_BASE(0) | MAP_BASE(24) | BG_PRIORITY(3) | BG_SIZE_1 | BG_256_COLOR | BG_PRIORITY(3);

    // Don't show any sprites except for the first one
    for (int i = 1; i < 128; ++i) {
        OAM[i].attr0 = OBJ_DISABLE | OBJ_256_COLOR;
    }

    // Load sprite stuff into memory
    dmaCopy(heroPalette, SPRITE_PALETTE, heroPaletteLen);
    dmaCopy(heroTileset, OBJ_BASE_ADR, heroTilesetLen);

    // Load BG stuff into memory
    dmaCopy(BGTileset, TILE_BASE_ADR(0), BGTilesetLen);
    dmaCopy(BGPalette, BG_PALETTE, BGPaletteLen);

    int mapx = 0;
    int mapy = 0;

    int herox = 0;
    int heroy = 0;

    int herospeed = 5;

    OAM[0].attr0 = OBJ_Y(0) | OBJ_256_COLOR;
    OAM[0].attr1 = ATTR1_SIZE_16 | OBJ_X(0);


    while (true) {
        VBlankIntrWait();
        scanKeys();
        if (keysHeld() & KEY_RIGHT) {
            herox += herospeed;
            moveHero(&herox, &heroy, &mapx, &mapy);
        }
        if (keysHeld() & KEY_LEFT) {
            herox -= herospeed;
            moveHero(&herox, &heroy, &mapx, &mapy);
        }
        if (keysHeld() & KEY_UP) {
            heroy -= herospeed;
            moveHero(&herox, &heroy, &mapx, &mapy);
        }
        if (keysHeld() & KEY_DOWN) {
            heroy += herospeed;
            moveHero(&herox, &heroy, &mapx, &mapy);
        }
        if (keysDown() & KEY_A) {
            herox = 0;
            heroy = 0;
            moveHero(&herox, &heroy, &mapx, &mapy);
        }
    }
}
