from transbank.webpay.webpay_plus.transaction import Transaction
import os
from typing import Dict, Any


class WebpayService:
    """
    Servicio para gestionar transacciones con Webpay Plus en ambiente de INTEGRACIÓN
    Implementa: crear, confirmar, obtener estado y reembolsar transacciones
    """
    
    def __init__(self):
        """
        Inicializa el servicio de Webpay para AMBIENTE DE INTEGRACIÓN
        Usa las credenciales oficiales de integración de Transbank
        """
        # Credenciales oficiales de integración de Transbank
        # Código de comercio de integración
        self.commerce_code = "597055555532"
        # API Key de integración (también llamada "secret key")
        self.api_key = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
    
    def _get_transaction(self) -> Transaction:
        """
        Crea una instancia de Transaction para el ambiente de INTEGRACIÓN
        """
        return Transaction.build_for_integration(self.commerce_code, self.api_key)
    
    def create_transaction(self, buy_order: str, session_id: str, amount: float, return_url: str) -> Dict[str, Any]:
        """
        Crea una nueva transacción de pago
        
        Args:
            buy_order: Orden de compra (máx 26 caracteres)
            session_id: ID de sesión único
            amount: Monto de la transacción
            return_url: URL a la que Webpay redirigirá después del pago
            
        Returns:
            Dict con success, url y token de la transacción
        """
        try:
            tx = self._get_transaction()
            response = tx.create(buy_order, session_id, amount, return_url)
            
            # Manejar respuesta según versión del SDK
            # Versión 3.x usa diccionarios, versión 2.x usa objetos
            if isinstance(response, dict):
                # Versión 3.x
                return {
                    "success": True,
                    "url": response.get('url'),
                    "token": response.get('token'),
                    "buy_order": buy_order,
                    "session_id": session_id,
                    "amount": amount
                }
            else:
                # Versión 2.x
                return {
                    "success": True,
                    "url": response.url,
                    "token": response.token,
                    "buy_order": buy_order,
                    "session_id": session_id,
                    "amount": amount
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al crear transacción: {str(e)}"
            }
    
    def commit_transaction(self, token: str) -> Dict[str, Any]:
        """
        Confirma una transacción después del pago
        
        Args:
            token: Token de la transacción a confirmar
            
        Returns:
            Dict con toda la información de la transacción confirmada
        """
        try:
            tx = self._get_transaction()
            response = tx.commit(token)
            
            # Manejar respuesta según versión del SDK
            if isinstance(response, dict):
                # Versión 3.x
                return {
                    "success": True,
                    "vci": response.get('vci'),
                    "amount": response.get('amount'),
                    "status": response.get('status'),
                    "buy_order": response.get('buy_order'),
                    "session_id": response.get('session_id'),
                    "card_detail": response.get('card_detail'),
                    "accounting_date": response.get('accounting_date'),
                    "transaction_date": response.get('transaction_date'),
                    "authorization_code": response.get('authorization_code'),
                    "payment_type_code": response.get('payment_type_code'),
                    "response_code": response.get('response_code'),
                    "installments_amount": response.get('installments_amount'),
                    "installments_number": response.get('installments_number'),
                    "balance": response.get('balance')
                }
            else:
                # Versión 2.x
                return {
                    "success": True,
                    "vci": response.vci,
                    "amount": response.amount,
                    "status": response.status,
                    "buy_order": response.buy_order,
                    "session_id": response.session_id,
                    "card_detail": response.card_detail,
                    "accounting_date": response.accounting_date,
                    "transaction_date": response.transaction_date,
                    "authorization_code": response.authorization_code,
                    "payment_type_code": response.payment_type_code,
                    "response_code": response.response_code,
                    "installments_amount": response.installments_amount,
                    "installments_number": response.installments_number,
                    "balance": response.balance
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al confirmar transacción: {str(e)}"
            }
    
    def get_status(self, token: str) -> Dict[str, Any]:
        """
        Obtiene el estado actual de una transacción
        
        Args:
            token: Token de la transacción
            
        Returns:
            Dict con el estado completo de la transacción
        """
        try:
            tx = self._get_transaction()
            response = tx.status(token)
            
            # Manejar respuesta según versión del SDK
            if isinstance(response, dict):
                # Versión 3.x
                return {
                    "success": True,
                    "vci": response.get('vci'),
                    "amount": response.get('amount'),
                    "status": response.get('status'),
                    "buy_order": response.get('buy_order'),
                    "session_id": response.get('session_id'),
                    "card_detail": response.get('card_detail'),
                    "accounting_date": response.get('accounting_date'),
                    "transaction_date": response.get('transaction_date'),
                    "authorization_code": response.get('authorization_code'),
                    "payment_type_code": response.get('payment_type_code'),
                    "response_code": response.get('response_code'),
                    "installments_amount": response.get('installments_amount'),
                    "installments_number": response.get('installments_number'),
                    "balance": response.get('balance')
                }
            else:
                # Versión 2.x
                return {
                    "success": True,
                    "vci": response.vci,
                    "amount": response.amount,
                    "status": response.status,
                    "buy_order": response.buy_order,
                    "session_id": response.session_id,
                    "card_detail": response.card_detail,
                    "accounting_date": response.accounting_date,
                    "transaction_date": response.transaction_date,
                    "authorization_code": response.authorization_code,
                    "payment_type_code": response.payment_type_code,
                    "response_code": response.response_code,
                    "installments_amount": response.installments_amount,
                    "installments_number": response.installments_number,
                    "balance": response.balance
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al obtener estado de transacción: {str(e)}"
            }
    
    def refund_transaction(self, token: str, amount: float) -> Dict[str, Any]:
        """
        Realiza un reembolso de una transacción
        
        Args:
            token: Token de la transacción a reembolsar
            amount: Monto a reembolsar
            
        Returns:
            Dict con el resultado del reembolso
        """
        try:
            tx = self._get_transaction()
            response = tx.refund(token, amount)
            
            # Manejar respuesta según versión del SDK
            if isinstance(response, dict):
                # Versión 3.x
                return {
                    "success": True,
                    "type": response.get('type'),
                    "authorization_code": response.get('authorization_code'),
                    "authorization_date": response.get('authorization_date'),
                    "nullified_amount": response.get('nullified_amount'),
                    "balance": response.get('balance'),
                    "response_code": response.get('response_code')
                }
            else:
                # Versión 2.x
                return {
                    "success": True,
                    "type": response.type,
                    "authorization_code": response.authorization_code,
                    "authorization_date": response.authorization_date,
                    "nullified_amount": response.nullified_amount,
                    "balance": response.balance,
                    "response_code": response.response_code
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al realizar reembolso: {str(e)}"
            }


# Instancia global del servicio
webpay_service = WebpayService()