import sqlite3
import os
from models.clientes import Cliente
from models.carros import Carro
from models.reservas import Reserva

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'revite.db')


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_bd():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with conectar() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cedula          TEXT PRIMARY KEY,
                nombres         TEXT NOT NULL,
                apellidos       TEXT NOT NULL,
                foto            TEXT DEFAULT '',
                celular         TEXT NOT NULL,
                contraseña      TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS carros (
                placa  TEXT PRIMARY KEY,
                marca  TEXT NOT NULL,
                modelo TEXT NOT NULL,
                ano    INTEGER NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                origen         TEXT NOT NULL,
                destino        TEXT NOT NULL,
                horario        TEXT NOT NULL,
                cedula_cliente TEXT REFERENCES clientes(cedula)
            )
        """)


def cargar_clientes():
    with conectar() as conn:
        filas = conn.execute("SELECT * FROM clientes").fetchall()

    return [
        Cliente(
            cedula=fila['cedula'],
            nombres=fila['nombres'],
            apellidos=fila['apellidos'],
            foto=fila['foto'],
            celular=fila['celular'],
            contraseña=fila['contraseña']
        )
        for fila in filas
    ]


def guardar_cliente(cliente):
    try:
        with conectar() as conn:
            conn.execute("""
                INSERT INTO clientes (cedula, nombres, apellidos, foto, celular, contraseña)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(cedula) DO UPDATE SET
                    nombres    = excluded.nombres,
                    apellidos  = excluded.apellidos,
                    foto       = excluded.foto,
                    celular    = excluded.celular,
                    contraseña = excluded.contraseña
            """, (
                cliente.get_cedula(),
                cliente.get_nombres(),
                cliente.get_apellidos(),
                cliente.get_foto(),
                cliente.get_celular(),
                cliente.get_contraseña()
            ))
        return True
    except Exception:
        return False


def buscar_cliente_por_cedula(cedula):
    with conectar() as conn:
        fila = conn.execute(
            "SELECT * FROM clientes WHERE cedula = ?", (cedula,)
        ).fetchone()

    if fila is None:
        return None

    return Cliente(
        cedula=fila['cedula'],
        nombres=fila['nombres'],
        apellidos=fila['apellidos'],
        foto=fila['foto'],
        celular=fila['celular'],
        contraseña=fila['contraseña']
    )


def cargar_carros():
    with conectar() as conn:
        filas = conn.execute("SELECT * FROM carros").fetchall()

    return [
        Carro(marca=fila['marca'], modelo=fila['modelo'], ano=fila['ano'], placa=fila['placa'])
        for fila in filas
    ]


def guardar_carro(carro):
    try:
        with conectar() as conn:
            conn.execute("""
                INSERT INTO carros (placa, marca, modelo, ano)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(placa) DO UPDATE SET
                    marca  = excluded.marca,
                    modelo = excluded.modelo,
                    ano    = excluded.ano
            """, (carro.get_placa(), carro.get_marca(), carro.get_modelo(), carro.get_ano()))
        return True
    except Exception:
        return False


def eliminar_carro(placa):
    try:
        with conectar() as conn:
            conn.execute("DELETE FROM carros WHERE placa = ?", (placa,))
        return True
    except Exception:
        return False


def cargar_reservas():
    with conectar() as conn:
        filas = conn.execute("SELECT * FROM reservas").fetchall()

    reservas = []
    for fila in filas:
        cliente = buscar_cliente_por_cedula(fila['cedula_cliente']) if fila['cedula_cliente'] else None
        reservas.append(Reserva(
            origen=fila['origen'],
            destino=fila['destino'],
            horario=fila['horario'],
            cliente=cliente
        ))

    return reservas


def guardar_reserva(reserva):
    cedula = reserva.get_cliente().get_cedula() if reserva.get_cliente() else None

    try:
        with conectar() as conn:
            conn.execute("""
                INSERT INTO reservas (origen, destino, horario, cedula_cliente)
                VALUES (?, ?, ?, ?)
            """, (reserva.get_origen(), reserva.get_destino(), reserva.get_horario(), cedula))
        return True
    except Exception:
        return False


def eliminar_reserva(indice):
    try:
        with conectar() as conn:
            filas = conn.execute("SELECT id FROM reservas ORDER BY id").fetchall()

            if 0 <= indice < len(filas):
                conn.execute("DELETE FROM reservas WHERE id = ?", (filas[indice]['id'],))
                return True
        return False
    except Exception:
        return False


inicializar_bd()