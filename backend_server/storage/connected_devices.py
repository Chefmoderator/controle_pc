connected_pcs = {}

def register_pc(pc_id: str, ws):
    connected_pcs[pc_id] = ws

def unregister_pc(pc_id: str):
    if pc_id in connected_pcs:
        del connected_pcs[pc_id]

def get_pc_socket(pc_id: str):
    return connected_pcs.get(pc_id)
