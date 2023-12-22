import os
import re

"""
# is important to put the path of the MC_path before calling this file
# the MC_code is used as the name of the carpet of the course
with open("./MC_path.txt") as file:
    MC_path = file.read().strip("\n").strip()
    if MC_path.endswith("/"):
        MC_code = MC_path.split("/")[-2]
    else:
        MC_code = MC_path.split("/")[-1]
        MC_path += "/"
"""
class Find:
    MC_path = ""
    # set the path we ar going to use
    def set_path(path: str):
        # path: de directory of the course
        if path.endswith("/"):
            Find.MC_path = path
        else:
            Find.MC_path = path + "/"

    # Find a document or a file inside the course
    def doc_find(n_sec : int, name : str) -> str:
        # n_sec: number of the section
        # name: name of the file
        # return: the path of the file
        assert Find.MC_path != "", "Is necessary to set the Find.MC_path"
        
        dir1 = os.listdir(Find.MC_path)
        
        Sec = list(filter(lambda x: re.match(".*[s|S]ection.*"+str(n_sec)+".*", x), dir1))[0]
        
        dir2 = os.listdir(Find.MC_path + Sec)
        
        try:
            doc = list(filter(lambda x: re.match(".*"+name.split("(")[0]+".*", x), dir2))[0]
        except:
            print(name, dir2)
            raise IndexError
        
        return Find.MC_path + Sec + "/" + doc

# converts any file to a HTML elemnt to put in the course
def PDFtoHTML(sec: int, text: str, name: str, s_mat: str = "") -> str:
    # sec: number of section of the file
    # text: name of file/s which have to be converted ("file1, file2, " or "file")
    # name: name which apears in the HTML element
    # s_mat: default file name to search (in case is not finded)

    ret = []

    for mat in text.split(","):
        mat = mat.strip() # mat is one element of text
        
        if mat.startswith("http"):
            if mat.endswith(".pdf"):
                ret.append(f'<iframe src="{mat}" width="100%" height="1200"></iframe>')
            else:
                end = mat.split(".")[-1]
                if end == "php" or end == "html" or mat.endswith("/"):
                    ret.append(f'<a href="{mat}">{mat}</a>')
                ret.append(f'<a href="{mat}" download="{name}.{end}">{name}.{end}</a>')
        try:
            fsrc = Find.doc_find(sec, mat)
        except IndexError:
            if s_mat != "":
                fsrc = Find.doc_find(sec, s_mat)
            else:
                raise IndexError

        src = fsrc.split("/")[-1]
        end = src.split(".")[-1]

        if not re.match(".*"+mat.split("(")[0]+".*", src):
            n_src = mat + "." + end
            os.rename(fsrc, fsrc[:fsrc.find(src)] + n_src)

        if src.endswith(".pdf"):
            ret.append(f'<iframe src="/static/{src.split("/")[-1]}" width="100%" height="1200"></iframe>')
        else:
            end = src.split(".")[-1]
            ret.append(f'<a href="/static/{src.split("/")[-1]}" download="{name}.{end}">{name}.{end}</a>')
    
    return "\n".join(ret)

# to convert lists to strings as you like
def formateer(lista : list, final: str) -> str:
    # lista: original list
    # final: the end of every element
    # output: a string of the list
    string = ""
    last = lista[-1]
    for i in lista:
        if type(i) == float:
            string += f"{i:2.1f}" + final
        
        
        if i != last:
            string += ", "
    
    return string

