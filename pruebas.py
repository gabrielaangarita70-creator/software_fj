from cliente import Cliente
from servicios import ReservaSalas, AlquilerEquipos, AsesoriaEspecializada
from reservas import Reserva
from excepciones import DatosInvalidosError, ServicioNoDisponibleError

c = Cliente("123", "Gabriela Angarita", "gaby@correo.com", "3001234567")

# 1. Servicio no disponible
try:
    e = AlquilerEquipos("E1", "Portátil HP", 30000, 5, disponible=False)
    Reserva(c, e, 1)
except DatosInvalidosError as err:
    print("1 OK:", err, "| causa:", type(err.__cause__).__name__)

# 2. Asistentes por encima de la capacidad
try:
    s = ReservaSalas("S1", "Sala Creativa", 50000, 10)
    Reserva(c, s, 2, horas=2, asistentes=15)
except DatosInvalidosError as err:
    print("2 OK:", err)

# 3. Asesoría de más de 8 horas
try:
    a = AsesoriaEspecializada("A1", "Asesoría Python", 80000, "Programación")
    Reserva(c, a, 1, duracion=9)
except DatosInvalidosError as err:
    print("3 OK:", err)

# 4. Cantidad inválida
try:
    s = ReservaSalas("S2", "Sala Creativa", 50000, 10)
    Reserva(c, s, 0)
except DatosInvalidosError as err:
    print("4 OK:", err)

# 5. Reserva válida con IVA y sin IVA
s = ReservaSalas("S3", "Sala Creativa", 50000, 10)
r1 = Reserva(c, s, 2, con_iva=True,  horas=2, asistentes=8)
r2 = Reserva(c, s, 2, con_iva=False, horas=2, asistentes=8)
print("5a con IVA:", r1.costo_total)
print("5b sin IVA:", r2.costo_total)
r1.confirmar()
print("5c:", r1.describir())