from utils.excepciones import ValidacionError
from utils.logger import registrar_evento

def validar_monto_positivo(monto, concepto):
    """
    Aporte Alex: Valida que los cobros y depósitos sean mayores a cero.
    Registra errores en el log para auditoría de Software FJ.
    """
    try:
        if monto <= 0:
            raise ValidacionError(f"Monto inválido para {concepto}: {monto}. Debe ser positivo.")
    except ValidacionError as e:
        # Esto cumple con el requisito de registro de errores en archivo
        registrar_evento(f"Validación Alex fallida: {str(e)}", "ERROR")
        raise e
    