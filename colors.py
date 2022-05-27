from collections import namedtuple

Color = namedtuple("Color", '''
    base00 
    base01 
    base02 
    base03 
    base04 
    base05 
    base06 
    base07 
    base08 
    base09 
    base0A 
    base0B 
    base0C 
    base0D 
    base0E
    base0F
''')

default_dark = Color(
    "#181818",
    "#282828",
    "#383838",
    "#585858",
    "#b8b8b8",
    "#d8d8d8",
    "#e8e8e8",
    "#f8f8f8",
    "#ab4642",
    "#dc9656",
    "#f7ca88",
    "#a1b56c",
    "#86c1b9",
    "#7cafc2",
    "#ba8baf",
    "#a16946",
)
