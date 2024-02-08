#### TrenchBroom Entity Browser like an Assets Browser

Avoid creating cycler_sprite or env_sprites and manually setting the model/sprite path. Plus: you have a quick model/sprite preview before placing the entity without using external viewers.

![image](https://github.com/G2Pavon/TAB/assets/14117486/702c8466-c3f2-493f-ab8f-a117a3f55991)

![image](https://github.com/G2Pavon/TAB/assets/14117486/650067be-5852-4981-8626-2827e6cd2838)


---
# How works:

`fgd_generator.py` reads the game path (e.g: `/home/user/steam/steamapps/common/Half-Life/cstrike/` ). Then `models.fgd` and `sprites.fgd` are generated.

```
// ... Base class: Targetname, Angles, FrameRate, RenderFields, ConvertToCycler ...

// Models
@PointClass base(Targetname, Angles, FrameRate, RenderFields, ConvertToCycler) size(-8 -8 -8, 8 8 8) color(204 0 255) model({ "path": "models/example.mdl" }) = prop_example : "Model" 
[ model(string): "Path" : "models/example.mdl"]

@PointClass base(Targetname, Angles, FrameRate, RenderFields, ConvertToCycler) size(-8 -8 -8, 8 8 8) color(204 0 255) model({ "path": "models/sub_folder/box.mdl" }) = prop_box : "Model" 
[ model(string): "Path" : "models/sub_folder/box.mdl"]

// Rest of models...
```

```
// ... Base class: Targetname, Angles, FrameRate, RenderFields, ToggleSprite, ConvertToEnvSprite ...

// Sprites
@PointClass base(Targetname, Angles, FrameRate, RenderFields, ToggleSprite, ConvertToEnvSprite) size(-8 -8 -8, 8 8 8) color(204 0 255) iconsprite("sprites/ikgrass3.spr") = spr_ikgrass3 : "Sprite" 
[ model(string): "Path" : "models/ikgrass3.spr"]

// Resot of sprites...
```

---
`entity_converter.py` read the `.map` file and covert the `prop_*` entities into `cycler_sprite` and the `spr_*` entities into `env_sprite` (during the compiling task)

| Before | After|
|--------|------|
| ![image](https://github.com/G2Pavon/TAB/assets/14117486/01ee2b8d-edcc-4495-98c7-7e5c9034250b)| ![image](https://github.com/G2Pavon/TAB/assets/14117486/f270773f-f29a-4792-a487-570dd62f5467) |
---

# How to use

Download the current repo and goldsrcmap repo (https://github.com/G2Pavon/goldsrcmap)
Extract the files in your working directory:
```
Mapping/tools/TAB/utils
Mapping/tools/TAB/format
Mapping/tools/TAB/__init__.py
Mapping/tools/TAB/goldsrcmap.py
Mapping/tools/TAB/fgd_generator.py
Mapping/tools/TAB/entity_converter.py
```
Now follow the next steps:

# Generate FGD:

1) Open terminal/cmd in `Mapping/tools/TAB`

Example in linux:
```
cd Mapping/tools/TAB
```

2) Run `fgd_generator.py <path to game folder>`:
```
python3 fgd_generator.py /home/user/steam/steamapps/common/Half-Life/cstrike
```
![image](https://github.com/G2Pavon/TAB/assets/14117486/13953d8b-3581-49b4-8b00-97c146dc931f)


Output:

>Mapping/tools/TAB/models.fgd
>
>Mapping/tools/TAB/sprites.fgd

# Setting up FGD in Trenchbroom: 

1) Navigate to the folder where the game configuration files are located (where TrenchBroom.exe is located, or `user/share/trenchbroom` in linux.

2) Paste `models.fgd` and `sprites.fgd` into `games/Halflife`

3) Incude new fgds with your other fgds (create a combined FGD, e.g: combined.fgd) with following text:
```
@include "zhlt.fgd"
@include "HalfLife.fgd"
@include "models.fgd"
@include "sprites.fgd"
```

4) Open `GameConfig.cfg`, goto `entities` and replace ` "definitions": [ "HalfLife.fgd" ]` by ` "definitions": [ "combined.fgd" ]`. Make sure you have `"setDefaultProperties": true`:
```
    "entities": {
        "definitions": [ "combine.fgd" ],
        "defaultcolor": "0.6 0.6 0.6 1.0",
        "setDefaultProperties": true
    },
```

---
Now you have all models and sprites from your game folder into Entity Browser (Recommendation: press ![image](https://github.com/G2Pavon/TAB/assets/14117486/97cee766-828f-4b05-aa0d-384c745df196) to group entities by name) 

![image](https://github.com/G2Pavon/TAB/assets/14117486/d6392241-0b84-4421-878b-c82ceb55d39c)

---

# cycler_sprite conversion (for Counter-Strike): 

1) Goto `Run->Compile Map...`

2) Select your profile

![image](https://github.com/G2Pavon/TAB/assets/14117486/0ec37f66-6c5a-4068-b79e-2e8bf597159c)


3) Add new `Run Tool` Task after `Export Map` task and before `hlcsg` task
![image](https://github.com/G2Pavon/TAB/assets/14117486/8af59b0f-db21-4a21-95dc-ca7864d0b4cf)


4) Config the new task:
    >WARNING!!! This will overwrite the .map file you are editing in trenchbroom if the file is located in ${WORK_DIR_PATH}
   - Tool Path: `python3`
   - Parameters: `path/to/entity_converter.py ${WORK_DIR_PATH}/${MAP_BASE_NAME}.map`


![image](https://github.com/G2Pavon/TAB/assets/14117486/2616cc5d-058b-482e-a0df-645b45c0c2bf)
