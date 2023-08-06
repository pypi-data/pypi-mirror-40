from xml.dom.minidom import parse
from PIL import Image
from jinja2 import Environment, FileSystemLoader
import os


class GBARPGMaker:
    def __init__(self, config):
        self.config = config

        self.maps = {}
        for map_ in config.maps:
            self.maps[map_] = Map(config.maps[map_])

        self.sprites = {}
        for sprite in config.sprites:
            self.sprites[sprite] = Sprite(config.sprites[sprite])

        self.jinja_env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), "jinja_templates")))

    def parse(self):
        for map_ in self.maps:
            self.maps[map_].parse()
        for sprite in self.sprites:
            self.sprites[sprite].parse()

    def write_image_data(self, output_folder):
        context = {
            "maps": self.maps,
            "sprites": self.sprites
            }

        renderedc = self.jinja_env.get_template("imageData.c").render(context)
        renderedh = self.jinja_env.get_template("imageData.h").render(context)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(output_folder + "/imageData.c", 'w') as f:
            f.write(renderedc)

        with open(output_folder + "/imageData.h", 'w') as f:
            f.write(renderedh)

    def write_main(self, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        context = {
            "maps": self.maps,
            "sprites": self.sprites
            }

        rendered = self.jinja_env.get_template("main.c").render(context)

        with open(output_folder + "/main.c", 'w') as f:
            f.write(rendered)

    def write_graphics(self, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        context = {
            "maps": self.maps,
            "sprites": self.sprites
            }

        renderedc = self.jinja_env.get_template("graphics.c").render(context)
        renderedh = self.jinja_env.get_template("graphics.h").render(context)

        with open(output_folder + "/graphics.c", 'w') as f:
            f.write(renderedc)

        with open(output_folder + "/graphics.h", 'w') as f:
            f.write(renderedh)

    def make_game(self):
        self.parse()
        self.write_image_data("./source")
        self.write_main("./source")
        self.write_graphics("./source")


class Sprite:
    def __init__(self, sprite_config):
        self.image_path = sprite_config["image_path"]
        self.tiles = []
        self.size = []
        self.colors = []
        self.palette = []
        self.tileset = []

    def parse(self):
        self.parse_image()
        self.generate_for_gba()

    def generate_for_gba(self):
        for color in self.colors:
            self.palette.append(0)
            for i, part in enumerate(color):
                self.palette[-1] += int(part * (31 / 255)) << (i * 5)

        for tile in self.tiles:
            for i in range(0, 64, 4):
                word = 0
                for o, val in enumerate(tile[i:i+4]):
                    word += val << 8 * o
                self.tileset.append(word)

    def parse_image(self):
        image = Image.open(self.image_path).convert("RGBA")
        image = image.convert("P", palette=Image.ADAPTIVE)
        image_palette = image.getpalette()
        color_legend = {}
        self.size = [int(image.size[0] / 8), int(image.size[1] / 8)]
        for i in range(0, len(image_palette), 3):
            next_color = image_palette[i:i + 3]
            if next_color in self.colors:
                color_legend[int(i / 3)] = self.colors.index(next_color)
                continue
            self.colors.append(next_color)
            color_legend[int(i / 3)] = len(self.colors) - 1
        for yi in range(0, image.size[1], 8):
            for xi in range(0, image.size[0], 8):
                tile = []
                for pixel_index, pixel in enumerate(list(image.crop((xi, yi, xi + 8, yi + 8)).getdata())):
                    tile.append(color_legend[pixel])
                self.tiles.append(tile)

    def print_tiles(self):
        for o in range(len(self.tiles)):
            for i in range(0, 64, 8):
                print(self.tiles[o][i:i+8])
            print("-"*(8*3))


class Map:
    def __init__(self, map_config):
        self.tmx_path = map_config["tmx_path"]
        self.bottom_layer_name = map_config["bottom_layer_name"]
        self.middle_layer_name = map_config["middle_layer_name"]
        self.top_layer_name = map_config["top_layer_name"]
        try:
            self.special_layer_name = map_config["special_layer_name"]
        except KeyError:
            self.special_layer_name = None

        self.tiles = [[0 for i in range(64)]]
        self.colors = [[0, 0, 0]]
        self.size = []

        self.specials_count = 0
        self.specials = []

        self.layer_tile_maps = []
        self.layer_names = []
        self.layer_sizes = []
        self.tile_legend = {0: 0}

        self.palette = []
        self.tileset = []

    def parse(self):
        self.parse_tilemap()
        self.size.append(max([i[0] for i in self.layer_sizes]))
        self.size.append(max([i[1] for i in self.layer_sizes]))
        self.generate_for_gba()
        for i in range(self.size[0] * self.size[1]):
            self.specials.append(0)
        self.parse_walls(self.middle_layer_name)
        self.parse_specials(self.special_layer_name)

    def generate_for_gba(self):
        for color in self.colors:
            self.palette.append(0)
            for i, part in enumerate(color):
                self.palette[-1] += int(part * (31 / 255)) << (i * 5)

        for tile in self.tiles:
            for i in range(0, 64, 4):
                word = 0
                for o, val in enumerate(tile[i:i+4]):
                    word += val << 8 * o
                self.tileset.append(word)

    def parse_tilemap(self):
        tmx_file_element = parse(self.tmx_path).documentElement
        for tileset_index, tileset_element in enumerate(tmx_file_element.getElementsByTagName("tileset")):
            first_tile_index = int(tileset_element.getAttribute("firstgid"))
            tsx_path = os.path.normpath(os.path.dirname(self.tmx_path) + "/" + tileset_element.getAttribute("source"))
            self.parse_tileset(tsx_path, first_tile_index)

        for layer_index, layer_element in enumerate(tmx_file_element.getElementsByTagName("layer")):
            if layer_element.getAttribute("name") not in [self.bottom_layer_name, self.middle_layer_name, self.top_layer_name]:
                continue
            self.layer_names.append(layer_element.getAttribute("name").replace(" ", "_"))
            self.layer_sizes.append([
                int(layer_element.getAttribute("width")),
                int(layer_element.getAttribute("height"))
                ])
            self.layer_tile_maps.append([])
            data = layer_element.getElementsByTagName("data")[0].firstChild.data.replace('\n', '').split(',')
            for map_entry in data:
                try:
                    self.layer_tile_maps[-1].append(self.tile_legend[int(map_entry)])
                except KeyError:
                    print("problem")
                    self.layer_tile_maps[-1].append(0)

    def parse_tileset(self, tsx_path, first_tile_index):
        tile_index = first_tile_index
        tileset_file_element = parse(tsx_path).documentElement
        try:
            properties = tileset_file_element.getElementsByTagName("properties")[0].getElementsByTagName("property")
            for property_ in properties:
                if (property_.getAttribute("name") == "DontParse" and property_.getAttribute("value") == 'true'):
                    return
                if (property_.getAttribute("name") == "SpecialTileset" and property_.getAttribute("value") == 'true'):
                    return
        except IndexError:
            print("properties were not found")
        for image_element in tileset_file_element.getElementsByTagName("image"):
            image_path = os.path.normpath(os.path.dirname(tsx_path) + "/" + image_element.getAttribute("source"))
            image = Image.open(image_path).convert("RGBA")
            image = image.convert("P", palette=Image.ADAPTIVE)
            image_palette = image.getpalette()
            color_legend = {}
            for i in range(0, len(image_palette), 3):
                next_color = image_palette[i:i + 3]
                if next_color in self.colors:
                    color_legend[int(i / 3)] = self.colors.index(next_color)
                    continue
                self.colors.append(next_color)
                color_legend[int(i / 3)] = len(self.colors) - 1
            for yi in range(0, image.size[1], 8):
                for xi in range(0, image.size[0], 8):
                    tile = []
                    for pixel in list(image.crop((xi, yi, xi + 8, yi + 8)).getdata()):
                        tile.append(color_legend[pixel])
                    self.tile_legend[tile_index] = len(self.tiles)
                    self.tile_legend[tile_index | 2147483648] = len(self.tiles) | 1024
                    self.tile_legend[tile_index | 1073741824] = len(self.tiles) | 2048
                    self.tile_legend[tile_index | 3221225472] = len(self.tiles) | 3072
                    self.tiles.append(tile)
                    tile_index += 1

    def parse_specials(self, layer_name):
        tmx_file_element = parse(self.tmx_path).documentElement
        known_specials = {"0": 0}
        for layer_element in tmx_file_element.getElementsByTagName("layer"):
            if layer_element.getAttribute("name") != layer_name:
                continue
            special_layer_size = [int(layer_element.getAttribute("width")), int(layer_element.getAttribute("height"))]
            data = layer_element.getElementsByTagName("data")[0].firstChild.data.replace('\n', '').split(',')
            for map_entry_index, map_entry in enumerate(data):
                try:
                    self.specials[self.size[0] * int(map_entry_index / special_layer_size[0]) + map_entry_index % special_layer_size[0]] += known_specials[map_entry]
                except KeyError:
                    known_specials[map_entry] = 1 << (self.specials_count + 1)
                    self.specials_count += 1
                    self.specials[self.size[0] * int(map_entry_index / special_layer_size[0]) + map_entry_index % special_layer_size[0]] += known_specials[map_entry]

    def parse_walls(self, layer_name):
        layer_index = self.layer_names.index(layer_name)
        for i, t in enumerate(self.layer_tile_maps[layer_index]):
            if t == 0:
                pass
            else:
                self.specials[self.size[0] * int(i / self.layer_sizes[layer_index][0]) + i % self.layer_sizes[layer_index][0]] += 1

    def print_tiles(self):
        for o in range(len(self.tiles)):
            for i in range(0, 64, 8):
                print(self.tiles[o][i:i+8])
            print("-"*(8*3))
