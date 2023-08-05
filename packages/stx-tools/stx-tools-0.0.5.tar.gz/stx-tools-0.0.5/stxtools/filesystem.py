# Python's Libraries
# import re
import shutil
import os
from pathlib import Path

# Own's Libraries
from stxtools.data import Error


class Folder(object):

    def __init__(self, _abspath):
        self.abspath = _abspath
        self.name = Path(_abspath).parts[-1]

    def __str__(self):
        return self.abspath

    def get_Abspath(self):
        return self.abspath

    def is_Exist(self, _raise_error_on=None):
        """Metodo que valida la existencia de la carpeta.

        Args:
            _raise_error_on (:obj:`bool`, optional): Si se recibe True se
                lanzara una excepción si el folder existe. En caso de False
                se lanzara la excepción si este no existe.

        Returns:
            bool: True si el folder existe. False si no existe.
        """
        value = os.path.exists(self.abspath)
        if value:
            if _raise_error_on:
                raise Error(
                    "validacion",
                    "La carpeta '%s' ya existe" % (self.abspath),
                    "carpeta ya existe",
                    ""
                )

            return True
        else:
            if _raise_error_on is False:
                raise Error(
                    "validacion",
                    "La carpeta '%s' no existe" % (self.abspath),
                    "carpeta no existe",
                    "",
                )

            return False

    def get_Basepath(self):
        basepath = os.path.abspath(
            os.path.join(
                self.abspath,
                os.pardir
            )
        )
        return basepath

    def create(self, _raise_errors=False, _create_struct=False):
        if self.is_Exist():
            error = Error(
                "validacion",
                "La carpeta '%s' ya existe" % (self.abspath),
                "carpeta ya existe",
                ""
            )
            if _raise_errors:
                raise error

            print(error)
            return False

        folder_base = Folder(self.get_Basepath())
        if folder_base.is_Exist() is False:
            if _create_struct is False:
                error = Error(
                    "validacion",
                    "No existe el directorio padre '%s'" % (
                        folder_base
                    ),
                    "carpeta no existe",
                    ""
                )
                if _raise_errors:
                    raise error
                print(error)
                return False

        try:
            os.makedirs(self.abspath)
            print("Carpeta '%s' creada con exito" % (self.abspath))
            return True
        except Exception as error:
            if _raise_errors:
                raise error
            print(str(error))
            return False

    def get_QtyFiles(self, _num_levels=None):
        self.is_Exist(_raise_error_on=False)

        elements = os.walk(self.abspath)
        qty = 0
        level = 0
        for directory_path, list_dir_names, list_file_names in elements:
            qty += len(list_file_names)

            level += 1
            if _num_levels == level:
                break

        return qty

    def get_QtyFolders(self, _num_levels=None):
        self.is_Exist(_raise_error_on=False)

        elements = os.walk(self.abspath)
        qty = 0
        level = 0
        for directory_path, list_dir_names, list_file_names in elements:
            qty += len(list_dir_names)

            level += 1
            if _num_levels == level:
                break

        return qty

    def get_QtyElements(self, _num_levels=None, _summary=False):
        self.is_Exist(_raise_error_on=False)

        elements = os.walk(self.abspath)

        if _summary:
            qty_elements = 0
            level = 0
            for directory_path, list_dir_names, list_file_names in elements:
                qty_elements += len(list_dir_names)
                qty_elements += len(list_file_names)

                level += 1
                if _num_levels == level:
                    break

            return qty_elements

        else:
            qty_files = 0
            qty_folders = 0
            level = 0
            for directory_path, list_dir_names, list_file_names in elements:
                qty_files += len(list_dir_names)
                qty_folders += len(list_file_names)

                level += 1
                if _num_levels == level:
                    break

            return qty_folders, qty_files

    def get_Files(self, _num_levels=None):
        self.is_Exist(_raise_error_on=False)

        level = 0
        list_files = []
        elements = os.walk(self.abspath)
        for directory_path, list_dir_names, list_file_names in elements:
            for file_name in list_file_names:
                folder = Folder(directory_path)
                file = File(folder, file_name)
                list_files.append(file)
            level += 1
            if _num_levels == level:
                break

        return list_files

    def get_Folders(self, _num_levels=None):
        self.is_Exist(_raise_error_on=False)

        level = 0
        list_folders = []
        elements = os.walk(self.abspath)
        for directory_path, list_dir_names, list_file_names in elements:
            for dir_name in list_dir_names:
                path = os.path.join(
                    directory_path,
                    dir_name
                )
                folder = Folder(path)
                list_folders.append(folder)
            level += 1
            if _num_levels == level:
                break

        return list_folders

    def find_File_ByName(self, _file_name):
        self.is_Exist(_raise_error_on=False)

        list_folders = []
        elements = os.walk(self.abspath)
        for directory_path, list_dir_names, list_file_names in elements:
            for file_name in list_file_names:
                (title, extension) = os.path.splitext(file_name)
                (ftile, fextension) = os.path.splitext(_file_name)

                if title.upper() == ftile.upper() and \
                   extension.upper() == fextension.upper():
                    folder = Folder(directory_path)
                    file = File(folder, file_name)
                    list_folders.append(file)

        return list_folders

    def find_File_ByExtension(self, _extension):
        self.is_Exist(_raise_error_on=False)

        list_folders = []
        elements = os.walk(self.abspath)
        for directory_path, list_dir_names, list_file_names in elements:
            for file_name in list_file_names:
                (title, extension) = os.path.splitext(file_name)

                if extension.upper() == _extension.upper():
                    folder = Folder(directory_path)
                    file = File(folder, file_name)
                    list_folders.append(file)

        return list_folders

    def add_Folders(self, _list_folder_names, _raise_errors=False):
        if self.is_Exist() is False:
            error = Error(
                "validacion",
                "La carpeta '%s' no existe" % (self.abspath),
                "carpeta no existe",
                "",
            )
            if _raise_errors:
                raise error

            print(error)
            return False

        for folder_name in _list_folder_names:
            path = os.path.join(self.abspath, folder_name)
            new_folder = Folder(path)
            new_folder.create(_raise_errors=_raise_errors)
        return True

    def delete(self, _with_content=False, _raise_errors=False):
        if self.is_Exist() is False:
            error = Error(
                "validacion",
                "La carpeta '%s' no existe" % (self.abspath),
                "carpeta no existe",
                "",
            )
            if _raise_errors:
                raise error

            print(error)
            return False

        content_qty = self.get_QtyElements(
            _num_levels=1,
            _summary=True
        )
        if _with_content is False:
            if content_qty:
                error = Error(
                    "validacion",
                    "La carpeta '%s' contiene archivos "
                    "o carpetas, por lo tanto no se puede "
                    "eliminar" % (self.abspath),
                    "no se puede eliminar",
                    "",
                )
                if _raise_errors:
                    raise error

                print(error)
                return False

        try:
            shutil.rmtree(self.abspath)
            msg_qty = ""
            if content_qty:
                msg_qty = "y su contenido de '%s' elementos" % content_qty
            print(
                "La carpeta '%s' %s fue eliminada "
                "con exito." % (self.abspath, msg_qty)
            )
            return True
        except Exception as error:
            if _raise_errors:
                raise error
            print(str(error))
            return False

    def delete_Content(self):
        pass

    def __repr__(self):
        return self.name.encode('ascii', 'ignore').decode('ascii')


