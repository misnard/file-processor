from progress.bar import Bar
from collections import Counter
import os
import shutil


class file_object():
    def __init__(self):
        self.types = {
            "Video": ("avi", "mp4", "mov", "mpg", "mp2", "m2p", "dif", "vob", "mkv", "flv", "mpeg", "asf", "ts")
        }

    def get_type(self, file):
        ext = file.split(".")[-1]

        for t, extensions in self.types.items():
            if ext in extensions:
                return t


class Finder():
    def __init__(self, start_path):
        self.start_path = start_path

    def crawler(self, walk):
        fo = file_object()
        files_dict = {}
        if walk:
            for dirpath, _, files in os.walk(self.start_path):
                for f in files:
                    f = dirpath + "/" + f
                    if os.path.isfile(f):
                        ftype = fo.get_type(f)

                        if ftype is not None:
                            files_dict.update({f: ftype})

        else:
            for path in os.listdir(self.start_path):
                f = os.path.join(self.start_path, path)
                if os.path.isfile(f):
                    ftype = fo.get_type(f)

                    if ftype is not None:
                        files_dict.update({f: ftype})

        return files_dict


print("""
  ______    _              _                    _               
 (_) |  o  | |            | |               o  | | o            
    _|_    | |  _     __  | |  __,   ,   ,     | |     _   ,_   
   / | ||  |/  |/    /    |/  /  |  / \_/ \_|  |/  |  |/  /  |  
  (_/   |_/|__/|__/  \___/|__/\_/|_/ \/  \/ |_/|__/|_/|__/   |_/
                                               |\               
                                               |/               
""")

base_path = "test"
dest_path = ""
walk = True

# First we count numbers of folder in this folder

sub_folders = ["."]
for path in os.listdir(base_path):
    if os.path.isdir(os.path.join(base_path, path)):
        sub_folders.append(os.path.join(base_path, path))

folder_count = len(sub_folders)
print(f"{folder_count} folder found here.")
print("")

# Second, process current folder without sub folders

print(sub_folders)  # del
for folder in sub_folders:
    print(f"Process folder => {folder}")

    finder = Finder(folder)
    files = finder.crawler(walk)
    found_types_count = Counter(files.values())

    print(f"Found {len(files)} files:")
    for t, count in found_types_count.items():
        print(f"'{t}': {count}")
    print("")

    bar = Bar("Processing", max=len(files))
    for f, t in files.items():
        file_name = f.split("/")[-1]
        shutil.move(f, f"{dest_path}{t}/{file_name}")
        bar.next()

    bar.finish()

    # Third reorder files

    print(files)
