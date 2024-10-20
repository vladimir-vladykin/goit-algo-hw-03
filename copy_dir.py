import sys
from pathlib import Path
import shutil

DEFAULT_DST_DIR_NAME = "dist"
FALLBACK_FILE_FORMAT = "unknown"

def main():
    # collect src and dst directories paths
    if len(sys.argv) > 1:
        # we expect first arg after script name is gonna be path to the source dir,
        # and the second optional arg is path to the destination dir
        src_dir_path = sys.argv[1]
        dst_dir_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_DST_DIR_NAME
        
    else:
        print("No valid arguments provided.\nProgram expect path to source directory as first argument, and path to desination directory as second one.")
        return


    # validate paths
    src_dir = Path(src_dir_path)
    dst_dir = Path(dst_dir_path)    

    # if dst dir does not exists, let's just create destination dir for user
    if not dst_dir.exists():
        print(f"Destination directory does not exist, creating...\n")
        dst_dir.mkdir(parents=True)

    # ensure that paths lead to dirs, not files
    if not src_dir.is_dir():
        print(f"Error. There's not valid source directory by path {src_dir_path}.")
        return
    if not dst_dir.is_dir():
        print(f"Error. There's not valid source directory by path {dst_dir_path}.")
        return

    
    # so here we have two valid paths to existing directories, let's perform copying
    copy_dir_with_sorting(src_dir, dst_dir)


def copy_dir_with_sorting(src_dir, dst_dir):
    # 1. Traverse src dir and collect all files
    # 2. Copy files to dst dir, with grouping by file format (so we ignore original
    # hierarchy of dirs in src_dir, instead we create flat structure in dst_dir)

    all_files = collect_all_files_from_dir(src_dir)
    
    if len(all_files) == 0:
        print("No files found in source directory, nothing to copy")
        return

    print(f"Perform copying from {src_dir}...")
    copy_files_into_dir_with_sorting(dst_dir, all_files)
    print("Copying ended")


def collect_all_files_from_dir(src_dir):
    # will contain all files found in src_dir
    dir_files_list = []

    for dir_item in src_dir.iterdir():
        if dir_item.is_file():
            # this is file, add to list so it will be copied later
            dir_files_list.append(dir_item)
        if dir_item.is_dir():
            # this is dir, let's add to list all its files
            dir_files_list.extend(collect_all_files_from_dir(dir_item))
            
    return dir_files_list


def copy_files_into_dir_with_sorting(dst_dir, all_files):
    for src_file in all_files:
        # for each file:
        # 1. figure out it's format
        # 2. based on that create sub-directory (if not exists)
        # 3. perform copy
        # 4. log + proceed to next file in case of error

        format = get_file_format(src_file)
        
        sub_dir_path = dst_dir.name + "/" + format
        sub_dir = Path(sub_dir_path)
        sub_dir.mkdir(exist_ok = True)

        dst_file_path = sub_dir_path + "/" + src_file.name
        dst_file = Path(dst_file_path)

        try:
            shutil.copyfile(src_file, dst_file)
        except:
            print(f"Error while copying file {dst_file_path}, proceed to next file")


def get_file_format(file) -> str:
    split_symbol = '.'
    if split_symbol not in file.name:
        # file with no format, let's group such files into separate folder
        return FALLBACK_FILE_FORMAT
    
    _, format = file.name.split(split_symbol)
    return format



if __name__ == "__main__":
    main()