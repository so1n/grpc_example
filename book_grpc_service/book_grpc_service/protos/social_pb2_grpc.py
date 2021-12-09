# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import social_pb2 as protos_dot_social__pb2


class BookSocialStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.like_book = channel.unary_unary(
                '/book_social.BookSocial/like_book',
                request_serializer=protos_dot_social__pb2.LikeBookRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get_book_like = channel.unary_unary(
                '/book_social.BookSocial/get_book_like',
                request_serializer=protos_dot_social__pb2.GetBookLikesRequest.SerializeToString,
                response_deserializer=protos_dot_social__pb2.GetBookLikesListResult.FromString,
                )
        self.comment_book = channel.unary_unary(
                '/book_social.BookSocial/comment_book',
                request_serializer=protos_dot_social__pb2.CommentBookRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get_book_comment = channel.unary_unary(
                '/book_social.BookSocial/get_book_comment',
                request_serializer=protos_dot_social__pb2.GetBookCommentRequest.SerializeToString,
                response_deserializer=protos_dot_social__pb2.GetBookCommentListResult.FromString,
                )


class BookSocialServicer(object):
    """Missing associated documentation comment in .proto file."""

    def like_book(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_book_like(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def comment_book(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_book_comment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BookSocialServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'like_book': grpc.unary_unary_rpc_method_handler(
                    servicer.like_book,
                    request_deserializer=protos_dot_social__pb2.LikeBookRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get_book_like': grpc.unary_unary_rpc_method_handler(
                    servicer.get_book_like,
                    request_deserializer=protos_dot_social__pb2.GetBookLikesRequest.FromString,
                    response_serializer=protos_dot_social__pb2.GetBookLikesListResult.SerializeToString,
            ),
            'comment_book': grpc.unary_unary_rpc_method_handler(
                    servicer.comment_book,
                    request_deserializer=protos_dot_social__pb2.CommentBookRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get_book_comment': grpc.unary_unary_rpc_method_handler(
                    servicer.get_book_comment,
                    request_deserializer=protos_dot_social__pb2.GetBookCommentRequest.FromString,
                    response_serializer=protos_dot_social__pb2.GetBookCommentListResult.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'book_social.BookSocial', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BookSocial(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def like_book(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/book_social.BookSocial/like_book',
            protos_dot_social__pb2.LikeBookRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_book_like(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/book_social.BookSocial/get_book_like',
            protos_dot_social__pb2.GetBookLikesRequest.SerializeToString,
            protos_dot_social__pb2.GetBookLikesListResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def comment_book(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/book_social.BookSocial/comment_book',
            protos_dot_social__pb2.CommentBookRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_book_comment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/book_social.BookSocial/get_book_comment',
            protos_dot_social__pb2.GetBookCommentRequest.SerializeToString,
            protos_dot_social__pb2.GetBookCommentListResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
