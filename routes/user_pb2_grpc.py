# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import user_pb2 as user__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(
        GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in user_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class UserServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetUserRPC = channel.unary_unary(
            '/UserService/GetUserRPC',
            request_serializer=user__pb2.GetUserRequest.SerializeToString,
            response_deserializer=user__pb2.GetUserResponse.FromString,
            _registered_method=True)
        self.PostUserRPC = channel.unary_unary(
            '/UserService/PostUserRPC',
            request_serializer=user__pb2.PostUserRequest.SerializeToString,
            response_deserializer=user__pb2.PostUserResponse.FromString,
            _registered_method=True)
        self.PutUserRPC = channel.unary_unary(
            '/UserService/PutUserRPC',
            request_serializer=user__pb2.PutUserRequest.SerializeToString,
            response_deserializer=user__pb2.PutUserResponse.FromString,
            _registered_method=True)
        self.DeleteUserRPC = channel.unary_unary(
            '/UserService/DeleteUserRPC',
            request_serializer=user__pb2.DeleteUserRequest.SerializeToString,
            response_deserializer=user__pb2.DeleteUserResponse.FromString,
            _registered_method=True)


class UserServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetUserRPC(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PostUserRPC(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PutUserRPC(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteUserRPC(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'GetUserRPC': grpc.unary_unary_rpc_method_handler(
            servicer.GetUserRPC,
            request_deserializer=user__pb2.GetUserRequest.FromString,
            response_serializer=user__pb2.GetUserResponse.SerializeToString,
        ),
        'PostUserRPC': grpc.unary_unary_rpc_method_handler(
            servicer.PostUserRPC,
            request_deserializer=user__pb2.PostUserRequest.FromString,
            response_serializer=user__pb2.PostUserResponse.SerializeToString,
        ),
        'PutUserRPC': grpc.unary_unary_rpc_method_handler(
            servicer.PutUserRPC,
            request_deserializer=user__pb2.PutUserRequest.FromString,
            response_serializer=user__pb2.PutUserResponse.SerializeToString,
        ),
        'DeleteUserRPC': grpc.unary_unary_rpc_method_handler(
            servicer.DeleteUserRPC,
            request_deserializer=user__pb2.DeleteUserRequest.FromString,
            response_serializer=user__pb2.DeleteUserResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'UserService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('UserService', rpc_method_handlers)

 # This class is part of an EXPERIMENTAL API.


class UserService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetUserRPC(request,
                   target,
                   options=(),
                   channel_credentials=None,
                   call_credentials=None,
                   insecure=False,
                   compression=None,
                   wait_for_ready=None,
                   timeout=None,
                   metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/UserService/GetUserRPC',
            user__pb2.GetUserRequest.SerializeToString,
            user__pb2.GetUserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def PostUserRPC(request,
                    target,
                    options=(),
                    channel_credentials=None,
                    call_credentials=None,
                    insecure=False,
                    compression=None,
                    wait_for_ready=None,
                    timeout=None,
                    metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/UserService/PostUserRPC',
            user__pb2.PostUserRequest.SerializeToString,
            user__pb2.PostUserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def PutUserRPC(request,
                   target,
                   options=(),
                   channel_credentials=None,
                   call_credentials=None,
                   insecure=False,
                   compression=None,
                   wait_for_ready=None,
                   timeout=None,
                   metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/UserService/PutUserRPC',
            user__pb2.PutUserRequest.SerializeToString,
            user__pb2.PutUserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteUserRPC(request,
                      target,
                      options=(),
                      channel_credentials=None,
                      call_credentials=None,
                      insecure=False,
                      compression=None,
                      wait_for_ready=None,
                      timeout=None,
                      metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/UserService/DeleteUserRPC',
            user__pb2.DeleteUserRequest.SerializeToString,
            user__pb2.DeleteUserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)