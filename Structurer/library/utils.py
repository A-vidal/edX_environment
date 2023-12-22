import os
import re
import argparse
import datetime

from fuzzywuzzy import fuzz # only for the similar function

MC_proposals = "./MC proposals from partners/"
Docs_path = "./Data/Docs.csv"
Register_path = "./Data/Register.csv"

# select the most similar string (pattern) from a list (place)
def similar(pattern: str, place: list) -> str:
    # output: the most similar string
    return max([(fuzz.token_set_ratio(pattern,i),i) for i in place])[1]

# format the name with version and date
def format_vesrion(MC_code: str) -> str:
    # MC_code: the code of the course
    # output: the formal name of the tar.gz
    formato = "^MC\d{2}_v\d+_\d{6}.tar.gz$"
    name_file = list(filter(lambda x: re.match(MC_code+formato[8:13], x), os.listdir("./Final_output")))[-1]
    vesrion = int(name_file[6:name_file.rfind("_")])
    fecha = datetime.date.today().strftime("%d%m%y")
    final = MC_code + f"_v{vesrion + 1}_" + fecha
    return final

# get the arguments to the python execution
def get_args(args: tuple[type], args_help: tuple[str] = ("",)) -> list:
    # input: list of tuples (name, type, help)
    # output: list of the arguments
    is_help = not args_help == ("",)
    args_len = len(args)
    assert not is_help or args_len == len(args_help), "args and help must be same size"
    parser = argparse.ArgumentParser()
    arg_form = "input_"
    for i in range(args_len):
        if is_help:
            parser.add_argument(arg_form + str(i), type=args[i], help=args_help[i])
        else:
            parser.add_argument(arg_form + str(i), type=args[i], help=f"a {args[i]} argument")
    arguments = vars(parser.parse_args())
    return  [arguments[arg_form + str(i)] for i in range(args_len)]

class MC_docs:
    def __init__(self, 
                 proposals: str = "./MC proposals from partners/", 
                 docs: str = "./Data/Docs.csv", 
                 register: str = "./Data/Register.csv") -> None:
        self.MC_proposals = proposals
        self.Docs_path = docs
        self.Register_path = register
    
    # Search in (MC_proposals) for a (title) and a (partner)
    def word_find(self, title : str, partner : str) -> str:
        # outpùt: path like "./MC_proposals/partner/title.docx"
        
        dir1 = os.listdir(self.MC_proposals)
        
        Inst = list(filter(lambda x: re.match(".*"+partner+".*", x), dir1))[0]
        
        dir2 = os.listdir(self.MC_proposals + Inst)
        
        try:
            doc = list(filter(lambda x: re.match(".*"+title+".*", x), dir2))[0]
        except IndexError: # try inverse search
            doc = similar((f"{partner} - {title}.docx")[::-1], list(map(lambda x: x[::-1], dir2)))[::-1]
        
        return self.MC_proposals + Inst + "/" + doc

    # return the document related to that MC_code (code)
    def get_doc(self, code: str) -> str:
        # output: the path of the document related
        _ = open(self.Docs_path)
        iterator = [i.replace("\n", "").split("\t") for i in _.readlines()]
        for row in iterator:
            if str(row[0]) == code:
                MC_name = str(row[1])
                print("The doc of the course is:", MC_name)
                doc_word = self.word_find(row[1], row[2])
        _.close()
        del _
        return doc_word

    # create a register of which MC are converted to tar.gz 
    def register(self):
        tars = list(filter(lambda x: x.endswith(".tar.gz"),os.listdir("./Final_output")))

        file = open(self.Docs_path, "r")
        lines = file.readlines()
        file.close()

        intro = ["MC code", "TAR file"]

        lines[0] = "\t".join(intro)

        for i in range(1, len(lines)):
            MC = lines[i].replace("\n", "").split("\t")
            tar = str(any(filter(lambda x: re.match(".*"+lines[i].split("\t")[0]+".*", x.split(".")[0]), tars)))
            try:
                MC[3] = tar
            except IndexError:
                MC.append(tar)
            lines[i] = "\t".join([MC[0], MC[3]])

        file = open(self.Register_path, "w")
        file.write("\n".join(lines))
        file.close()

        l = [i.split("\t")[0] for i in lines[1:] if not eval(i.split("\t")[-1])]

        print("Register Completed:\nRemaining: ", len(l),"\n", l, "\n", sep="")


# Search in (MC_proposals) for a (title) and a (partner)
def word_find(title : str, partner : str, doc_path: str = MC_proposals) -> str:
    # outpùt: path like "./MC_proposals/partner/title.docx"
    
    dir1 = os.listdir(doc_path)
    
    Inst = list(filter(lambda x: re.match(".*"+partner+".*", x), dir1))[0]
    
    dir2 = os.listdir(doc_path + Inst)
    
    try:
        doc = list(filter(lambda x: re.match(".*"+title+".*", x), dir2))[0]
    except IndexError: # try inverse search
        doc = similar((f"{partner} - {title}.docx")[::-1], list(map(lambda x: x[::-1], dir2)))[::-1]
    
    return doc_path + Inst + "/" + doc

# return the document related to that MC_code (code)
def get_doc(code: str, docs_path: str = Docs_path) -> str:
    # output: the path of the document related
    _ = open(docs_path)
    iterator = [i.replace("\n", "").split("\t") for i in _.readlines()]
    for row in iterator:
        if str(row[0]) == code:
            MC_name = str(row[1])
            print("The doc of the course is:", MC_name)
            doc_word = word_find(row[1], row[2])
    _.close()
    del _
    return doc_word

# create a register of which MC are converted to tar.gz 
def register(docs_path: str = Docs_path, register_path: str = Register_path):
    tars = list(filter(lambda x: x.endswith(".tar.gz"),os.listdir("./Final_output")))

    file = open(docs_path, "r")
    lines = file.readlines()
    file.close()

    intro = ["MC code", "TAR file"]

    lines[0] = "\t".join(intro)

    for i in range(1, len(lines)):
        MC = lines[i].replace("\n", "").split("\t")
        tar = str(any(filter(lambda x: re.match(".*"+lines[i].split("\t")[0]+".*", x.split(".")[0]), tars)))
        try:
            MC[3] = tar
        except IndexError:
            MC.append(tar)
        lines[i] = "\t".join([MC[0], MC[3]])

    file = open(register_path, "w")
    file.write("\n".join(lines))
    file.close()

    l = [i.split("\t")[0] for i in lines[1:] if not eval(i.split("\t")[-1])]

    print("Register Completed:\nRemaining: ", len(l),"\n", l, "\n", sep="")

# format the name with version and date
def format_vesrion(MC_code: str) -> str:
    # MC_code: the code of the course
    # output: the formal name of the tar.gz
    formato = "^MC\d{2}_v\d+_\d{6}.tar.gz$"
    name_file = list(filter(lambda x: re.match(MC_code+formato[8:13], x), os.listdir("./Final_output")))[-1]
    vesrion = int(name_file[6:name_file.rfind("_")])
    fecha = datetime.date.today().strftime("%d%m%y")
    final = MC_code + f"_v{vesrion + 1}_" + fecha
    return final