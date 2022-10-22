import click

from gradience.utils.preset import Preset
from gradience.utils.themes import Theme


@click.command()
@click.argument("preset", type=click.Path(exists=True), required=True)
def apply_preset(preset):
    preset = Preset(preset_path=preset)
    theme = Theme(preset.name, preset)
    theme.create()
