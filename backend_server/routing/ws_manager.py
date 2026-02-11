import json
from storage.connected_devices import set_response
from utils.signature import verify_signature
from utils.replay_protection import check_replay
from loguru import logger

async def handle_pc_connection(pc_id: str, token: str, websocket):
    await websocket.accept()
    register_pc(pc_id, websocket)
    logger.info(f"[PC CONNECTED] {pc_id}")

    try:
        while True:
            msg = await websocket.receive_text()
            if not verify_signature(msg) or not check_replay(msg):
                logger.warning(f"Invalid or replay message from {pc_id}")
                await websocket.close(code=4002)
                break

            try:
                payload = msg.split("|")[0]
                data = json.loads(payload)
                cmd_id = data.get("cmd_id")
                result = data.get("result")
                if cmd_id:
                    set_response(pc_id, cmd_id, result)
            except Exception as e:
                logger.error(f"Error parsing message from {pc_id}: {e}")

    except Exception as e:
        logger.error(f"[PC DISCONNECTED] {pc_id} ({e})")
    finally:
        unregister_pc(pc_id)
