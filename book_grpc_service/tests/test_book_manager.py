import grpc
import pytest
import pytest_mock
from typing import Callable, List

from book_grpc_service.protos import manager_pb2, manager_pb2_grpc
from book_grpc_service.interceptor.customer_top import CustomerTopInterceptor
from book_grpc_service.handler.manager import ManagerService
from tests.client_interceptor.customer_top import CustomerTopInterceptor as ClientCustomerTopInterceptor


@pytest.fixture(scope="module")
def grpc_add_to_server() -> Callable:
    return manager_pb2_grpc.add_BookManagerServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer() -> ManagerService:
    return ManagerService()


@pytest.fixture(scope="module")
def grpc_interceptors() -> List[grpc.ServerInterceptor]:
    return [CustomerTopInterceptor()]


@pytest.fixture(scope="module")
def grpc_stub(grpc_channel: grpc.Channel) -> manager_pb2_grpc.BookManagerStub:
    channel: grpc.Channel = grpc.intercept_channel(grpc_channel, ClientCustomerTopInterceptor())
    return manager_pb2_grpc.BookManagerStub(channel)


class Testmanager:
    pass
