import os
import tarfile

# create a tar.gz file from a directory
def make_tarfile(output_filename, source_dir):
    # output_filename: name or path of the tar.gz
    # source_dir: directory to compress
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

_ = type(lambda x: True) # Only for aplaying restrictive use

# Like a input function but it's in loop until the condition is satisfied
def w_input(text : str, condition: _ = lambda x: True) -> str:
    # text: prompt text or question
    # condition: a function to satisfy (input: str)
    # output: the input return
    inp = input(text)
    while not condition(inp):
        print("Try again")
        inp = input(text)
    return inp

# a condition if the input is in the MC_input carpet
def search_MC(course: str) -> bool:
    # course: the course inside MC_input
    try:
        os.listdir("./MC_input").index(course)
        return True
    except:
        return False

# a condition for a bool prompt
def y_n_conf(x: str) -> bool:
    # x: the input
    return any(map(lambda s: x.lower().strip() == s, ["yes", "no", "y", "n", "si", "s"]))

# transform a input in a bool
def y_n_comp(x: str) -> bool:
    # x: the input
    if any(map(lambda s: x.lower().strip() == s, ["yes", "y", "si", "s"])):
        return True
    if any(map(lambda s: x.lower().strip() == s, ["no", "n"])):
        return False

# executes a CMD command
def exec(command: str):
    # command: the CMD prompt
    err = os.system(command)
    assert err == 0, "Error in {exec()} command: " + command

# copy the files to the Excel_output carpet
def copy_output(code: str):
    # code: the code of the course
    try:
        exec(f"xcopy .\\xnf2edx_cli\\data\\output\\{code}\\{code} .\\Excel_output\\{code}\\ /e")
    except AssertionError:
        print(f"Error in copy_output({code})")
        exit(1)

# move all the media into the future tar.gz carpet
def move_media(code: str):
    # code: the code of the course
    path = "./MC_input/"+ code + "/"

    files = []
    for i in list(filter(lambda x: x.find(".") == -1, os.listdir(path))):
        files += [path + i + "/" + j for j in list(filter(lambda x: x.find(".mp4") == -1 and x.find(".mov") == -1 and x.find(".mkv") == -1, os.listdir(path + i)))]

    f_files = str(files).replace("', '","\" \"").replace('[\'','(\"').replace('\']','\")').replace("/","\\")

    try:
        exec(f"for %I in {f_files} do copy %I \".\\Excel_output\\{code}\\static\" ")
    except AssertionError:
        print(f"Error in move_media({code})")
        exit(1)

# clean all the auxiliar files
def clean_env(code: str):
    # code: the code of the course
    commands = { # dict[command: error code]
        f"erase /s /q .\\xnf2edx_cli\\data\\output\\{code}": 1,
        f"rmdir /s /q .\\xnf2edx_cli\\data\\output\\{code}": 1,
        f"erase /s /q .\\Excel_output\\{code}\\": 1,
        f"rmdir /s /q .\\Excel_output\\{code}": 1,
        f"erase /q .\\Excel_output\\{code}.xlsm": 1
    }
    for i in commands.keys():
        commands[i] = os.system(i)
    
    if any([i > 0 for i in commands.values()]):
        print(f"Error in clean_env({code})")
        print("Please revise it manualy, it could block some directorys directly related")
        exit(1)