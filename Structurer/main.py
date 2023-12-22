import os
import datetime

from library.utils import get_args, get_doc
from library.extras import Doc, get_logo
from library.control import Find, revise

path = os.getcwd() # working directory

MC_path, bot_able = get_args([str, str],[
    "The Course Directory path used as input",
    "If the user wants to use Chrome (True/False)"
]) # get the argument at the execution

Find.set_path(MC_path) # set the path for revision and file management

MC_code = MC_path.split("/")[2] # extract the code
MC_sections = ["Template", "Tests"] # the sections in the excel
doc_word = get_doc(MC_code) # get the microcredential document


from library.excel_read import Excel_read, find_excel

excel_name = find_excel(MC_path, MC_code) # find the excel file
excel_in = Excel_read(MC_path + excel_name, *MC_sections) # open the excel

MC_title, MC_lecturer, MC_inst = excel_in.get_info() # get the general info
Tests = excel_in.get_tests()
Units = excel_in.get_units()

excel_in.save()
excel_in.close()

evaluation = revise(MC_code, Units, Tests) # revise if it's all in order
# evaluation: a string that describes the scoring method


logo = get_logo("./Data/res4city-logo-rectangle.svg") # get the logo in HTML

document = Doc(doc_word) # open the word


bot_able = bot_able == str(True)

if bot_able:
    from library.YT_bot import Bot # test the bot
    Bot.test()
    # (Unit, MC_code, MC_name, Overview, Inst, Lecturers)
    desc_plantilla = "\n\n".join([
        "This video belongs to a Master of RES4City in https://www.res4city.eu/",
        "Unit: {0}",
        "Course: {1}",
        "{2}",
        "{3}\n",
        "Lecturers: {4}",
        "{5}"
    ])

    desc_plantilla = desc_plantilla.format(
        "{0}", 
        MC_code, 
        MC_title, 
        document.desc_overview, 
        MC_inst, 
        MC_lecturer
    )

    YTbot = Bot(MC_path) # open the browser

    if len([i[6] for i in Units if type(i[6]) == list]) > 0:
        # if there's a video to upload, upload it
        excel_in.upload_videos(YTbot, Units, desc_plantilla)

del excel_in # it's not useful anymore

# check if all the videos are uploaded
_ = [i[6] for i in Units if i[6] != None]
assert all(map(lambda x: type(x) == str and len(x) == 11, _)), f"No estan todos los videos subidos: {_}"
del _


from library.excel_write import Excel_write

excel_out = Excel_write(MC_path) #create a copy of the template

datos_generales = [ # The principal page of the excel
    [
        MC_code,
        MC_title,
        datetime.datetime(2024, 1, 1, 0, 0),
        datetime.datetime(2024, 1, 1, 0, 0),
        "English"
    ],
    [
        MC_lecturer, # Intro_dic["Lecturers"],
        None,
        document.description_dic["Background of the proposed micro-credential"] + "\n\n" + document.description_dic["Overview of the micro-credential"],
        document.description_dic["Prerequisites"],
        document.description_dic["Learning objectives"],
    ],
    [
        MC_inst, # Intro_dic["Institution"],
        document.description_dic["ECTS"].strip() + " ECTS",
        None,
        None,
        evaluation
    ],
    [
        None,
        "Z-Posgrade",
        "2024-001",
        "No",
        logo
    ],
    [
        datetime.datetime(2024, 1, 1, 0, 0),
        None,
        None,
        None,
        "Si"
    ]
]

excel_out.upload(datos_generales, Units, Tests) # load all the data

excel_out.save()
excel_out.close() # Save the excel
del excel_out

print("\nStructure Completed!\n")

if bot_able:
    YTbot.list_name(MC_code, MC_title)

    input("Press Enter to close the bot\n")
    print("Closing... (this can be delayed due uploading videos)\n")
    del YTbot