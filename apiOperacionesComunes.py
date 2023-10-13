from flask import jsonify
import apiDB

def respJson(exito,mensaje,datos):
    return jsonify({'success': exito,'message':mensaje,'data':datos})

def verificaToken(token):
    if token != "":
        resultado=apiDB.consultaSelect(f"Select * from users where binary token='{token}'")
        if (len(resultado))==0:
            return False
        else:
            return True
    #------------------------------------------------------------------------------------------
