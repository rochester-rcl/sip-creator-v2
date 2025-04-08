import os
import shutil
import csv
import pathlib
import hashlib
from zipfile import ZipFile

def disable_all(window):
    window['-CSV_PATH-'].update(disabled=True)
    window['-FILE_BROWSE_BUTTON-'].update(disabled=True)
    window['-OUTPUT-'].update(disabled=True)
    window['-FOLDER_BROWSE_BUTTON-'].update(disabled=True)
    window['-OUTPUT-'].update(disabled=True)
    window['-ABOUT-'].update(disabled=True)
    window['-EXIT-'].update(disabled=True)
    window['-LETS_GOOOO-'].update(disabled=True)

def enable_all(window):
    window['-CSV_PATH-'].update(disabled=False)
    window['-FILE_BROWSE_BUTTON-'].update(disabled=False)
    window['-OUTPUT-'].update(disabled=False)
    window['-FOLDER_BROWSE_BUTTON-'].update(disabled=False)
    window['-OUTPUT-'].update(disabled=False)
    window['-ABOUT-'].update(disabled=False)
    window['-EXIT-'].update(disabled=False)
    window['-LETS_GOOOO-'].update(disabled=False)

# CSV INDICES:
# IDENTIFIER - 0 | XIP TITLE - 1 |  XIP DESCRIPTION - 2 | SECURITY TAG - 3 | PRES FILE EXT - 4 | ACC FILE EXT - 5
# ID 1 LABEL - 6 | ID 2 LABEL - 7 | ID 2 VALUE - 8 | ID 3 LABEL - 9 | ID 3 VALUE - 10 | ID 4 LABEL - 11 | ID 4 VALUE - 12

def main_process(window, status_bar, project_csv_value, project_dir_value, progress_bar):
    status_bar.update(value='')
    for del_file in os.listdir(path = project_dir_value):
        del_path = os.path.join(project_dir_value, del_file)
        if del_file in ('Thumbs.db', 'desktop.ini'):
            os.remove(del_path)
    count = 0
    fhand = open(project_csv_value, 'r', newline='', encoding='utf8')
    csv_reader = csv.reader(fhand, delimiter=',', quotechar='"')
    next(csv_reader)
    for row in csv_reader:
        identifer = row[0].strip()
        if identifer == '':
            count += 1
            progress_bar.update(current_count=count)
            continue
        xip_title = row[1].strip()
        xip_desc = row[2].strip()
        sec_tag = row[3].strip()
        pres_file_ext = row[4].strip()
        acc_file_ext = row[5].strip()
        id_1_label = row[6].strip()
        id_2_label = row[7].strip()
        id_2_value = row[8].strip()
        id_3_label = row[9].strip()
        id_3_value = row[10].strip()
        id_4_label = row[11].strip()
        id_4_value = row[12].strip()
        status_bar.update(value = 'Current Asset: ' + identifer)
        window.refresh()
        asset_path = os.path.join(project_dir_value, identifer)
        os.mkdir(path=asset_path)
        if acc_file_ext != '':
            os.mkdir(os.path.join(asset_path, 'Representation_Access'))
        if pres_file_ext != '':
            os.mkdir(os.path.join(asset_path, 'Representation_Preservation'))
        for file in os.listdir(path = project_dir_value):
            file_path = os.path.join(project_dir_value, file)
            if file.startswith(identifer):
                if acc_file_ext != '' and file.endswith(acc_file_ext):
                    os.mkdir(os.path.join(asset_path, 'Representation_Access', file.split('.')[0].strip()))
                    shutil.move(file_path, os.path.join(asset_path,'Representation_Access', file.split('.')[0].strip(), file))
                if pres_file_ext != '' and file.endswith(pres_file_ext):
                    os.mkdir(os.path.join(asset_path,'Representation_Preservation', file.split('.')[0].strip()))
                    shutil.move(file_path, os.path.join(asset_path, 'Representation_Preservation', file.split('.')[0].strip(), file))
        path_paxstage = os.path.join(asset_path, 'pax_stage')
        os.mkdir(path_paxstage)
        if acc_file_ext != '':
            shutil.move(os.path.join(asset_path, 'Representation_Access'), path_paxstage)
        if pres_file_ext != '':
            shutil.move(os.path.join(asset_path, 'Representation_Preservation'), path_paxstage)
        zip_dir = pathlib.Path(path_paxstage)
        pax_path = os.path.join(asset_path, identifer + '.pax.zip')
        pax_obj = ZipFile(pax_path, 'w')
        for file_path in zip_dir.rglob("*"):
            pax_obj.write(file_path, arcname = file_path.relative_to(zip_dir))
        pax_obj.close()
        shutil.rmtree(path_paxstage)
        if xip_title == '':
            xip_title = identifer
        pax_hand = open(pax_path, 'rb')
        pax_read = pax_hand.read()
        sha1_checksum = hashlib.sha1(pax_read).hexdigest()
        pax_hand.close()
        opex1 = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <opex:OPEXMetadata xmlns:opex="http://www.openpreservationexchange.org/opex/v1.0">
        <opex:Properties>
            <opex:Title>{xip_title}</opex:Title>
            <opex:Description>{xip_desc}</opex:Description>
            <opex:Identifiers>
                <opex:Identifier type="{id1_label}">{id1_value}</opex:Identifier>\n'''.format(xip_title=xip_title, xip_desc=xip_desc, id1_label=id_1_label, id1_value=identifer)
        opex2 = ''
        if id_2_label != '' and id_2_value != '':
            opex2 += '\t\t\t\t<opex:Identifier type="{id2_label}">{id2_value}</opex:Identifier>\n'.format(id2_label=id_2_label, id2_value=id_2_value)
        if id_3_label != '' and id_3_value != '':
            opex2 += '\t\t\t\t<opex:Identifier type="{id3_label}">{id3_value}</opex:Identifier>\n'.format(id3_label=id_3_label, id3_value=id_3_value)
        if id_4_label != '' and id_4_value != '':
            opex2 += '\t\t\t\t<opex:Identifier type="{id4_label}">{id4_value}</opex:Identifier>\n'.format(id4_label=id_4_label, id4_value=id_4_value)
        opex3 = '''\t\t\t</opex:Identifiers>
            <SecurityDescriptor>{sec_tag}</SecurityDescriptor> 
        </opex:Properties>
        <opex:Transfer>
            <opex:Fixities>
                <opex:Fixity type="SHA-1" value="{sha1_checksum}"/>
            </opex:Fixities>
        </opex:Transfer>
    </opex:OPEXMetadata>'''.format(sec_tag=sec_tag, sha1_checksum=sha1_checksum)
        opex = opex1 + opex2 + opex3
        opex = opex.replace(' & ', ' and ') # example: &quot; = "
        pax_md_hand = open(os.path.join(asset_path, identifer + '.pax.zip.opex'), 'w', encoding='utf8')
        pax_md_hand.write(opex)
        pax_md_hand.close()
        shutil.move(os.path.join(asset_path, identifer + '.pax.zip'), os.path.join(project_dir_value, identifer + '.pax.zip'))
        shutil.move(os.path.join(asset_path, identifer + '.pax.zip.opex'), os.path.join(project_dir_value, identifer + '.pax.zip.opex'))
        shutil.rmtree(asset_path)
        count += 1
        progress_bar.update(current_count=count)
        window.refresh()
    fhand.close()
    os.startfile(project_dir_value)
