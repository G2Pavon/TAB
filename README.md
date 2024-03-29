#### TrenchBroom Entity Browser like an Assets Browser

Avoid creating cycler_sprite and env_sprites entities and manually setting the model/sprite path. Plus: you have a quick model/sprite preview before placing the entity without using external viewers.

![image](https://github.com/G2Pavon/TAB/assets/14117486/702c8466-c3f2-493f-ab8f-a117a3f55991)

![image](https://github.com/G2Pavon/TAB/assets/14117486/650067be-5852-4981-8626-2827e6cd2838)


---
# How works:

`fgd_generator.py` reads the game path (e.g: `/Half-Life/cstrike/` ). Then `models.fgd` and `sprites.fgd` are generated.

```C
// ... Base class: Targetname, Angles, FrameRate, RenderFields, ConvertToCycler ...

// Models
@PointClass base(Targetname, Angles, FrameRate, RenderFields, ConvertToCycler) size(-8 -8 -8, 8 8 8) color(204 0 255) model({ "path": "models/example.mdl" }) = prop_example : "Model" 
[ model(string): "Path" : "models/example.mdl"]

@PointClass base(Targetname, Angles, FrameRate, RenderFields, ConvertToCycler) size(-8 -8 -8, 8 8 8) color(204 0 255) model({ "path": "models/sub_folder/box.mdl" }) = prop_box : "Model" 
[ model(string): "Path" : "models/sub_folder/box.mdl"]

// Rest of models...
```

```C
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

Extract the files in your working directory:
```C
Mapping/tools/TAB/fgd_generator.py
Mapping/tools/TAB/entity_converter.py
Mapping/tools/TAB/base.py
```
Now follow the next steps:

# Generate FGD:

1) Open terminal/cmd in `Mapping/tools/TAB`

2) Run `fgd_generator.py`:
```Shell
python fgd_generator.py path/to/Half-Life/mod
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
```C
@include "zhlt.fgd"
@include "HalfLife.fgd"
@include "models.fgd"
@include "sprites.fgd"
```

4) Open `GameConfig.cfg`, goto `entities` and replace ` "definitions": [ "HalfLife.fgd" ]` by ` "definitions": [ "combined.fgd" ]`. Make sure you have `"setDefaultProperties": true`:
```JSON
    "entities": {
        "definitions": [ "combine.fgd" ],
        "defaultcolor": "0.6 0.6 0.6 1.0",
        "setDefaultProperties": true
    },
```

---
Now you have all models and sprites from your game folder into Entity Browser (Recommendation: press ![image](https://github.com/G2Pavon/TAB/assets/14117486/97cee766-828f-4b05-aa0d-384c745df196) to group entities by name) 

![image](https://github.com/G2Pavon/TAB/assets/14117486/d6392241-0b84-4421-878b-c82ceb55d39c)
![image](https://github.com/G2Pavon/TAB/assets/14117486/6b50c9a4-40c4-4ffb-bfc4-d5fa24f9e37c)


---

# Update FGD
This is a method to easy-fast update the fgd when new models or sprites are added to your `models/`  `sprites/` folder.

> First, if you use linux probably you need change the permissions of the destination directory

```bash
sudo chmod a+w <prefix>/share/trenchbroom/games/your_game
```
> where \<prefix\> is the installation prefix



- Add a new compile profile and config like this:

![image](https://github.com/G2Pavon/TAB/assets/14117486/55d19edf-0a29-4686-8c52-f0f282b5d0ef)



- Now when you add new models or sprites, only you need is goto  `Run` -> `Compile map` -> select profile -> `Compile` -> `Close` -> (Reload Entity Definitions) press `F6`






---
# cycler_sprite and env_sprite converter (for Counter-Strike): 
 Install [goldsrcmap](https://github.com/G2Pavon/goldsrcmap)

```shell
pip install goldsrcmap
```

1) Goto `Run->Compile Map...`

2) Select your profile


3) Add new `Run Tool` task after `Export Map` and before `hlcsg`


4) Config the new task:
    >WARNING!!! This will overwrite the .map file you are editing in trenchbroom if the file is located in ${WORK_DIR_PATH}. RECOMMENDATION: add a new export map task ${MAP_BASE_NAME}_backup.map before
   - Tool Path: `python`
   - Parameters: `path/to/entity_converter.py ${WORK_DIR_PATH}/${MAP_BASE_NAME}.map`


![image](https://github.com/G2Pavon/TAB/assets/14117486/282b6ff9-610e-4615-9ff3-d7a7440cba7f)

