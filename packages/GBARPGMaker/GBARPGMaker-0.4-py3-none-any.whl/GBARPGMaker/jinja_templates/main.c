#include <gba.h>
#include <stdio.h>
#include <stdlib.h>

#include "imageData.h"
#include "graphics.h"

int main(void) {
    irqInit();
    irqEnable(IRQ_VBLANK);
    SetMode(BG0_ON | BG1_ON | BG2_ON | OBJ_ENABLE | OBJ_1D_MAP);

    REG_BG0CNT = TILE_BASE(0) | MAP_BASE(24) | BG_SIZE_1 | BG_256_COLOR | BG_PRIORITY(3);
    REG_BG1CNT = TILE_BASE(0) | MAP_BASE(25) | BG_SIZE_1 | BG_256_COLOR | BG_PRIORITY(1);
    REG_BG2CNT = TILE_BASE(0) | MAP_BASE(26) | BG_SIZE_1 | BG_256_COLOR | BG_PRIORITY(0);

    // Don't show any sprites except for the first one
    for (int i = 1; i < 128; ++i) {
        OAM[i].attr0 = OBJ_DISABLE | OBJ_256_COLOR;
    }

    loadSpritehero();
    loadSpritehero();
    loadSpritehero();
    loadSpritehero();

    loadMapmap1();

    OAM[0].attr0 = OBJ_Y(0) | OBJ_256_COLOR;
    OAM[0].attr1 = ATTR1_SIZE_32 | OBJ_X(0);
    OAM[0].attr2 = OBJ_PRIORITY(2);

    moveScreen(9, 9);
    moveScreen(0, 0);

    int herox = 0;
    int heroy = 0;

    int herospeed = 1;

    while (true) {
        VBlankIntrWait();
        scanKeys();
        int kd = keysDown();
        if (keysHeld() & KEY_RIGHT) {
            herox += herospeed;
            moveHero(&herox, &heroy);
        }
        if (keysHeld() & KEY_LEFT) {
            herox -= herospeed;
            moveHero(&herox, &heroy);
        }
        if (keysHeld() & KEY_UP) {
            heroy -= herospeed;
            moveHero(&herox, &heroy);
        }
        if (keysHeld() & KEY_DOWN) {
            heroy += herospeed;
            moveHero(&herox, &heroy);
        }
        if (kd & KEY_A) {
            herox = 0;
            heroy = 0;
            forceMoveScreen(0, 0);
            moveHero(&herox, &heroy);
        }
        if (kd & KEY_B) {
            herox = 0;
            heroy = 0;
            loadMapmap1();
            forceMoveScreen(0, 0);
            moveHero(&herox, &heroy);
        }
    }
}
