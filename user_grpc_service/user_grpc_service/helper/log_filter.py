import logging
from typing import Any

from .context import context_proxy


class ReqIDLogFilter(logging.Filter):
    """support print req id in log"""

    def filter(self, record: Any) -> Any:
        record.request_id = context_proxy.req_id or ""
        return record
