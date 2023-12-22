# edX_environment

This repository works for creating **OpenEdx** _MicroCredential_ courses compressed in _tar.gz_.

## MC format
Must have the a proposal of the course into the subfolder named after your institution. All ot that into `MC proposal for partners`

The MC work this way:
1. A folder with it's code to reconise them.
2. Inside a Section-divided subfolders with all the videos and extra material.
 - Videos: `MCXX-S1-Sub1-U1.mp4`.
 - Reading: any name specificated in the excel, if not `MCXX-S1-Sub1-U1.pdf`.
 - Other: any name specified in the excel.
* MC: identifies the microcredential (use the MC code assigned)
* S: identifies the section (thus, it must correspond to the parent folder, e.g., S1 for “section 1”)
* Sub: identifies the subsection
* U: identifies the unit
3. An Excel with all the information as the example

# Use

## Configuration
* Python 3.10 or later need to be installed
* _X2E.venv_ can be recreated in _"dependences.yaml"_ or _"requeriment.txt"_.
* Check that in "Data.csv" you have the information of all courses and universities.
* Install **Chrome Beta** (recommended) and place its address in _"chrome_options.json"_. You also need the diriver _"chromedriver.exe"_ of the appropriate version. In case is not intalled, you cant use de YouTube or Chrome bot.
* Inside _"Data/"_ must be the logo of the course (must be change from the code)

## Execution
* Place the course folder in the "MC_input" folder.
* Execute the file "go.bat" from the CMD. (**Only Windows**).
* Enter the **exact** name of the folder you used (this name will have the tar.gz).
* Answer the Chrome option (you can not use it, specially if it's not configurated).
* Answer if you want to clean all the generated auxiliary files (In the "Excel_output" folder and some other auxiliar directories).
* Pick up the tar.gz from the "Final_output" folder.

## Maintenance
* Chrome may be updated and you may need to update the driver for the desired compatibility:
* * _To do this, you have to change the `chromedriver.exe` file for the new one_
* To work around with the Chrome bot you have to use the _"YT_editor.ipynb"_ file.
* Inside ".vscode" you can configure its debug session.
* **ALERT!** The excels open extension doesn't work properly and prevents to open files, even if they have the correct information inside.
* If there are many errors you can run step by step with "Step_by_step.ipynb".

# Behavior
### Start
First the "go.bat" is executed, which activates the environment and executes "start.py".
Inside "start.py" all the prompts are made and "main.py" with its appropriate arguments, as well as "xnf2edx_cli" are executed in cascade. Then all the outputs are directed to "Excel_output" and in "Final_output" the tar.gz is formed. Then everything is cleaned up.

### Main
1.	Read
 * We import libraries and extract the arguments of the execution; we look for the path and the code of the course through the name of the folder entered.
 * We create functions and utilities.
 * We open the "Docs.csv" to find the corresponding "MC proposal from partners".
 * We go to "Template" and extract the institute, the title and the teacher.
 * Then, also by rows, we read the units. We generate another matrix.
 * We close the files correctly.
2.	Revision
 * We generate functions for the check.
 * We check that the number of tests matches the unit assessments.
 * We check that the assessments add up to 100% in total.
 * We search all the documents to make sure that none are missing.
 * Repeat the process for the videos.
 * We stop the execution in case any condition is not fulfilled.
3.	Upload
 * We read the svg of the logo and the docx.
 * If you haven't been prompted to use Chrome, we jump to Write directly.
 * We create the upload bot.
 * Formalise the description of the videos
 * One by one, we upload the videos and display the links on the command line.
 * Check that they have all been uploaded, and leave Chrome open for now.
4.	Writing
 * Create a copy of "TemplateXNF.xlsm" to convert to OpenEdx format.
 * We write the course description.
 * We filter the tasks and classify them by type.
 * Upload the task types.
 * We write the units and lessons.
 * From the tests, we write the problems.
 * We close the copy correctly in "Excel_output".
5.	Close
 * If you haven't been prompted to use Chrome, we close the programme.
 * We wait until all the videos are uploaded.
 * We modify the characteristics of the playlist.
 * We open the closing page to ensure that it does not close prematurely.
 * When the button is pressed, the programme will close.

### Compiling
Once we have finished the "main.py" we have the Excel of the course. All that remains is to run the course creator with the new Excel and check that there are no errors.
Once we have checked that everything is in good conditions, we copy the web in "Excel_output" and we introduce the documents of the course.
With all the files, we compress them in a tar.gz in "Final_output".
If the user wishes, all web files and documents are deleted except the tar.gz.
Comparing the "Final_output" folder and "Docs.csv" the "Register.csv" file is generated to know which course is missing and which is compressed.
At this point in the execution, if there has been a problem, it would have already been noticed by blocking the programme. If this is not the case, we can be assured of a successful course.
This concludes the description of the structure and functioning of this code.
