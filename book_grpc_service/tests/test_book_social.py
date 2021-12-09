import grpc
import pytest
import pytest_mock
from typing import Callable, List

from book_grpc_service.protos import social_pb2, social_pb2_grpc
from book_grpc_service.interceptor.customer_top import CustomerTopInterceptor
from book_grpc_service.handler.social import SocialService
from tests.client_interceptor.customer_top import CustomerTopInterceptor as ClientCustomerTopInterceptor


@pytest.fixture(scope="module")
def grpc_add_to_server() -> Callable:
    return social_pb2_grpc.add_BookSocialServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer() -> SocialService:
    return SocialService()


@pytest.fixture(scope="module")
def grpc_interceptors() -> List[grpc.ServerInterceptor]:
    return [CustomerTopInterceptor()]


@pytest.fixture(scope="module")
def grpc_stub(grpc_channel: grpc.Channel) -> social_pb2_grpc.BookSocialStub:
    channel: grpc.Channel = grpc.intercept_channel(grpc_channel, ClientCustomerTopInterceptor())
    return social_pb2_grpc.BookSocialStub(channel)


class TestSocial:
    pass
