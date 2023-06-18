import sys
from pathlib import Path
import shutil 
from uuid import uuid4

CATEGORIES = {"Audio": [".mp3", ".ogg", ".wav", ".amr", ".aiff"],
              "Documents": [".doc", ".docx", ".xlsx", ".pptx", ".pdf", ".txt"],
              "Images": [".jpeg", ".png", ".jpg", ".svg"],
              "Video": [".avi", "mp4", ".mov", ".mkv"],
              "Archives": [".zip", ".gz", ".tar"],
              "Other": []}

CYRILLIC_SYMBOLS = "абвгґдеёєжзиіїйклмнопрстуфхцчшщъыьэюя"

TRANSLATION = ("a", "b", "v", "h", "g", "d", "e", "e", "ie" "zh", "z",
               "y", "i", "yi", "y", "j", "k", "l", "m", "n", "o", "p",
               "r", "s", "t", "u", "f", "kh", "ts", "ch", "sh", "shch",
               "", "y", "", "e", "yu", "ya")

BAD_SYMBOLS = ("!", "#", "$", "%", "&", "(", ")", "*", "+", ",", " ", "-", ":", ";", "<", "=", ">", "@", "[", "]", "^", "{", "}", "|")

TRANS = {}
for c, t in zip(list(CYRILLIC_SYMBOLS), TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

for i in BAD_SYMBOLS:
    TRANS[ord(i)] = "_"

def normalize(name: str) -> str:
    trans_name = name.translate(TRANS)
    return trans_name

def get_extensions(path: Path):
    ext_str = " "
    for item in path.iterdir():
        if item.is_file():
            if item.suffix[1:] not in ext_str:
                ext_str += " " + item.suffix[1:]
    return ext_str


def report(path: Path):    
    for item in path.iterdir():
        if item.is_dir() and item.name in CATEGORIES.keys():
            print("{}".format(" " * 60))
            print("|{}".format("*" * 60))
            print("|{:^60}".format(item.name))
            print("|{}".format("-" * 60))
            print("|{:<60}".format(get_extensions(item)))
            print("|{}".format("-" * 60))
            for it in item.iterdir():
                if it.is_file():
                    print("|{:<60}".format(it.name))
            print("|{}".format("-" * 60))
            

def unpack_archives(path: Path):
    arch_path = path.joinpath("Archives")
    for arch in arch_path.iterdir():
        try:     
            shutil.unpack_archive(arch, arch_path.joinpath(arch.stem), arch.suffix[1:])
        except shutil.ReadError as er:
            print(f"File {er}")
        except ValueError as er:
            print(f"File {arch} {er}")
        
def del_empty_folders(path: Path) -> None:
    for item in path.iterdir():        
        if item.is_dir():
            del_empty_folders(item)
            if not any(item.iterdir()):
                try:
                    item.rmdir()
                except UnicodeEncodeError as er:
                    print(f"{er}")
                except OSError as er:
                    print(f"{er}")


def move_file(file: Path, path: Path, categorie: str) -> None:    
    target_dir = path.joinpath(categorie)
    if not target_dir.exists():
        target_dir.mkdir()
    new_name = target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}")
    if new_name.exists():        
        new_name = new_name.with_name(f"{new_name.stem}_{uuid4()}{file.suffix}")
    if file.parent != target_dir:
        file.replace(new_name)

def get_categorie(file: Path) -> str:
    ext = file.suffix.lower()
    for categorie, extensions in CATEGORIES.items():
        if ext in extensions:
            return categorie
    return "Other"

def sort_folder(path: Path, item_path: Path) -> None:    
    for item in item_path.iterdir():        
        if item.is_dir():
            if item.name in CATEGORIES.keys():                
                continue
            sort_folder(path, item)
        elif item.is_file():                          
            categorie = get_categorie(item)
            move_file(item, path, categorie)
    
def main():
    try:
        path = Path(sys.argv[1])        
    except IndexError as er:
        return f"Specify the folder to sort"
    
    if not path.exists():
        return f"Folder with path {path} doesn't exist."
    
    sort_folder(path, path)        
    del_empty_folders(path)
    unpack_archives(path)
    report(path)
    return "Sorting is complete"

if __name__ == "__main__":
    print(main())
   
