from models import User
from db import init_db

import grpc
import user_pb2
import user_pb2_grpc

from concurrent import futures
from typing import List
import asyncio

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MongoDB connection


async def on_startup():
    """
    Initializes the MongoDB connection at startup.
    """

    await init_db()
    logger.info("Database connection initialized")


# gRPC servicer class


class UserServiceServicer(user_pb2_grpc.UserServiceServicer):

    """
    gRPC servicer class for handling user operations.
    """

    # ----------------------------------------------------------------------------->
    # GET ------------------------------------------------------------------------->
    # ----------------------------------------------------------------------------->

    async def GetUserRPC(self, request, context):
        """
        Handles the GetUserRPC request.

        PARAMS:
        - request: gRPC request containing the CNIC of the user.
        - context: gRPC context for the request.

        RETURNS:
        The user details if found, else sets the context to NOT_FOUND.

        """

        logger.info(f"Received GetUserRPC request for CNIC: {request.cnic}")
        user = await User.find_one(User.cnic == request.cnic)
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

    # ------------------------------------------------------------------------------>
    # POST ------------------------------------------------------------------------->
    # ------------------------------------------------------------------------------>

    async def PostUserRPC(self, request, context):
        """
        Handles the PostUserRPC request.

        PARAMS:
        - request: gRPC request containing the user details to be created.
        - context: gRPC context for the request.

        RETURNS:
        A new user if the CNIC does not already exist, else sets the context to ALREADY_EXISTS.

        """

        logger.info(f"Received PostUserRPC request for CNIC: {request.cnic}")
        existing_user = await User.find_one(User.cnic == request.cnic)
        if existing_user:
            context.set_details("User already exists")
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            logger.warning(f"User with CNIC {request.cnic} already exists")

            return user_pb2.PostUserResponse()

        try:
            new_user = User(
                cnic=request.cnic,
                forename=request.forename,
                surname=request.surname,
                address=request.address,
                email=request.email,
                password=request.password
            )
            await new_user.insert()
            logger.info(f"User created: {new_user}")

            return user_pb2.PostUserResponse(
                message="User created successfully")
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return user_pb2.PostUserResponse()

    # ----------------------------------------------------------------------------->
    # PUT ------------------------------------------------------------------------->
    # ----------------------------------------------------------------------------->

    async def PutUserRPC(self, request, context):
        """
        Handles the PutUserRPC request.

        PARAMS:
        - request: gRPC request containing the updated user details.
        - context: gRPC context for the request.

        RETURNS:
        Updates the user details if found, else sets the context to NOT_FOUND.

        """

        logger.info(f"Received PutUserRPC request for CNIC: {request.cnic}")
        user = await User.find_one(User.cnic == request.cnic)
        if user:
            user.forename = request.forename
            user.surname = request.surname
            user.address = request.address
            user.email = request.email
            if request.password:
                user.password = request.password
            await user.save()
            logger.info(f"User updated: {user}")

            return user_pb2.PutUserResponse(
                message="User updated successfully")
        else:
            context.set_details("User not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            logger.warning(f"User with CNIC {request.cnic} not found")

            return user_pb2.PutUserResponse()

    # -------------------------------------------------------------------------------->
    # DELETE ------------------------------------------------------------------------->
    # -------------------------------------------------------------------------------->

    async def DeleteUserRPC(self, request, context):
        """
        Handles the DeleteUserRPC request.

        PARAMS:
        - request: gRPC request containing the CNIC of the user to be deleted.
        - context: gRPC context for the request.

        RETURNS:
        Deletes the user if found, else sets the context to NOT_FOUND.

        """

        logger.info(f"Received DeleteUserRPC request for CNIC: {request.cnic}")
        user = await User.find_one(User.cnic == request.cnic)
        if user:
            await user.delete()
            logger.info(f"User with CNIC {request.cnic} deleted")

            return user_pb2.DeleteUserResponse(
                message="User deleted successfully")
        else:
            context.set_details("User not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            logger.warning(f"User with CNIC {request.cnic} not found")

            return user_pb2.DeleteUserResponse(message="User not found")


async def serve():
    """
    Starts the gRPC server.
    """

    logger.info("Starting gRPC server")
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    logger.info("Server started, listening on port 50051")
    await server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    loop.run_until_complete(serve())
