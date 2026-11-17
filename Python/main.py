# ==========================================
# SGA-DO: Sistema de Gestión Académica
# Alineado al Diagrama UML y al informe de Entregable #1
# Rafael Hidalgo | Entregable #4 Implementación en Python
# ==========================================

class Persona:
    def __init__(self, cedula, nombreCompleto, correoElectronico):
        # Atributos privados (-) según UML
        self._cedula = cedula
        self._nombreCompleto = nombreCompleto
        self._correoElectronico = correoElectronico

    # Métodos consultores (+) según UML
    def cedula(self):
        return self._cedula

    def nombreCompleto(self):
        return self._nombreCompleto

    def correoElectronico(self):
        return self._correoElectronico


class Alumno(Persona):
    def __init__(self, cedula, nombreCompleto, correoElectronico, programaAcademico):
        super().__init__(cedula, nombreCompleto, correoElectronico)
        self._programaAcademico = programaAcademico
        self._notas = []  # List<float> [max 3]

    def agregarNota(self, nota: float):
        if len(self._notas) < 3:
            self._notas.append(nota)
            return True
        return False

    def notas(self):
        return self._notas

    def programa(self):
        return self._programaAcademico


class Profesor(Persona):
    def __init__(self, cedula, nombreCompleto, correoElectronico, especialidadAcademica, materiaAsignada):
        super().__init__(cedula, nombreCompleto, correoElectronico)
        self._especialidadAcademica = especialidadAcademica
        self._materiaAsignada = materiaAsignada

    def especialidadAcademica(self):
        return self._especialidadAcademica

    def materiaAsignada(self):
        return self._materiaAsignada


# ==========================================
# JERARQUÍA DE PROGRAMA ACADÉMICO
# ==========================================

class ProgramaAcademico:
    def __init__(self, nombrePrograma):
        self._nombrePrograma = nombrePrograma

    def nombrePrograma(self):
        return self._nombrePrograma

    def calcularPromedio(self, notas):
        if not notas:
            return 0.0
        return sum(notas) / len(notas)

    def calcularAprobacion(self, notas):
        return False


class Curso(ProgramaAcademico):
    def __init__(self):
        super().__init__("Curso")

    def calcularAprobacion(self, notas):
        if not notas or len(notas) < 3:
            return False
        # Regla UML: Promedio >= 10/20
        return self.calcularPromedio(notas) >= 10.0


class Diplomado(ProgramaAcademico):
    def __init__(self):
        super().__init__("Diplomado")

    def calcularAprobacion(self, notas):
        if not notas or len(notas) < 3:
            return False
        # Regla UML: Promedio >= 14/20
        return self.calcularPromedio(notas) >= 14.0


class Bootcamp(ProgramaAcademico):
    def __init__(self):
        super().__init__("Bootcamp")

    def calcularAprobacion(self, notas):
        if not notas or len(notas) < 3:
            return False
        # Regla UML: Ninguna nota < 14/20
        return all(nota >= 14.0 for nota in notas)


# ==========================================
# CLASE PRINCIPAL DE CONTROL SGA-DO
# ==========================================

