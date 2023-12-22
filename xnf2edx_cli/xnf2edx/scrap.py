__author__ = "Leonardo Salom Muñoz, Sergio Puche García"
import urllib
from lxml import html, cssselect
import requests
import sys
import importlib
from loguru import logger

from xnf2edx.consts import DATA_OUTPUT

importlib.reload(sys)

validformats = ["png", "jpg", "gif", "bmp", "tif"]


def scrappWeb(url, filter, path, base):
    try:
        # webdata =urllib2.urlopen(url)
        webdata = requests.get(url)
    except Exception:
        return url
    webstring = webdata.text
    # encoding = chardet.detect(webstring)
    # webstring =  webstring.decode(encoding['encoding']).encode('utf-8')
    if filter == "":
        return webstring
    # nyapa da morte for the android course.
    htmlobj = html.fromstring(webstring)
    sel = cssselect.CSSSelector(filter)
    try:
        htmlobj = getImages(sel(htmlobj)[0], path, base)
        htmlobj = html.tostring(htmlobj)
    except IndexError:
        # with open(DATA_OUTPUT.joinpath("ayns.html"), "w+") as f:
        #     logger.info("Awayns")
        #     logger.info(f"Path: {path}")
        #     logger.info(f"Base: {base}")
        #     logger.info(f"CSS filter: {filter} (type {type(filter)})")
        #     f.write(webstring)
        htmlobj = ""
    return htmlobj


def getImages(_htmlobj, path, _base):
    sel = cssselect.CSSSelector("img")
    htmlobj = _htmlobj
    images = sel(htmlobj)
    for image in images:
        originalsrc = image.attrib["src"]
        if validImageFormat(originalsrc):
            if _base != "":
                fileUrl = getFileUrl(_base, originalsrc)
            else:
                fileUrl = getFileUrl(htmlobj.base, originalsrc)

            fileName = path + fileUrl.split("/")[-1].replace("%20", "_")
            staticUrl = "/static/" + fileName.split("/")[-1]
            saveFile(fileUrl, fileName)
            image.attrib["src"] = staticUrl
    return htmlobj


def saveFile(fileUrl, fileName):
    try:
        resource = urllib.request.urlopen(fileUrl)
        output = open(fileName, "wb")
        output.write(resource.read())
        output.close()
    except:
        print("no se ha podido descargar" + fileUrl)


def getFileUrl(url, src):
    if src.startswith("data:"):
        return src
    else:
        return urllib.parse.urljoin(url, src).replace(" ", "%20")


def validImageFormat(src):
    extension = src.split(".")[len(src.split(".")) - 1].lower()
    return extension in validformats
