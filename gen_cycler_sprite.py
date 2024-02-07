from __future__ import annotations

import os
import argparse
import goldsrcmap as gsm 

def main(map_file):
    print("-----------------------------------------------")
    print("Converting 'prop_' entity to 'cycler_sprite' ...")
    m = gsm.load_map(map_file)
    cycler_list = []
    kv_pairs = {}
    for entity in m.entities:
        if 'to_cycler' in entity and entity['to_cycler'] == '1':
            for key, value in entity.properties.items():
                if key not in ['classname', 'origin', 'to_cycler']:
                    kv_pairs[key] = value
                elif key == 'origin':
                    x, y, z = map(float, str(value).split())
                    origin = [x, y, z]
            cycler_sprite = gsm.Entity('cycler_sprite', origin, kv_pairs)
            cycler_list.append(cycler_sprite)
            entity.properties = {}
    m.add_entity(cycler_list)
    
    file_name, _ = os.path.splitext(os.path.basename(map_file))
    
    output_file = f"{file_name}.map"
    print(" cycler_sprite conversion completed !!! ")
    gsm.save_map(m, output_file)
    print(f"Modified: '{output_file}' \n ---------------------------------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert entities with 'to_cycler' attribute to cycler_sprite")
    parser.add_argument("map_file", help="Path to the input .map file")
    args = parser.parse_args()
    main(args.map_file)