class File(object):
    """Objeto para el manejo de archivos.

    Attributes:
        name (str): Nombre del archivo con todo y extensión.
        title (str): Nombre del archivo sin extensión.
        extension (str): Extensión del archivo.
        folder (Folder): Carpeta que contiene el archivo
        folder_old (Folder): Cuando se mueve el archivo, este atributo
            guarda temporalmente el folder anterior
        obj (FileObject): Objecto de python para operaciones avanzadas.
    """

    def __init__(self, _folder, _name):
        """Constructor.

        PARAMETROS:
            _folder = Objeto de tipo Folder.
            _name = Nombre del archivo con todo y extension.
        """
        self.name = _name
        self.title = os.path.splitext(_name)[0]
        self.extension = os.path.splitext(_name)[1]
        self.folder = _folder
        self.folder_old = None
        self.obj = None

    def get_Abspath(self):
        abspath = os.path.join(
            self.folder.abspath,
            self.name
        )
        return abspath

    def is_Exist(self, _raise_error_on=None):
        """Metodo que valida la existencia del archivo.

        Args:
            _raise_error_on (:obj:`bool`, optional): Si se recibe True se
                lanzara una excepción si el archivo existe. En caso de False
                se lanzara la excepción si este no existe.

        Returns:
            bool: True si el archivo existe. False si no existe.
        """
        value = os.path.isfile(self.get_Abspath())
        if value:
            if _raise_error_on:
                raise Error(
                    "validacion",
                    "El archivo '%s' ya existe" % (self.get_Abspath()),
                    "archivo existe",
                    ""
                )
            print()
            return True
        else:
            if _raise_error_on is False:
                raise Error(
                    "validacion",
                    "El archivo '%s' no existe" % (self.get_Abspath()),
                    "archivo no existe",
                    ""
                )
            return False

    def has_Extension(self, _extension, _raise_error_on=None):
        if self.extension.lower() == _extension.lower():
            if _raise_error_on:
                raise Error(
                    "validacion",
                    "El archivo '%s' contiene la extension '%s'" % (
                        self.name,
                        _extension
                    ),
                    "contiene extensión",
                    "",
                )
            return True
        else:
            if _raise_error_on is False:
                raise Error(
                    "validacion",
                    "El archivo '%s' no contiene la extension '%s'" % (
                        self.name,
                        _extension
                    ),
                    "no contiene extensión",
                    "",
                )
            return False

    def create(self, _overwrite=False, _raise_errors=False):
        """Metodo que crea el archivo en el sistema de archivos.

        Args:
            _overwrite (:obj:`bool`, optional): Si se recibe True en caso de
                no existir el directorio o el archivo, estos seran creados.
            _raise_errors (:obj:`bool`, optional): Si se recibe False en caso
                de error se terminara la ejecución con un error, de lo
                contrario se mostrar un mensaje en consola.
        """
        if _raise_errors:
            self.folder.is_Exist(_raise_error_on=False)
            if _overwrite is False:
                self.is_Exist(_raise_error_on=True)

            try:
                self.file_object = open(self.get_Abspath(), "w")
                print("Archivo '%s' creado con exito en '%s'" % (
                    self.name, self.folder.abspath))
                return True
            except Exception as error:
                raise Error(
                    type(error).__name__,
                    str(error),
                    "",
                    "",
                )

        else:
            try:
                self.folder.is_Exist(_raise_error_on=False)
                file_exist = self.is_Exist()
                if _overwrite is False:
                    if file_exist:
                        print("Archivo '%s' ya existe en el folder '%s'" % (
                            self.name, self.folder.abspath))
                        return False

                self.file_object = open(self.get_Abspath(), "w")
                print("Archivo '%s' creado con exito en '%s'" % (
                    self.name, self.folder.abspath))
                return True
            except Exception as error:
                print(str(error))

    def get_Object(self, _raise_errors=False):
        obj = None
        if _raise_errors:
            self.is_Exist(_raise_error_on=False)
            obj = open(self.get_Abspath())
        else:
            if self.is_Exist():
                try:
                    obj = open(self.get_Abspath())
                except Exception as error:
                    print(str(error))
            else:
                error = Error(
                    "validacion",
                    "El archivo '%s' no existe" % (self.get_Abspath()),
                    "archivo no existe",
                    ""
                )
                print(error)
        return obj

    def delete(self, _raise_errors=False):
        if _raise_errors:
            self.is_Exist(_raise_error_on=False)
            os.remove(self.get_Abspath())

        else:
            if self.is_Exist():
                try:
                    os.remove(self.get_Abspath())
                except Exception as error:
                    print(str(error))
            else:
                error = Error(
                    "validacion",
                    "El archivo '%s' no existe" % (self.get_Abspath()),
                    "archivo no existe",
                    ""
                )
                print(error)
                return False

        print(
            "El archivo '%s' fue eliminado "
            "con exito." % self.get_Abspath()
        )
        return True

    def copy(self, _folder_to, _raise_errors=False):
        """ Por defaul reemplaza el archivo."""
        if _folder_to.is_Exist() is False:
            error = Error(
                "validacion",
                "La carpeta destino '%s' no existe" % (
                    _folder_to.get_Abspath()
                ),
                "carpeta no existe",
                ""
            )
            if _raise_errors:
                raise error
            print(error)
            return False

        if self.is_Exist() is False:
            error = Error(
                "validacion",
                "El archivo '%s' no existe" % (self.get_Abspath()),
                "archivo no existe",
                ""
            )
            if _raise_errors:
                raise error
            print(error)
            return False

        try:
            file_abspath_to = os.path.join(_folder_to.get_Abspath(), self.name)
            shutil.copy2(self.get_Abspath(), file_abspath_to)

            print(
                "El archivo '%s' fue copiado con exito a: \n"
                "{}" % (self.name, _folder_to.abspath)
            )
            return True
        except Exception as error:
            if _raise_errors:
                raise error

            print(str(error))
            return False

    def move(self, _folder_to, _replace=False):
        pass

    def write(self, _value):
        pass

    def __repr__(self):
        return self.name.encode('ascii', 'ignore').decode('ascii')
