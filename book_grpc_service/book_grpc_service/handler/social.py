import grpc
from google.protobuf.empty_pb2 import Empty

from book_grpc_service.dal.social import social_dal
from book_grpc_service.helper.field import proto_load

from book_grpc_service.protos import social_pb2 as social_message
from book_grpc_service.protos import social_pb2_grpc as social_service


class SocialService(social_service.BookSocialServicer):
    def like_book(self, request: social_message.LikeBookRequest,
                  context: grpc.ServicerContext) -> Empty:
        social_dal.like_book(isbn=request.isbn, like=request.like, uid=request.uid)
        return Empty()

    def get_book_like(self, request: social_message.GetBookLikesRequest,
                      context: grpc.ServicerContext) -> social_message.GetBookLikesListResult:
        return social_message.GetBookLikesListResult(result=proto_load(social_dal.get_book_likes(isbn=request.isbn)))

    def comment_book(self, request: social_message.CommentBookRequest,
                     context: grpc.ServicerContext) -> Empty:
        social_dal.comment_book(isbn=request.isbn, content=request.content, uid=request.uid)
        return Empty()

    def get_book_comment(self, request: social_message.GetBookCommentRequest,
                         context: grpc.ServicerContext) -> social_message.GetBookCommentListResult:
        return social_message.GetBookLikesListResult(
            result=proto_load(
                social_dal.get_book_comment(
                    isbn=request.isbn,
                    create_time=request.next_create_time,
                    limit=request.limit
                )
            )
        )