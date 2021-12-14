import grpc
import pytest
from typing import Callable, List

from book_grpc_service.protos import social_pb2, social_pb2_grpc
from book_grpc_service.interceptor.customer_top import CustomerTopInterceptor
from book_grpc_service.handler.social import SocialService
from book_grpc_service.helper.conn_proxy import g_db_pool, SteadyDBConnection
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
    def test_like_book(self, grpc_stub: social_pb2_grpc.BookSocialStub) -> None:
        isbn: str = "test_isbn"
        uid: str = "66666666"
        try:
            like_request: social_pb2.LikeBookRequest = social_pb2.LikeBookRequest(
                isbn=isbn,
                like=True,
                uid=uid
            )
            grpc_stub.like_book(like_request, metadata=[])
            get_book_like_request: social_pb2.GetBookLikesRequest = social_pb2.GetBookLikesRequest(
                isbn=[isbn]
            )
            get_book_like_result: social_pb2.GetBookLikesListResult = grpc_stub.get_book_like(
                get_book_like_request,
                metadata=[]
            )
            assert get_book_like_result.result
            assert get_book_like_result.result[0].book_like == 1

            grpc_stub.like_book(
                social_pb2.LikeBookRequest(
                    isbn=isbn,
                    like=False,
                    uid=uid
                ),
                metadata=[]
            )

            get_book_like_result = grpc_stub.get_book_like(
                get_book_like_request,
                metadata=[]
            )
            assert get_book_like_result.result
            assert get_book_like_result.result[0].book_like == 0
        finally:
            conn: SteadyDBConnection = g_db_pool.connection()
            with conn.cursor() as cursor:
                ret: int = cursor.execute("DELETE FROM book_like WHERE isbn=%s", (isbn, ))
            conn.commit()
            assert ret == 1

    def test_comment_bool(self, grpc_stub: social_pb2_grpc.BookSocialStub) -> None:
        isbn: str = "test_isbn"
        uid: str = "66666666"
        try:
            comment_book_request: social_pb2.CommentBookRequest = social_pb2.CommentBookRequest(
                isbn=isbn,
                content="test content",
                uid=uid
            )
            grpc_stub.comment_book(request=comment_book_request)
            get_book_comment_request: social_pb2.GetBookCommentRequest = social_pb2.GetBookCommentRequest(
                isbn=[isbn]
            )
            result: social_pb2.GetBookCommentListResult = grpc_stub.get_book_comment(request=get_book_comment_request)
            assert result.result
            assert result.result[0].isbn == isbn
        finally:
            conn: SteadyDBConnection = g_db_pool.connection()
            with conn.cursor() as cursor:
                ret: int = cursor.execute("DELETE FROM book_comment WHERE isbn=%s", (isbn,))
            conn.commit()
            # assert ret == 1