class Revise:
    def __init__(self, MC_code: str, Units: list, Tests: list) -> None:
        # MC_code: the code of the course
        # Units: units from the MC course
        # Tests: tests of the MC course
        self.MC_code = MC_code
        self.Units = Units
        self.Tests = Tests
    
    # revise if the unit has its respective tests
    def test(self, unit: list) -> bool:
        # unit: unit to revise tests
        n = 0
        for test in self.Tests:
            if test[:6:2] == unit[:6:2]:
                n += 1
        
        exp = int(re.findall("[0-9]+", unit[-1])[0])
        
        ret = n == exp
        
        if not ret:
            print(f"error in test {unit[:6:2]}: expected {exp}, had {n}")
        
        return ret
    
    # revise all te units for its tests
    test_list = lambda self: [self.test(i) for i in self.Units if type(i[-2]) == int or type(i[-2]) == float]

    # make an overall evaluation and check if it's coherent
    def notas(self) -> tuple[list, str]:
        # output 1: list of the evaluations of all the units
        # output 2: description of the evaluations
        lista_notas = []

        for i in self.Units:
            if type(i[-2]) == str:
                continue
            
            if i[-2] == None:
                continue
            
            if i[-2] == 0:
                continue
            
            lista_notas.append(i[-2] * 100)

        if len(lista_notas) == 0:
            assert False, "No existen evaluaciones"
        elif len(lista_notas) == 1:
            Evaluacion = "1 exam of 100%"
        else:
            Evaluacion = f"{len(lista_notas)} exams of {formateer(lista_notas, '%')} respectively."
            
            Evaluacion = Evaluacion #.replace("[", "").replace("]","%").replace(",", "%,")
            
            i = Evaluacion.rfind(",")
            
            Evaluacion = Evaluacion[:i] + " and" + Evaluacion[i+1:]
        
        return lista_notas, Evaluacion
    
    # revise if all the documents of a unit are available
    def doc(self, unit: list) -> bool:
        # unit: the unit in regard to
        try:
            ret = []
            for doc in unit[-1].split(", "):
                try:
                    Find.doc_find(unit[0], doc)
                except IndexError:
                    if unit[-1].strip().startswith("http"):
                        ret.append(True)
                        continue
                    unit[-1] = Find.doc_find(unit[0], f"{self.MC_code}-S{unit[0]}-Sub{unit[2]}-U{unit[4]}").split("/")[-1]
                ret.append(True)
            return all(ret)
        except IndexError:
            print(f"error in doc '{unit[-1]}'{'[{0}]'.format(len(ret)) if len(unit[-1].split(', ')) > 1 else ''} in Section {unit[0]}")
            return False
    
    # revise all the units for their docs
    doc_list = lambda self: [self.doc(i) for i in self.Units if i[-2] == None and i[-1] != None and i[6] == None]

    # revise if the video has the correct format
    def video(self, unit: list) -> bool:
        # unit: the unit in regard to
        video = unit[6]
        path, title, row = video
        
        filename = path.split("/")[-1]
        
        try:
            Find.doc_find(unit[0], filename)
            ret = True
        except:
            ret = False
            print(f"error in video {filename} not found: in row {row}")
        
        return ret
    
    # revise all the units for their videos
    video_list = lambda self: [self.video(i) for i in self.Units if type(i[6]) == list]

    # revise all the course
    def all(self) -> str:
        # output: the descriptions the evaluation of the course

        test_revised = self.test_list()

        lista_notas, evaluacion = self.notas()

        doc_revised = self.doc_list()

        # revise all the units for their videos
        video_revised = self.video_list()

        # all the type of revisions with its error messages
        revise_dict = {
            f"los test no son correctos \n{test_revised}": all(test_revised),
            f"las notas no suma 100% \n{lista_notas}": sum(lista_notas) == 100,
            f"no se han encontrado todos los documentos \n{doc_revised}": all(doc_revised),
            f"no se han encontrado todos los videos por subir \n{video_revised}": all(video_revised)
        }

        # show all the errors
        for i in revise_dict.keys():
            if not revise_dict[i]:
                print(i)

        # test if it can keep going
        assert all([revise_dict[i] for i in revise_dict.keys()]), "¡¡¡No se puede continuar con el proceso!!!"

        return evaluacion


