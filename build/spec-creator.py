# -*- coding: utf-8 -*-
# combines spec files so that multiple executables can share its dependencies
# trying to avoid size bloat
# https://pyinstaller.readthedocs.io/en/v3.3.1/spec-files.html#multipackage-bundles
# https://github.com/pyinstaller/pyinstaller/issues/1358

from pathlib import Path
import re

MAIN_EXEFILE_NAME = 'twitter_image_dl'
SPECPATH = Path(__file__).resolve().parents[1] / 'build' / 'spec'
SPECFILE_DL = SPECPATH / 'dl.spec'
SPECFILE_GUI = SPECPATH / 'twitter_image_dl.spec'
SPECFILE_BUILD = SPECPATH / 'build.spec'
SPECFILE_BEGINNING ="""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

"""

def parse_specfile(filepath):
    analyze_clause = []
    pyz_exe_clause = []
    coll_clause = []

    with filepath.open(mode='r', encoding='utf-8') as f:
        analyze_clause_pattern = re.compile(r'^a = .*')
        pyz_clause_pattern = re.compile(r'^pyz = .*')
        coll_caluse_pattern = re.compile(r'^coll = .*')
        current_clause = None

        for line in f:
            if analyze_clause_pattern.match(line):
                current_clause = analyze_clause
            if pyz_clause_pattern.match(line):
                current_clause = pyz_exe_clause
            if coll_caluse_pattern.match(line):
                current_clause = coll_clause
            if current_clause is not None:
                current_clause.append(line)

    return [
        ''.join(analyze_clause),
        ''.join(pyz_exe_clause),
        ''.join(coll_clause)
    ]

def rename_object(parsed_file, prefix):
    [analyze_clause, pyz_exe_clause, coll_clause] = parsed_file
    object_names = ['a', 'pyz', 'exe']

    for object_name in object_names:
        new_name = prefix + object_name

        analyze_clause = re.sub(
            f'{object_name} = ',
            f'{new_name} = ',
            analyze_clause
        )
        pyz_exe_clause = re.sub(
            f'\\b{object_name}\\b',
            f'{new_name}',
            pyz_exe_clause
        )
        coll_clause = re.sub(
            f'\\b{object_name}\\b',
            f'{new_name}',
            coll_clause
        )

    return [analyze_clause, pyz_exe_clause, coll_clause]

def merge_coll(*renamed_clauses):
    spec_objects_argument_pattern = re.compile(r'COLLECT\((.*?)[ ]+strip=False', re.DOTALL)
    rest_argument_pattern = re.compile(r'(strip=False.*)\)', re.DOTALL)
    arguments = ''

    for clauses in renamed_clauses:
        coll_clause = clauses[2]
        arguments += spec_objects_argument_pattern.search(coll_clause)[1]
        arguments += 15 * ' ' # maintain indentation level
    arguments += rest_argument_pattern.search(renamed_clauses[0][2])[1]

    return f'coll = COLLECT({arguments})'

parsed_gui = parse_specfile(SPECFILE_GUI)
parsed_dl = parse_specfile(SPECFILE_DL)

gui_prefix = 'gui_'
renamed_gui = rename_object(parsed_gui, gui_prefix)
dl_prefix = 'dl_'
renamed_dl = rename_object(parsed_dl, dl_prefix)
merge_clause = f'MERGE( ({gui_prefix}a, "gui", "twitter_image_dl"), ({dl_prefix}a, "dl", "dl") )\n'
merged_coll = merge_coll(renamed_gui, renamed_dl)

with SPECFILE_BUILD.open('w', encoding='utf-8') as f:
    f.write(SPECFILE_BEGINNING)
    f.write(renamed_gui[0])
    f.write(renamed_dl[0])
    f.write('\n')
    f.write(merge_clause)
    f.write('\n')
    f.write(renamed_gui[1])
    f.write(renamed_dl[1])
    f.write(merged_coll)

def test_specfile():
    # testing that I am getting what i want
    SPECFILE_BUILD_REF = SPECPATH / 'build.spec.bak'

    with SPECFILE_BUILD.open('r', encoding='utf-8') as f:
        built_content = f.read()

    with SPECFILE_BUILD_REF.open('r', encoding='utf=8') as f:
        reference_content = f.read()

    assert built_content == reference_content

# test_specfile()
