import os
import argparse

from base import BASE_CLASSES_MODELS, BASE_CLASSES_SPRITES

FGD_MODELS_NAME = "models.fgd" # Customizable
FGD_SPRITES_NAME = "sprites.fgd" # Customizable

ENTITY_PREFIX_MODELS = "prop" # Customizable
ENTITY_PREFIX_SPRITES = "spr" # Customizable

BASE_MODELS = "Targetname, Angles, FrameRate, RenderFields, ConvertToCycler"
BASE_SPRITES = "Targetname, Angles, FrameRate, RenderFields, ToggleSprite, ConvertToEnvSprite"

ENTITY_POINT_SIZE = "-8 -8 -8, 8 8 8" # Customizable
ENTITY_POINT_COLOR = "204 0 255" # Customizable

EXCLUDE_SUBFOLDERS_MODELS = ['player','shield'] # Customizable
EXCLUDE_PREFIX_MODELS = ['p_', 'v_', 'w_'] # Customizable
EXCLUDE_WORD_MODELS = ['hostage', 'guerilla'] # Customizable
EXCLUDE_EXACT_WORD_MODELS = ['player'] # Customizable

EXCLUDE_SUBFOLDERS_SPRITES = ['trenchbroom'] # Customizable
EXCLUDE_PREFIX_SPRITES = ['640'] # Customizable
EXCLUDE_WORD_SPRITES = ['rifle_smoke', 'radar', 'pistol_smoke', 'muzzleflash', 'iplayer', 'ch_sniper'] # Customizable
EXCLUDE_EXACT_WORD_SPRITES = ['c4', 'sniper_scope', 'shadow_circle', 'radio', 'left', 'left2', 'ihostage', 'ic4', 'ibackpack', 'defuser'] # Customizable


def should_exclude(file_path, exclude_prefix, exclude_word, exclude_exact_word) -> bool:
    """Checks if the file should be excluded based on predefined conditions"""
    filename = os.path.basename(file_path).lower()
    if filename.startswith(tuple(exclude_prefix)) or any(word in filename for word in exclude_word) \
            or any(word.lower() == filename.split('.')[0] for word in exclude_exact_word):
        return True
    return False

def find_directory(game_path, subdir) -> str:
    """Finds the specified subdirectory within the game path"""
    directory_path = os.path.join(game_path, subdir.replace('\\', '/'))
    if os.path.exists(directory_path):
        return directory_path
    else:
        raise FileNotFoundError(f"'{subdir}' directory not found in {game_path}")

def find_files(directory, file_extension, exclude_folders, exclude_prefix, exclude_word, exclude_exact_word) -> list:
    """Finds all files within the given directory that meet the exclusion criteria"""
    files = []
    for root, dirs, filenames in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclude_folders]
        for file in filenames:
            if file.lower().endswith(file_extension):  # Check if file has desired extension
                file_path = os.path.join(root, file).replace('\\', '/')
                if not should_exclude(file_path, exclude_prefix, exclude_word, exclude_exact_word):
                    files.append(file_path)
    return files

def generate_and_write_fgd(files, extension, output_file_path, base_classes, entity_prefix, file_extension):
    """Generates FGD content based on the provided list of files"""
    content = base_classes
    content += f"\n\n//\n// {'Models' if extension == '.mdl' else 'Sprites'}\n//\n\n"  # FGD comment

    entity_count = {}

    for file_path in files:
        entity_name = os.path.splitext(os.path.basename(file_path))[0]
        subfolder = os.path.relpath(os.path.dirname(file_path), MODELS_DIRECTORY if 'models' in output_file_path else SPRITES_DIRECTORY)

        if subfolder == '.':
            subfolder = ''
        entity_path = os.path.join(subfolder, f"{entity_name}.{file_extension}").replace('\\', '/')

        if entity_name in entity_count:
            entity_count[entity_name] += 1
            classname = f"{entity_prefix}_{entity_name}_d{entity_count[entity_name]}"
        else:
            entity_count[entity_name] = 1
            classname = f"{entity_prefix}_{entity_name}"

        content += "@PointClass "
        if extension == '.mdl':
            content += f'base({BASE_MODELS}) size({ENTITY_POINT_SIZE}) color({ENTITY_POINT_COLOR}) '
            content += f'model({{ "path": "models/{entity_path}" }}) = {classname} : "Model" \n[ model(string): "Path" : "models/{entity_path}"]\n\n'
            
        elif extension == '.spr':
            content += f'base({BASE_SPRITES}) size({ENTITY_POINT_SIZE}) color({ENTITY_POINT_COLOR}) '
            content += f'iconsprite("sprites/{entity_path}") = {classname} : "Sprite" \n[ model(string): "Path" : "models/{entity_path}"]\n\n'


    with open(output_file_path, "w") as file:
        file.write(content)

    print(f"File '{os.path.splitext(os.path.basename(output_file_path))[0]}.fgd' Generated at: ", output_file_path)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generate models.fgd and sprites.fgd files for TrenchBroom (only .mdl and .spr)',
        usage=' %(prog)s GAME_PATH \n\
        only models: %(prog)s GAME_PATH -m \n\
        only sprites: %(prog)s GAME_PATH -s \n '
    )
    parser.add_argument('game', metavar='GAME_PATH', type=str, help='Path to the game directory')
    parser.add_argument('-m', '--models', action='store_true', help='Generate only models FGD')
    parser.add_argument('-s', '--sprites', action='store_true', help='Generate only sprites FGD')
    args = parser.parse_args()

    if args.models or args.sprites:
        return args.game, args.models, args.sprites
    else:
        return args.game, True, True



if __name__ == "__main__":
    GAME_PATH, models, sprites = parse_arguments()

    file_extension = ('.mdl', '.spr')

    if models:
        MODELS_DIRECTORY = find_directory(GAME_PATH, "models")
        mdl_files = find_files(MODELS_DIRECTORY, file_extension[0], EXCLUDE_SUBFOLDERS_MODELS, EXCLUDE_PREFIX_MODELS, EXCLUDE_WORD_MODELS, EXCLUDE_EXACT_WORD_MODELS)
        output_file_path = os.path.join(os.path.dirname(__file__), FGD_MODELS_NAME)
        generate_and_write_fgd(mdl_files, file_extension[0],output_file_path, BASE_CLASSES_MODELS, ENTITY_PREFIX_MODELS, "mdl")

    if sprites:
        SPRITES_DIRECTORY = find_directory(GAME_PATH, "sprites")
        spr_files = find_files(SPRITES_DIRECTORY, file_extension[1], EXCLUDE_SUBFOLDERS_SPRITES, EXCLUDE_PREFIX_SPRITES, EXCLUDE_WORD_SPRITES, EXCLUDE_EXACT_WORD_SPRITES)
        output_file_path = os.path.join(os.path.dirname(__file__), FGD_SPRITES_NAME)
        generate_and_write_fgd(spr_files, file_extension[1],output_file_path, BASE_CLASSES_SPRITES, ENTITY_PREFIX_SPRITES, "spr")
