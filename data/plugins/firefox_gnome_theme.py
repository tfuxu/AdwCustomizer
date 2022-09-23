from yapsy.IPlugin import IPlugin
from gi.repository import Gtk, Adw
import os
from pathlib import Path

BASE = """
################################################################################
# Generated by the firefox-gnome-theme plugin
# Made by Gradience Team for GNOME Firefox Theme
################################################################################

:root {{
    --d_1: {d_1};
    --d_2: {d_2};
    --d_3: {d_3};
    --d_4: {d_4};
    --l_1: {l_1};
    --l_2: {l_2};
    --l_3: {l_3};
    --l_4: {l_4};

    --bg: {bg};
    --fg: {fg};

    --blk: {blk};
    --red: {red};
    --grn: {grn};
    --ylw: {ylw};
    --blu: {blu};
    --pnk: {pnk};
    --cyn: {cyn};
    --wht: {wht};
    --b_blk: {b_blk};
    --b_red: {b_red};
    --b_grn: {b_grn};
    --b_ylw: {b_ylw};
    --b_blu: {b_blu};
    --b_pnk: {b_pnk};
    --b_cyn: {b_cyn};
    --b_wht: {b_wht};
}}

:root {{
    --gnome-browser-before-load-background:        var(--s_1);
    --gnome-accent-bg:                             var(--blu);
    --gnome-accent:                                var(--b_blu);
    --gnome-toolbar-background:                    var(--s_1);
    --gnome-toolbar-color:                         var(--l_4);
    --gnome-toolbar-icon-fill:                     var(--l_3);
    --gnome-inactive-toolbar-color:                var(--l_2);
    --gnome-inactive-toolbar-border-color:         var(--d_4);
    --gnome-inactive-toolbar-icon-fill:            var(--l_1);
    --gnome-menu-background:                       var(--d_3);
    --gnome-headerbar-background:                  var(--d_1);
    --gnome-button-destructive-action-background:  var(--red);
    --gnome-entry-color:                           var(--l_4);
    --gnome-inactive-entry-color:                  var(--l_3);
    --gnome-switch-slider-background:              var(--l_3);
    --gnome-switch-active-slider-background:       var(--l_4);
    --gnome-inactive-tabbar-tab-background:        var(--d_1);
    --gnome-inactive-tabbar-tab-active-background: var(--d_1);
    --gnome-tabbar-tab-background:                 var(--d_1);
    --gnome-tabbar-tab-hover-background:           var(--d_2);
    --gnome-tabbar-tab-active-background:          var(--d_2);
    --gnome-tabbar-tab-active-hover-background:    var(--d_3);
    --gnome-tabbar-tab-active-background-contrast: var(--d_4);
}}
"""


