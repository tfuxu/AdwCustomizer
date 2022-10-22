# preset.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022 Gradience Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import random
import semver
import json
import os

from gradience.settings_schema import settings_schema
from gradience.utils.utils import buglog, to_slug_case
from gradience.utils.css import parse_css
from gradience.utils.exceptions import GradienceMonetUnsupportedBackgroundError, GradienceError

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from material_color_utilities_python import (
    redFromArgb,
    greenFromArgb,
    blueFromArgb,
    alphaFromArgb,
    themeFromImage,
    Image,
)


def rgba_from_argb(argb, alpha=None) -> str:
    base = "rgba({}, {}, {}, {})"

    red = redFromArgb(argb)
    green = greenFromArgb(argb)
    blue = blueFromArgb(argb)
    if not alpha:
        alpha = alphaFromArgb(argb)

    return base.format(red, green, blue, alpha)


presets_dir = os.path.join(
    os.environ.get("XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"),
    "presets",
)

AMAZING_NAMES = [
    "Amazing",
    "Wonderful",
    "My Preset",
    "Splendide",
    "Magnifique",
    "Cool",
    "Superbe",
    "Awesome",
]


class BasePreset:
    variables = {}
    palette = {}
    custom_css = {
        "gtk4": "",
        "gtk3": "",
    }

    def __init__(self, css=None, preset=None, preset_path=None):
        if css:
            self.load_preset_from_css(css)
        elif preset:
            self.load_preset_from_json(preset)
        elif preset_path:
            self.load_preset_from_path(preset_path)
        else:
            self.no_preset()

    def no_preset(self):
        self.variables = {
            "accent_color": "rgb(220,138,221)",
            "accent_bg_color": "rgb(145,65,172)",
            "accent_fg_color": "#ffffff",
            "destructive_color": "#ff7b63",
            "destructive_bg_color": "#c01c28",
            "destructive_fg_color": "#ffffff",
            "success_color": "#8ff0a4",
            "success_bg_color": "#26a269",
            "success_fg_color": "#ffffff",
            "warning_color": "#f8e45c",
            "warning_bg_color": "#cd9309",
            "warning_fg_color": "rgba(0, 0, 0, 0.8)",
            "error_color": "#ff7b63",
            "error_bg_color": "#c01c28",
            "error_fg_color": "#ffffff",
            "window_bg_color": "rgb(36,31,49)",
            "window_fg_color": "rgb(255,255,255)",
            "view_bg_color": "rgb(36,31,49)",
            "view_fg_color": "#ffffff",
            "headerbar_bg_color": "rgb(36,31,49)",
            "headerbar_fg_color": "#ffffff",
            "headerbar_border_color": "rgba(0,0,0,0)",
            "headerbar_backdrop_color": "@window_bg_color",
            "headerbar_shade_color": "rgba(0,0,0,0.25)",
            "card_bg_color": "rgba(255,255,255,0.08)",
            "card_fg_color": "#ffffff",
            "card_shade_color": "rgba(0,0,0,0.25)",
            "dialog_bg_color": "rgb(36,31,49)",
            "dialog_fg_color": "#ffffff",
            "popover_bg_color": "rgb(36,31,49)",
            "popover_fg_color": "#ffffff",
            "shade_color": "rgba(0,0,0,0.36)",
            "scrollbar_outline_color": "rgb(0,0,0)",
        }
        self.palette = {
            "blue_": {
                "1": "#99c1f1",
                "2": "#62a0ea",
                "3": "#3584e4",
                "4": "#1c71d8",
                "5": "#1a5fb4",
            },
            "green_": {
                "1": "#8ff0a4",
                "2": "#57e389",
                "3": "#33d17a",
                "4": "#2ec27e",
                "5": "#26a269",
            },
            "yellow_": {
                "1": "#f9f06b",
                "2": "#f8e45c",
                "3": "#f6d32d",
                "4": "#f5c211",
                "5": "#e5a50a",
            },
            "orange_": {
                "1": "#ffbe6f",
                "2": "#ffa348",
                "3": "#ff7800",
                "4": "#e66100",
                "5": "#c64600",
            },
            "red_": {
                "1": "#f66151",
                "2": "#ed333b",
                "3": "#e01b24",
                "4": "#c01c28",
                "5": "#a51d2d",
            },
            "purple_": {
                "1": "#dc8add",
                "2": "#c061cb",
                "3": "#9141ac",
                "4": "#813d9c",
                "5": "#613583",
            },
            "brown_": {
                "1": "#cdab8f",
                "2": "#b5835a",
                "3": "#986a44",
                "4": "#865e3c",
                "5": "#63452c",
            },
            "light_": {
                "1": "#ffffff",
                "2": "#f6f5f4",
                "3": "#deddda",
                "4": "#c0bfbc",
                "5": "#9a9996",
            },
            "dark_": {
                "1": "#77767b",
                "2": "#5e5c64",
                "3": "#3d3846",
                "4": "#241f31",
                "5": "#000000",
            },
        }

    def load_preset_from_path(self, preset_path):
        with open(preset_path, "r", encoding="utf-8") as file:
            self.load_preset_from_json(json.loads(file.read()))

    def load_preset_from_json(self, preset):
        self.variables = preset["variables"]
        self.palette = preset["palette"]
        if "custom_css" in preset:
            self.custom_css = preset["custom_css"]

    def load_preset_from_css(self, css):
        self.variables, self.palette, self.custom_css = load_preset_from_css(css)

    def to_json(self):
        return {
            "variables": self.variables,
            "palette": self.palette,
            "custom_css": self.custom_css,
        }

    def to_css(self, app_type):
        final_css = ""
        for key in self.variables.keys():
            final_css += f"@define-color {key} {self.variables[key]};\n"
        for prefix_key in self.palette.keys():
            for key in self.palette[prefix_key].keys():
                final_css += f"@define-color {prefix_key + key} {self.palette[prefix_key][key]};\n"
        final_css += self.custom_css.get(app_type, "")
        return final_css


