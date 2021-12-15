import hashlib
import uuid

import grpc
from google.protobuf.empty_pb2 import Empty
from user_grpc_service.dal.user import UserTypedDict, user_dal
from user_grpc_service.helper.conn_proxy import conn_proxy
from user_grpc_service.protos import user_pb2 as user_message
from user_grpc_service.protos import user_pb2_grpc as user_service


class UserService(user_service.UserServicer):
    @conn_proxy()
    def check_user_login(
        self, request: user_message.LogoutUserRequest, context: grpc.ServicerContext
    ) -> user_message.CheckLoginResult:
        return user_message.CheckLoginResult(
            result=user_dal.check_login(uid=request.uid, token=request.token)
        )

    @conn_proxy()
    def logout_user(
        self, request: user_message.LogoutUserRequest, context: grpc.ServicerContext
    ) -> Empty:
        user_dal.logout_user(uid=request.uid, token=request.token)
        return Empty()

    @conn_proxy()
    def login_user(
        self, request: user_message.LoginUserRequest, context: grpc.ServicerContext
    ) -> user_message.LoginUserResult:
        token: str = hashlib.sha256(str(uuid.uuid1()).encode("utf-8")).hexdigest()
        user_dict: UserTypedDict = user_dal.login_user(
            uid=request.uid, password=request.password, token=token
        )
        return user_message.LoginUserResult(
            uid=request.uid, user_name=user_dict["user_name"], token=token
        )

    @conn_proxy()
    def create_user(
        self, request: user_message.CreateUserRequest, context: grpc.ServicerContext
    ) -> Empty:
        user_dal.create_user(
            uid=request.uid, user_name=request.user_name, password=request.password
        )
        return Empty()

    @conn_proxy()
    def delete_user(
        self, request: user_message.DeleteUserRequest, context: grpc.ServicerContext
    ) -> Empty:
        user_dal.delete_user(uid=request.uid)
        return Empty()
