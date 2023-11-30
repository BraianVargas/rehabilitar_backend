import apiDB


def nuevo_usuario(data):
    query = f"insert into users (username, password, name) values ('{data['username']}','{data['password']}','{data['name']}')"

    usuario_id = apiDB.consultaGuardar(query)[0]['last_insert_id()']

    return usuario_id