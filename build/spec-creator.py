# -*- coding: utf-8 -*-

from pathlib import Path
import re

SPECPATH = Path(__file__).resolve().parents[1] / 'build' / 'spec'
SPECPATH_DL = SPECPATH / 'twitter_image_dl.spec'
SPECPATH_GUI = SPECPATH / 'gui.spec'
SPECPATH_BUILD = SPECPATH / 'build.spec'
SPECFILE_BEGINNING ="""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

"""

def parse_specfile(filepath):
    analyze_clause = []
    rest = []

    with filepath.open(mode='r', encoding='utf-8') as f:
        analyze_clause_pattern = re.compile(r'^a = .*')
        pyz_clause_pattern = re.compile(r'^pyz = .*')
        current_clause = None

        for line in f:
            if analyze_clause_pattern.match(line):
                current_clause = analyze_clause
            if pyz_clause_pattern.match(line):
                current_clause = rest
            if current_clause is not None:
                current_clause.append(line)

    return [ ''.join(analyze_clause), ''.join(rest) ]

def rename_object(parsed_file, prefix):
    [ analyze_clause, rest ] = parsed_file
    object_names = ['a', 'pyz', 'exe', 'coll']

    for object_name in object_names:
        new_name = prefix + object_name

        analyze_clause = re.sub(
            f'{object_name} = ',
            f'{new_name} = ',
            analyze_clause
        )
        rest = re.sub(
            f'\\b{object_name}\\b',
            f'{new_name}',
            rest
        )

    return [ analyze_clause, rest ]

parsed_dl = parse_specfile(SPECPATH_DL)
parsed_gui = parse_specfile(SPECPATH_GUI)

dl_prefix = 'dl_'
renamed_dl = rename_object(parsed_dl, 'dl_')
gui_prefix = 'gui_'
renamed_gui = rename_object(parsed_gui, 'gui_')

merge_clause = f'MERGE( ({gui_prefix}a, "gui", "gui"), ({dl_prefix}a, "dl", "twitter_image_dl") )\n'

with SPECPATH_BUILD.open('w', encoding='utf-8') as f:
    f.write(SPECFILE_BEGINNING)
    f.write(renamed_dl[0])
    f.write(renamed_gui[0])
    f.write('\n')
    f.write(merge_clause)
    f.write('\n')
    f.write(renamed_dl[1])
    f.write(renamed_gui[1])
