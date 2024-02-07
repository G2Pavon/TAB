import os
import argparse

FGD_NAME = "models.fgd" # Customizable FGD name
BASE_CLASSES = """// FGD that allow display models in Trenchbroom Entity Browser 
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

@BaseClass = ConvertToCycler
[   
    to_cycler(choices) : "Convert to cycler_sprite": 1 =
    [   
        0: "no"
        1: "yes"
    ]
]
"""
BASE = "Targetname, Angles, FrameRate, RenderFields, ConvertToCycler" # 'to_cycler' is used in gen_cycler_sprite.py

ENTITY_POINT_SIZE = "-8 -8 -8, 8 8 8" # Customizable point size to display in Trenchbroom
ENTITY_POINT_COLOR = "204 0 255" # Customizable point color to display in Trenchbroom
ENTITY_PREFIX = "prop" #  Customizable prefix will be displayed in Trenchbroom Entity Browser

# Skip these folders/models
EXCLUDE_FOLDERS = ['player', 'shield']
EXCLUDE_PREFIX = ['p_', 'v_', 'w_'] # weapons
EXCLUDE_WORD = ['hostage', 'guerilla']
EXCLUDE_EXACT_WORD = ['player']
# EXCLUDE_T_MODELS = ['T.mdl'] # contain the textures for the main model, an old optimization technique that is not necessary in this days

def should_exclude(file_path) -> bool:
    """Checks if the file should be excluded based on predefined conditions"""
    filename = os.path.basename(file_path).lower()
    if filename.endswith('.mdl') and not filename.startswith(tuple(EXCLUDE_PREFIX)) \
            and not any(word in filename for word in EXCLUDE_WORD) \
            and not any(word.lower() == filename.split('.')[0] for word in EXCLUDE_EXACT_WORD):
        return False
    return True

def find_mdl_files(folder) -> list:
    """Finds all .mdl files within the given folder"""
    mdl_files = []
    for root, dirs, files in os.walk(folder):
        # Exclude specified folders
        dirs[:] = [d for d in dirs if d not in EXCLUDE_FOLDERS]
        for file in files:
            file_path = os.path.join(root, file)
            if not should_exclude(file_path):
                mdl_files.append(file_path)
    return mdl_files

def generate_and_write_fgd(mdl_files, output_file_path):
    """Generates FGD content based on the provided list of .mdl files and writes it to the output file"""
    content = BASE_CLASSES
    content += "\n\n//\n// Models\n//\n\n" # FGD comment

    model_count = {}  # Dictionary to keep track of model counts

    for mdl_file in mdl_files:
        model_name = os.path.splitext(os.path.basename(mdl_file))[0]
        subfolder = os.path.relpath(os.path.dirname(mdl_file), MODELS_DIRECTORY)

        if subfolder == '.':
            subfolder = ''  # If the model is in the root folder (models/file.mdl), no need to include a subfolder
        mdl_path = os.path.join(subfolder, f"{model_name}.mdl")

        # Check for duplicated model name (add 'd#' suffix)
        if model_name in model_count:
            model_count[model_name] += 1
            # Example: prop_test_d2.mdl
            classname = f"{ENTITY_PREFIX}_{model_name}_d{model_count[model_name]}" 
        else:
            # Initialize the count for this model name
            model_count[model_name] = 1
            # Example: prop_test.mdl
            classname = f"{ENTITY_PREFIX}_{model_name}" 

        content += "@PointClass "
        content += f"base({BASE}) size({ENTITY_POINT_SIZE}) color({ENTITY_POINT_COLOR})"
        content += f'model({{ "path": "models/{mdl_path}" }}) = {classname} : "Model" \n[ model(string): "Path" : "models/{mdl_path}"]\n\n'

    with open(output_file_path, "w") as file:
        file.write(content)

    print(f"FGD '{FGD_NAME}' Generated at: ", output_file_path)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate models.fgd file for Half-Life')
    parser.add_argument('models_directory', metavar='MODELS_DIRECTORY', type=str,
                        help='Directory containing the models')
    args = parser.parse_args()
    return args.models_directory


if __name__ == "__main__":
    MODELS_DIRECTORY = parse_arguments()
    mdl_files = find_mdl_files(MODELS_DIRECTORY)
    output_file_path = os.path.join(os.path.dirname(__file__), FGD_NAME)
    generate_and_write_fgd(mdl_files, output_file_path)