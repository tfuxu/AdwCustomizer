# custom_presets.py
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

import os
import json

from gi.repository import GLib, Soup

from gradience.utils.preset import presets_dir
from gradience.utils.utils import to_slug_case, buglog
from gradience.utils.exceptions import GradienceError


# Open Soup3 session
session = Soup.Session()


def fetch_presets(repo) -> [dict, list]:
    try:
        request = Soup.Message.new("GET", repo)
        body = session.send_and_read(request, None)
    except GLib.GError as e:  # offline
        if e.code == 1:
            buglog(f"Failed to establish a new connection. Exc: {e}")
            return False, False
        else:
            buglog(f"Unhandled Libsoup3 GLib.GError error code {e.code}. Exc: {e}")
            return False, False
    try:
        raw = json.loads(body.get_data())
    except json.JSONDecodeError as e:
        buglog(f"Error with decoding JSON data. Exc: {e}")
        return False, False

    preset_dict = {}
    url_list = []

    for data in raw.items():
        data = list(data)
        data.insert(0, to_slug_case(data[0]))

        url = data[2]
        data.pop(2)  # Remove preset URL from list

        to_dict = iter(data)
        # Convert list back to dict
        preset_dict.update(dict(zip(to_dict, to_dict)))

        url_list.append(url)

    return preset_dict, url_list

def get_as_json(url):
    print(f"Downloading preset from {url}...")

    try:
        request = Soup.Message.new("GET", url)
        body = session.send_and_read(request, None)
    except GLib.GError as error:  # offline
        if error.code == 1:
            print(f"Failed to establish a new connection. Exc: {error}")
            return False, False
        else:
            print(f"Unhandled Libsoup3 GLib.GError error code {error.code}. Exc: {error}")
            return False, False
    try:
        data = body.get_data()
        raw = json.loads(data)
    except json.JSONDecodeError as error:
        print(f"Error with decoding JSON data. Exc: {error}")
        return False, False

    return True, json.dumps(raw, indent=4)


def download_preset(name, repo_name, url) -> None:
    status, data = get_as_json(url)

    if status:
        try:
            with open(
                os.path.join(
                    presets_dir,
                    repo_name,
                    to_slug_case(name) + ".json",
                ),
                "w",
                encoding="utf-8",
            ) as f:
                f.write(data)
                f.close()
        except OSError as e:
            buglog(f"Failed to write data to a file. Exc: {e}")
    else:
        raise GradienceError("Failed to download preset.")