class DarkPreset(BasePreset):
    def no_preset(self):

        self.variables = {
            "accent_color": "#78aeed",
            "accent_bg_color": "#3584e4",
            "accent_fg_color": "#ffffff",
            "destructive_color": "#ff7b63",
            "destructive_bg_color": "#c01c28",
            "destructive_fg_color": "#ffffff",
            "success_color": "#8ff0a4",
            "success_bg_color": "#26a269",
            "success_fg_color": "#ffffff",
            "warning_color": "#f8e45c",
            "warning_bg_color": "#cd9309",
            "warning_fg_color": "rgba(0, 0, 0, 0.8)",
            "error_color": "#ff7b63",
            "error_bg_color": "#c01c28",
            "error_fg_color": "#ffffff",
            "window_bg_color": "#242424",
            "window_fg_color": "#ffffff",
            "view_bg_color": "#1e1e1e",
            "view_fg_color": "#ffffff",
            "headerbar_bg_color": "#303030",
            "headerbar_fg_color": "#ffffff",
            "headerbar_border_color": "#ffffff",
            "headerbar_backdrop_color": "@window_bg_color",
            "headerbar_shade_color": "rgba(0, 0, 0, 0.36)",
            "card_bg_color": "rgba(255, 255, 255, 0.08)",
            "card_fg_color": "#ffffff",
            "card_shade_color": "rgba(0, 0, 0, 0.36)",
            "dialog_bg_color": "#383838",
            "dialog_fg_color": "#ffffff",
            "popover_bg_color": "#383838",
            "popover_fg_color": "#ffffff",
            "shade_color": "rgba(0,0,0,0.36)",
            "scrollbar_outline_color": "rgba(0,0,0,0.5)",
        }


