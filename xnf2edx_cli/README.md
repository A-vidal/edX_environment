# Description

CLI tool for converting XNF files to .tar.gz edX courses.

Based in the work developed by leosamu at:
https://github.com/leosamu/UPVX-tools

# Installation
There are two ways to install the project: the traditional way & using Docker

## Docker
Using a Docker container is the easiest way if you want to avoid errors that
might arise from incompatibilities with your own environment or if you don't
want to install any additional software, create virtual environments, etc.
However, you will need to install Docker in your system, of course.

You have the official docs about setting up Docker in various OS here:

https://docs.docker.com/get-docker/

### Getting the image
When using Docker, once again, you have two possibilities to get the image:

1. Download a prebuilt image from Docker Hub (available at
   https://hub.docker.com/repository/docker/serbaf/xnf2edx_cli):
    
`docker image pull serbaf/xnf2edx_cli:latest`

2. Build the image yourself using the Dockerfile in the project (last argument
   in the command is the path to the Dockerfile parent dir):

`docker build -t serbaf/xnf2edx .`

### Running the container
Once the image has been built or downloaded, you can execute the script within
a running container. To do so, you will need to use the call to the script
normally (`python main.py some_xnf_file.xlsm`) but within a xnf2edx running
container (`docker run serbaf/xnf2edx_cli`) and sharing the input file and the
output directory between your host and the container, which can be done using
volumes (`-v /your/host/path:/container/path`).

The output path in the container will always be `/xnf2edx_cli/data/output`, and
you can map it to whatever directory you want in your computer. The input file
can be mapped freely, but the easiest might be to put it simply in the
`xnf2edx_cli` directory, which is the working dir for the container.

One example of execution would be the following:

```
docker run 
-v /home/user/xnf2edx_cli/data/input/TemplateXNF.xlsm:/xnf2edx_cli/TemplateXNF.xlsm 
-v /home/user/Downloads/test/:/xnf2edx_cli/data/output/ 
serbaf/xnf2edx_cli 
python main.py TemplateXNF.xlsm
```

Using Windows:
```
docker run 
-v C:/Users/ndesp/Downloads/TemplateXNF.xlsm:/xnf2edx_cli/TemplateXNF.xlsm 
-v C:/Users/ndesp/Downloads/test:/xnf2edx_cli/data/output/ 
serbaf/xnf2edx_cli 
python main.py TemplateXNF.xlsm
```

## Traditional way
This way consists in simply downloading the source code, preparing the Python
environment and launching the script. It's simple enough, however, maybe in
some environments unexpected problems might appear, in which case you can
always use the Docker method.

1. Clone the project

    `git clone https://git.upv.es/serpucga/xnf2edx_cli.git`

2. Go to the project root directory

    `cd xnf2edx_cli`

3. Create a python3 (3.6 or newer) virtual environment:

    ```
    python -m venv .venv
    ```
    
4. Activate the environment:
    
    - On Linux:
        `source .venv/bin/activate`

    - On Windows:
        `.\venv\Scripts\activate.bat`

5. Install the requirements in the active venv (use dev.txt if you need the
   development/debugging libs)

    `python -m pip install -r requirements/prod.txt`

6. Launch passing the XNF file as the only argument

    `python main.py ~/Downloads/XNF.xlsm`

7. You will find the generated outputs at dir **./data/output/{xnffilename}/**
    1. .tar.gz course: **{coursecode}.tar.gz**
    2. Untarred course directory: **{coursecode}**
    3. Logs: **logs.html**
    4. Possible errors (empty if everything OK): **errors.html**

# Templates and test files

In the assets folder you will find an excel file with a template in English and
another with a template in Spanish that you can modify to create your courses
and an example file with questions that can be imported to the corresponding
tab calling the macro with control+U from the spreadsheet (remember to
activate macros when loading the spreadsheet).

# Videos with instructions

You can find a list of videos explaining how to use the tool in
https://media.upv.es/#/portal/channel/be588530-4bcb-11ed-8670-895e92548ce9

These videos were created in Spanish to help the UPV professors creating MOOCs,
so there are some references to internal processes that will not help you
(mainly to the extraction of the codes of the videos from the UPV media system,
but we have created a specific video explaining how to extract data from a
Youtube playlist).

Most of the videos have been dubbed in English using an automated
text-to-speech process that gets the translation from transcript files.
