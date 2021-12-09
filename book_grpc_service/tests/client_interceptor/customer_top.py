import inspect
import logging
from typing import Any, Callable, Dict, List, Optional, Type

from common.components.context_proxy import context_proxy
from common.exception import (
    base_exception,
    call_exception,
    call_other_system,
    case_exception,
    param_exception,
    sms_exception,
    user_exception,
)

from .base import GRPC_RESPONSE, BaseInterceptor, ClientCallDetailsType

logger: logging.Logger = logging.getLogger()


class CustomerTopInterceptor(BaseInterceptor):
    def __init__(self, exc_list: Optional[List[Type[Exception]]] = None):
        self.exc_dict: Dict[str, Type[Exception]] = {}
        for key, exc in globals()["__builtins__"].items():
            if inspect.isclass(exc) and issubclass(exc, Exception):
                self.exc_dict[key] = exc
        for exc_module in [
            base_exception,
            call_exception,
            case_exception,
            param_exception,
            sms_exception,
            param_exception,
            user_exception,
            call_other_system,
        ]:
            for exc_name in dir(exc_module):
                exc = getattr(exc_module, exc_name, None)
                if not exc:
                    continue
                if inspect.isclass(exc) and issubclass(exc, base_exception.BaseServerException):
                    self.exc_dict[exc.__name__] = exc
        if exc_list:
            for exc in exc_list:
                if issubclass(exc, Exception):
                    self.exc_dict[exc.__name__] = exc

    def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        call_details: ClientCallDetailsType,
    ) -> GRPC_RESPONSE:
        if call_details.metadata is not None:
            call_details.metadata.append(("customer-user-agent", "Python3"))  # type: ignore
            call_details.metadata.append(("request_id", context_proxy.request_id))
        response: GRPC_RESPONSE = method(call_details, request_or_iterator)
        metadata_dict: dict = {item.key: item.value for item in response.initial_metadata()}
        if metadata_dict.get("customer-user-agent") == "Python3":
            exc_name: str = metadata_dict.get("exc_name", "")
            exc_info: str = metadata_dict.get("exc_info", "")
            exc: Optional[Type[Exception]] = self.exc_dict.get(exc_name)
            if exc:
                raise exc(exc_info)
        return response
