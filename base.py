BASE_CLASSES_MODELS = """
// FGD that allows displaying models in Trenchbroom Entity Browser 
// Like an asset browser

//
// Base Classes
//

@BaseClass = Targetname 
[ 
    targetname(target_source) : "Name"
]

@BaseClass = Angles
[
    angles(string) : "Pitch Yaw Roll (Y Z X)" : "0 0 0"
]

@BaseClass = FrameRate
[
    framerate(integer) : "Frames per second" : 10
]

@BaseClass = RenderFields
[
    renderfx(choices) :"Render FX" : 0 =
    [
        0: "Normal"
        1: "Slow Pulse"
        2: "Fast Pulse"
        3: "Slow Wide Pulse"
        4: "Fast Wide Pulse"
        9: "Slow Strobe"
        10: "Fast Strobe"
        11: "Faster Strobe"
        12: "Slow Flicker"
        13: "Fast Flicker"
        5: "Slow Fade Away"
        6: "Fast Fade Away"
        7: "Slow Become Solid"
        8: "Fast Become Solid"
        14: "Constant Glow"
        15: "Distort"
        16: "Hologram (Distort + fade)"
    ]
    rendermode(choices) : "Render Mode" : 0 =
    [
        0: "Normal"
        1: "Color"
        2: "Texture"
        3: "Glow"
        4: "Solid"
        5: "Additive"
    ]
    renderamt(integer) : "FX Amount (1 - 255)"
    rendercolor(color255) : "FX Color (R G B)" : "0 0 0"
]

@BaseClass = ConvertProp
[   
    convert_prop(choices) : "" : 1 =
    [   
        0: "no"
        1: "yes"
    ]
]
"""

BASE_CLASSES_SPRITES = """
// FGD that allows displaying sprites in Trenchbroom Entity Browser 
// Like an asset browser

//
// Base Classes
//

@BaseClass = Targetname 
[ 
    targetname(target_source) : "Name"
]

@BaseClass = Angles
[
    angles(string) : "Pitch Yaw Roll (Y Z X)" : "0 0 0"
]

@BaseClass = FrameRate
[
    framerate(integer) : "Frames per second" : 10
]

@BaseClass = RenderFields
[
    renderfx(choices) :"Render FX" : 0 =
    [
        0: "Normal"
        1: "Slow Pulse"
        2: "Fast Pulse"
        3: "Slow Wide Pulse"
        4: "Fast Wide Pulse"
        9: "Slow Strobe"
        10: "Fast Strobe"
        11: "Faster Strobe"
        12: "Slow Flicker"
        13: "Fast Flicker"
        5: "Slow Fade Away"
        6: "Fast Fade Away"
        7: "Slow Become Solid"
        8: "Fast Become Solid"
        14: "Constant Glow"
        15: "Distort"
        16: "Hologram (Distort + fade)"
    ]
    rendermode(choices) : "Render Mode" : 0 =
    [
        0: "Normal"
        1: "Color"
        2: "Texture"
        3: "Glow"
        4: "Solid"
        5: "Additive"
    ]
    rendercolor(color255) : "FX Color (R G B)" : "0 0 0"
]

@BaseClass = ToggleSprite
[   
    spawnflags(flags) =
    [
        1: "Start on" : 0
        2: "Play Once" : 0
    ]
]

@BaseClass = ConvertSprite
[
    convert_sprite(choices) : "": 1 =
    [   
        0: "no"
        1: "yes"
    ]
]
"""
