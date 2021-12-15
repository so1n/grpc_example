import logging
import time
from typing import Any, Callable, List, Tuple

import grpc
from user_grpc_service.helper.context import context_proxy

from .base import BaseInterceptor

logger: logging.Logger = logging.getLogger()


class CustomerTopInterceptor(BaseInterceptor):
    def intercept(
        self,
        next_handler_method: Callable,
        request_proto_message: Any,
        context: grpc.ServicerContext,
    ) -> Any:
        start_time: float = time.time()
        return_initial_metadata: List[Tuple] = [("customer-user-agent", "Python3")]
        try:
            # run grpc handler
            return next_handler_method(request_proto_message, context)
        except Exception as e:
            # Delivery exception
            if self.metadata_dict.get("customer-user-agent", "") == "Python3":
                return_initial_metadata.append(("exc_name", e.__class__.__name__))
                return_initial_metadata.append(("exc_info", str(e)))
            logging.exception(
                f"{context_proxy.method} request exc:{e.__class__.__name__} error:{e}"
            )
            raise e
        finally:
            context.send_initial_metadata(return_initial_metadata)
            logging.info(
                f"Got Request. method:{self.method}, code:{context.code()}, detail:{context.details()}, duration:{time.time() - start_time}"
            )
