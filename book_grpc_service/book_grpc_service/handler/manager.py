import grpc
from google.protobuf.empty_pb2 import Empty

from book_grpc_service.dal.manager import manager_dal
from book_grpc_service.helper.conn_proxy import conn_proxy
from book_grpc_service.helper.field import proto_load, timestamp_to_datetime
from book_grpc_service.protos import manager_pb2 as manager_message
from book_grpc_service.protos import manager_pb2_grpc as manager_service


class ManagerService(manager_service.BookManagerServicer):

    @conn_proxy()
    def create_book(self, request: manager_message.CreateBookRequest,
                    context: grpc.ServicerContext) -> Empty:
        manager_dal.create_book(
            isbn=request.isbn,
            author=request.book_author,
            book_name=request.book_name,
            book_desc=request.book_desc,
            book_url=request.book_url
        )
        return Empty()

    @conn_proxy()
    def delete_book(self, request: manager_message.DeleteBookRequest,
                    context: grpc.ServicerContext) -> Empty:
        manager_dal.delete_book(isbn=request.isbn)
        return Empty()

    @conn_proxy()
    def get_book(self, request: manager_message.GetBookRequest,
                 context: grpc.ServicerContext) -> manager_message.GetBookResult:
        return manager_message.GetBookResult(**proto_load(manager_dal.get_book(isbn=request.isbn)))

    @conn_proxy()
    def get_book_list(self, request: manager_message.GetBookListRequest,
                      context: grpc.ServicerContext) -> manager_message.GetBookListResult:
        return manager_message.GetBookListResult(
            result=proto_load(manager_dal.get_book_list(create_time=timestamp_to_datetime(request.next_create_time, default=None), limit=request.limit))
        )