class LightPreset(BasePreset):
    def no_preset(self):
        self.variables = {
            "accent_color": "#1c71d8",
            "accent_bg_color": "#3584e4",
            "accent_fg_color": "#ffffff",
            "destructive_color": "#c01c28",
            "destructive_bg_color": "#e01b24",
            "destructive_fg_color": "#ffffff",
            "success_color": "#26a269",
            "success_bg_color": "#2ec27e",
            "success_fg_color": "#ffffff",
            "warning_color": "#ae7b03",
            "warning_bg_color": "#e5a50a",
            "warning_fg_color": "rgba(0, 0, 0, 0.8)",
            "error_color": "#c01c28",
            "error_bg_color": "#e01b24",
            "error_fg_color": "#ffffff",
            "window_bg_color": "#fafafa",
            "window_fg_color": "rgba(0, 0, 0, 0.8)",
            "view_bg_color": "#ffffff",
            "view_fg_color": "#000000",
            "headerbar_bg_color": "#ebebeb",
            "headerbar_fg_color": "rgba(0, 0, 0, 0.8)",
            "headerbar_border_color": "rgba(0, 0, 0, 0.8)",
            "headerbar_backdrop_color": "@window_bg_color",
            "headerbar_shade_color": "rgba(0, 0, 0, 0.07)",
            "card_bg_color": "#ffffff",
            "card_fg_color": "rgba(0, 0, 0, 0.8)",
            "card_shade_color": "rgba(0, 0, 0, 0.07)",
            "dialog_bg_color": "#fafafa",
            "dialog_fg_color": "rgba(0, 0, 0, 0.8)",
            "popover_bg_color": "#ffffff",
            "popover_fg_color": "rgba(0, 0, 0, 0.8)",
            "shade_color": "rgba(0,0,0,0.07)",
            "scrollbar_outline_color": "rgb(255,255,255)",
        }


class PrettyPurple(BasePreset):
    def no_preset(self):
        self.variables = {
            "accent_color": "rgb(220,138,221)",
            "accent_bg_color": "rgb(145,65,172)",
            "accent_fg_color": "#ffffff",
            "destructive_color": "#ff7b63",
            "destructive_bg_color": "#c01c28",
            "destructive_fg_color": "#ffffff",
            "success_color": "#8ff0a4",
            "success_bg_color": "#26a269",
            "success_fg_color": "#ffffff",
            "warning_color": "#f8e45c",
            "warning_bg_color": "#cd9309",
            "warning_fg_color": "rgba(0, 0, 0, 0.8)",
            "error_color": "#ff7b63",
            "error_bg_color": "#c01c28",
            "error_fg_color": "#ffffff",
            "window_bg_color": "rgb(36,31,49)",
            "window_fg_color": "rgb(255,255,255)",
            "view_bg_color": "rgb(36,31,49)",
            "view_fg_color": "#ffffff",
            "headerbar_bg_color": "rgb(36,31,49)",
            "headerbar_fg_color": "#ffffff",
            "headerbar_border_color": "rgba(0,0,0,0)",
            "headerbar_backdrop_color": "@window_bg_color",
            "headerbar_shade_color": "rgba(0,0,0,0.25)",
            "card_bg_color": "rgba(255,255,255,0.08)",
            "card_fg_color": "#ffffff",
            "card_shade_color": "rgba(0,0,0,0.25)",
            "dialog_bg_color": "rgb(36,31,49)",
            "dialog_fg_color": "#ffffff",
            "popover_bg_color": "rgb(36,31,49)",
            "popover_fg_color": "#ffffff",
            "shade_color": "rgba(0,0,0,0.36)",
            "scrollbar_outline_color": "rgb(0,0,0)",
        }


