from library.cli import *

from library.utils import register, format_vesrion

code = w_input(f"Insert the exact folder name of the course: \n{os.listdir('./MC_input')}\n--> ", search_MC)

in1 = "./MC_input/"+ code + "/"

in2 = str(y_n_comp(w_input("You want to use the chrome bot? (y/n): \n--> ", y_n_conf)))

exec(f"call .\\X2E.venv\\Scripts\\activate.bat & python .\\Structurer\\main.py {in1} {in2} && python .\\xnf2edx_cli\\main.py .\\Excel_output\\{code}.xlsm")

exec(f"xcopy .\\xnf2edx_cli\\data\\output\\{code}\\{code} .\\Excel_output\\{code}\\ /e")

move_media(code)

tar_name = format_vesrion(code)

make_tarfile(f".\\Final_output\\{tar_name}.tar.gz", f".\\Excel_output\\{code}")

print(f"\nTAR.GZ CREATED: {tar_name}\n")

if y_n_comp(w_input("Clean the enviroment? (y/n): \n--> ", y_n_conf)):
    clean_env(code)
    print("\nEnviroment cleaned\n")

from library.utils import register

register()

exit()