from pathlib import Path

from sdx_base.run import run
from sdx_base.server.server import RouterConfig

from app.routes import router, unrecoverable_error_handler
from app.settings import Settings
from app.txid import get_tx_id

if __name__ == '__main__':
    proj_root = Path(__file__).parent  # sdx-cleanup dir
    router_config = RouterConfig(
        router, tx_id_getter=get_tx_id, on_unrecoverable_handler=unrecoverable_error_handler
    )
    run(Settings, routers=[router_config], proj_root=proj_root)
