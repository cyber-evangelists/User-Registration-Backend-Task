# import grpc
# from concurrent import futures
# import asyncio
# import logging
# import user_pb2
# import user_pb2_grpc

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # In-memory storage
# users = {}

# class UserServiceServicer(user_pb2_grpc.UserServiceServicer):

#     async def GetUserRPC(self, request, context):
#         logger.info(f"Received GetUserRPC request for CNIC: {request.cnic}")
#         user = users.get(request.cnic)
#         if user:
#             logger.info(f"User found: {user}")
#             return user_pb2.GetUserResponse(
#                 cnic=user.cnic,
#                 forename=user.forename,
#                 surname=user.surname,
#                 address=user.address,
#                 email=user.email
#             )
#         else:
#             context.set_details("User not found")
#             context.set_code(grpc.StatusCode.NOT_FOUND)
#             logger.warning(f"User with CNIC {request.cnic} not found")
#             return user_pb2.GetUserResponse()

#     def PostUserRPC(self, request, context):
#         logger.info(f"Received PostUserRPC request for CNIC: {request.cnic}")
#         if request.cnic in users:
#             context.set_details("User already exists")
#             context.set_code(grpc.StatusCode.ALREADY_EXISTS)
#             logger.warning(f"User with CNIC {request.cnic} already exists")
#             return user_pb2.PostUserResponse()
#         try:
#             new_user = user_pb2.GetUserResponse(
#                 cnic=request.cnic,
#                 forename=request.forename,
#                 surname=request.surname,
#                 address=request.address,
#                 email=request.email
#             )
#             users[request.cnic] = new_user
#             logger.info(f"User created: {new_user}")
#             return user_pb2.PostUserResponse(message="User created successfully")
#         except Exception as e:
#             logger.error(f"Error creating user: {e}")
#             context.set_details(str(e))
#             context.set_code(grpc.StatusCode.INTERNAL)
#             return user_pb2.PostUserResponse()

#     async def PutUserRPC(self, request, context):
#         logger.info(f"Received PutUserRPC request for CNIC: {request.cnic}")
#         user = users.get(request.cnic)
#         if user:
#             user.forename = request.forename
#             user.surname = request.surname
#             user.address = request.address
#             user.email = request.email
#             if request.password:
#                 user.password = request.password
#             logger.info(f"User updated: {user}")
#             return user_pb2.PutUserResponse(message="User updated successfully")
#         else:
#             context.set_details("User not found")
#             context.set_code(grpc.StatusCode.NOT_FOUND)
#             logger.warning(f"User with CNIC {request.cnic} not found")
#             return user_pb2.PutUserResponse()

#     async def DeleteUserRPC(self, request, context):
#         logger.info(f"Received DeleteUserRPC request for CNIC: {request.cnic}")
#         if request.cnic in users:
#             del users[request.cnic]
#             logger.info(f"User with CNIC {request.cnic} deleted")
#             return user_pb2.DeleteUserResponse(message="User deleted successfully")
#         else:
#             context.set_details("User not found")
#             context.set_code(grpc.StatusCode.NOT_FOUND)
#             logger.warning(f"User with CNIC {request.cnic} not found")
#             return user_pb2.DeleteUserResponse(message="User not found")

# def serve():
#     logger.info("Starting gRPC server")
#     server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
#     user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
#     server.add_insecure_port('[::]:50051')
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(server.start())
#     logger.info("Server started, listening on port 50051")
#     loop.run_until_complete(server.wait_for_termination())

# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     serve()

import grpc
from concurrent import futures
import asyncio
import logging
import user_pb2
import user_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage
users = {}

class UserServiceServicer(user_pb2_grpc.UserServiceServicer):

    async def GetUserRPC(self, request, context):
        logger.info(f"Received GetUserRPC request for CNIC: {request.cnic}")
        user = users.get(request.cnic)
        if user:
            logger.info(f"User found: {user}")
            return user_pb2.GetUserResponse(
                cnic=user.cnic,
                forename=user.forename,
                surname=user.surname,
                address=user.address,
                email=user.email
            )
        else:
            context.set_details("User not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            logger.warning(f"User with CNIC {request.cnic} not found")
            return user_pb2.GetUserResponse()

    def PostUserRPC(self, request, context):
        logger.info(f"Received PostUserRPC request for CNIC: {request.cnic}")
        if request.cnic in users:
            context.set_details("User already exists")
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            logger.warning(f"User with CNIC {request.cnic} already exists")
            return user_pb2.PostUserResponse()
        try:
            new_user = user_pb2.GetUserResponse(
                cnic=request.cnic,
                forename=request.forename,
                surname=request.surname,
                address=request.address,
                email=request.email
            )
            users[request.cnic] = new_user
            logger.info(f"User created: {new_user}")
            return user_pb2.PostUserResponse(message="User created successfully")
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return user_pb2.PostUserResponse()

    async def PutUserRPC(self, request, context):
        logger.info(f"Received PutUserRPC request for CNIC: {request.cnic}")
        user = users.get(request.cnic)
        if user:
            user.forename = request.forename
            user.surname = request.surname
            user.address = request.address
            user.email = request.email
            if request.password:
                user.password = request.password
            logger.info(f"User updated: {user}")
            return user_pb2.PutUserResponse(message="User updated successfully")
        else:
            context.set_details("User not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            logger.warning(f"User with CNIC {request.cnic} not found")
            return user_pb2.PutUserResponse()

    async def DeleteUserRPC(self, request, context):
        logger.info(f"Received DeleteUserRPC request for CNIC: {request.cnic}")
        if request.cnic in users:
            del users[request.cnic]
            logger.info(f"User with CNIC {request.cnic} deleted")
            return user_pb2.DeleteUserResponse(message="User deleted successfully")
        else:
            context.set_details("User not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            logger.warning(f"User with CNIC {request.cnic} not found")
            return user_pb2.DeleteUserResponse(message="User not found")

def serve():
    logger.info("Starting gRPC server")
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.start())
    logger.info("Server started, listening on port 50051")
    loop.run_until_complete(server.wait_for_termination())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
