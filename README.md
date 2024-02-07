# TAB

![image](https://github.com/G2Pavon/TAB/assets/14117486/d6392241-0b84-4421-878b-c82ceb55d39c)

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

