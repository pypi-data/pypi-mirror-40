from xml.dom.minidom import parse
from PIL import Image
from jinja2 import Environment, FileSystemLoader
import os


class GBARPGMaker:
    def __init__(self, tilemap_path, hero_image_path):
        self.tilemap_path = tilemap_path
        self.hero_image_path = hero_image_path

        # list of colors in RGB format - RGB lists of 3 values from 0 to 255
        self.BGcolors = []
        # list of tiles, each tile is a 2D list (8x8) of color indices
        self.BGtiles = []
        # list of maps, there is a map for each layer, a map is a list of screenblock entries
        self.BGtile_maps = []
        self.BGtile_map_names = []
        self.BGtile_map_sizes = []
        # a dict mapping tilemap values to screenblock entries
        self.BGtile_legend = {}

        # each list contains data for each sprite - first sprite its colors in the first element of OBJcolors and its tiles in the firs element of OBJtiles
        self.OBJcolors = []
        self.OBJtiles = []
        self.OBJnames = []
        self.OBJsizes = []

    def parse_tilemap(self):
        map_file_element = parse(self.tilemap_path).documentElement
        for tileset_element in map_file_element.getElementsByTagName("tileset"):
            first_tile_index = int(tileset_element.getAttribute("firstgid"))
            tileset_path = os.path.normpath(os.path.dirname(self.tilemap_path) + "/" + tileset_element.getAttribute("source"))
            self.parse_tileset(tileset_path, first_tile_index)

        for layer_index, layer_element in enumerate(map_file_element.getElementsByTagName("layer")):
            self.BGtile_map_names.append(layer_element.getAttribute("name").replace(" ", "_"))
            self.BGtile_map_sizes.append([
                int(layer_element.getAttribute("width")),
                int(layer_element.getAttribute("height"))
                ])
            self.BGtile_maps.append([])
            data = layer_element.getElementsByTagName("data")[0].firstChild.data.replace('\n', '').split(',')
            for map_entry in data:
                try:
                    self.BGtile_maps[layer_index].append(self.BGtile_legend[int(map_entry)])
                except KeyError:
                    self.BGtile_maps[layer_index].append(0)

    def parse_tileset(self, tileset_path, first_tile_index):
        tile_index = first_tile_index
        tileset_file_element = parse(tileset_path).documentElement
        for image_element in tileset_file_element.getElementsByTagName("image"):
            image_path = os.path.normpath(os.path.dirname(tileset_path) + "/" + image_element.getAttribute("source"))
            image = Image.open(image_path).convert("RGBA")
            image = image.convert("P", palette=Image.ADAPTIVE)
            image_palette = image.getpalette()
            color_legend = {}
            for i in range(0, len(image_palette), 3):
                next_color = image_palette[i:i + 3]
                if next_color in self.BGcolors:
                    color_legend[int(i / 3)] = self.BGcolors.index(next_color)
                    continue
                self.BGcolors.append(next_color)
                color_legend[int(i / 3)] = len(self.BGcolors) - 1
            for yi in range(0, image.size[1], 8):
                for xi in range(0, image.size[0], 8):
                    tile = []
                    for pixel in list(image.crop((xi, yi, xi + 8, yi + 8)).getdata()):
                        tile.append(color_legend[pixel])
                    self.BGtile_legend[tile_index] = len(self.BGtiles)
                    self.BGtile_legend[tile_index | 2147483648] = len(self.BGtiles) | 1024
                    self.BGtile_legend[tile_index | 1073741824] = len(self.BGtiles) | 2048
                    self.BGtile_legend[tile_index | 3221225472] = len(self.BGtiles) | 3072
                    self.BGtiles.append(tile)
                    tile_index += 1

    def parse_OBJ_image(self, OBJ_image_path, tile_map_name):
        image = Image.open(OBJ_image_path).convert("RGBA")
        image = image.convert("P", palette=Image.ADAPTIVE)
        image_palette = image.getpalette()
        color_legend = {}
        self.OBJcolors.append([])
        self.OBJtiles.append([])
        self.OBJnames.append(tile_map_name)
        self.OBJsizes.append([int(image.size[0] / 8), int(image.size[1] / 8)])
        for i in range(0, len(image_palette), 3):
            next_color = image_palette[i:i + 3]
            if next_color in self.OBJcolors[-1]:
                color_legend[int(i / 3)] = self.OBJcolors[-1].index(next_color)
                continue
            self.OBJcolors[-1].append(next_color)
            color_legend[int(i / 3)] = len(self.OBJcolors[-1]) - 1
        for yi in range(0, image.size[1], 8):
            for xi in range(0, image.size[0], 8):
                tile = []
                for pixel_index, pixel in enumerate(list(image.crop((xi, yi, xi + 8, yi + 8)).getdata())):
                    tile.append(color_legend[pixel])
                self.OBJtiles[-1].append(tile)

    def write_image_data(self, output_path):
        # list of colors in GBA native format (BGR 5bit depth)
        BGpalette = []
        # tileset in GBA native format
        BGtileset = []

        for color in self.BGcolors:
            BGpalette.append(0)
            for i, part in enumerate(color):
                BGpalette[-1] += int(part * (31 / 255)) << (i * 5)

        for tile in self.BGtiles:
            for i in range(0, 64, 4):
                word = 0
                for o, val in enumerate(tile[i:i+4]):
                    word += val << 8 * o
                BGtileset.append(word)

        OBJpalettes = []
        OBJtilesets = []

        for i in range(len(self.OBJcolors)):
            OBJpalettes.append([])
            for color in self.OBJcolors[i]:
                OBJpalettes[-1].append(0)
                for i, part in enumerate(color):
                    OBJpalettes[-1][-1] += int(part * (31 / 255)) << (i * 5)

        for i in range(len(self.OBJtiles)):
            OBJtilesets.append([])
            for tile in self.OBJtiles[i]:
                for i in range(0, 64, 4):
                    word = 0
                    for o, val in enumerate(tile[i:i+4]):
                        word += val << 8 * o
                    OBJtilesets[-1].append(word)

        jinja_env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), "jinja_templates")))

        context = {
            "BGpalette": BGpalette,
            "BGtileset": BGtileset,
            "BGtile_maps": self.BGtile_maps,
            "BGtile_map_names": self.BGtile_map_names,
            "BGtile_map_sizes": self.BGtile_map_sizes,
            "OBJpalettes": OBJpalettes,
            "OBJtilesets": OBJtilesets,
            "OBJnames": self.OBJnames,
            "OBJsizes": self.OBJsizes
            }

        renderedc = jinja_env.get_template("imageData.c").render(context)
        renderedh = jinja_env.get_template("imageData.h").render(context)

        with open(output_path + ".c", 'w') as f:
            f.write(renderedc)

        with open(output_path + ".h", 'w') as f:
            f.write(renderedh)

    def write_main(self):
        pass

    def make_game(self):
        self.parse_tilemap()
        self.parse_OBJ_image(self.hero_image_path, "hero")
        self.write_image_data("./source/imageData")

    def print_BGtiles(self):
        for o in range(len(self.BGtiles)):
            for i in range(0, 64, 8):
                print(self.BGtiles[o][i:i+8])
            print("-"*(8*3))

    def print_OBJtiles(self):
        for BGtile in self.BGtiles:
            for o in range(len(BGtile)):
                for i in range(0, 64, 8):
                    print(BGtile[o][i:i+8])
                print("-"*(8*3))
