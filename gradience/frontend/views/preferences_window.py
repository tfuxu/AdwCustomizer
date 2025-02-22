# preferences_window.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022-2023, Gradience Team
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

from gradience.backend.flatpak_overrides import create_gtk_user_override, remove_gtk_user_override
from gradience.backend.flatpak_overrides import create_gtk_global_override, remove_gtk_global_override

from gradience.backend.constants import rootdir

from gradience.backend.logger import Logger

logging = Logger()


@Gtk.Template(resource_path=f"{rootdir}/ui/preferences_window.ui")
class GradiencePreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = "GradiencePreferencesWindow"

    gtk4_user_theming_switch = Gtk.Template.Child()
    gtk4_global_theming_switch = Gtk.Template.Child()

    gtk3_user_theming_switch = Gtk.Template.Child()
    gtk3_global_theming_switch = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.settings = parent.settings

        self.app = self.parent.get_application()
        self.win = self.app.get_active_window()

        self.set_transient_for(self.win)

        self.setup()

    def setup(self):
        self.setup_flatpak_group()

    def setup_flatpak_group(self):
        user_flatpak_theming_gtk4 = self.settings.get_boolean(
            "user-flatpak-theming-gtk4"
        )

        user_flatpak_theming_gtk3 = self.settings.get_boolean(
            "user-flatpak-theming-gtk3"
        )

        self.gtk4_user_theming_switch.set_state(
            user_flatpak_theming_gtk4
        )

        # self.gtk4_global_theming_switch.set_state(global_flatpak_theming_gtk4)

        self.gtk3_user_theming_switch.set_state(
            user_flatpak_theming_gtk3
        )
        
        # self.gtk3_global_theming_switch.set_state(global_flatpak_theming_gtk3)

        self.gtk4_user_theming_switch.connect(
            "state-set", self.on_gtk4_user_theming_switch_toggled
        )

        self.gtk3_user_theming_switch.connect(
            "state-set", self.on_gtk3_user_theming_switch_toggled
        )

    def on_gtk4_user_theming_switch_toggled(self, *args):
        state = self.gtk4_user_theming_switch.props.state

        if not state:
            create_gtk_user_override(self.settings, "gtk4", self)
        else:
            remove_gtk_user_override(self.settings, "gtk4", self)

            logging.debug(
                f"user-flatpak-theming-gtk4: {self.settings.get_boolean('user-flatpak-theming-gtk4')}"
            )

    def on_gtk3_user_theming_switch_toggled(self, *args):
        state = self.gtk3_user_theming_switch.props.state

        if not state:
            create_gtk_user_override(self.settings, "gtk3", self)
        else:
            remove_gtk_user_override(self.settings, "gtk3", self)

            logging.debug(
                f"user-flatpak-theming-gtk3: {self.settings.get_boolean('user-flatpak-theming-gtk3')}"
            )

    def on_gtk4_global_theming_switch_toggled(self, *args):
        state = self.gtk4_global_theming_switch.props.state

        if not state:
            create_gtk_global_override(self.settings, "gtk4", self)
        else:
            remove_gtk_global_override(self.settings, "gtk4", self)

            logging.debug(
                f"global-flatpak-theming-gtk4: {self.settings.get_boolean('global-flatpak-theming-gtk4')}"
            )

    def on_gtk3_global_theming_switch_toggled(self, *args):
        state = self.gtk3_global_theming_switch.props.state

        if not state:
            create_gtk_global_override(self.settings, "gtk3", self)
        else:
            remove_gtk_global_override(self.settings, "gtk3", self)

            logging.debug(
                f"global-flatpak-theming-gtk3: {self.settings.get_boolean('global-flatpak-theming-gtk3')}"
            )
