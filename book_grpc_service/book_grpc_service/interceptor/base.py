import abc
import logging
import uuid
from typing import Any, Callable, Tuple

import grpc

from book_grpc_service.helper.context import context_proxy, WithContext

logger: logging.Logger = logging.getLogger()


class BaseInterceptor(grpc.ServerInterceptor):
    """reference by: https://github.com/d5h-foss/grpc-interceptor/blob/master/src/grpc_interceptor/server.py"""

    @property
    def method(self) -> str:
        if not context_proxy.inited:
            raise ValueError("Not init")
        return context_proxy.method

    @property
    def package(self) -> str:
        if not context_proxy.inited:
            raise ValueError("Not init")
        return context_proxy.package

    @property
    def method_name(self) -> str:
        if not context_proxy.inited:
            raise ValueError("Not init")
        return context_proxy.method_name

    @property
    def service(self) -> str:
        if not context_proxy.inited:
            raise ValueError("Not init")
        return context_proxy.service

    @property
    def metadata_dict(self) -> dict:
        if not context_proxy.inited:
            raise ValueError("Not init")
        return context_proxy.metadata_dict

    @staticmethod
    def _context_handle(handler_call_details: grpc.HandlerCallDetails) -> None:
        method: str = handler_call_details.method  # type: ignore
        _, package_and_service, method_name = method.split("/")
        *maybe_package, service = package_and_service.rsplit(".", maxsplit=1)
        package = maybe_package[0] if maybe_package else ""

        metadata_dict = {}
        for item in handler_call_details.invocation_metadata:  # type:ignore
            metadata_dict.update({item.key: item.value})

        context_proxy.req_id = metadata_dict.get("request_id", str(uuid.uuid4()))
        context_proxy.method = method
        context_proxy.package = package
        context_proxy.service = service
        context_proxy.method_name = method_name
        context_proxy.metadata_dict = metadata_dict
        context_proxy.inited = True

    @abc.abstractmethod
    def intercept(
        self,
        next_handler_method: Callable,
        request_proto_message: Any,
        context: grpc.ServicerContext,
    ) -> Any:
        return next_handler_method(request_proto_message, context)

    def intercept_service(
        self,
        continuation: Callable[[grpc.HandlerCallDetails], grpc.RpcMethodHandler],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        next_handler: grpc.RpcMethodHandler = continuation(handler_call_details)
        handler_factory, next_handler_method, grpc_type = _get_factory_and_method(next_handler)

        def invoke_intercept_method(request_proto_message: Any, context: grpc.ServicerContext) -> Any:
            if not context_proxy.inited:
                with WithContext():
                    self._context_handle(handler_call_details)
                    context_proxy.grpc_type = grpc_type
                    return self.intercept(next_handler_method, request_proto_message, context)
            else:
                return self.intercept(next_handler_method, request_proto_message, context)

        return handler_factory(
            invoke_intercept_method,
            request_deserializer=next_handler.request_deserializer,  # type: ignore
            response_serializer=next_handler.response_serializer,  # type: ignore
        )


def _get_factory_and_method(rpc_handler: grpc.RpcMethodHandler) -> Tuple[Callable, Callable, str]:
    if rpc_handler.unary_unary:  # type: ignore
        return grpc.unary_unary_rpc_method_handler, rpc_handler.unary_unary, "unary_unary"  # type: ignore
    elif rpc_handler.unary_stream:  # type: ignore
        return grpc.unary_stream_rpc_method_handler, rpc_handler.unary_stream, "unary_stream"  # type: ignore
    elif rpc_handler.stream_unary:  # type: ignore
        return grpc.stream_unary_rpc_method_handler, rpc_handler.stream_unary, "stream_unary"  # type: ignore
    elif rpc_handler.stream_stream:  # type: ignore
        return grpc.stream_stream_rpc_method_handler, rpc_handler.stream_stream, "stream_stream"  # type: ignore
    else:  # pragma: no cover
        raise RuntimeError("RPC handler implementation does not exist")
