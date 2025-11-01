# webpay_service.py
import os
from transbank.webpay.webpay_plus.transaction import Transaction # type: ignore

# Modo integración - Usar variables de entorno en producción
COMMERCE_CODE = os.getenv("TRANSBANK_COMMERCE_CODE", "597055555532")
API_KEY = os.getenv("TRANSBANK_API_KEY", "579B532A7440BB0C9079DED94D31EA161EBE3BBA")

# Configurar credenciales a nivel de clase
Transaction.commerce_code = COMMERCE_CODE
Transaction.api_key = API_KEY

class WebpayService:
    def __init__(self):
        """Inicializa el servicio de Webpay Plus"""
        # Transaction ya está configurado con las credenciales a nivel de clase
        pass
    
    def create_transaction(self, buy_order: str, session_id: str, amount: float, return_url: str):
        """
        Crea una transacción en Webpay Plus
        
        Args:
            buy_order: Orden de compra (máx 26 caracteres)
            session_id: Identificador de sesión
            amount: Monto de la transacción
            return_url: URL de retorno después del pago
            
        Returns:
            dict: Respuesta con token y url de pago
        """
        try:
            response = Transaction.create(
                buy_order=buy_order,
                session_id=session_id,
                amount=int(amount),
                return_url=return_url
            )
            return {
                "success": True,
                "token": response.get("token"),
                "url": response.get("url")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def commit_transaction(self, token: str):
        """
        Confirma una transacción después del pago
        
        Args:
            token: Token de la transacción
            
        Returns:
            dict: Detalles de la transacción confirmada
        """
        try:
            response = Transaction.commit(token=token)
            return {
                "success": True,
                "data": response
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_status(self, token: str):
        """
        Obtiene el estado de una transacción
        
        Args:
            token: Token de la transacción
            
        Returns:
            dict: Estado de la transacción
        """
        try:
            response = Transaction.status(token=token)
            return {
                "success": True,
                "data": response
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def refund_transaction(self, token: str, amount: float):
        """
        Realiza un reembolso de una transacción
        
        Args:
            token: Token de la transacción
            amount: Monto a reembolsar
            
        Returns:
            dict: Resultado del reembolso
        """
        try:
            response = Transaction.refund(
                token=token,
                amount=int(amount)
            )
            return {
                "success": True,
                "data": response
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Instancia singleton del servicio
webpay_service = WebpayService()
