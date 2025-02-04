import logging

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from src.core.settings import app_config
from src.websocket_server.consumer import base_websocket_manager_consumer
from src.websocket_server.dependencies import verify_websocket_api_key
from src.websocket_server.services.decorators import (
    TelegramNotificationWsServerReceiveHandlerDecorator,
)
from src.websocket_server.services.ws_handler import (
    IWsServerReceiveHandler,
    WsServerReceiveHandler,
)


_logger = logging.getLogger(__name__)


router = APIRouter()


@router.websocket("/ws/v1/base-middleware-soft-server")
async def websocket_middleware_soft_endpoint(
    websocket: WebSocket, api_key: str = Depends(verify_websocket_api_key)
):
    _logger.debug("New connect = %s", websocket)
    client_id: str = await base_websocket_manager_consumer.connect(websocket)
    _logger.debug(
        "client_id = %s, notification to telegram = %s",
        client_id,
        app_config.ws_server_notification_telegram,
    )
    if app_config.ws_server_notification_telegram:
        handler: IWsServerReceiveHandler = (
            TelegramNotificationWsServerReceiveHandlerDecorator(
                receive_handler=WsServerReceiveHandler()
            )
        )
    else:
        handler: IWsServerReceiveHandler = WsServerReceiveHandler()
    try:
        while True:
            data = await base_websocket_manager_consumer.receive(client_id)
            _logger.debug("Полученные данные от клиента = %s", data)
            try:
                response_handler_data: dict = await handler.execute(data)
                if len(response_handler_data) > 0:
                    await base_websocket_manager_consumer.send_personal_message(
                        message_data=response_handler_data, client_id=client_id
                    )
            except Exception as er:
                _logger.warning(
                    "Во время обработки пакета от клиента возникла ошибка", exc_info=er
                )
    except WebSocketDisconnect:
        base_websocket_manager_consumer.disconnect(client_id)