# revise all the course
def revise(MC_code: str, Units: list, Tests: list) -> str:
    # MC_code: the code of the course
    # Units: units from the MC course
    # Tests: tests of the MC course
    # output: the descriptions the evaluation of the course

    # revise if the unit has its respective tests
    def revise_test(unit: list) -> bool:
        # unit: unit to revise tests
        n = 0
        for test in Tests:
            if test[:6:2] == unit[:6:2]:
                n += 1
        
        exp = int(re.findall("[0-9]+", unit[-1])[0])
        
        ret = n == exp
        
        if not ret:
            print(f"error in test {unit[:6:2]}: expected {exp}, had {n}")
        
        return ret

    # revise all te units for its tests
    test_revised = [revise_test(i) for i in Units if type(i[-2]) == int or type(i[-2]) == float]

    def revise_notas() -> tuple[list, str]:
        # output 1: list of the evaluations of all the units
        # output 2: description of the evaluations
        lista_notas = []

        for i in Units:
            if type(i[-2]) == str:
                continue
            
            if i[-2] == None:
                continue
            
            if i[-2] == 0:
                continue
            
            lista_notas.append(i[-2] * 100)

        if len(lista_notas) == 0:
            assert False, "No existen evaluaciones"
        elif len(lista_notas) == 1:
            Evaluacion = "1 exam of 100%"
        else:
            Evaluacion = f"{len(lista_notas)} exams of {formateer(lista_notas, '%')} respectively."
            
            Evaluacion = Evaluacion #.replace("[", "").replace("]","%").replace(",", "%,")
            
            i = Evaluacion.rfind(",")
            
            Evaluacion = Evaluacion[:i] + " and" + Evaluacion[i+1:]
        
        return lista_notas, Evaluacion
    
    lista_notas, evaluacion = revise_notas()

    # revise if all the documents of a unit are available
    def revise_doc(unit: list) -> bool:
        # unit: the unit in regard to
        try:
            ret = []
            for doc in unit[-1].split(", "):
                try:
                    Find.doc_find(unit[0], doc)
                except IndexError:
                    if unit[-1].strip().startswith("http"):
                        ret.append(True)
                        continue
                    unit[-1] = Find.doc_find(unit[0], f"{MC_code}-S{unit[0]}-Sub{unit[2]}-U{unit[4]}").split("/")[-1]
                ret.append(True)
            return all(ret)
        except IndexError:
            print(f"error in doc '{unit[-1]}'{'[{0}]'.format(len(ret)) if len(unit[-1].split(', ')) > 1 else ''} in Section {unit[0]}")
            return False

    # revise all the units for their docs
    doc_revised = [revise_doc(i) for i in Units if i[-2] == None and i[-1] != None and i[6] == None]

    # revise if the video has the correct format
    def revise_video(unit: list) -> bool:
        # unit: the unit in regard to
        video = unit[6]
        path, title, row = video
        
        filename = path.split("/")[-1]
        
        try:
            Find.doc_find(unit[0], filename)
            ret = True
        except:
            ret = False
            print(f"error in video {filename} not found: in row {row}")
        
        return ret

    # revise all the units for their videos
    video_revised = [revise_video(i) for i in Units if type(i[6]) == list]

    # all the type of revisions with its error messages
    revise_dict = {
        f"los test no son correctos \n{test_revised}": all(test_revised),
        f"las notas no suma 100% \n{lista_notas}": sum(lista_notas) == 100,
        f"no se han encontrado todos los documentos \n{doc_revised}": all(doc_revised),
        f"no se han encontrado todos los videos por subir \n{video_revised}": all(video_revised)
    }

    # show all the errors
    for i in revise_dict.keys():
        if not revise_dict[i]:
            print(i)

    # test if it can keep going
    assert all([revise_dict[i] for i in revise_dict.keys()]), "¡¡¡No se puede continuar con el proceso!!!"

    return evaluacion
