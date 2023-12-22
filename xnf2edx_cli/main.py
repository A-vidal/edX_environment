__author__ = "Leonardo Salom Muñoz, Sergio Puche García"
__credits__ = "Leonardo Salom Muñoz, Sergio Puche García"
__version__ = "0.0.1-SNAPSHOT"
__maintainer__ = "Sergio Puche García"
__email__ = "spuche@upv.es"
__status__ = "Development"


import argparse
import xlrd
import shutil
from loguru import logger
from pathlib import Path

from xnf2edx.xnf2edx import generate_Edx
from xnf2edx.consts import DATA_OUTPUT


########
# MAIN #
########
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="The Excel file path used as input")
    args = parser.parse_args()

    PROJECT_DIR = DATA_OUTPUT.joinpath(Path(args.input).stem)
    if PROJECT_DIR.exists():
        shutil.rmtree(PROJECT_DIR)

    logger.info("Reading Excel file...")
    wb = xlrd.open_workbook(args.input)
    logger.info("Generating EdX course in a tarball...")
    results = generate_Edx(wb, str(PROJECT_DIR))

    if results["path"] not in (None, ""):
        tarball_path = PROJECT_DIR.joinpath(results["path"])
        dest_path = tarball_path.parent.parent.joinpath(tarball_path.name)
        tarball_path.rename(dest_path)

    if results["log"] not in (None, ""):
        logger.info("Dumping logs...")
        with open(PROJECT_DIR.joinpath("logs.html"), "w") as f:
            f.write(results["log"])
    if results["error"] not in (None, ""):
        logger.info("Dumping error logs...")
        with open(PROJECT_DIR.joinpath("errors.html"), "w") as f:
            f.write(results["error"])

    logger.info("Process completed!")