class FirefoxGnomeThemePlugin(IPlugin):
    title = "Firefox Gnome Theme"
    author = "Gradience Team"
    description = "This plugin will customize the Gnome theme for Firefox"
    variables = None
    palette = None
    preset = {
        "variables": None,
        "palette": None,
        "custom_css": None,
    }
    plugin_id = "firefox_gnome_theme"
    # Custom settings shown on a separate view
    custom_settings = {"overwrite": True}
    css = BASE
    browser_row = Adw.EntryRow(
        title="Path to the profile directory",
    )
    profile_dir = None

    def activate(self):
        # This is called when the plugin is activated
        # It does nothing here, but you can use it to initialize
        pass

    def deactivate(self):
        # This is called when the plugin is deactivated
        # It does nothing here, but you can use it to clean up
        pass

    def give_preset_settings(self, preset_settings, custom_settings=None):
        # This is called by Gradience for giving to the plugin, the preset settings
        self.preset = preset_settings
        self.variables = preset_settings["variables"]
        self.palette = preset_settings["palette"]
        if custom_settings:
            self.custom_settings = custom_settings

    def open_settings(self):
        # This is called when the user clicks on the settings button
        # I've choosed to leave the liberty to the plugin creator to decide how to show the settings
        # But it's recommended to use a Adw.PreferencesWindow
        self.window = Adw.PreferencesWindow()
        self.window.set_title("Firefox Gnome Theme Plugin")
        self.main_page = Adw.PreferencesPage()
        # Apply
        self.apply_pref = Adw.PreferencesGroup()
        self.apply_pref.set_title("Apply")
        self.apply_pref.set_description("Preferences for applying the theme")

        self.overwrite_row = Adw.ActionRow(
            title="Overwrite",
            subtitle="Overwrite the existing userChrome.css file",
        )
        self.overwrite_switch = Gtk.Switch()
        self.overwrite_switch.set_active(self.custom_settings["overwrite"])
        self.overwrite_switch.connect("notify::active", self.on_overwrite)
        self.overwrite_switch.set_valign(Gtk.Align.CENTER)
        self.overwrite_row.add_suffix(self.overwrite_switch)
        self.overwrite_row.connect("activate", self.on_overwrite)
        self.apply_pref.add(self.overwrite_row)
        self.main_page.add(self.apply_pref)

        # Browser
        self.browser_pref = Adw.PreferencesGroup()
        self.browser_pref.set_title("Browser")
        self.browser_pref.set_description(
            "Choose where profiles are stored. If you don't know what this is, leave it as default, it will work in most cases."
        )

        self.browser_row = Adw.EntryRow(
            title="Path to the directory where profiles are stored",
        )
        self.browser_row.set_text("~/.mozilla/firefox")
        self.browser_row.set_show_apply_button(True)
        self.browser_row.connect("apply", self.on_apply)
        self.browser_pref.add(self.browser_row)

        self.main_page.add(self.browser_pref)

        self.window.add(self.main_page)
        self.window.present()

    def on_apply(self, widget):
        self.profile_dir = Path(self.browser_row.get_text()).expanduser()
        if not self.profile_dir.exists():
            self.browser_row.set_css_classes(["error"])
            self.profile_dir = None
        else:
            self.browser_row.remove_css_class("error")

    def on_overwrite(self, widget, _):
        # This is called when the user changes the overwrite setting
        self.custom_settings["overwrite"] = not self.custom_settings["overwrite"]

    def validate(self):
        # Normally, it would be a good idea to validate the settings here
        # But because there is only one setting and it can onbly be a boolean
        # It's not necessary, but it's good practice
        # If there would be an error, it's should return True, and the error message in a dictionary
        return False, None

    def apply(self, dark_theme=False):
        # This is called when the user clicks on the apply button (the one in the headerbar)
        # You can use dark_theme to know if the user wants a dark theme or not

        if self.profile_dir:
            profile_dir = self.profile_dir
        else:
            profile_dir = Path("~/.mozilla/firefox/").expanduser()
        profiles = []
        if profile_dir.exists():
            os.chdir(profile_dir)
            for folder in profile_dir.iterdir():
                if folder.is_dir():
                    if (
                        str(folder).endswith(".default-release")
                        or str(folder).endswith(".default")
                        or str(folder).endswith(".default-nightly")
                        or str(folder).endswith(".dev-edition-default")
                    ):
                        profiles.append(folder)

        if len(profiles) == 0:
            print("No profiles found")
            return
        self.css = self.css.format(
            d_1=self.palette["dark_"]["1"],
            d_2=self.palette["dark_"]["2"],
            d_3=self.palette["dark_"]["3"],
            d_4=self.palette["dark_"]["4"],
            l_1=self.palette["light_"]["1"],
            l_2=self.palette["light_"]["2"],
            l_3=self.palette["light_"]["3"],
            l_4=self.palette["light_"]["4"],
            bg=self.variables["window_bg_color"],
            fg=self.variables["window_fg_color"],
            red=self.palette["red_"]["5"],
            grn=self.palette["green_"]["5"],
            ylw=self.palette["yellow_"]["5"],
            blu=self.palette["blue_"]["5"],
            pnk=self.palette["purple_"]["5"],
            cyn=self.palette["blue_"]["5"],
            wht=self.palette["light_"]["5"],
            blk=self.palette["dark_"]["5"],
            b_red=self.palette["red_"]["1"],
            b_grn=self.palette["green_"]["1"],
            b_ylw=self.palette["yellow_"]["1"],
            b_blu=self.palette["blue_"]["1"],
            b_pnk=self.palette["purple_"]["1"],
            b_cyn=self.palette["blue_"]["1"],
            b_wht=self.palette["light_"]["1"],
            b_blk=self.palette["dark_"]["1"],
        )
        for profile in profiles:
            profile = (
                profile / "chrome" / "firefox-gnome-theme" / "customChrome.css"
            )
            if profile.exists():
                if self.custom_settings["overwrite"]:
                    with open(profile, "w", encoding="utf-8") as f:
                        f.write(self.css)
            else:
                with open(profile, "w", encoding="utf-8") as f:
                    f.write(self.css)

    def save(self):
        return self.custom_settings
