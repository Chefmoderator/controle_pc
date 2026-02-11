from fastapi import WebSocket
from storage.connected_devices import register_user, unregister_user
from loguru import logger

async def handle_user_connection(pc_id: str, token: str, websocket: WebSocket):
    await websocket.accept()
    register_user(pc_id, websocket)
    logger.info(f"[USER CONNECTED] for PC {pc_id}")

    try:
        while True:
            # Можно читать сообщения от клиента, если нужны команды через WS
            msg = await websocket.receive_text()
            logger.info(f"[USER MESSAGE] {msg}")
    except Exception as e:
        logger.error(f"[USER DISCONNECTED] PC {pc_id}: {e}")
    finally:
        unregister_user(pc_id)
