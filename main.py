# sort script
import shutil
from pathlib import Path
import os
import string
from zipfile import ZipFile
import sys
import re


data_formats = {
    "images": ('.jpeg', '.png', '.jpg', '.svg', '.bmp'),
    "video": ('.avi', '.mp4', '.mov', '.mkv'),
    "documents": ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
    "audio": ('.mp3', '.ogg', '.wav', '.amr'),
    "archives": ('.zip', '.gz', '.tar'),
    "unknown": None}



def normalize(name):
    translit = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
                'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
                'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
                'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': '', 'ь': '', 'э': 'e',
                'ю': 'u', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO',
                'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
                'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
                'Ц': 'C', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': '', 'Ь': '', 'Э': 'E',
                'Ю': 'U', 'Я': 'YA', ',': '_', '?': '_', ' ': '_', '~': '_', '!': '_', '@': '_', '#': '_',
                '$': '_', '%': '_', '^': '_', '&': '_', '*': '_', '(': '_', ')': '_', '-': '_', '=': '_', '+': '_',
                ':': '_', ';': '_', '<': '_', '>': '_', '\'': '_', '"': '_', '\\': '_', '/': '_', '№': '_',
                '[': '_', ']': '_', '{': '_', '}': '_', 'ґ': 'g', 'ї': 'ii', 'є': 'e', 'Ґ': 'G', 'Ї': 'ii',
                'Є': 'E', '—': '_'}
    for key in translit:
        name = name.replace(key, translit[key])
        name = re.sub(r'\W', '_', name)
    return name


def remove_folders(path):
    for d in os.listdir(path):
        a = os.path.join(path, d)
        if os.path.isdir(a):
            remove_folders(a)
            if not os.listdir(a):
                os.rmdir(a)



def sort_files(glob_object: Path) -> str:
    folders = {
        "images": [],
        "documents": [],
        "archives": [],
        "audio": [],
        "video": [],
        "unknown": []}

    for item in glob_object:
        if item.is_file():
            file_suffix = item.suffix
            if file_suffix in data_formats["images"]:
                folders["images"].append(item)
            elif file_suffix in data_formats["documents"]:
                folders["documents"].append(item)
            elif file_suffix in data_formats["archives"]:
                folders["archives"].append(item)
            elif file_suffix in data_formats["audio"]:
                folders["audio"].append(item)
            elif file_suffix in data_formats["video"]:
                folders["video"].append(item)
            else:
                folders["unknown"].append(item)
    return folders


def move_files(path: str):
    work_dir = Path(path).resolve()
    dict_files = sort_files(work_dir.glob('**/*'))
    for file_types, files in dict_files.items():
        for f in files:
            file = Path(f)
            suffix = file.suffix
            normal_name = normalize(file.stem) + suffix
            if not Path(work_dir, file_types).exists():
                Path(work_dir, file_types).mkdir()
            if not Path(work_dir, file_types).exists():
                Path(work_dir, file_types).mkdir()
            file.replace(Path(work_dir, file_types, normal_name))
            if file_types == "archives":
                try:
                    shutil.unpack_archive(Path.joinpath(work_dir, file), Path.joinpath(work_dir, file_types))
                    file.replace(Path(work_dir, file_types, normal_name))
                except Exception:
                    continue

    remove_folders(path)


def main():
    path = None
    try:
        path = sys.argv[1]
    except IndexError:
        path = input('Enter path to folder:')
    move_files(path)
    print(f'Files in folder: {path} were sorted successfully!')


if __name__ == '__main__':
    main()

