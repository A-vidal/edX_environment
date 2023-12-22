# coding=utf-8
__author__ = "Leonardo Salom Muñoz, Sergio Puche García"
__credits__ = "Leonardo Salom Muñoz, Sergio Puche García"
__version__ = "0.0.1-SNAPSHOT"
__maintainer__ = "Sergio Puche García"
__email__ = "spuche@upv.es"
__status__ = "Development"

import os
import tarfile
import shutil
import xlrd
import datetime
import json

# import operator
import re
import urllib
import io
from lxml import etree
from loguru import logger

# Import constants
from xnf2edx.consts import (
    ENTITIES,
    CCERTROW,
    CDATOSGENERALESNOMBREPOS,
    CPROBLEMASROW,
    CSUBSHEET,
    CSUBROW,
    CUNIDADROW,
    WRONGIMG,
    OKIMG,
    CDATOSGENERALESCATEGORIAPOS,
    CDATOSGENERALESEDICIONPOS,
    CDATOSGENERALESABOUTVIDEOPOS,
    CDATOSGENERALESINFOPOS,
    CDATOSGENERALESDURATIONPOS,
    CDATOSGENERALESABOUTPOS,
    CDATOSGENERALESPREREQUISITESPOS,
    CUNIDADCHAPTERNAMECOL,
    CDATOSGENERALESTEACHERSPOS,
    CTTAREASTARTROW,
    CTTAREAWEIGHTCOL,
    CTTAREAABREVIATURECOL,
    CTTAREAAMOUNTCOL,
    CTTAREATYPECOL,
    CTTAREADISCARDCOL,
    CTABSHEET,
    CDATOSGENERALESSTARTDATEPOS,
    CDATOSGENERALESENDDATEPOS,
    CDATOSGENERALESDISPLAYNAMEPOS,
    CDATOSGENERALESPOLICIES,
    CCERTIDCOL,
    CCERTDESCCOL,
    CCERTACTIVECOL,
    CCERTNOMCOL,
    CCERTVERSIONCOL,
    CCERTSIGNIDCOL,
    CCERTSIGNNOMCOL,
    CCERTSIGNORGCOL,
    CCERTSIGNPATHCOL,
    CCERTSIGNTITCOL,
    CTABNOMBREROW,
    CTABCONTENTROW,
    CDATOSGENERALESPROGRAMPOS,
    CDATOSGENERALESEVALPOS,
    CUNIDADCHAPTERIDCOL,
    CUNIDADSUBSECTIONIDCOL,
    CUNIDADSTARTDATECOL,
    CUNIDADENDDATECOL,
    CUNIDADSUBSECTIONNAMECOL,
    CUNIDADFORMATCOL,
    CCURSOCHAPTERIDCOL,
    CCURSOSUBSECTIONIDCOL,
    CCURSOLESSONIDCOL,
    CCURSOOBJETIVOSCOL,
    CCURSOVIDEOCOL,
    CCURSORESUMECOL,
    CCURSOFORUMCOL,
    CCURSOLESSONDISPLAYNAMECOL,
    CCURSORESETCOL,
    DEFAULTPROBLEMMAXATTEMPTS,
    DEFAULTPROBLEMWEIGHT,
    DEFAULTPROBLEMSHOWANSWER,
    CTTAREATRYCOL,
    CTTAREAWEIGHTPROBLEMCOL,
    CTTAREASHOWANSWERCOL,
    CPROBLEMASIDUNIDADCOL,
    CPROBLEMASIDSUBSECCIONCOL,
    CPROBLEMASIDLECCIONCOL,
    CPROBLEMASPREVIACOL,
    RESETJS,
    CPROBLEMASINTENTOSCOL,
    CPROBLEMASSHOWANSWERCOL,
    CPROBLEMASWEIGHTCOL,
    CPROBLEMASTIPOCOL,
    CPROBLEMASENUNCIADOCOL,
    CPROBLEMASCOMENTARIOCOL,
    CPROBLEMASCORRECTACOL,
    CPROBLEMASRESPUESTACOL,
    CSUBVIDEOIDCOL,
    CSUBSHEADERROW,
    CDATOSGENERALESVERSION,
    CDATOSGENERALESROW,
    CTTAREAROW,
    CCURSOROW,
    CCURSOSHEET,
    CDATOSGENERALESSHEET,
    CPROBLEMASSHEET,
    CTTAREASHEET,
    CUNIDADSHEET,
    SA_ALWAYS_ROW,
    SA_ANSWERED_ROW,
    SA_ATTEMPTED_ROW,
    SA_CLOSED_ROW,
    SA_FINISHED_ROW,
    SA_PASTDATE_ROW,
    SA_NEVER_ROW,
    YES_ROW,
    NO_ROW,
)
from xnf2edx.utils import (
    get_sheet,
    get_version,
    get_values_with_fallback,
)
from xnf2edx import scrap

# Global variables
path = ""
problemSetID = 1
stufftoreturn = {"path": "", "coursename": "", "log": "", "error": ""}

# Some config to avoid unexpected behaviour
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True


def generate_Edx(_wb, _path):
    """
    Main script makes the calls in order to clean the resulting thir and after that
    generate that dir and the targz that we will use to import the course

    :param _wb: Excel workbook opened with xlrd (*xlrd.open_workbook*)
    :param _path: output dir where the tarball will be dumped to
    """
    global stufftoreturn
    stufftoreturn["log"] = ""
    stufftoreturn["error"] = ""
    stufftoreturn["coursename"] = ""
    stufftoreturn["path"] = ""

    datos_generales_sheet = get_sheet(_wb, CDATOSGENERALESSHEET, CDATOSGENERALESROW)
    course_name = datos_generales_sheet.cell_value(
        CDATOSGENERALESNOMBREPOS[0], CDATOSGENERALESNOMBREPOS[1]
    )

    checkVersion(_wb)
    select_base_path(_path, course_name)
    clean()
    create_directory_tree()
    create_policies(_wb)
    create_course_id_file(_wb)
    create_roots(_wb)
    create_course(_wb)
    create_about(_wb)
    # create_info(_wb)
    addtolog("path", make_tarfile(_wb))
    return stufftoreturn


def select_base_path(_path, course_name):
    global path
    try:
        addtolog("log", "<p><b>Seleccionando ruta base</b></p><ul>")
        if course_name == "":
            path = _path + "/unnamedcourse"
            addtolog(
                "log",
                "<li>"
                + WRONGIMG
                + "No se ha encontrado el nombre del curso, cambiado al nombre por "
                + "defecto UNNAMEDCOURSE</li>",
            )
            addtolog("coursename", "unnamedcourse")
        else:
            path = _path + "/" + course_name
            addtolog(
                "coursename",
                course_name,
            )
            addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at select_base_path")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Ha ocurrido un error al acceder al nombre del curso, revise el nombre "
            + "del curso y el formato</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")
    finally:
        logger.info(f"Path value established: {path}")


