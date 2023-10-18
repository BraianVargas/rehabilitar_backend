from flask import jsonify


def procesar_datos(_dni, token, datos_frontend):
    try:
        # Realiza validaciones adicionales del token si es necesario
        if not token:
            return jsonify({'Error': "Token no proporcionado"}), 400
        if len(token) != 100:
            return jsonify({'Error': "Token no válido"}), 400

        # Procesa los datos del frontend
        # Aquí puedes realizar validaciones, almacenarlos en una base de datos, etc.

        # Ejemplo: almacenar datos en una base de datos
        # db.guardar_datos(_dni, datos_frontend)

        # Devuelve una respuesta exitosa
        return jsonify({'Mensaje': 'Datos procesados exitosamente'}), 200

    except Exception as e:
        return jsonify({'Error': str(e)}), 500