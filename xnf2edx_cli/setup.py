import re
from pathlib import Path
from setuptools import find_packages, setup

ROOT = Path(__file__).parent
README = ROOT.joinpath("README.md").read_text()
rgx = re.compile(r"""^\s*__version__\s*=\s*["'](\d+\.\d+\.\d+)["']\s*$""")


def get_version(module_init):
    module_path = ROOT.joinpath(module_init)
    with open(module_path) as f:
        for l in f.readlines():
            m = rgx.match(l)
            if m is not None:
                return m[1]
    raise Exception("Couldn't parse version")


setup(
    name="xnf2edx_cli",
    version=get_version("xnf2edx/__init__.py"),
    description="A tool to convert courses from XNF to .tar.gz",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://git.upv.es/serpucga/xnf2edx_cli",
    author="Leonardo Salom Muñoz, Sergio Puche García",
    author_email="leosamu@upv.es, spuche@upv.es",
    license="AGPL3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(),
)