def clean():
    """
    Deletes the directory from previous generations
    """
    logger.info(f"Executing clean() to remove previous output at {path}")
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
    except Exception as e:
        addtolog("log", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p>")
        logger.exception("Failure at clean")


def create_directory_tree():
    """
    Generates the directory structure needed for our xml project
    """
    logger.info("Generating directory tree")
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            addtolog("log", "<p><b>Creacion de directorios</b></p><ul>")
            if not os.path.exists(path + "/course"):
                os.makedirs(path + "/course")
            addtolog("log", "<li>" + OKIMG + " Course</li>")

            if not os.path.exists(path + "/problem"):
                os.makedirs(path + "/problem")
            addtolog("log", "<li>" + OKIMG + " Problem</li>")

            if not os.path.exists(path + "/sequential"):
                os.makedirs(path + "/sequential")
            addtolog("log", "<li>" + OKIMG + " Sequential</li>")

            if not os.path.exists(path + "/vertical"):
                os.makedirs(path + "/vertical")
            addtolog("log", "<li>" + OKIMG + " Vertical</li>")

            if not os.path.exists(path + "/video"):
                os.makedirs(path + "/video")
            addtolog("log", "<li>" + OKIMG + " Video</li>")

            if not os.path.exists(path + "/policies"):
                os.makedirs(path + "/policies")
            addtolog("log", "<li>" + OKIMG + " Policies</li>")

            if not os.path.exists(path + "/chapter"):
                os.makedirs(path + "/chapter")
            addtolog("log", "<li>" + OKIMG + " Chapter</li>")

            if not os.path.exists(path + "/roots"):
                os.makedirs(path + "/roots")
            addtolog("log", "<li>" + OKIMG + " Roots</li>")

            if not os.path.exists(path + "/html"):
                os.makedirs(path + "/html")
            addtolog("log", "<li>" + OKIMG + " Html</li>")

            if not os.path.exists(path + "/about"):
                os.makedirs(path + "/about")
            addtolog("log", "<li>" + OKIMG + " About</li>")

            if not os.path.exists(path + "/info"):
                os.makedirs(path + "/info")
            addtolog("log", "<li>" + OKIMG + " Info</li>")

            if not os.path.exists(path + "/discussion"):
                os.makedirs(path + "/discussion")
            addtolog("log", "<li>" + OKIMG + " Discussion</li>")

            if not os.path.exists(path + "/policies"):
                os.makedirs(path + "/policies")
            addtolog("log", "<li>" + OKIMG + " Policies</li>")

            if not os.path.exists(path + "/tabs"):
                os.makedirs(path + "/tabs")
            addtolog("log", "<li>" + OKIMG + " Tabs</li>")

            if not os.path.exists(path + "/static"):
                os.makedirs(path + "/static")
            addtolog("log", "<li>" + OKIMG + " Static</li>")

            if not os.path.exists(path + "/static/subs"):
                os.makedirs(path + "/static/subs")
            addtolog("log", "<li>" + OKIMG + " Subs</li>")

            addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at created_directory_tree")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Ha ocurrido un error durante la fase de creación de directorios, por "
            + "favor pongase en contacto con el administrador del sitio.</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def create_course_id_file(_wb):
    """
    generates course.xml in the main dir
    """

    try:
        xmlfile = path + "/course.xml"
        addtolog("log", "<p><b>Creacion de course</b></p><ul>")

        sheet = get_sheet(_wb, CDATOSGENERALESSHEET, CDATOSGENERALESROW)
        addtolog("log", "<li>" + OKIMG + " Carga de hoja datos generales</li>")

        courseCat = sheet.cell_value(
            CDATOSGENERALESCATEGORIAPOS[0], CDATOSGENERALESCATEGORIAPOS[1]
        )
        addtolog("log", "<li>" + OKIMG + " Categoría del curso</li>")

        courseID = sheet.cell_value(
            CDATOSGENERALESNOMBREPOS[0], CDATOSGENERALESNOMBREPOS[1]
        ) + sheet.cell_value(CDATOSGENERALESEDICIONPOS[0], CDATOSGENERALESEDICIONPOS[1])
        addtolog("log", "<li>" + OKIMG + " ID del curso (nombre+edición)</li>")

        courseName = sheet.cell_value(
            CDATOSGENERALESNOMBREPOS[0], CDATOSGENERALESNOMBREPOS[1]
        )
        addtolog("log", "<li>" + OKIMG + " Nombre del curso</li>")

        # Create the root element
        page = etree.Element(
            "course", org=courseCat, course=courseName, url_name=courseID
        )
        # Make a new document tree
        doc = etree.ElementTree(page)

        # Save to XML file
        doc.write(xmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8")
        addtolog("log", "</ul>")

    except Exception as e:
        logger.exception("Failure at create_course_id_file")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación de course</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def create_roots(_wb):
    """
    generates the xml in roots for current course
    """
    try:
        addtolog("log", "<p><b>Creacion de roots</b></p><ul>")

        sheet = get_sheet(_wb, CDATOSGENERALESSHEET, CDATOSGENERALESROW)
        addtolog("log", "<li>" + OKIMG + " Carga de hoja datos generales</li>")

        courseCat = sheet.cell_value(
            CDATOSGENERALESCATEGORIAPOS[0], CDATOSGENERALESCATEGORIAPOS[1]
        )
        addtolog("log", "<li>" + OKIMG + " Categoría del curso</li>")

        courseID = sheet.cell_value(
            CDATOSGENERALESNOMBREPOS[0], CDATOSGENERALESNOMBREPOS[1]
        ) + sheet.cell_value(CDATOSGENERALESEDICIONPOS[0], CDATOSGENERALESEDICIONPOS[1])
        addtolog("log", "<li>" + OKIMG + " ID del curso (nombre+edición)</li>")

        courseName = sheet.cell_value(
            CDATOSGENERALESNOMBREPOS[0], CDATOSGENERALESNOMBREPOS[1]
        )
        addtolog("log", "<li>" + OKIMG + " Nombre del curso</li>")

        xmlfile = path + "/roots/" + courseID + ".xml"

        # Create the root element
        page = etree.Element(
            "course", org=courseCat, course=courseName, url_name=courseID
        )
        # Make a new document tree
        doc = etree.ElementTree(page)

        # Save to XML file
        doc.write(xmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8")
        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at create_roots")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación de roots</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def create_about(_wb):
    """
    creates the about files
    """
    create_about_video(_wb)
    create_about_overview(_wb)


def create_about_video(_wb):
    """
    creates the about video file
    """
    try:
        addtolog("log", "<p><b>Creación de About Video</b></p><ul>")
        sheet = get_sheet(_wb, CDATOSGENERALESSHEET, CDATOSGENERALESROW)
        addtolog("log", "<li>" + OKIMG + " Carga de hoja datos generales</li>")

        htmlfile = path + "/about/video.html"
        page = etree.Element(
            "iframe",
            width="560",
            height="315",
            src="//www.youtube.com/embed/"
            + sheet.cell_value(
                CDATOSGENERALESABOUTVIDEOPOS[0], CDATOSGENERALESABOUTVIDEOPOS[1]
            )
            + "?autoplay=0&rel=0",
            frameborder="0",
            allowfullscreen="",
        )
        addtolog("log", "<li>" + OKIMG + " About video</li>")
        # Make a new document tree
        doc = etree.ElementTree(page)

        doc.write(htmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8")
        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at create_about_video")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación de about video</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def create_about_overview(_wb):
    """
    generates the overview file
    """
    try:
        addtolog("log", "<p><b>Creación de About Overview</b></p><ul>")
        sheet = get_sheet(_wb, CDATOSGENERALESSHEET, CDATOSGENERALESROW)
        sheetunits = get_sheet(_wb, CUNIDADSHEET, CUNIDADROW)
        addtolog("log", "<li>" + OKIMG + " Carga de hoja datos generales</li>")

        htmlpath = path + "/about/overview.html"
        info = sheet.cell_value(CDATOSGENERALESINFOPOS[0], CDATOSGENERALESINFOPOS[1])
        addtolog("log", "<li>" + OKIMG + " Info de</li>")

        if info[:1] != "<":
            info = "<p>" + info + "</p>"

        duration = sheet.cell_value(
            CDATOSGENERALESDURATIONPOS[0], CDATOSGENERALESDURATIONPOS[1]
        )
        addtolog("log", "<li>" + OKIMG + " Duration de</li>")

        if duration[:1] != "<":
            duration = "<p>" + duration + "</p>"

        about = sheet.cell_value(CDATOSGENERALESABOUTPOS[0], CDATOSGENERALESABOUTPOS[1])
        addtolog("log", "<li>" + OKIMG + " Acerca de</li>")

        if about[:1] != "<":
            about = "<p>" + about + "</p>"
        prerequisites = sheet.cell_value(
            CDATOSGENERALESPREREQUISITESPOS[0], CDATOSGENERALESPREREQUISITESPOS[1]
        )
        if prerequisites[:1] != "<":
            prerequisites = "<p>" + prerequisites + "</p>"
        addtolog("log", "<li>" + OKIMG + " Prerequisitos</li>")

        units = ""
        prev = ""
        i = 1
        while (
            sheetunits.nrows > i
            and sheetunits.cell_value(i, CUNIDADCHAPTERNAMECOL) != ""
        ):
            if prev != str(sheetunits.cell_value(i, CUNIDADCHAPTERNAMECOL)):
                units = (
                    units
                    + "<li>"
                    + str(sheetunits.cell_value(i, CUNIDADCHAPTERNAMECOL))
                    + "</li>"
                )
                prev = str(sheetunits.cell_value(i, CUNIDADCHAPTERNAMECOL))
            i = i + 1
        units = "<ol>" + units + "</ol>"

        inforoot = etree.Element("section", Class="info")
        info_writer = etree.ElementTree(inforoot)
        inforoot.append(etree.parse(io.StringIO("<h2>Duration</h2>\n")).getroot())
        inforoot.append(parse_html_cell(duration))
        inforoot.append(
            etree.parse(io.StringIO("<h2>Context and overview</h2>\n")).getroot()
        )
        inforoot.append(parse_html_cell(info))

        aboutroot = etree.Element("section", Class="about")
        about_writer = etree.ElementTree(aboutroot)
        aboutroot.append(etree.parse(io.StringIO("<h2>Learning objectives</h2>\n")).getroot())
        aboutroot.append(parse_html_cell(about))

        prerequisiteroot = etree.Element("section", Class="prerequisites")
        prerequisitewriter = etree.ElementTree(prerequisiteroot)
        prerequisiteroot.append(
            etree.parse(io.StringIO("<h2>Background</h2>\n")).getroot()
        )
        prerequisiteroot.append(parse_html_cell(prerequisites))
        prerequisiteroot.append(
            etree.parse(io.StringIO("<h2>Units</h2>\n")).getroot()
        )
        prerequisiteroot.append(parse_html_cell(units))

        coursestaffroot = etree.Element("section", Class="course-staff")
        coursestaffwriter = etree.ElementTree(coursestaffroot)
        coursestaffroot.append(
            etree.parse(io.StringIO("<h2>Teacher</h2>\n")).getroot()
        )
        teacherNames = str(
            sheet.cell_value(
                CDATOSGENERALESTEACHERSPOS[0], CDATOSGENERALESTEACHERSPOS[1]
            )
        )
        teacherNames = re.split(r"\,+|\;+", str(teacherNames))

        teacherCount = 0
        teacherRow = CDATOSGENERALESTEACHERSPOS[0] + 2
        addtolog("log", "<ul> <b><l>Profesores</l></b> ")
        while (
            sheet.nrows > teacherRow
            and str(sheet.cell_value(teacherRow, CDATOSGENERALESTEACHERSPOS[1])) != ""
        ):
            article = etree.SubElement(coursestaffroot, "article", Class="teacher")
            div = etree.SubElement(article, "div", Class="teacher-image")
            etree.SubElement(
                div, "img", src="/static/", align="left", style="margin:0 20 px 0 "
            )
            teacherName = etree.SubElement(article, "p")
            teacherName.text = str(teacherNames[teacherCount]).strip()
            teacherDescription = etree.SubElement(article, "p")
            teacherDescription.text = str(
                sheet.cell_value(teacherRow, CDATOSGENERALESTEACHERSPOS[1])
            )
            addtolog(
                "log",
                "<li>"
                + OKIMG
                + " Profesor "
                + str(teacherCount + 1)
                + ": "
                + str(teacherNames[teacherCount]),
            )
            teacherRow += 1
            teacherCount += 1
        addtolog("log", "</ul>")

        info_writer.write(
            htmlpath, pretty_print=True, xml_declaration=False, encoding="utf-8"
        )
        with open(htmlpath, "ab") as htmlfile:
            about_writer.write(
                htmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8"
            )
            prerequisitewriter.write(
                htmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8"
            )
            coursestaffwriter.write(
                htmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8"
            )

        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at create_about_overview")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación de about overview</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def create_policies(_wb):
    """
    this creates the policies file
    """
    create_policies_grading(_wb)
    create_policies_course(_wb)


def create_policies_grading(_wb):
    """
    this create the grading policies, now we can add them in the import
    """
    try:
        addtolog("log", "<p><b>Creación de Grading Policies</b></p><ul>")
        # need course edition to create folder
        sheet = get_sheet(_wb, CDATOSGENERALESSHEET, CDATOSGENERALESROW)
        addtolog("log", "<li>" + OKIMG + " Carga de hoja datos generales</li>")
        sheetGrading = get_sheet(_wb, CTTAREASHEET, CTTAREAROW)
        addtolog("log", "<li>" + OKIMG + " Carga de hoja tareas</li>")
        edition = sheet.cell_value(
            CDATOSGENERALESNOMBREPOS[0], CDATOSGENERALESNOMBREPOS[1]
        ) + sheet.cell_value(CDATOSGENERALESEDICIONPOS[0], CDATOSGENERALESEDICIONPOS[1])
        if not os.path.exists(path + "/policies/" + edition):
            os.makedirs(path + "/policies/" + edition)
        jsonfile = path + "/policies/" + edition + "/grading_policy.json"
        addtolog("log", "<li>" + OKIMG + " creado grading_policy.json</li>")
        taskrow = CTTAREASTARTROW
        grading_policy = {"GRADER": [], "GRADE_CUTOFFS": {"PASS": 0.5}}
        addtolog("log", "<ul>")
        while sheetGrading.nrows > taskrow:
            weight = float(sheetGrading.cell_value(taskrow, CTTAREAWEIGHTCOL))
            # if the teacher uses non decimal notation for the weight
            if weight > 1:
                weight = weight / 100

            grade = {
                "short_label": str(
                    sheetGrading.cell_value(taskrow, CTTAREAABREVIATURECOL)
                ),
                "min_count": str(sheetGrading.cell_value(taskrow, CTTAREAAMOUNTCOL)),
                "type": str(sheetGrading.cell_value(taskrow, CTTAREATYPECOL)),
                "drop_count": int(sheetGrading.cell_value(taskrow, CTTAREADISCARDCOL)),
                "weight": weight,
            }
            if grade["type"] != "":
                grading_policy["GRADER"].append(grade)
                addtolog(
                    "log",
                    "<li>"
                    + OKIMG
                    + " Añadido grade: "
                    + str(sheetGrading.cell_value(taskrow, CTTAREAABREVIATURECOL))
                    + "</li>",
                )
            taskrow += 1
        addtolog("log", "</ul>")

        with open(jsonfile, "w") as fp:
            json.dump(grading_policy, fp)

        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at create_policies_grading")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación de Grading Policies</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def create_policies_course(_wb):
    """
    will create course policies
    {
        "pdf_textbooks": [
            {
                "chapters": [
                    {
                        "title": "Ejercicios de Complejos",
                        "url": "/static/Ejercicios_complejos.pdf"
                    },
                    {
                        "title": "Inverso de un complejo ",
                        "url": "/static/Resolucion_de_sistema_ecuaciones.pdf"
                    },
                    {
                        "title": "Tabla de \\u00e1ngulos principales",
                        "url": "/static/Angulos.pdf"
                    }
                ],
                "id": "9Material_Adicional",
                "tab_title": "Material Adicional"
            }
        ],
        ,
        }
    }
    """
    try:
        addtolog("log", "<p><b>Creación de Course Policies</b></p><ul>")
        # need course edition to create folder
        sheet = get_sheet(_wb, CDATOSGENERALESSHEET, CDATOSGENERALESROW)
        addtolog("log", "<li>" + OKIMG + " Carga de hoja datos generales</li>")
        # back compatibility if sheet tabs does not exist we dont add them
        addtolog("log", "<li>" + OKIMG + " Carga de hoja tabs</li>")
        edition = sheet.cell_value(
            CDATOSGENERALESNOMBREPOS[0], CDATOSGENERALESNOMBREPOS[1]
        ) + sheet.cell_value(CDATOSGENERALESEDICIONPOS[0], CDATOSGENERALESEDICIONPOS[1])
        if not os.path.exists(path + "/policies/" + edition):
            os.makedirs(path + "/policies/" + edition)
        jsonfile = path + "/policies/" + edition + "/policy.json"
        addtolog("log", "<li>" + OKIMG + " creado policy.json</li>")

        courseStartDate = sheet.cell_value(
            CDATOSGENERALESSTARTDATEPOS[0], CDATOSGENERALESSTARTDATEPOS[1]
        )
        if courseStartDate != "":
            courseStartDate = datetime.datetime(
                *xlrd.xldate_as_tuple(courseStartDate, xlrd.Book.datemode)
            )
        else:
            courseStartDate = datetime.date.today() - datetime.timedelta(1)

        courseEndDate = sheet.cell_value(
            CDATOSGENERALESENDDATEPOS[0], CDATOSGENERALESENDDATEPOS[1]
        )

        if courseEndDate != "":
            courseEndDate = datetime.datetime(
                *xlrd.xldate_as_tuple(courseEndDate, xlrd.Book.datemode)
            )
        else:
            courseEndDate = datetime.date.today() - datetime.timedelta(1)

        courseDisplayName = (
            sheet.cell_value(
                CDATOSGENERALESDISPLAYNAMEPOS[0], CDATOSGENERALESDISPLAYNAMEPOS[1]
            )
            if sheet.cell_value(
                CDATOSGENERALESDISPLAYNAMEPOS[0], CDATOSGENERALESDISPLAYNAMEPOS[1]
            )
            != ""
            else "Display Name Not Set"
        )
        # could check how fill fields instructor info and learning info so we use them
        #
        # instructor_info": {
        #    "instructors": []
        # },
        # "learning_info": [],
        #

        policy = {
            "course/"
            + edition: {
                # MAÑANA CAMBIAR LA EDICION Y AÑADIRLE LAS POLICIES
                "display_name": courseDisplayName,
                "start": str(courseStartDate),
                "end": str(courseEndDate),
                "xml_attributes": {
                    "filename": [
                        "course/" + edition + ".xml",
                        "course/" + edition + ".xml",
                    ]
                },
                "tabs": [
                    {"name": "Courseware", "type": "courseware"},
                    {"name": "Course Info", "type": "course_info"},
                    {"name": "Textbooks", "type": "textbooks"},
                    {"name": "Discussion", "type": "discussion"},
                    {"is_hidden": True, "name": "Wiki", "type": "wiki"},
                    {"name": "Progress", "type": "progress"},
                    {"name": "Textbooks", "type": "pdf_textbooks"},
                    {
                        "name": "Program",
                        "type": "static_tab",
                        "url_slug": "course_program",
                    },
                ],
            }
        }

        for policyiter in CDATOSGENERALESPOLICIES:
            if sheet.cell_value(policyiter["coords"][0], policyiter["coords"][1]) != "":
                if policyiter["datatype"] == "text" or policyiter["datatype"] == "num":
                    policy["course/" + edition][
                        policyiter["fieldname"]
                    ] = sheet.cell_value(
                        policyiter["coords"][0], policyiter["coords"][1]
                    )
                if policyiter["datatype"] == "json":
                    try:
                        policy["course/" + edition][
                            policyiter["fieldname"]
                        ] = json.loads(
                            sheet.cell_value(
                                policyiter["coords"][0], policyiter["coords"][1]
                            )
                        )
                    except Exception as e:
                        addtolog(
                            "error",
                            "<a href='#error"
                            + str(len(stufftoreturn["error"]))
                            + "'><p>"
                            + WRONGIMG
                            + "Error agregando la politica situada en "
                            + policyiter["coords"][0]
                            + ", "
                            + policyiter["coords"][1]
                            + "</p>",
                        )
                        addtolog(
                            "error",
                            "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>",
                        )
                if policyiter["datatype"] == "bool":
                    if sheet.cell_value(
                        policyiter["coords"][0], policyiter["coords"][1]
                    ) in get_values_with_fallback(_wb, YES_ROW, "Sí"):
                        policy["course/" + edition][policyiter["fieldname"]] = True
                    elif sheet.cell_value(
                        policyiter["coords"][0], policyiter["coords"][1]
                    ) in get_values_with_fallback(_wb, NO_ROW, "No"):
                        policy["course/" + edition][policyiter["fieldname"]] = False
                if policyiter["datatype"] == "date":
                    policy["course/" + edition][policyiter["fieldname"]] = str(
                        datetime.datetime(
                            *xlrd.xldate_as_tuple(
                                sheet.cell_value(
                                    policyiter["coords"][0], policyiter["coords"][1]
                                ),
                                xlrd.Book.datemode,
                            )
                        )
                    )

        if (
            "cert_html_view_enabled" in policy["course/" + edition]
            and policy["course/" + edition]["cert_html_view_enabled"] is True
        ):
            try:
                certificates = {"certificates": []}
                sheetCert = get_sheet(_wb, CCERTSHEET, CCERTROW)
                certrow = 1
                certificate = {"id": ""}
                while sheetCert.nrows > certrow:
                    if certificate["id"] != sheetCert.cell_value(certrow, CCERTIDCOL):
                        if certificate["id"] != "":
                            certificates["certificates"].append(certificate)
                        certificate["description"] = sheetCert.cell_value(
                            certrow, CCERTDESCCOL
                        )
                        certificate["id"] = sheetCert.cell_value(certrow, CCERTIDCOL)
                        if sheetCert.cell_value(
                            certrow, CCERTACTIVECOL
                        ) in get_values_with_fallback(_wb, YES_ROW, "Sí"):
                            active = True
                        else:
                            active = False
                        certificate["is_active"] = active
                        certificate["name"] = sheetCert.cell_value(certrow, CCERTNOMCOL)
                        certificate["version"] = sheetCert.cell_value(
                            certrow, CCERTVERSIONCOL
                        )
                        certificate["signatories"] = []
                    sign = {
                        "certificate": sheetCert.cell_value(certrow, CCERTIDCOL),
                        "id": sheetCert.cell_value(certrow, CCERTSIGNIDCOL),
                        "name": sheetCert.cell_value(certrow, CCERTSIGNNOMCOL),
                        "organization": sheetCert.cell_value(certrow, CCERTSIGNORGCOL),
                        "signature_image_path": sheetCert.cell_value(
                            certrow, CCERTSIGNPATHCOL
                        ),
                        "title": sheetCert.cell_value(certrow, CCERTSIGNTITCOL),
                    }
                    certificate["signatories"].append(sign)
                    certrow += 1
                certificates["certificates"].append(certificate)
                policy["course/" + edition]["certificates"] = certificates
            except Exception as e:
                pass

        # must generate course program html
        generate_course_program(_wb)
        addtolog("log", "<ul>")
        tabrow = 1
        hastabs = any(CTABSHEET in names for names in _wb.sheet_names())
        if hastabs:
            sheetTabs = _wb.sheet_by_name(CTABSHEET)
            while sheetTabs.nrows > tabrow:
                tab = {
                    "name": str(sheetTabs.cell_value(tabrow, CTABNOMBREROW)),
                    "type": "static_tab",
                    "url_slug": "tab_"
                    + str(sheetTabs.cell_value(tabrow, CTABNOMBREROW)).replace(
                        " ", "_"
                    ),
                }
                if tab["name"] != "":
                    policy["course/" + edition]["tabs"].append(tab)
                    # tenemos que generar el archivo html del tab
                    generatetab(
                        "tab_" + str(sheetTabs.cell_value(tabrow, CTABNOMBREROW)),
                        str(sheetTabs.cell_value(tabrow, CTABCONTENTROW)),
                    )
                    addtolog(
                        "log",
                        "<li>"
                        + OKIMG
                        + " Añadido tab: "
                        + str(sheetTabs.cell_value(tabrow, CTTAREAABREVIATURECOL))
                        + "</li>",
                    )
                tabrow += 1
        addtolog("log", "</ul>")

        with open(jsonfile, "w") as fp:
            json.dump(policy, fp)
        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at create_policies_course")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación de Course Policies</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def generate_course_program(_wb):
    """
    generates course program tab
    """
    try:
        addtolog("log", "<p><b>Creación del course program</b></p><ul>")
        sheet = get_sheet(_wb, CDATOSGENERALESSHEET, CDATOSGENERALESROW)
        sheetunits = get_sheet(_wb, CUNIDADSHEET, CUNIDADROW)
        addtolog("log", "<li>" + OKIMG + " Carga de hoja datos generales</li>")

        htmlpath = path + "/tabs/course_program.html"
        info = sheet.cell_value(CDATOSGENERALESINFOPOS[0], CDATOSGENERALESINFOPOS[1])
        addtolog("log", "<li>" + OKIMG + " Info de</li>")

        if info[:1] != "<":
            info = "<p>" + info + "</p>"

        duration = sheet.cell_value(
            CDATOSGENERALESDURATIONPOS[0], CDATOSGENERALESDURATIONPOS[1]
        )
        addtolog("log", "<li>" + OKIMG + " Duration de</li>")

        if duration[:1] != "<":
            duration = "<p>" + duration + "</p>"

        about = sheet.cell_value(CDATOSGENERALESABOUTPOS[0], CDATOSGENERALESABOUTPOS[1])
        addtolog("log", "<li>" + OKIMG + " Acerca de</li>")
        if about[:1] != "<":
            about = "<p>" + about + "</p>"

        program = sheet.cell_value(
            CDATOSGENERALESPROGRAMPOS[0], CDATOSGENERALESPROGRAMPOS[1]
        )
        addtolog("log", "<li>" + OKIMG + " programacion</li>")
        if program != "" and program[:1] != "<":
            program = "<p>" + program + "</p>"

        evaluacion = sheet.cell_value(
            CDATOSGENERALESEVALPOS[0], CDATOSGENERALESEVALPOS[1]
        )
        addtolog("log", "<li>" + OKIMG + " evaluacion</li>")
        if evaluacion != "" and evaluacion[:1] != "<":
            evaluacion = "<p>" + evaluacion + "</p>"

        prerequisites = sheet.cell_value(
            CDATOSGENERALESPREREQUISITESPOS[0], CDATOSGENERALESPREREQUISITESPOS[1]
        )
        if prerequisites[:1] != "<":
            prerequisites = "<p>" + prerequisites + "</p>"
        addtolog("log", "<li>" + OKIMG + " Prerequisitos</li>")

        units = ""
        prev = ""
        i = 1
        while (
            sheetunits.nrows > i
            and sheetunits.cell_value(i, CUNIDADCHAPTERNAMECOL) != ""
        ):
            if prev != str(sheetunits.cell_value(i, CUNIDADCHAPTERNAMECOL)):
                units = (
                    units
                    + "<li>"
                    + str(sheetunits.cell_value(i, CUNIDADCHAPTERNAMECOL))
                    + "</li>"
                )
                prev = str(sheetunits.cell_value(i, CUNIDADCHAPTERNAMECOL))
            i = i + 1
        units = "<p><ol>" + units + "</ol></p>"

        inforoot = etree.Element("section", Class="info")
        info_writer = etree.ElementTree(inforoot)
        inforoot.append(etree.parse(io.StringIO("<h2>Duration</h2>\n")).getroot())
        inforoot.append(parse_html_cell(duration))
        inforoot.append(
            etree.parse(io.StringIO("<h2>Context and overview</h2>\n")).getroot()
        )
        inforoot.append(parse_html_cell(info))

        aboutroot = etree.Element("section", Class="about")
        about_writer = etree.ElementTree(aboutroot)
        aboutroot.append(etree.parse(io.StringIO("<h2>Learning objectives</h2>\n")).getroot())
        aboutroot.append(parse_html_cell(about))

        prerequisiteroot = etree.Element("section", Class="prerequisites")
        prerequisitewriter = etree.ElementTree(prerequisiteroot)
        prerequisiteroot.append(
            etree.parse(io.StringIO("<h2>Background</h2>\n")).getroot()
        )
        prerequisiteroot.append(parse_html_cell(prerequisites))
        prerequisiteroot.append(
            etree.parse(io.StringIO("<h2>Units</h2>\n")).getroot()
        )
        prerequisiteroot.append(parse_html_cell(units))
        if program != "":
            prerequisiteroot.append(
                etree.parse(io.StringIO("<h2>Temporary program</h2>\n")).getroot()
            )
            prerequisiteroot.append(parse_html_cell(program))
        if evaluacion != "":
            prerequisiteroot.append(
                etree.parse(io.StringIO("<h2>Evaluation</h2>\n")).getroot()
            )
            prerequisiteroot.append(parse_html_cell(evaluacion))

        info_writer.write(
            htmlpath, pretty_print=True, xml_declaration=False, encoding="utf-8"
        )
        with open(htmlpath, "ab") as htmlfile:
            about_writer.write(
                htmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8"
            )
            prerequisitewriter.write(
                htmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8"
            )

        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at generate_course_program")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del course program</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def generatetab(_tabname, _tabcontent):
    """
    generates tab html file
    """
    try:
        addtolog("log", "<p><b>Creación del tab" + _tabname + "</b></p><ul>")
        htmlfile = path + "/tabs/" + _tabname.replace(" ", "_") + ".html"
        with open(htmlfile, "w") as html:
            html.write(_tabcontent)

        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at generatetab")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del tab</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def create_course(_wb):
    """
    this generates the course main file wich
    contains a list of chapters for the course
    """

    try:
        addtolog("log", "<p><b>Creación del curso</b></p><ul>")
        sheet = get_sheet(_wb, CDATOSGENERALESSHEET, CDATOSGENERALESROW)
        addtolog("log", "<li>" + OKIMG + " Carga de hoja datos generales</li>")

        sheetUnidad = get_sheet(_wb, CUNIDADSHEET, CUNIDADROW)
        addtolog("log", "<li>" + OKIMG + " Carga de hoja Unidad</li>")

        courseID = sheet.cell_value(
            CDATOSGENERALESNOMBREPOS[0], CDATOSGENERALESNOMBREPOS[1]
        ) + sheet.cell_value(CDATOSGENERALESEDICIONPOS[0], CDATOSGENERALESEDICIONPOS[1])
        addtolog("log", "<li>" + OKIMG + " Id del curso</li>")
        courseDisplayName = (
            sheet.cell_value(
                CDATOSGENERALESDISPLAYNAMEPOS[0], CDATOSGENERALESDISPLAYNAMEPOS[1]
            )
            if sheet.cell_value(
                CDATOSGENERALESDISPLAYNAMEPOS[0], CDATOSGENERALESDISPLAYNAMEPOS[1]
            )
            != ""
            else "Display Name Not Set"
        )
        addtolog("log", "<li>" + OKIMG + " DisplayName del curso</li>")

        courseStartDate = sheet.cell_value(
            CDATOSGENERALESSTARTDATEPOS[0], CDATOSGENERALESSTARTDATEPOS[1]
        )
        if courseStartDate != "":
            courseStartDate = datetime.datetime(
                *xlrd.xldate_as_tuple(courseStartDate, xlrd.Book.datemode)
            )
        else:
            courseStartDate = datetime.date.today() - datetime.timedelta(1)
        addtolog("log", "<li>" + OKIMG + " Fecha de inicio del curso</li>")

        courseEndDate = sheet.cell_value(
            CDATOSGENERALESENDDATEPOS[0], CDATOSGENERALESENDDATEPOS[1]
        )
        if courseEndDate != "":
            courseEndDate = datetime.datetime(
                *xlrd.xldate_as_tuple(courseEndDate, xlrd.Book.datemode)
            )
        else:
            courseEndDate = datetime.date.today() - datetime.timedelta(1)
        addtolog("log", "<li>" + OKIMG + " Fecha de fin del curso</li>")

        xmlfile = path + "/course/" + courseID + ".xml"

        # Create the root element
        page = etree.Element(
            "course",
            display_name=courseDisplayName,
            start=str(courseStartDate),
            end=str(courseEndDate),
        )
        # Make a new document tree
        doc = etree.ElementTree(page)
        currentChapter = ""
        urlName = ""
        addtolog("log", "<ul> <b><l>Unidades del curso</l></b> ")
        for row in range(1, sheetUnidad.nrows):
            if currentChapter != sheetUnidad.cell_value(row, CUNIDADCHAPTERIDCOL):
                currentChapter = sheetUnidad.cell_value(row, CUNIDADCHAPTERIDCOL)
                urlName = "Unidad" + str(
                    int(sheetUnidad.cell_value(row, CUNIDADCHAPTERIDCOL))
                )
                etree.SubElement(page, "chapter", url_name=urlName)
                create_chapter(_wb, row, urlName, str(courseStartDate))
                addtolog("log", "<li>" + OKIMG + " " + str(urlName) + ", enlazada</li>")
        addtolog("log", "</ul>")
        # Save to XML file
        doc.write(xmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8")
        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at create_course")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del curso</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def create_chapter(_wb, _startRow, _urlName, _courseStartDate):
    """
    creates a chapter.xml file
    witch contains a list of sections
    :param _startRow:
    :param _urlName:
    """

    try:
        addtolog("log", "<p><b>Creación de la Unidad" + str(_urlName) + "</b></p><ul>")
        sheetUnidad = get_sheet(_wb, CUNIDADSHEET, CUNIDADROW)
        addtolog("log", "<li>" + OKIMG + " Carga de hoja Unidad</li>")
        addtolog("log", "<li>" + OKIMG + " Carga de hoja Problemas</li>")
        currentChapter = sheetUnidad.cell_value(_startRow, CUNIDADCHAPTERIDCOL)
        addtolog(
            "log",
            "<li>" + OKIMG + " Seleccionada Unidad:" + str(currentChapter) + "</li>",
        )
        chapterDisplayName = sheetUnidad.cell_value(_startRow, CUNIDADCHAPTERNAMECOL)
        addtolog("log", "<li>" + OKIMG + " Display Name</li>")
        strChapterID = _urlName
        # this will serve as counter for the problems in the chapter
        global problemSetID
        problemSetID = 1
        xmlfile = path + "/chapter/" + strChapterID + ".xml"

        # Create the root element
        page = etree.Element("chapter", display_name=chapterDisplayName)
        # Make a new document tree
        doc = etree.ElementTree(page)
        urlName = ""
        # Add normal childrens
        addtolog("log", "<ul> <b><l>Secuenciales de la unidad</l></b> ")
        for row in range(_startRow, sheetUnidad.nrows):
            if currentChapter == sheetUnidad.cell_value(row, CUNIDADCHAPTERIDCOL):
                urlName = (
                    strChapterID
                    + "Subsection"
                    + str(int(sheetUnidad.cell_value(row, CUNIDADSUBSECTIONIDCOL)))
                    + "Sequential"
                )
                etree.SubElement(page, "sequential", url_name=urlName)
                sequentialStartDate = sheetUnidad.cell_value(row, CUNIDADSTARTDATECOL)
                if sequentialStartDate != "":
                    sequentialStartDate = datetime.datetime(
                        *xlrd.xldate_as_tuple(sequentialStartDate, xlrd.Book.datemode)
                    )
                else:
                    sequentialStartDate = _courseStartDate

                sequentialEndDate = sheetUnidad.cell_value(row, CUNIDADENDDATECOL)
                if sequentialEndDate != "":
                    sequentialEndDate = datetime.datetime(
                        *xlrd.xldate_as_tuple(sequentialEndDate, xlrd.Book.datemode)
                    )

                createSequential(
                    _wb,
                    "A",
                    sheetUnidad.cell_value(row, CUNIDADCHAPTERIDCOL),
                    sheetUnidad.cell_value(row, CUNIDADSUBSECTIONIDCOL),
                    sheetUnidad.cell_value(row, CUNIDADCHAPTERNAMECOL),
                    sheetUnidad.cell_value(row, CUNIDADSUBSECTIONNAMECOL),
                    urlName,
                    str(sheetUnidad.cell_value(row, CUNIDADFORMATCOL)),
                    str(sequentialStartDate),
                    str(sequentialEndDate),
                )
            else:
                break

        addtolog("log", "</ul>")

        addtolog("log", "</ul>")
        # Save to XML file
        doc.write(xmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8")
    except Exception as e:
        logger.exception("Failure at create_chapter")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación de la Unidad</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def createSequential(
    _wb,
    _type,
    _section,
    _subsection,
    _sectionDisplayName,
    _subsectionDisplayName,
    _urlName,
    _format,
    _startDate,
    _endDate,
):
    """
    creates sequential files wich contains a list of vertical files for each lesson and
    the problems of that lesson
    :param _type:
    :param _section:
    :param _subsection:
    :param _sectionDisplayName:
    :param _subsectionDisplayName:
    :param _urlName:
    :param _format:
    :param _startDate:
    :param _endDate:
    """

    try:
        addtolog("log", "<p><b>Creación del secuencial" + _urlName + "</b></p><ul>")
        sheetCurso = get_sheet(_wb, CCURSOSHEET, CCURSOROW)
        addtolog("log", "<li>" + OKIMG + " Carga de hoja Curso</li>")
        # sheetProblem = _wb.sheet_by_name(CPROBLEMASSHEET)

        currentChapter = _section
        currentSubsection = _subsection
        strSubsectionID = _urlName
        xmlfile = path + "/sequential/" + strSubsectionID + ".xml"

        # TO-DO check if endDate goes to the end field
        if _format != "":
            _graded = "true"
        else:
            _graded = "false"

        page = etree.Element(
            "sequential",
            display_name=_subsectionDisplayName,
            format=_format,
            graded=_graded,
            start=_startDate,
            due=_endDate,
        )
        addtolog("log", "<li>" + OKIMG + " Creado nodo del secuencial</li>")
        # Make a new document tree
        doc = etree.ElementTree(page)
        # Unidad1Subsection1Vertical1
        # TO-DO generate the range with a binary search
        addtolog("log", "<ul> <b><l>Elementos del secuencial</l></b> ")
        for row in range(1, sheetCurso.nrows):
            if currentChapter == sheetCurso.cell_value(
                row, CCURSOCHAPTERIDCOL
            ) and currentSubsection == sheetCurso.cell_value(
                row, CCURSOSUBSECTIONIDCOL
            ):

                urlName = (
                    "Unidad"
                    + str(int(currentChapter))
                    + "Subsection"
                    + str(int(currentSubsection))
                    + "Vertical"
                    + str(int(sheetCurso.cell_value(row, CCURSOLESSONIDCOL)))
                )
                if (
                    sheetCurso.cell_value(row, CCURSOOBJETIVOSCOL) != ""
                    or sheetCurso.cell_value(row, CCURSOVIDEOCOL) != ""
                    or sheetCurso.cell_value(row, CCURSORESUMECOL) != ""
                    or sheetCurso.cell_value(row, CCURSOFORUMCOL) != ""
                ):
                    etree.SubElement(page, "vertical", url_name=urlName)
                    createVertical(
                        _wb,
                        currentChapter,
                        currentSubsection,
                        sheetCurso.cell_value(row, CCURSOLESSONIDCOL),
                        row,
                        urlName,
                        _sectionDisplayName,
                        _subsectionDisplayName,
                    )
                    addtolog("log", "<li>" + OKIMG + " Creado el vertical</li>")

                problemRow = findProblems(
                    _wb,
                    currentChapter,
                    currentSubsection,
                    sheetCurso.cell_value(row, CCURSOLESSONIDCOL),
                )
                if problemRow > 0:
                    urlName += "Problems"
                    if _type == "A":
                        if sheetCurso.cell_value(row, CCURSOLESSONDISPLAYNAMECOL) != "":
                            displayName = sheetCurso.cell_value(
                                row, CCURSOLESSONDISPLAYNAMECOL
                            )
                        else:
                            displayName = "Examen"
                    else:
                        displayName = "Actividad " + str(problemSetID)
                    etree.SubElement(page, "vertical", url_name=urlName)
                    lessonResset = ""
                    try:
                        lessonResset = sheetCurso.cell_value(row, CCURSORESETCOL)
                    except Exception:
                        lessonResset = ""

                    createProblemSet(
                        _wb,
                        currentChapter,
                        currentSubsection,
                        sheetCurso.cell_value(row, CCURSOLESSONIDCOL),
                        problemRow,
                        urlName,
                        displayName,
                        lessonResset,
                    )
                    addtolog("log", "<li>" + OKIMG + " Creado el problemset</li>")

            if currentChapter < sheetCurso.cell_value(row, CCURSOCHAPTERIDCOL):
                break

        addtolog("log", "</ul>")

        doc.write(xmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8")

        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at createSequential")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del Secuencial</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def parseShowAnswer(_wb, _showanswer):
    rel = [
        (SA_ALWAYS_ROW, "always", "Siempre"),
        (SA_ANSWERED_ROW, "answered", "Respondida"),
        (SA_ATTEMPTED_ROW, "attempted", "Intentada"),
        (SA_CLOSED_ROW, "closed", "Cerrada"),
        (SA_PASTDATE_ROW, "past_due", "Fecha pasada"),
        (SA_NEVER_ROW, "never", "Nunca"),
        (SA_FINISHED_ROW, "finished", "Terminada"),
    ]
    for x in rel:
        values = [w.lower() for w in get_values_with_fallback(_wb, x[0], x[2])]
        if _showanswer.lower() in values:
            return x[1]


def getProblemInheritedAtributes(_wb, _Chapter, _Subsection):
    """
    retuns a dict with the problem atributes that inherits for a subsection
        weight
        showanswer
        maxatepts
    """
    try:
        addtolog(
            "log", "<p><b>Buscando atributos heredados de los problemas</b></p><ul>"
        )

        sheetUnit = get_sheet(_wb, CUNIDADSHEET, CUNIDADROW)
        addtolog("log", "<li>" + OKIMG + " Carga de la hoja problemas</li>")
        sheetTasks = get_sheet(_wb, CTTAREASHEET, CTTAREAROW)
        addtolog("log", "<li>" + OKIMG + " Carga de la hoja problemas</li>")
        inherited_attributes = {
            "max_attempts": DEFAULTPROBLEMMAXATTEMPTS,
            "weight": DEFAULTPROBLEMWEIGHT,
            "showanswer": DEFAULTPROBLEMSHOWANSWER,
        }
        tasktype = ""
        for row in range(0, sheetUnit.nrows):
            if _Chapter == sheetUnit.cell_value(
                row, CUNIDADCHAPTERIDCOL
            ) and _Subsection == sheetUnit.cell_value(row, CUNIDADSUBSECTIONIDCOL):
                tasktype = sheetUnit.cell_value(row, CUNIDADFORMATCOL)
                break
        if tasktype != "":
            for row in range(0, sheetTasks.nrows):
                if tasktype == sheetTasks.cell_value(row, CTTAREATYPECOL):
                    if (
                        sheetTasks.cell_value(row, CTTAREATRYCOL) != ""
                        and sheetTasks.cell_value(row, CTTAREATRYCOL) != "null"
                    ):
                        max_attempts = int(sheetTasks.cell_value(row, CTTAREATRYCOL))
                    else:
                        max_attempts = "null"
                    inherited_attributes = {
                        "max_attempts": max_attempts,
                        "weight": sheetTasks.cell_value(row, CTTAREAWEIGHTPROBLEMCOL),
                        "showanswer": parseShowAnswer(
                            _wb, sheetTasks.cell_value(row, CTTAREASHOWANSWERCOL)
                        ),
                    }

        addtolog(
            "log",
            "<li>" + OKIMG + " Atributos de problemas heredados correctamente</li>",
        )
        addtolog("log", "</ul>")
        return inherited_attributes
    except Exception as e:
        logger.exception("Failure at getProblemInheritedAtributes")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error cargando atributos heredados</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def createProblemSet(
    _wb, _Chapter, _Subsection, _Lesson, _row, _urlName, _displayName, _resetSet
):
    """
    creates the sets of problems related with a lesson
    :param _Chapter:
    :param _Subsection:
    :param _Lesson:
    :param _row:
    :param _urlName:
    """

    try:
        addtolog(
            "log", "<p><b>Creación del problemset " + str(_urlName) + "</b></p><ul>"
        )
        global problemSetID
        displayName = _displayName
        xmlfile = path + "/vertical/" + _urlName + ".xml"
        problemID = 1
        page = etree.Element("vertical", display_name=displayName)
        # Make a new document tree
        doc = etree.ElementTree(page)
        sheetProblem = get_sheet(_wb, CPROBLEMASSHEET, CPROBLEMASROW)

        addtolog("log", "<li>" + OKIMG + " Carga de la hoja problemas</li>")
        problemattr = getProblemInheritedAtributes(_wb, _Chapter, _Subsection)

        for row in range(_row, sheetProblem.nrows):
            if (
                _Chapter == sheetProblem.cell_value(row, CPROBLEMASIDUNIDADCOL)
                and _Subsection
                == sheetProblem.cell_value(row, CPROBLEMASIDSUBSECCIONCOL)
                and _Lesson == sheetProblem.cell_value(row, CPROBLEMASIDLECCIONCOL)
            ):
                urlName = _urlName + str(problemID)
                # if the problem has a previa add an html element
                if sheetProblem.cell_value(row, CPROBLEMASPREVIACOL) != "":
                    etree.SubElement(page, "html", url_name=urlName + "Previa")
                    createHtml(
                        urlName + "Previa",
                        sheetProblem.cell_value(row, CPROBLEMASPREVIACOL),
                        displayName,
                    )
                    displayName = ""
                    addtolog(
                        "log",
                        "<li>" + OKIMG + " Creado html con previa del problema</li>",
                    )
                etree.SubElement(page, "problem", url_name=urlName)
                # call generate problem
                createProblem(_wb, displayName, row, urlName, problemattr)
                displayName = ""  # only the 1st problem on a problemSet has displayName
                problemID += 1

        if _resetSet != "":
            # Unidad1Subsection1Vertical1Resumen
            urlName = _urlName + "Reset"
            # Here we check for URL filter and stuff patatas
            etree.SubElement(page, "html", url_name=urlName)
            htmlstring = RESETJS

            displayName = "Reiniciar problemas"
            createHtml(urlName, htmlstring, displayName)
            addtolog("log", "<li>" + OKIMG + " Reset agregado correctamente</li>")
            # else:
            #    print "vaquita"

        problemSetID += 1
        doc.write(xmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8")
        addtolog("log", "<li>" + OKIMG + " Set de problemas creado correctamente</li>")
        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at createProblemSet")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del set de problemas</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def createProblem(_wb, _displayName, _row, _urlName, _problemattr):
    """
    creates a problem object xml
    :param _displayName:
    :param _row:
    :param _urlName:
    """

    try:
        addtolog("log", "<li>Creación del problema " + str(_urlName) + "</li><ul>")
        sheetProblem = get_sheet(_wb, CPROBLEMASSHEET, CPROBLEMASROW)
        xmlfile = path + "/problem/" + _urlName + ".xml"
        if (
            sheetProblem.cell_value(_row, CPROBLEMASINTENTOSCOL) != ""
            and sheetProblem.cell_value(_row, CPROBLEMASINTENTOSCOL) != "null"
        ):
            max_attempts = int(sheetProblem.cell_value(_row, CPROBLEMASINTENTOSCOL))
        elif (
            _problemattr.get("max_attempts") != ""
            and _problemattr.get("max_attempts") != "null"
        ):
            max_attempts = int(_problemattr.get("max_attempts"))
        else:
            max_attempts = "null"

        if sheetProblem.cell_value(_row, CPROBLEMASSHOWANSWERCOL) != "":
            showanswer = parseShowAnswer(
                _wb, sheetProblem.cell_value(_row, CPROBLEMASSHOWANSWERCOL)
            )
        elif _problemattr.get("showanswer") != "":
            showanswer = _problemattr.get("showanswer")
        else:
            showanswer = "finished"

        if sheetProblem.cell_value(_row, CPROBLEMASWEIGHTCOL) != "":
            weight = sheetProblem.cell_value(_row, CPROBLEMASWEIGHTCOL)
        elif _problemattr.get("weight") != "":
            weight = _problemattr.get("weight")
        else:
            weight = 1

        type = sheetProblem.cell_value(_row, CPROBLEMASTIPOCOL)
        addtolog("log", "<li>" + OKIMG + "Tipo de problema cargado correctamente</li>")
        nounce = sheetProblem.cell_value(_row, CPROBLEMASENUNCIADOCOL)
        addtolog(
            "log", "<li>" + OKIMG + "Enunciado del problema cargado correctamente</li>"
        )

        if type == "Custom":
            page = parse_html_cell(nounce)
            # Make a new document tree
            doc = etree.ElementTree(page)
        else:
            # if nounce[:1] != "<":
            nounce = "<p>" + nounce + "</p>"

            comentary = sheetProblem.cell_value(_row, CPROBLEMASCOMENTARIOCOL)
            if comentary != "":
                comentary = "<div class='detailed-solution'>" + comentary + "</div>"
                addtolog(
                    "log", "<li>" + OKIMG + "Comentario cargado correctamente</li>"
                )

            page = etree.Element(
                "problem",
                display_name=_displayName,
                markdown="null",
                max_attempts=str(max_attempts),
                showanswer=showanswer,
                weight=str(weight),
            )
            # Make a new document tree
            doc = etree.ElementTree(page)
            # add the nounce of the problem
            page.append(parse_html_cell(nounce))
            # switch(type):
            #    case "Multichoice":
            #    break
            if type.lower() == "multichoice":
                problemMultiChoice(_wb, page, _row)
            elif type.lower() == "checkbox":
                problemCheckBox(_wb, page, _row)
            elif type.lower() == "numericalinput":
                problemNumerical(_wb, page, _row)
            elif type.lower() == "textinput":
                problemText(_wb, page, _row)
            elif type.lower() == "inlinedropdown":
                problemInlineDropdown(_wb, page, _row)
            elif type.lower() == "inlinetext":
                problemInlineText(_wb, page, _row)
            else:
                addtolog(
                    "error", "<p>" + WRONGIMG + "Error en la creación del problema</p>"
                )
                addtolog(
                    "error",
                    "<p>"
                    + WRONGIMG
                    + "Error message: Estas tratando de crear problemas sin definir el tipo!!!</p>",
                )

            # add the solution (unique comentary)
            if comentary != "":
                comentary = "<solution>" + comentary + "</solution>"
                # solution = etree.SubElement(page, 'solution')
                page.append(parse_html_cell(comentary))

        doc.write(xmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8")
        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at createProblem")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del problema</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def problemText(_wb, _page, _row):
    """
    add the text input response box
    <stringresponse answer="Michigan" type="ci" >
    <textline size="20"/>
    </stringresponse>
    :param _page:
    :param _row:
    """
    try:
        addtolog("log", "<li>Problema de tipo texto " + str(_row) + "</li><ul>")
        sheetProblem = get_sheet(_wb, CPROBLEMASSHEET, CPROBLEMASROW)
        right_answers_index = sheetProblem.cell_value(_row, CPROBLEMASCORRECTACOL)
        # comma separated
        right_answers_index = [
            int(float(i)) for i in str(right_answers_index).split(";")
        ]
        current_answer_col = CPROBLEMASRESPUESTACOL
        current_answer_index = 1
        right_answers = []
        wrong_answers = []
        while (
            sheetProblem.ncols > current_answer_col
            and sheetProblem.cell_value(_row, current_answer_col) != ""
        ):
            if current_answer_index in right_answers_index:
                right_answers.append(
                    {
                        "answer": fixhtmlentities(
                            str(sheetProblem.cell_value(_row, current_answer_col))
                        ),
                        "hint": fixhtmlentities(
                            str(sheetProblem.cell_value(_row, current_answer_col + 1))
                        ),
                    }
                )
            else:
                wrong_answers.append(
                    {
                        "answer": fixhtmlentities(
                            str(sheetProblem.cell_value(_row, current_answer_col))
                        ),
                        "hint": fixhtmlentities(
                            str(sheetProblem.cell_value(_row, current_answer_col + 1))
                        ),
                    }
                )
            current_answer_index += 1
            current_answer_col += 2

        root = etree.SubElement(
            _page, "stringresponse", answer=str(right_answers[0]["answer"])
        )
        correcthint = etree.SubElement(root, "correcthint")
        correcthint.text = str(right_answers[0]["hint"])
        del right_answers_index[0]

        for answer in right_answers:
            etree.SubElement(root, "additional_answer", answer=str(answer["answer"]))

        etree.SubElement(root, "textline", size="20")
        for answer in wrong_answers:
            wrongAnswer = etree.SubElement(
                root, "stringequalhint", answer=str(answer["answer"])
            )
            wrongAnswer.text = str(answer["hint"])

        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at problemText")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del problema de tipo texto</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def problemNumerical(_wb, _page, _row):
    """
    add the numerical input response box
    <numericalresponse answer="3.14159">
    <responseparam type="tolerance" default=".02" />
    <formulaequationinput />
    </numericalresponse>
    :param _page:
    :param _row:
    """
    try:
        addtolog("log", "<li>Problema de numérico " + str(_row) + "</li><ul>")
        sheetProblem = get_sheet(_wb, CPROBLEMASSHEET, CPROBLEMASROW)
        tolerance = sheetProblem.cell_value(_row, CPROBLEMASCORRECTACOL)
        answerCol = CPROBLEMASRESPUESTACOL

        root = etree.SubElement(
            _page,
            "numericalresponse",
            answer=str(sheetProblem.cell_value(_row, answerCol)),
        )
        etree.SubElement(
            root, "responseparam", type="tolerance", default=str(tolerance)
        )
        hint = etree.SubElement(root, "correcthint")
        hint.text = str(sheetProblem.cell_value(_row, answerCol + 1))
        etree.SubElement(root, "formulaequationinput")
        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at problemNumerical")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del problema de tipo numérico</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def problemMultiChoice(_wb, _page, _row):
    """
    adds the options in a multichoice problem type
    :param _page:
    :param _row:
    """
    try:
        addtolog("log", "<li>Problema de tipo multichoice " + str(_row) + "</li><ul>")
        sheetProblem = get_sheet(_wb, CPROBLEMASSHEET, CPROBLEMASROW)
        rightAnswer = sheetProblem.cell_value(_row, CPROBLEMASCORRECTACOL)
        answerCol = CPROBLEMASRESPUESTACOL
        currentAnswer = 1
        root = etree.SubElement(_page, "multiplechoiceresponse")
        choicegroup = etree.SubElement(root, "choicegroup", type="MultipleChoice")
        while (
            sheetProblem.ncols > answerCol
            and sheetProblem.cell_value(_row, answerCol) != ""
        ):
            choice = etree.SubElement(
                choicegroup,
                "choice",
                correct=str((rightAnswer == currentAnswer)).lower(),
            )
            choice.text = fixhtmlentities(str(sheetProblem.cell_value(_row, answerCol)))
            if str(sheetProblem.cell_value(_row, answerCol + 1)) != "":
                hintText = (
                    "<choicehint>"
                    + str(sheetProblem.cell_value(_row, answerCol + 1))
                    + "</choicehint>"
                )
                choice.append(parse_html_cell(hintText))

            currentAnswer += 1
            answerCol += 2
        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at problemMultiChoice")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del problema de tipo multichoice</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def problemCheckBox(_wb, _page, _row):
    """
    adds the options in a checkbox problem type
    :param _page:
    :param _row:
    """
    try:
        addtolog("log", "<li>Problema de tipo checkbox " + str(_row) + "</li><ul>")
        sheetProblem = get_sheet(_wb, CPROBLEMASSHEET, CPROBLEMASROW)
        rightAnswer = sheetProblem.cell_value(_row, CPROBLEMASCORRECTACOL)
        # comma separated
        rightAnswer = str(rightAnswer).split(";")
        answerCol = CPROBLEMASRESPUESTACOL
        currentAnswer = 1
        root = etree.SubElement(_page, "choiceresponse")
        choicegroup = etree.SubElement(root, "checkboxgroup", direction="Vertical")
        while (
            sheetProblem.ncols > answerCol
            and sheetProblem.cell_value(_row, answerCol) != ""
        ):
            choice = etree.SubElement(
                choicegroup,
                "choice",
                correct=str(str(currentAnswer) in rightAnswer).lower(),
            )
            choice.text = fixhtmlentities(str(sheetProblem.cell_value(_row, answerCol)))
            if str(sheetProblem.cell_value(_row, answerCol + 1)) != "":
                hintText = (
                    "<choicehint>"
                    + str(sheetProblem.cell_value(_row, answerCol + 1))
                    + "</choicehint>"
                )
                choice.append(parse_html_cell(hintText))

            currentAnswer += 1
            answerCol += 2

        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at problemCheckBox")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del problema de tipo checkbox</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def problemInlineDropdown(_wb, _page, _row):
    """
    <problem>
    <optionresponse>
        <p style="display:inline">\(Pr[F_s] = Pr\Big[ \big( F_1\)</p>
        <optioninput label="" options="('&#x2229;','&#x222a;')" correct="&#x2229;" inline="1"></optioninput>
        <p style="display:inline">\(F_2 \big) \)</p>
      <optioninput label="" options="('&#x2229;','&#x222a;')" correct="&#x2229;" inline="1"></optioninput>
        <p style="display:inline">\(F_3 \Big] \)</p>
    </optionresponse>
    </problem>
    """
    try:
        addtolog(
            "log", "<li>Problema de tipo inlinedropdown " + str(_row) + "</li><ul>"
        )
        sheetProblem = get_sheet(_wb, CPROBLEMASSHEET, CPROBLEMASROW)
        enunciadoText = sheetProblem.cell_value(_row, CPROBLEMASENUNCIADOCOL)
        enunciadoSplit = re.split(r"\[\{+|\}\]+", str(enunciadoText))
        enunciadoRespuestas = re.findall(r"\[\{(.*?)\}\]", str(enunciadoText))
        for node in _page.getiterator():
            if node.tag == "p":
                _page.remove(node)  # we remove the nounce in this type of problems
        root = etree.SubElement(_page, "optionresponse")
        for enunciadoPart in enunciadoSplit:
            if enunciadoPart in enunciadoRespuestas:
                # <optioninput label="" options="('&#x2229;','&#x222a;')"
                #   correct="&#x2229;" inline="1"></optioninput>
                pass
                respuestaSplit = enunciadoPart.split(";")
                correcta = ""
                nounce = '<optioninput label="" options="('
                for respuesta in respuestaSplit:
                    if respuesta.startswith("***"):
                        correcta = str(respuesta.replace("***", ""))
                        respuesta = str(respuesta.replace("***", ""))
                    nounce = nounce + "'" + respuesta + "',"
                nounce = (
                    nounce[:-1]
                    + ')" correct="'
                    + correcta
                    + '" inline="1"></optioninput>'
                )
                root.append(parse_html_cell(nounce))
            else:
                nounce = '<p style="display:inline">' + enunciadoPart + "</p>"
                root.append(parse_html_cell(nounce))
        """
        <script type="text/javascript">
            $('span.status').css('display','none');
            $("button.show").click(function(){
                console.log("fsgf")
                if (this.textContent =="Show Answer Reveal Answer"||this.textContent =="Mostrar respuesta Reveal Answer"){
                    $('span[id^="answer"]',$(this.parentNode.parentNode)).after($('<b>}</b>'));
                    $('span[id^="answer"]',$(this.parentNode.parentNode)).before($('<b>{</b>'));
                }
                else{
                    $("b:contains('{')",$(this.parentNode.parentNode)).remove();
                    $("b:contains('}')",$(this.parentNode.parentNode)).remove();
                }
            });
        </script>
        """
        javascriptAux = (
            '<script type="text/javascript">'
            + '$("button.show").click(function(){'
            + 'if (this.textContent.toLowerCase().startsWith("show")||'
            + 'this.textContent.toLowerCase().startsWith("mostrar")){'
            + "$('span[id^=\"answer\"]',$(this.parentNode.parentNode))"
            + ".after($('<b>}</b>'));"
            + "$('span[id^=\"answer\"]',$(this.parentNode.parentNode))"
            + ".before($('<b>{</b>'));"
            + "}else{"
            + "$(\"b:contains('{')\",$(this.parentNode.parentNode)).remove();"
            + "$(\"b:contains('}')\",$(this.parentNode.parentNode)).remove();"
            + "}});</script>"
        )
        _page.append(
            etree.parse(
                io.StringIO(javascriptAux),
                etree.XMLParser(recover=True, encoding="utf-8"),
            ).getroot()
        )
        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at problemInlineDropdown")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del problema de tipo inlinedropdown</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def problemInlineText(_wb, _page, _row):
    """
    <problem>
    <stringresponse answer="Michigan" type="ci" inline="1" >
      <additional_answer>Dr. Martin Luther King, Junior</additional_answer>
      <additional_answer>Martin Luther King, Jr.</additional_answer>
      <additional_answer>Martin Luther King</additional_answer>
      <p style="display:inline">Which US state has Lansing as its capital?</p>
      <textline size="20" inline="1"/>
    </stringresponse>
    <stringresponse answer="Michigan" type="ci" inline="1" >
      <p style="display:inline">Which US state has Lansing as its capital?</p>
      <textline size="20" inline="1"/>
      <p style="display:inline">adsfafdadsfasdf?</p>
    </stringresponse>

    <solution>
    <div class="detailed-solution">
    <p>Explanation</p>

    <p>Lansing is the capital of Michigan, although it is not Michigan's largest city,
    or even the seat of the county in which it resides.</p>

    </div>
    </solution>

    </problem>
    """
    try:
        addtolog("log", "<li>Problema de tipo inlinetext " + str(_row) + "</li><ul>")
        sheetProblem = get_sheet(_wb, CPROBLEMASSHEET, CPROBLEMASROW)
        enunciadoText = sheetProblem.cell_value(_row, CPROBLEMASENUNCIADOCOL)
        enunciadoSplit = re.split(r"\[\{+|\}\]+", str(enunciadoText))
        enunciadoRespuestas = re.findall(r"\[\{(.*?)\}\]", str(enunciadoText))
        for node in _page.getiterator():
            if node.tag == "p":
                _page.remove(node)  # we remove the nounce in this type of problems
        for enunciadoPart in enunciadoSplit:
            if enunciadoPart in enunciadoRespuestas:
                pass
                """
                <stringresponse answer="Michigan" type="ci" inline="1" >
                  <additional_answer>Dr. Martin Luther King, Junior</additional_answer>
                  <additional_answer>Martin Luther King, Jr.</additional_answer>
                  <additional_answer>Martin Luther King</additional_answer>
                  <textline size="20" inline="1"/>
                </stringresponse>
                """
                respuestaSplit = enunciadoPart.split(";")
                respuestaLenght = 0
                nounce = (
                    '<stringresponse answer="'
                    + str(respuestaSplit[0])
                    + '" type="ci" inline="1" >'
                )
                for respuesta in respuestaSplit:
                    nounce = (
                        nounce
                        + "<additional_answer>"
                        + str(respuesta)
                        + "</additional_answer>"
                    )
                    if len(respuesta) > respuestaLenght:
                        respuestaLenght = len(respuesta) + 2
                nounce = (
                    nounce
                    + '<textline size="'
                    + str(respuestaLenght)
                    + '" inline="1"/></stringresponse>'
                )
                _page.append(parse_html_cell(nounce))
            else:
                nounce = '<p style="display:inline">' + str(enunciadoPart) + "</p>"
                _page.append(parse_html_cell(nounce))
        """
        <script type="text/javascript">
            $('p.status').css('display','none');
            $("button.show").click(function(){
                if (this.textContent =="Show Answer Reveal Answer"||this.textContent =="Mostrar respuesta Reveal Answer"){
                    $('p.answer',$(this.parentNode.parentNode)).after($('<b>}</b>'));
                    $('p.answer',$(this.parentNode.parentNode)).before($('<b>{</b>'));
                }
                else{
                    $("b:contains('{')",$(this.parentNode.parentNode)).remove();
                    $("b:contains('}')",$(this.parentNode.parentNode)).remove();
                }
            });
        </script>
        """
        javascriptAux = (
            '<script type="text/javascript">'
            + "$('.status').css('display','none');"
            + '$("button.show").click(function(){'
            + 'if (this.textContent.toLowerCase().startsWith("show")||this.textContent.toLowerCase().startsWith("mostrar")){'
            + "$('p.answer',$(this.parentNode.parentNode)).after($('<b>}</b>'));"
            + "$('p.answer',$(this.parentNode.parentNode)).before($('<b>{</b>'));"
            + "}else{"
            + "$(\"b:contains('{')\",$(this.parentNode.parentNode)).remove();"
            + "$(\"b:contains('}')\",$(this.parentNode.parentNode)).remove();"
            + "}});</script>"
        )
        _page.append(
            etree.parse(
                io.StringIO(javascriptAux),
                etree.XMLParser(recover=True, encoding="utf-8"),
            ).getroot()
        )
        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at problemInlineText")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del problema inline text </p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def createVertical(
    _wb,
    _Chapter,
    _Subsection,
    _Lesson,
    _row,
    _urlName,
    _ChapterDisplayName,
    _SubsectionDisplayName,
):
    """
    creates the vertical files wich has links to every element in the vertical
    html Objetivos
    video Video
    html Resumen
    forumlink Foro
    :param _Chapter:
    :param _Subsection:
    :param _Lesson:
    :param _row:
    :param _urlName:
    :param _ChapterDisplayName:
    :param _SubsectionDisplayName:
    """
    try:
        addtolog(
            "log", "<p><b>Creación del vertical : " + str(_urlName) + "</b></p><ul>"
        )
        baseName = (
            "Unidad"
            + str(int(_Chapter))
            + "Subsection"
            + str(int(_Subsection))
            + "Vertical"
            + str(int(_Lesson))
        )
        sheetCurso = get_sheet(_wb, CCURSOSHEET, CCURSOROW)
        addtolog("log", "<li>" + OKIMG + " Carga de hoja curso</li>")
        sheetDatosGenerales = get_sheet(_wb, CDATOSGENERALESSHEET, CDATOSGENERALESROW)
        addtolog("log", "<li>" + OKIMG + " Carga de hoja datos generales</li>")

        courseName = sheetDatosGenerales.cell_value(
            CDATOSGENERALESNOMBREPOS[0], CDATOSGENERALESNOMBREPOS[1]
        )
        displayName = sheetCurso.cell_value(_row, CCURSOLESSONDISPLAYNAMECOL)
        xmlfile = path + "/vertical/" + _urlName + ".xml"
        page = etree.Element("vertical", display_name=displayName)
        # Make a new document tree
        doc = etree.ElementTree(page)

        if sheetCurso.cell_value(_row, CCURSOOBJETIVOSCOL) != "":
            # Unidad1Subsection1Vertical1Objetivos
            urlName = baseName + "Objetivos"
            etree.SubElement(page, "html", url_name=urlName)
            # Here we check for URL filter and stuff patatas
            htmlstring = sheetCurso.cell_value(_row, CCURSOOBJETIVOSCOL)
            createHtml(urlName, htmlstring, displayName)
            displayName = ""
            addtolog("log", "<li>" + OKIMG + " Objetivos agregado correctamente</li>")

        if sheetCurso.cell_value(_row, CCURSOVIDEOCOL) != "":
            # Unidad1Subsection1Vertical1Video
            urlName = baseName + "Video"
            etree.SubElement(page, "video", url_name=urlName)
            createVideo(
                urlName, sheetCurso.cell_value(_row, CCURSOVIDEOCOL), displayName, _wb
            )
            displayName = ""
            addtolog("log", "<li>" + OKIMG + " Video agregado correctamente</li>")

        if sheetCurso.cell_value(_row, CCURSORESUMECOL) != "":
            # Unidad1Subsection1Vertical1Resumen
            urlName = baseName + "Resumen"
            # Here we check for URL filter and stuff patatas
            etree.SubElement(page, "html", url_name=urlName)
            htmlstring = sheetCurso.cell_value(_row, CCURSORESUMECOL)
            createHtml(urlName, htmlstring, displayName)
            displayName = ""
            addtolog("log", "<li>" + OKIMG + " Resumen agregado correctamente</li>")

        if sheetCurso.cell_value(_row, CCURSOFORUMCOL) != "":
            # Unidad1Subsection1Vertical1Discussion
            urlName = baseName + "Discussion"
            etree.SubElement(page, "discussion", url_name=urlName)
            discussionCategory = (
                "Tema " + str(int(_Chapter)) + ": " + _ChapterDisplayName
            )
            discussionID = courseName + str(int(_Chapter)) + "_" + str(int(_Subsection))
            createDiscussion(
                urlName,
                discussionCategory,
                _SubsectionDisplayName,
                discussionID,
                displayName,
            )
            displayName = ""
            addtolog(
                "log", "<li>" + OKIMG + " Enlace al foro agregado correctamente</li>"
            )

        doc.write(xmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8")
        addtolog("log", "</ul>")
    except Exception as e:
        logger.exception("Failure at createVertical")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del vertical</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def uploadSubs(_url, _subid):
    try:
        subfile = urllib.request.urlopen(_url)
        output = open(path + "/static/subs/" + _subid, "wb")
        output.write(subfile.read())
        output.close()
    except Exception as e:
        logger.exception("Failure at uploadSubs")
        addtolog(
            "log",
            "<li>" + WRONGIMG + "Error al subir el subtitulo:" + str(e) + "</li>",
        )
        addtolog(
            "error", "<p>" + WRONGIMG + "Error al subir el subtitulo:" + _url + "</p>"
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p>")


def substosjson(_subid, _videoid):
    file = open(path + "/static/subs/" + _subid)
    jsonfile = path + "/static/subs_" + _videoid + ".srt.sjson"
    stringu = file.read()
    splitgu = stringu.splitlines()
    strsjson = {"start": [], "end": [], "text": []}
    x = 0
    while x < len(splitgu):
        i = 1
        if len(splitgu) > x + 2:
            start = splitgu[x + 1].split(" --> ")[0]
            start = (
                int(start.split(":")[0]) * 3600000
                + int(start.split(":")[1]) * 60000
                + int(float(start.split(":")[2].replace(",", ".")) * 1000)
            )
            end = splitgu[x + 1].split(" --> ")[1]
            end = (
                int(end.split(":")[0]) * 3600000
                + int(end.split(":")[1]) * 60000
                + int(float(end.split(":")[2].replace(",", ".")) * 1000)
            )
            text = splitgu[x + 2]
            while splitgu[x + 2 + i] != "":
                text = text + "\n" + splitgu[x + 2 + i]
                i = i + 1
            strsjson["start"].append(start)
            strsjson["end"].append(start)
            strsjson["text"].append(text)
        x = x + 3 + i
    with open(jsonfile, "w") as fp:
        json.dump(strsjson, fp)


def createVideo(_urlName, _videoURL, _displayName, _wb):
    """
    generates the video xml file
    :param _urlName:
    :param _videoURL:
    :param _displayName:
    """
    try:
        xmlfile = path + "/video/" + _urlName + ".xml"
        page = etree.Element(
            "video",
            youtube="1.00:" + _videoURL,
            display_name=_displayName,
            youtube_id_1_0=_videoURL,
        )
        # check if the XNF has the subs sheet
        try:
            sheetSubs = get_sheet(_wb, CSUBSHEET, CSUBROW)
            for row in range(1, sheetSubs.nrows):
                if _videoURL == sheetSubs.cell_value(
                    row, CSUBVIDEOIDCOL
                ):  # if the video has subs
                    for col in range(1, sheetSubs.ncols):
                        if sheetSubs.cell_value(row, col) != "":
                            # and upload it
                            uploadSubs(
                                sheetSubs.cell_value(row, col),
                                sheetSubs.cell_value(CSUBSHEADERROW, col)
                                + _videoURL
                                + ".srt",
                            )
                            if (
                                sheetSubs.cell_value(CSUBSHEADERROW, col).lower()
                                == "en"
                            ):
                                page.attrib["sub"] = _videoURL
                                substosjson(
                                    sheetSubs.cell_value(CSUBSHEADERROW, col)
                                    + _videoURL
                                    + ".srt",
                                    _videoURL,
                                )
                            else:
                                # for each sub add a subelement transcript
                                etree.SubElement(
                                    page,
                                    "transcript",
                                    language=sheetSubs.cell_value(CSUBSHEADERROW, col),
                                    src="subs/"
                                    + sheetSubs.cell_value(CSUBSHEADERROW, col)
                                    + _videoURL
                                    + ".srt",
                                )
        except Exception:
            logger.exception("Something bad happened")

        # Make a new document tree

        doc = etree.ElementTree(page)

        doc.write(xmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8")
    except Exception as e:
        logger.exception("Failure at createVideo")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del video</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def createHtml(_urlName, _htmlText, _displayName):
    """
    generates the xml and html file wich will link the html
    into the course
    :param _urlName:
    :param _htmlText:
    :param _displayName:
    """
    try:
        xmlfile = path + "/html/" + _urlName + ".xml"
        htmlfile = path + "/html/" + _urlName + ".html"
        page = etree.Element("html", filename=_urlName, display_name=_displayName)
        # Make a new document tree
        doc = etree.ElementTree(page)
        rawhtml = False
        htmlstring = _htmlText
        cssfilter = ""
        altbase = ""
        while (
            htmlstring.find("##from:") > -1
            and htmlstring.find(";##endfrom") > -1
            and htmlstring.find("##from:") < htmlstring.find(";##endfrom")
        ):
            iniciostring = htmlstring[0 : htmlstring.find("##from:")]
            scrapstring = htmlstring[
                htmlstring.find("##from:") : htmlstring.find(";##endfrom")
            ]
            finstring = htmlstring[htmlstring.find(";##endfrom") + 10 : len(htmlstring)]
            scrapdata = scrapstring.replace("##from:", "")
            scrapdata = scrapdata.split(
                ";##"
            )  # re.split(';##filter:|;##base:',scrapdata)
            for i in range(0, len(scrapdata)):
                if scrapdata[i].startswith("base:"):
                    altbase = scrapdata[i].lstrip("base:")
                if scrapdata[i].startswith("filter:"):
                    cssfilter = scrapdata[i].lstrip("filter:")

            scrapstring = scrap.scrappWeb(
                scrapdata[0], cssfilter, path + "/static/", altbase
            )

            htmlstring = iniciostring + scrapstring + finstring
            rawhtml = True

        """
        if htmlstring.startswith('##from:'):
            htmldata= htmlstring.strip('##from:').split(';##filter:')
            if len(htmldata)==2:
                cssfilter=htmldata[1]
            htmlstring = scrap.scrappWeb(htmldata[0],cssfilter, path +"/static/")
        """
        if rawhtml:
            doc.getroot().attrib["editor"] = "raw"
        doc.write(xmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8")
        # TO-DO VALIDATE HTMLS
        with open(htmlfile, "w") as html:
            html.write(htmlstring)
    except Exception as e:
        logger.exception("Failure at createHtml")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del html en "
            + _urlName
            + "</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def createDiscussion(
    _urlName, _discussionCategory, _SubsectionDisplayName, _discussionID, _displayName
):
    """
    generates the discussion file wich will link the discussion
    into the course
    :param _urlName:
    :param _discussionCategory:
    :param _SubsectionDisplayName:
    :param _discussionID:
    :param _displayName:
    """
    try:
        xmlfile = path + "/discussion/" + _urlName + ".xml"
        page = etree.Element(
            "discussion",
            discussion_category=_discussionCategory,
            discussion_target=_SubsectionDisplayName,
            discussion_id=_discussionID,
            display_name=_displayName,
        )
        # Make a new document tree
        doc = etree.ElementTree(page)

        doc.write(xmlfile, pretty_print=True, xml_declaration=False, encoding="utf-8")
    except Exception as e:
        logger.exception("Failure at createDiscussion")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del foro</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def findProblems(_wb, _chapter, _subSection, _lesson):
    """
    :param _chapter:
    :param _subSection:
    :param _lesson:
    :return:
    """
    sheetProblems = get_sheet(_wb, CPROBLEMASSHEET, CPROBLEMASROW)
    sheetProblems.nrows

    sheetProblems.nrows
    for row in range(1, sheetProblems.nrows):
        if (
            _chapter == sheetProblems.cell_value(row, CPROBLEMASIDUNIDADCOL)
            and _subSection == sheetProblems.cell_value(row, CPROBLEMASIDSUBSECCIONCOL)
            and _lesson == sheetProblems.cell_value(row, CPROBLEMASIDLECCIONCOL)
        ):
            return row
        else:
            if (
                sheetProblems.cell_type(row, CPROBLEMASIDUNIDADCOL) == 0
                or sheetProblems.cell_type(row, CPROBLEMASIDUNIDADCOL) == 5
                or sheetProblems.cell_type(row, CPROBLEMASIDUNIDADCOL) == 6
            ):
                return -1
    return -1


def checkVersion(_wb):
    try:
        addtolog("log", "<p><b>Comprobando la versión del template </b></p><ul>")
        sheet = get_sheet(_wb, CDATOSGENERALESSHEET, CDATOSGENERALESROW)
        if get_version(_wb) == CDATOSGENERALESVERSION:
            addtolog("log", "<li>" + OKIMG + " versión correcta</li>")
            addtolog("log", "</ul>")
            return True
        else:
            addtolog(
                "log",
                "<li>"
                + OKIMG
                + " versión incorrecta se esperaba la versión "
                + CDATOSGENERALESVERSION
                + " de la plantilla</li>",
            )
            addtolog("log", "</ul>")
            return False
    except Exception as e:
        logger.exception("Failure at checkVersion")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog("log", "</ul>")
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la comprobacion de la versión</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")
        return False


def fixhtmlentities(text):
    try:
        result = text
        for before, after in ENTITIES:
            result = re.sub(before, after, result)
        return str(result)
    except Exception as e:
        logger.exception("Failure at fixhtmlentities")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la conversión de entidades html</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def addtolog(log, message):
    global stufftoreturn
    stufftoreturn[log] += str(message)


def make_tarfile(_wb):
    """
    Packs all in a targz file ready to import.
    """
    try:
        logger.info("Creating tarball course")
        addtolog("log", "<p><b>Creación del paquete targz </b></p><ul>")
        sheet = get_sheet(_wb, CDATOSGENERALESSHEET, CDATOSGENERALESROW)
        tarpath = (
            path
            + "/"
            + sheet.cell_value(CDATOSGENERALESNOMBREPOS[0], CDATOSGENERALESNOMBREPOS[1])
            + ".tar.gz"
        )
        with tarfile.open(tarpath, "w:gz") as tar:
            for f in os.listdir(path):
                tar.add(path + "/" + f, arcname=os.path.basename(f))
            tar.close()
        addtolog(
            "log",
            "<li>" + OKIMG + " Creación del paquete targz completada con éxito </li>",
        )
        addtolog("log", "</ul>")
        return (
            sheet.cell_value(CDATOSGENERALESNOMBREPOS[0], CDATOSGENERALESNOMBREPOS[1])
            + "/"
            + sheet.cell_value(CDATOSGENERALESNOMBREPOS[0], CDATOSGENERALESNOMBREPOS[1])
            + ".tar.gz"
        )

    except Exception as e:
        logger.exception("Failure at make_tarfile")
        addtolog(
            "log",
            "<li id='error"
            + str(len(stufftoreturn["error"]))
            + "'>"
            + WRONGIMG
            + "Error message:"
            + str(e)
            + "</li>",
        )
        addtolog(
            "error",
            "<a href='#error"
            + str(len(stufftoreturn["error"]))
            + "'><p>"
            + WRONGIMG
            + "Error en la creación del paquete targz</p>",
        )
        addtolog("error", "<p>" + WRONGIMG + "Error message:" + str(e) + "</p></a>")


def parse_html_cell(cell_contents):
    elem = etree.parse(
        io.StringIO(fixhtmlentities(cell_contents)),
        etree.HTMLParser(recover=True, encoding="utf-8")
    ).getroot()
    if elem.tag == "html":
        children = elem.getchildren()
        if len(children) == 1 and children[0].tag == "body":
            elem = children[0]
            children = elem.getchildren()
            if len(children) > 1:
                elem.tag = "div"
            else:
                elem = children[0]
            return elem
    raise Exception("Something unexpected happened")
