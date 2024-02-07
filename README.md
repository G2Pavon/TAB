# TAB

---
# How works:

`mdl2fgd.py` reads the specified directory for .mdl files (e.g: `/home/user/steam/steam/steamapps/common/Half-Life/strike/models/` ). Then generate a `.fgd` with the following format:

```
// ... Base class: Targetname, Angles, FrameRate, RenderFields, ConvertToCycler ...

// Models
@PointClass base(Targetname, Angles, FrameRate, RenderFields, ConvertToCycler) size(-8 -8 -8, 8 8 8) color(204 0 255) model({ "path": "models/example.mdl" }) = prop_example : "Model" 
[ model(string): "Path" : "models/example.mdl"]

@PointClass base(Targetname, Angles, FrameRate, RenderFields, ConvertToCycler) size(-8 -8 -8, 8 8 8) color(204 0 255) model({ "path": "models/sub_folder/box.mdl" }) = prop_example : "Model" 
[ model(string): "Path" : "models/sub_folder/box.mdl"]

// ... Rest of models
```
---
`gen_cycler_sprite.py` read the `.map` file and covert the `prop_` entities into `cycler_sprite`

```
{
"classname" "prop_box"
"model" "models/sub_folder/box.mdl"
"angles" "0 0 0"
"framerate" "10"
"rendermode" "0"
"rendercolor" "0 0 0"
"renderfx" "0"
"to_cycler" "1"
"origin" "-192 -128 96"
}
```

To:

```
{
"classname" "cycler_sprite"
"model" "models/sub_folder/prop.mdl"
"angles" "0 0 0"
"framerate" "10"
"rendermode" "0"
"rendercolor" "0 0 0"
"renderfx" "0"
"origin" "-192 -128 96"
}
```
---

# How to use

Download the current repo and goldsrcmap repo (https://github.com/G2Pavon/goldsrcmap)
Extract the files in your working directory:
```
Mapping/tools/TAB/utils
Mapping/tools/TAB/format
Mapping/tools/TAB/__init__.py
Mapping/tools/TAB/goldsrcmap.py
Mapping/tools/TAB/mdl2fgd.py
Mapping/tools/TAB/gen_cycler_sprite.py
```
Now follow the next steps:

# Generate FGD:

open terminal/cmd in `Mapping/tools/TAB`

Example in linux:
```
cd `Mapping/tools/TAB`
```

Run `mdl2fgd.py`:
```
python3 mdl2fgd.py /home/user/steam/steam/steamapps/common/Half-Life/cstrike/models
```
Output:
```
Mapping/tools/TAB/models.fgd
```

# Setting up in Trenchbroom: 

Navigate to the folder where the game configuration (e.g: `Trenchbroom/games/Halflife`) files are located (where TrenchBroom.exe is located, or `user/share/trenchbroom` in linux).

Paste `models.fgd` into `games/Halflife`

Incude models.fgd with your other fgds (create a combined FGD, e.g: combined.fgd) with following text:
```
@include "zhlt.fgd"
@include "HalfLife.fgd"
@include "models.fgd"
```

Open `GameConfig.cfg`, goto `entities` and replace ` "definitions": [ "HalfLife.fgd" ]` by ` "definitions": [ "combined.fgd" ]`. Make sure you have `"setDefaultProperties": true`:
```
    "entities": {
        "definitions": [ "combine.fgd" ],
        "defaultcolor": "0.6 0.6 0.6 1.0",
        "setDefaultProperties": true
    },
```

---
Now you have all models from your game models/ folder into Entity Browser (Recommendation: press ![image](https://github.com/G2Pavon/TAB/assets/14117486/97cee766-828f-4b05-aa0d-384c745df196)

![image](https://github.com/G2Pavon/TAB/assets/14117486/d6392241-0b84-4421-878b-c82ceb55d39c)



