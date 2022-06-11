# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

from colors import Color, default_dark


# Variables
mod = "mod4"
terminal = "kitty"
launcher = "rofi -show drun"
margin = 4
border_width = 2


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])


# Keybindings
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn(launcher), desc="Spawn a command using a prompt widget"),

    # Volume Controls
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 2"), desc="Raise voume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 2"), desc="Lower volume"),
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t"), desc="Mute audio"),

    # # Playerctl Controls
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Play next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Play previous"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/pause audio"),
    Key([], "XF86AudioStop", lazy.spawn("playerctl pause"), desc="Pause audio"),

    # Group Controls
    Key([mod], 'Left', lazy.screen.prev_group(skip_managed=True,), desc="Move to previous group"),
    Key([mod], 'Right', lazy.screen.next_group(skip_managed=True,), desc="Move to next group"),
    Key([mod], 'Escape', lazy.screen.togglegroup(), desc="Toggle group"),
]


# Groups
groups = [
    Group(""),
    Group(""),
    Group(""),
    Group(""),
    Group(""),
    Group("")
]

for i, group in enumerate(groups, 1):
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key([mod], str(i),
                lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group.name)),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key([mod, "shift"], str(i),
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name)),
        ]
    )


# Layouts (I only like the Column layout)
layouts = [
    layout.Columns(
        border_focus=default_dark.base0E,
        border_width=border_width,
        margin=margin,
    ),
    layout.Floating(
        border_focus=default_dark.base0E,
        border_width=border_width,
    )
]


# Widgets
widget_defaults = dict(
    font="FiraCode",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# Defining my extra widgets
dot = widget.TextBox(text="", foreground=default_dark.base03, padding=10)

volume_widget = [
    widget.TextBox(text="", foreground=default_dark.base0A),
    widget.Volume(
        foreground=default_dark.base0A,
    )
]

net_widget = [
    widget.TextBox(text="", foreground=default_dark.base0B),
    widget.Wlan(foreground=default_dark.base0B)
]

mem_widget = [
    widget.TextBox(text="",foreground=default_dark.base0C),
    widget.Memory(foreground=default_dark.base0C)
]

layout_widget = [
    widget.CurrentLayout(foreground=default_dark.base0E)
]

clock_widget = [
    widget.TextBox(text="", foreground=default_dark.base0D),
    widget.Clock(format="%Y-%m-%d %a %I:%M %p", foreground=default_dark.base0D),
]

# Creating widgets
widgets = [
    widget.Sep(foreground=default_dark.base01, linewidth=4),
    widget.GroupBox(
        this_current_screen_border = default_dark.base0E,
        inactive = default_dark.base03,
        highlight_color=[default_dark.base01, default_dark.base03],
        highlight_method = 'line',
        urgent_alert_method = 'line',
    ),
    widget.Prompt(),
    widget.Spacer(),
    widget.WindowName(),
    widget.Spacer(),
    widget.Systray(),
]

# Extending widget list
widgets.extend(volume_widget)
widgets.append(dot)
widgets.extend(net_widget)
widgets.append(dot)
widgets.extend(mem_widget)
widgets.append(dot)
widgets.extend(layout_widget)
widgets.append(dot)
widgets.extend(clock_widget)
widgets.append(widget.Sep(foreground=default_dark.base01, linewidth=4))


# Creating Screen
screens = [
    Screen(
        top=bar.Bar(
            widgets,
            24,
            background=default_dark.base01,
            margin = [margin, margin, 0, margin],
        ),
        wallpaper="/home/colten/Pictures/Wallpapers/leaf.jpg",
        wallpaper_mode="stretch"
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="Steam"),
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="steam"), # Steam
    ],
    border_focus=default_dark.base0E,
    border_width=border_width,
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
