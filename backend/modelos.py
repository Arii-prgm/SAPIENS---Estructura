import datetime

class UsuarioApp:
    # Clase base para representar los usuarios del sistema (autenticación)
    def __init__(self, email, password, role, nombre):
        self.email = email
        self.password = password
        self.role = role
        self.nombre = nombre

    def to_auth_dict(self):
        # Retorna un diccionario con las credenciales de autenticación del usuario
        return {
            "password": self.password,
            "role": self.role,
            "nombre": self.nombre
        }

class Estudiante(UsuarioApp):
    # Clase que representa a un estudiante registrado, hereda de UsuarioApp
    def __init__(self, identificacion, nombre, carrera, semestre="1", fecha_registro=None, calificaciones=None, entregas=None, password="123456"):
        # Llamar al constructor de la clase base UsuarioApp
        email = f"{identificacion}@gmail.com"
        super().__init__(email, password, role="estudiante", nombre=nombre)
        
        self.identificacion = identificacion
        if isinstance(carrera, list):
            self.carreras = carrera
        else:
            self.carreras = [carrera] if carrera else []
        self.carrera = self.carreras[0] if self.carreras else ""
        self.semestre = semestre
        self.fecha_registro = fecha_registro or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.calificaciones = calificaciones or [
            {"materia": "Estructuras de Datos", "nota": 9.5},
            {"materia": "Álgebra Lineal", "nota": 8.0},
            {"materia": "Programación Orientada a Objetos", "nota": 10.0}
        ]
        self.entregas = entregas or {}

    def to_dict(self):
        # Retorna el objeto estudiante como un diccionario de Python
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "carrera": self.carreras,
            "semestre": self.semestre,
            "fecha_registro": self.fecha_registro,
            "calificaciones": self.calificaciones,
            "entregas": self.entregas
        }


class Materia:
    # Clase que representa una materia académica
    def __init__(self, codigo, nombre, creditos, horario="Por definir", deberes=None, paralelo="A", docente_email=None, docente_nombre=None, imagen=None, estudiantes_inscritos=None, semestre="1", carreras=None):
        self.codigo = str(codigo).upper()  # Clave de ordenamiento
        self.nombre = nombre
        self.creditos = creditos
        self.horario = horario
        self.deberes = deberes or {str(i): [] for i in range(1, 17)}
        self.paralelo = paralelo
        self.docente_email = docente_email
        self.docente_nombre = docente_nombre
        self.imagen = imagen
        self.estudiantes_inscritos = estudiantes_inscritos or []
        self.semestre = str(semestre)
        self.carreras = carreras or []

    def to_dict(self):
        # Retorna el objeto materia como un diccionario de Python
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "creditos": self.creditos,
            "horario": self.horario,
            "deberes": self.deberes,
            "paralelo": self.paralelo,
            "docente_email": self.docente_email,
            "docente_nombre": self.docente_nombre,
            "imagen": self.imagen,
            "estudiantes_inscritos": self.estudiantes_inscritos,
            "semestre": self.semestre,
            "carreras": self.carreras
        }


class Tarea:
    # Clase que representa una incidencia académica o tarea general
    def __init__(self, id_tarea, descripcion, email_estudiante=None, respuesta_docente="", nombre_docente=None):
        self.id_tarea = id_tarea
        self.descripcion = descripcion
        self.estado = "Pendiente"
        self.fecha_creacion = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.email_estudiante = email_estudiante
        self.respuesta_docente = respuesta_docente
        self.nombre_docente = nombre_docente

    def to_dict(self):
        # Retorna el objeto tarea/incidencia como un diccionario de Python
        return {
            "id_tarea": self.id_tarea,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion,
            "email_estudiante": self.email_estudiante,
            "respuesta_docente": self.respuesta_docente,
            "nombre_docente": self.nombre_docente
        }


class Accion:
    # Clase que representa una acción registrada en el historial del sistema
    def __init__(self, descripcion, destinatarios=None):
        self.descripcion = descripcion
        self.destinatarios = destinatarios if destinatarios is not None else []
        self.hora = datetime.datetime.now().strftime("%H:%M:%S")
        self.timestamp = int(datetime.datetime.now().timestamp() * 1000)

    def to_dict(self):
        # Retorna la acción formateada como diccionario de Python
        return {
            "descripcion": self.descripcion,
            "hora": self.hora,
            "timestamp": getattr(self, 'timestamp', int(datetime.datetime.now().timestamp() * 1000)),
            "destinatarios": getattr(self, 'destinatarios', [])
        }


class Docente(UsuarioApp):
    # Clase que representa a un docente del sistema, hereda de UsuarioApp
    def __init__(self, identificacion, nombre, carrera, especialidad="General", fecha_registro=None, password="123456"):
        email = f"{identificacion}@gmail.com"
        super().__init__(email, password, role="docente", nombre=nombre)
        
        self.identificacion = identificacion
        if isinstance(carrera, list):
            self.carreras = carrera
        else:
            self.carreras = [carrera] if carrera else []
        self.carrera = self.carreras[0] if self.carreras else ""
        self.especialidad = especialidad
        self.fecha_registro = fecha_registro or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        # Retorna el objeto docente como un diccionario de Python
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "carrera": self.carreras,
            "especialidad": self.especialidad,
            "fecha_registro": self.fecha_registro
        }


class Admin(UsuarioApp):
    # Clase que representa al administrador del sistema, hereda de UsuarioApp
    def __init__(self, email, password, nombre="Administrador Sapiens", nivel_acceso="Total"):
        super().__init__(email, password, role="admin", nombre=nombre)
        self.nivel_acceso = nivel_acceso

    def to_auth_dict(self):
        # Retorna los datos de autenticación del administrador incluyendo su nivel de acceso
        data = super().to_auth_dict()
        data["nivel_acceso"] = self.nivel_acceso
        return data

class Coordinador(UsuarioApp):
    # Clase que representa al coordinador de facultad, hereda de UsuarioApp
    def __init__(self, email, password, nombre="Coordinador Sapiens", facultad="General"):
        super().__init__(email, password, role="coordinador", nombre=nombre)
        self.facultad = facultad

    def to_auth_dict(self):
        # Retorna los datos de autenticación del coordinador incluyendo su facultad
        data = super().to_auth_dict()
        data["facultad"] = self.facultad
        return data
