import json
import os
from models.clientes import Cliente
from models.carros import Carro
from models.reservas import Reserva

CLIENTES_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'clientes.json')
CARROS_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'carros.json')
RESERVAS_JSON_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'reservas.json')

def cargar_clientes():
    if not os.path.exists(CLIENTES_JSON_PATH):
        return []

    try:
        with open(CLIENTES_JSON_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            clientes = []
            for cliente_data in data:
                cliente = Cliente(
                    cedula=cliente_data['cedula'],
                    nombres=cliente_data['nombres'],
                    apellidos=cliente_data['apellidos'],
                    foto=cliente_data['foto'],
                    contraseña=cliente_data['contraseña'],
                    celular=cliente_data['celular']
                )
                clientes.append(cliente)
            return clientes
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error al cargar clientes: {e}")
        return []

def guardar_clientes(clientes):
    os.makedirs(os.path.dirname(CLIENTES_JSON_PATH), exist_ok=True)

    data = []
    for cliente in clientes:
        cliente_dict = {
            'cedula': cliente.get_cedula(),
            'nombres': cliente.get_nombres(),
            'apellidos': cliente.get_apellidos(),
            'foto': cliente.get_foto(),
            'contraseña': cliente.get_contraseña(),
            'celular': cliente.get_celular()
        }
        data.append(cliente_dict)

    try:
        with open(CLIENTES_JSON_PATH, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar clientes: {e}")
        return False

def guardar_cliente(cliente):
    clientes = cargar_clientes()

    for c in clientes:
        if c.get_cedula() == cliente.get_cedula():
            c.set_nombres(cliente.get_nombres())
            c.set_apellidos(cliente.get_apellidos())
            c.set_foto(cliente.get_foto())
            c.set_contraseña(cliente.get_contraseña())
            c.set_celular(cliente.get_celular())
            return guardar_clientes(clientes)

    clientes.append(cliente)
    return guardar_clientes(clientes)

def buscar_cliente_por_cedula(cedula):
    clientes = cargar_clientes()
    for cliente in clientes:
        if cliente.get_cedula() == cedula:
            return cliente
    return None

def cargar_carros():
    if not os.path.exists(CARROS_JSON_PATH):
        return []

    try:
        with open(CARROS_JSON_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            carros = []
            for carro_data in data:
                carro = Carro(
                    marca=carro_data['marca'],
                    modelo=carro_data['modelo'],
                    ano=carro_data['ano'],
                    placa=carro_data['placa']
                )
                carros.append(carro)
            return carros
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error al cargar carros: {e}")
        return []

def guardar_carros(carros):
    os.makedirs(os.path.dirname(CARROS_JSON_PATH), exist_ok=True)

    data = []
    for carro in carros:
        carro_dict = {
            'marca': carro.get_marca(),
            'modelo': carro.get_modelo(),
            'ano': carro.get_ano(),
            'placa': carro.get_placa()
        }
        data.append(carro_dict)

    try:
        with open(CARROS_JSON_PATH, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar carros: {e}")
        return False

def cargar_reservas():
    if not os.path.exists(RESERVAS_JSON_PATH):
        return []

    try:
        with open(RESERVAS_JSON_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            reservas = []
            for reserva_data in data:
                cliente = buscar_cliente_por_cedula(reserva_data.get('cedula_cliente', ''))
                reserva = Reserva(
                    origen=reserva_data.get('origen', ''),
                    destino=reserva_data.get('destino', ''),
                    horario=reserva_data.get('horario', ''),
                    cliente=cliente
                )
                reservas.append(reserva)
            return reservas
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error al cargar reservas: {e}")
        return []

def guardar_reservas(reservas):
    os.makedirs(os.path.dirname(RESERVAS_JSON_PATH), exist_ok=True)

    data = []
    for reserva in reservas:
        reserva_dict = {
            'origen': reserva.get_origen(),
            'destino': reserva.get_destino(),
            'horario': reserva.get_horario(),
            'cedula_cliente': reserva.get_cliente().get_cedula() if reserva.get_cliente() else ''
        }
        data.append(reserva_dict)

    try:
        with open(RESERVAS_JSON_PATH, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar reservas: {e}")
        return False

def guardar_reserva(reserva):
    reservas = cargar_reservas()
    reservas.append(reserva)
    return guardar_reservas(reservas)