class SGADO:
    def __init__(self):
        self.listaAlumnos = []       # List<Alumno>
        self.listaProfesores = []    # List<Profesor>
        self.pilaDeshacer = []       # Stack<Action>
        self.colaCertificados = []   # Queue<Certificado>
        self.cargarDeArchivosTxt()

    def registrarAlumno(self):
        print("\n--- Registro de Alumno ---")
        cedula = input("Ingrese cédula: ").strip()

        for al in self.listaAlumnos:
            if al.cedula() == cedula:
                print("Error: Ya existe un alumno con esta cédula.")
                return

        nombre = input("Ingrese nombre completo: ").strip()
        correo = input("Ingrese correo electrónico: ").strip()

        while True:
            prog_tipo = input("Ingrese programa (Curso/Diplomado/Bootcamp): ").strip().capitalize()
            if prog_tipo == "Curso":
                prog_obj = Curso()
                break
            elif prog_tipo == "Diplomado":
                prog_obj = Diplomado()
                break
            elif prog_tipo == "Bootcamp":
                prog_obj = Bootcamp()
                break
            else:
                print("Error: Programa inválido. Opciones: Curso, Diplomado o Bootcamp.")

        nuevo_alumno = Alumno(cedula, nombre, correo, prog_obj)
        self.listaAlumnos.append(nuevo_alumno)
        self.guardarEnArchivosTxt()
        print("Alumno registrado exitosamente.")

    def registrarProfesor(self):
        print("\n--- Registro de Profesor ---")
        cedula = input("Ingrese cédula: ").strip()

        for pr in self.listaProfesores:
            if pr.cedula() == cedula:
                print("Error: Ya existe un profesor con esta cédula.")
                return

        nombre = input("Ingrese nombre completo: ").strip()
        correo = input("Ingrese correo electrónico: ").strip()
        especialidad = input("Ingrese especialidad académica: ").strip()
        materia = input("Ingrese materia asignada: ").strip()

        nuevo_profesor = Profesor(cedula, nombre, correo, especialidad, materia)
        self.listaProfesores.append(nuevo_profesor)
        self.guardarEnArchivosTxt()
        print("Profesor registrado exitosamente.")

    def ingresarNota(self):
        print("\n--- Registrar Notas a un Alumno ---")
        cedula = input("Ingrese la cédula del alumno: ").strip()

        alumno = next((a for a in self.listaAlumnos if a.cedula() == cedula), None)
        if not alumno:
            print("Error: Alumno no encontrado.")
            return

        if len(alumno.notas()) >= 3:
            print("Error: El alumno ya tiene las 3 notas registradas.")
            return

        print(f"\nAlumno: {alumno.nombreCompleto()} | Programa: {alumno.programa().nombrePrograma()}")
        print(f"Notas registradas actualmente: {alumno.notas()}")

        while True:
            try:
                nota = float(input("Ingrese la nueva nota (0 a 20): ").strip())
                if 0 <= nota <= 20:
                    posicion_nota = len(alumno.notas())
                    alumno.agregarNota(nota)
                    # Guardar en pilaDeshacer (Stack: Cédula, Posición, Nota)
                    self.pilaDeshacer.append((cedula, posicion_nota, nota))
                    self.guardarEnArchivosTxt()
                    print("Nota registrada correctamente.")
                    break
                print("Error: La nota debe estar entre 0 y 20.")
            except ValueError:
                print("Error: Debe ingresar un número válido.")

    def deshacerUltimaNota(self):
        print("\n--- Deshacer Último Registro de Nota ---")
        if not self.pilaDeshacer:
            print("No hay notas registradas en la pila para deshacer.")
            return

        cedula, pos, nota_eliminada = self.pilaDeshacer.pop()
        alumno = next((a for a in self.listaAlumnos if a.cedula() == cedula), None)

        if alumno and len(alumno.notas()) > pos:
            alumno.notas().pop(pos)
            self.guardarEnArchivosTxt()
            print(f"Último registro deshecho: Se eliminó la nota {nota_eliminada} del alumno con cédula {cedula}.")

    def procesarCertificados(self):
        print("\n--- Generar Cola de Certificados ---")
        self.colaCertificados.clear()

        for alumno in self.listaAlumnos:
            notas = alumno.notas()
            if len(notas) == 3 and alumno.programa().calcularAprobacion(notas):
                self.colaCertificados.append(alumno)

        with open("certificados_pendientes.txt", "w", encoding="utf-8") as f:
            for al in self.colaCertificados:
                f.write(f"{al.cedula()},{al.nombreCompleto()},{al.correoElectronico()},{al.programa().nombrePrograma()}\n")

        print("Cola de certificados generada correctamente.")
        print(f"Total de alumnos aprobados en cola: {len(self.colaCertificados)}")

    def mostrarReporteGeneral(self):
        print("\n================ REPORTE GENERAL ================")
        print("\n--- ALUMNOS REGISTRADOS ---")
        if not self.listaAlumnos:
            print("No hay alumnos registrados.")
        else:
            for al in self.listaAlumnos:
                notas = al.notas()
                print(f"\nCédula: {al.cedula()} | Nombre: {al.nombreCompleto()}")
                print(f"Correo: {al.correoElectronico()} | Programa: {al.programa().nombrePrograma()}")
                print(f"Notas: {notas}")

                if len(notas) < 3:
                    print("Estado: Pendiente de notas")
                else:
                    promedio = al.programa().calcularPromedio(notas)
                    print(f"Promedio: {round(promedio, 2)}")
                    if al.programa().calcularAprobacion(notas):
                        print("Estado: Aprobado")
                    else:
                        print("Estado: Reprobado")

        print("\n--- PROFESORES REGISTRADOS ---")
        if not self.listaProfesores:
            print("No hay profesores registrados.")
        else:
            for pr in self.listaProfesores:
                print(f"\nCédula: {pr.cedula()} | Nombre: {pr.nombreCompleto()}")
                print(f"Correo: {pr.correoElectronico()} | Especialidad: {pr.especialidadAcademica()} | Materia: {pr.materiaAsignada()}")

        print("\n=================================================")

    def guardarEnArchivosTxt(self):
        # Persistencia de Alumnos
        with open("alumnos.txt", "w", encoding="utf-8") as f:
            for al in self.listaAlumnos:
                notas_str = ",".join(str(n) for n in al.notas())
                f.write(f"{al.cedula()},{al.nombreCompleto()},{al.correoElectronico()},{al.programa().nombrePrograma()},{notas_str}\n")

        # Persistencia de Profesores
        with open("profesores.txt", "w", encoding="utf-8") as f:
            for pr in self.listaProfesores:
                f.write(f"{pr.cedula()},{pr.nombreCompleto()},{pr.correoElectronico()},{pr.especialidadAcademica()},{pr.materiaAsignada()}\n")

    def cargarDeArchivosTxt(self):
        self.listaAlumnos.clear()
        self.listaProfesores.clear()

        # Cargar Alumnos
        try:
            with open("alumnos.txt", "r", encoding="utf-8") as f:
                for linea in f:
                    datos = linea.strip().split(",")
                    if len(datos) >= 4:
                        cedula, nombre, correo, prog_nombre = datos[0], datos[1], datos[2], datos[3]

                        if prog_nombre == "Curso":
                            prog_obj = Curso()
                        elif prog_nombre == "Diplomado":
                            prog_obj = Diplomado()
                        else:
                            prog_obj = Bootcamp()

                        alumno = Alumno(cedula, nombre, correo, prog_obj)
                        for n in datos[4:]:
                            if n:
                                alumno.agregarNota(float(n))
                        self.listaAlumnos.append(alumno)
        except FileNotFoundError:
            pass

        # Cargar Profesores
        try:
            with open("profesores.txt", "r", encoding="utf-8") as f:
                for linea in f:
                    datos = linea.strip().split(",")
                    if len(datos) >= 5:
                        prof = Profesor(datos[0], datos[1], datos[2], datos[3], datos[4])
                        self.listaProfesores.append(prof)
        except FileNotFoundError:
            pass


# ==================================================
# CLASE CONTROLADORA DEL SISTEMA SGA-DO
# ==================================================

if __name__ == "__main__":
    sga = SGADO()

    while True:
        print("\n==================================================")
        print("SGA-DO: SISTEMA DIPLOMADOS ONLINE")
        print("==================================================")
        print("1. Registrar Alumno")
        print("2. Registrar Profesor")
        print("3. Registrar Notas a un Alumno")
        print("4. Deshacer Último Registro de Nota")
        print("5. Generar Cola de Certificados")
        print("6. Mostrar Reporte General")
        print("7. Salir")
        print("==================================================")

        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == "1":
            sga.registrarAlumno()
        elif opcion == "2":
            sga.registrarProfesor()
        elif opcion == "3":
            sga.ingresarNota()
        elif opcion == "4":
            sga.deshacerUltimaNota()
        elif opcion == "5":
            sga.procesarCertificados()
        elif opcion == "6":
            sga.mostrarReporteGeneral()
        elif opcion == "7":
            print("\nCerrando SGA Diplomados Online. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, seleccione un número del 1 al 7.")