class Preset:
    description = ""
    plugins = {}
    badges = {}
    repo = ""
    filename = ""
    name = ""
    default = "light"

    def __init__(
        self,
        name=None,
        repo="user",
        version=semver.parse_version_info("0.1.0"),
        dark=None,
        dark_css=None,
        light=None,
        light_css=None,
        preset_path=None,
        default="light",
        url=None,
    ):
        self.version = version
        if preset_path:
            self.load_from_file(preset_path)
        else:

            if dark:
                self.dark = DarkPreset(preset=dark)
            elif dark_css:
                self.dark = DarkPreset(css=dark_css)
            else:
                self.dark = DarkPreset()

            if light:
                self.light = LightPreset(preset=light)
            elif light_css:
                self.light = LightPreset(css=light_css)
            else:
                self.light = LightPreset()

            if name is not None:
                self.name = name
            else:
                self.name = random.choice(AMAZING_NAMES)
            self.filename = to_slug_case(self.name)
            self.repo = repo
            self.default = default
        print(f"Loaded preset {self.name}")
        print(f"Version       {self.version}")
        print(f"Repo          {self.repo}")

        if repo == "curated":
            self.url = f"https://raw.githubusercontent.com/GradienceTeam/Community/next/{self.repo}/{self.filename}.json"
        elif repo == "official":
            self.url = f"https://raw.githubusercontent.com/GradienceTeam/Community/next/{self.repo}/{self.filename}.json"
        else:
            self.url = url

        print(f"URL:          {self.url}")



    def load_dark(self, css=None, preset=None, preset_path=None):
        self.dark = DarkPreset(css, preset, preset_path)

    def load_light(self, css=None, preset=None, preset_path=None):
        self.light = LightPreset(css, preset, preset_path)

    def load_from_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except Exception as exc:
            raise GradienceError(f"Could not load preset from {path}") from exc

        self.repo = path.parent.name
        self.version = semver.parse_version_info(data["version"]) if "version" in data else semver.parse_version_info("0.1.0")
        self.name = data["name"] if "name" in data else random.choice(AMAZING_NAMES)
        self.filename = to_slug_case(self.name)
        self.description = data["description"] if "description" in data else ""
        self.badges = data["badges"] if "badges" in data else {}
        self.default = data["default"] if "default" in data else "light"
        self.dark = DarkPreset(preset=data["dark"]) if "dark" in data else DarkPreset()
        self.light = (
            LightPreset(preset=data["light"]) if "light" in data else LightPreset()
        )

    def update_from_json(self, data):
        self.badges = data["badges"] if "badges" in data else {}
        self.version = semver.parse_version_info(data["version"]) if "version" in data else semver.parse_version_info("0.1.0")
        self.description = data["description"] if "description" in data else ""
        self.default = data["default"] if "default" in data else "light"
        self.dark = DarkPreset(preset=data["dark"]) if "dark" in data else DarkPreset()
        self.light = LightPreset(preset=data["light"]) if "light" in data else LightPreset()
        self.save()
    def __repr__(self):
        return f"Preset({self.name})"

    @property
    def variables(self):
        return self.light.variables if self.default == "light" else self.dark.variables

    @property
    def pallette(self):
        return self.light.palette if self.default == "light" else self.dark.palette

    def __eq__(self, other: object) -> bool:
        return self.name == other.name and self.version == other.version

    def __gt__(self, other: object) -> bool:
        return self.version > other.version

    def __ge__(self, other: object) -> bool:
        return self.version >= other.version

    def __lt__(self, other: object) -> bool:
        return self.version < other.version

    def __le__(self, other: object) -> bool:
        return self.version <= other.version

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __int__(self):
        return int(self.version)

    def to_json(self):
        return {
            "name": self.name,
            "version": str(self.version),
            "description": self.description,
            "plugins": self.plugins,
            "badges": self.badges,
            "dark": self.dark.to_json(),
            "light": self.light.to_json(),
            "default": self.default,
        }

    def save(self, to=None):
        if to is None:
            to = os.path.join(presets_dir, self.repo, self.filename + ".json")
        with open(to, "w", encoding="utf-8") as file:
            file.write(json.dumps(self.to_json(), indent=4))

    @classmethod
    def new_from_background(cls, background, name):
        if str(background).endswith(".svg"):
            drawing = svg2rlg(background)
            background = os.path.join(
                os.environ.get("XDG_RUNTIME_DIR"), "gradience_bg.png"
            )
            renderPM.drawToFile(drawing, background, fmt="PNG")

        if background.endswith(".xml"):
            raise GradienceMonetUnsupportedBackgroundError(
                "Unsupported background type: XML"
            )
        else:
            try:
                monet_img = Image.open(background)
            except Exception as exc:
                raise FileNotFoundError("Background image not found") from exc
            else:
                basewidth = 64
                wpercent = basewidth / float(monet_img.size[0])
                hsize = int((float(monet_img.size[1]) * float(wpercent)))
                monet_img = monet_img.resize(
                    (basewidth, hsize), Image.Resampling.LANCZOS
                )
                theme = themeFromImage(monet_img)

                # palettes = theme["palettes"]

                # palette = {}
                # i = 0
                # for color in palettes.values():
                #     i += 1
                #     palette[str(i)] = hexFromArgb(color.tone(tone))

                # print(palette)
                palette = {
                    "blue_": {
                        "1": "#99c1f1",
                        "2": "#62a0ea",
                        "3": "#3584e4",
                        "4": "#1c71d8",
                        "5": "#1a5fb4",
                    },
                    "green_": {
                        "1": "#8ff0a4",
                        "2": "#57e389",
                        "3": "#33d17a",
                        "4": "#2ec27e",
                        "5": "#26a269",
                    },
                    "yellow_": {
                        "1": "#f9f06b",
                        "2": "#f8e45c",
                        "3": "#f6d32d",
                        "4": "#f5c211",
                        "5": "#e5a50a",
                    },
                    "orange_": {
                        "1": "#ffbe6f",
                        "2": "#ffa348",
                        "3": "#ff7800",
                        "4": "#e66100",
                        "5": "#c64600",
                    },
                    "red_": {
                        "1": "#f66151",
                        "2": "#ed333b",
                        "3": "#e01b24",
                        "4": "#c01c28",
                        "5": "#a51d2d",
                    },
                    "purple_": {
                        "1": "#dc8add",
                        "2": "#c061cb",
                        "3": "#9141ac",
                        "4": "#813d9c",
                        "5": "#613583",
                    },
                    "brown_": {
                        "1": "#cdab8f",
                        "2": "#b5835a",
                        "3": "#986a44",
                        "4": "#865e3c",
                        "5": "#63452c",
                    },
                    "light_": {
                        "1": "#ffffff",
                        "2": "#f6f5f4",
                        "3": "#deddda",
                        "4": "#c0bfbc",
                        "5": "#9a9996",
                    },
                    "dark_": {
                        "1": "#77767b",
                        "2": "#5e5c64",
                        "3": "#3d3846",
                        "4": "#241f31",
                        "5": "#000000",
                    },
                }

                dark_theme = theme["schemes"]["dark"]
                dark_variable = {
                    "accent_color": rgba_from_argb(dark_theme.primary),
                    "accent_bg_color": rgba_from_argb(dark_theme.primaryContainer),
                    "accent_fg_color": rgba_from_argb(dark_theme.onPrimaryContainer),
                    "destructive_color": rgba_from_argb(dark_theme.error),
                    "destructive_bg_color": rgba_from_argb(dark_theme.errorContainer),
                    "destructive_fg_color": rgba_from_argb(dark_theme.onErrorContainer),
                    "success_color": rgba_from_argb(dark_theme.tertiary),
                    "success_bg_color": rgba_from_argb(dark_theme.onTertiary),
                    "success_fg_color": rgba_from_argb(dark_theme.onTertiaryContainer),
                    "warning_color": rgba_from_argb(dark_theme.secondary),
                    "warning_bg_color": rgba_from_argb(dark_theme.onSecondary),
                    "warning_fg_color": rgba_from_argb(dark_theme.primary, "0.8"),
                    "error_color": rgba_from_argb(dark_theme.error),
                    "error_bg_color": rgba_from_argb(dark_theme.errorContainer),
                    "error_fg_color": rgba_from_argb(dark_theme.onError),
                    "window_bg_color": rgba_from_argb(dark_theme.surface),
                    "window_fg_color": rgba_from_argb(dark_theme.onSurface),
                    "view_bg_color": rgba_from_argb(dark_theme.surface),
                    "view_fg_color": rgba_from_argb(dark_theme.onSurface),
                    "headerbar_bg_color": rgba_from_argb(dark_theme.surface),
                    "headerbar_fg_color": rgba_from_argb(dark_theme.onSurface),
                    "headerbar_border_color": rgba_from_argb(dark_theme.primary, "0.8"),
                    "headerbar_backdrop_color": "@headerbar_bg_color",
                    "headerbar_shade_color": rgba_from_argb(dark_theme.shadow),
                    "card_bg_color": rgba_from_argb(dark_theme.primary, "0.05"),
                    "card_fg_color": rgba_from_argb(dark_theme.onSecondaryContainer),
                    "card_shade_color": rgba_from_argb(dark_theme.shadow),
                    "dialog_bg_color": rgba_from_argb(dark_theme.secondaryContainer),
                    "dialog_fg_color": rgba_from_argb(dark_theme.onSecondaryContainer),
                    "popover_bg_color": rgba_from_argb(dark_theme.secondaryContainer),
                    "popover_fg_color": rgba_from_argb(dark_theme.onSecondaryContainer),
                    "shade_color": rgba_from_argb(dark_theme.shadow),
                    "scrollbar_outline_color": rgba_from_argb(dark_theme.outline),
                }
                light_theme = theme["schemes"]["light"]
                light_variable = {
                    "accent_color": rgba_from_argb(light_theme.primary),
                    "accent_bg_color": rgba_from_argb(light_theme.primary),
                    "accent_fg_color": rgba_from_argb(light_theme.onPrimary),
                    "destructive_color": rgba_from_argb(light_theme.error),
                    "destructive_bg_color": rgba_from_argb(light_theme.errorContainer),
                    "destructive_fg_color": rgba_from_argb(
                        light_theme.onErrorContainer
                    ),
                    "success_color": rgba_from_argb(light_theme.tertiary),
                    "success_bg_color": rgba_from_argb(light_theme.tertiaryContainer),
                    "success_fg_color": rgba_from_argb(light_theme.onTertiaryContainer),
                    "warning_color": rgba_from_argb(light_theme.secondary),
                    "warning_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                    "warning_fg_color": rgba_from_argb(
                        light_theme.onSecondaryContainer
                    ),
                    "error_color": rgba_from_argb(light_theme.error),
                    "error_bg_color": rgba_from_argb(light_theme.errorContainer),
                    "error_fg_color": rgba_from_argb(light_theme.onError),
                    "window_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                    "window_fg_color": rgba_from_argb(light_theme.onSurface),
                    "view_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                    "view_fg_color": rgba_from_argb(light_theme.onSurface),
                    "headerbar_bg_color": rgba_from_argb(
                        light_theme.secondaryContainer
                    ),
                    "headerbar_fg_color": rgba_from_argb(light_theme.onSurface),
                    "headerbar_border_color": rgba_from_argb(
                        light_theme.primary, "0.8"
                    ),
                    "headerbar_backdrop_color": "@headerbar_bg_color",
                    "headerbar_shade_color": rgba_from_argb(
                        light_theme.secondaryContainer
                    ),
                    "card_bg_color": rgba_from_argb(light_theme.primary, "0.05"),
                    "card_fg_color": rgba_from_argb(light_theme.onSecondaryContainer),
                    "card_shade_color": rgba_from_argb(light_theme.shadow),
                    "dialog_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                    "dialog_fg_color": rgba_from_argb(light_theme.onSecondaryContainer),
                    "popover_bg_color": rgba_from_argb(light_theme.secondaryContainer),
                    "popover_fg_color": rgba_from_argb(
                        light_theme.onSecondaryContainer
                    ),
                    "shade_color": rgba_from_argb(light_theme.shadow),
                    "scrollbar_outline_color": rgba_from_argb(light_theme.outline),
                }

                dark_preset = {
                    "palette": palette,
                    "variables": dark_variable,
                    "custom_css": {
                        "gtk3": "",
                        "gtk4": "",
                    },
                }

                light_preset = {
                    "palette": palette,
                    "variables": light_variable,
                    "custom_css": {
                        "gtk3": "",
                        "gtk4": "",
                    },
                }

                return cls(name, dark=dark_preset, light=light_preset)


if __name__ == "__main__":
    p = Preset()
    buglog(p.variables)
    buglog(p.palette)
