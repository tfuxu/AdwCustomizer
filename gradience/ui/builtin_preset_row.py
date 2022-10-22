# builtin_preset_row.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022  Gradience Team
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

from gi.repository import Gtk, Adw

from gradience.utils.utils import to_slug_case, buglog
from gradience.constants import rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/builtin_preset_row.ui")
class GradienceBuiltinPresetRow(Adw.ActionRow):
    __gtype_name__ = "GradienceBuiltinPresetRow"

    apply_button = Gtk.Template.Child("apply_button")

    def __init__(self, name, toast_overlay, author="", **kwargs):
        super().__init__(**kwargs)

        self.name = name

        self.set_name(name)
        self.set_title(name)

        self.app = Gtk.Application.get_default()

        self.toast_overlay = toast_overlay

        apply_button = Gtk.Template.Child("apply_button")

    @Gtk.Template.Callback()
    def on_apply_button_clicked(self, *_args):
        buglog("apply")

        self.app.load_preset_from_resource(
            f"{rootdir}/presets/" + to_slug_case(self.name) + ".json"
        )
