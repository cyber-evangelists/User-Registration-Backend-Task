from models import UserModel, UserUpdateModel

from auth_handler import sign_jwt, decode_jwt
from auth_bearer import JWTBearer

from fastapi import WebSocket, WebSocketDisconnect
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse

import grpc
import user_pb2
import user_pb2_grpc

import re
import logging
from typing import List


app = FastAPI(
    # swagger_ui_parameters={"syntaxHighlight": False},  # Not needed in our case as i want syntax highlighting
    title="NADRA User Registration Portal",
    description="A FastAPI CRUD application for managing NADRA user registrations with proper user authentication and data storage in mongoDB.",
    version="1.0.0",
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Implemented websockets class


class ConnectionManager:

    """
    Manages WebSocket connections for broadcasting messages.
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Accepts a new WebSocket connection.

        """

        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Removes a WebSocket connection.
        """

        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """
        Sends a personal message to a specific WebSocket connection.
        """

        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """
        Broadcasts a message to all active WebSocket connections.
        """

        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


async def get_grpc_stub():
    """
    Creates and returns a gRPC stub for communicating with the user service/server.
    """

    channel = grpc.aio.insecure_channel('server:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)
    return stub, channel


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    """
    WebSocket endpoint for real-time communication.
    """

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Message text was: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


@app.get("/")
async def read_root() -> dict:
    """
    Root endpoint.
    Returns: **A welcome message**.
    """
    return {"message": "Welcome to NADRA User Registration Portal!"}

# -------------------------------------------------------------------------------->
# CREATE ------------------------------------------------------------------------->
# -------------------------------------------------------------------------------->


@app.post("/users/")
async def create_user(user: UserModel):
    """
    Creates a new user.

    PARAMS:
    - **user**: The user details.

    RETURNS:
    - **Response Message of user created or not**
    """

    logger.info(
        f"Creating user with CNIC: {user.cnic}, Forename: {user.forename}, Surname: {user.surname}, Address: {user.address}, Email: {user.email}")

    # Validations

    if not (isinstance(user.cnic, int) and len(str(user.cnic)) == 13):
        logger.error("Invalid CNIC, CNIC must be a 13-digit integer")
        raise HTTPException(
            status_code=400, detail="Invalid CNIC, CNIC must be a 13-digit integer")

    if user.forename is not None and not (1 <= len(user.forename) <= 50):
        logger.error(
            "Invalid forename, Forename must be between 1 and 50 characters")
        raise HTTPException(
            status_code=400, detail="Invalid forename, Forename must be between 1 and 50 characters")

    if user.surname is not None and not (1 <= len(user.surname) <= 50):
        logger.error(
            "Invalid surname, Surname must be between 1 and 50 characters")
        raise HTTPException(
            status_code=400, detail="Invalid surname, Surname must be between 1 and 50 characters")

    if user.address is not None and not (10 <= len(user.address) <= 80):
        logger.error(
            "Invalid address length, Address must be between 10 and 80 characters")
        raise HTTPException(
            status_code=400, detail="Invalid address length, Address must be between 10 and 80 characters")

    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_pattern, user.email):
        logger.error("Invalid email format")
        raise HTTPException(status_code=400, detail="Invalid email format")

    if user.password is not None:
        if not (8 <= len(user.password) <= 32):
            logger.error(
                "Invalid password length, Password must be between 8 and 32 characters")
            raise HTTPException(
                status_code=400, detail="Invalid password length, Password must be between 8 and 32 characters")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', user.password):
            logger.error("Password missing special characters")
            raise HTTPException(
                status_code=400, detail="Password must contain at least one special character")

    # If all validations pass, proceed with gRPC call
    stub, channel = await get_grpc_stub()
    try:
        response = await stub.PostUserRPC(user_pb2.PostUserRequest(
            cnic=user.cnic,
            forename=user.forename,
            surname=user.surname,
            address=user.address,
            email=user.email,
            password=user.password
        ))

        token = sign_jwt(user.cnic)  # Token generated

        logger.info(f"Response from gRPC server: {response.message}")

        # Broadcast message via WebSocket
        await manager.broadcast(f"New user created: {user.forename} {user.surname}")

        return {"message": response.message, "token": token}
    except grpc.aio.AioRpcError as e:
        logger.error(f"Error creating user via gRPC: {e}")
        raise HTTPException(status_code=500, detail=e.details())
    finally:
        await channel.close()

# ------------------------------------------------------------------------------>
# READ ------------------------------------------------------------------------->
# ------------------------------------------------------------------------------>


@app.get("/users/{cnic}", dependencies=[Depends(JWTBearer())])
async def get_user(cnic: int, token: str = Depends(JWTBearer())):
    """
    Retrieves a user by CNIC.

    PARAMS:
    - **cnic**: The CNIC of the user.
    - **token**: JWT token for authentication.

    RETURNS:
    - **Response Message of user retrieved or not authenticated**
    """

    logger.info(f"Fetching user with CNIC: {cnic}")

    # Decode the JWT token
    decoded_token = decode_jwt(token)
    if decoded_token["cnic"] != cnic:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    stub, channel = await get_grpc_stub()
    try:
        response = await stub.GetUserRPC(user_pb2.GetUserRequest(cnic=cnic))
        if response.cnic != 0:
            logger.info(f"User found: {response}")

            # Broadcast message via WebSocket
            await manager.broadcast(f"User found")

            return {
                "cnic": response.cnic,
                "forename": response.forename,
                "surname": response.surname,
                "address": response.address,
                "email": response.email
            }
        else:
            logger.info("User not found")

            # Broadcast message via WebSocket
            await manager.broadcast(f"User Not found")

            return {"message": "User not found"}

    except grpc.aio.AioRpcError as e:
        logger.error(f"Error fetching user: {e}")
        raise HTTPException(status_code=500, detail=e.details())
    finally:
        await channel.close()

# -------------------------------------------------------------------------------->
# UPDATE ------------------------------------------------------------------------->
# -------------------------------------------------------------------------------->


@app.put("/users/{cnic}", dependencies=[Depends(JWTBearer())])
async def update_user(cnic: int, user: UserUpdateModel,
                      token: str = Depends(JWTBearer())):
    """
    Updates a user by CNIC.

    PARAMS:
    - **cnic**: The CNIC of the user.
    - **user**: The updated user details.
    - **token**: JWT token for authentication.

    RETURNS:
    - **Response Message of user updated, not found or not authenticated**
    """

    logger.info(
        f"Updating user with CNIC: {cnic}, Forename: {user.forename}, Surname: {user.surname}, Address: {user.address}, Email: {user.email}")

    # Decode the JWT token
    decoded_token = decode_jwt(token)
    if decoded_token.get("cnic") != cnic:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    if user.forename is not None and not (1 <= len(user.forename) <= 50):
        logger.error(
            "Invalid forename, Forename must be between 1 and 50 characters")
        raise HTTPException(
            status_code=400, detail="Invalid forename, Forename must be between 1 and 50 characters")

    if user.surname is not None and not (1 <= len(user.surname) <= 50):
        logger.error(
            "Invalid surname, Surname must be between 1 and 50 characters")
        raise HTTPException(
            status_code=400, detail="Invalid surname, Surname must be between 1 and 50 characters")

    if user.address is not None and not (10 <= len(user.address) <= 80):
        logger.error(
            "Invalid address length, Address must be between 10 and 80 characters")
        raise HTTPException(
            status_code=400, detail="Invalid address length, Address must be between 10 and 80 characters")

    if user.email is not None:
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, user.email):
            logger.error("Invalid email format")
            raise HTTPException(status_code=400, detail="Invalid email format")

    if user.password is not None:
        if not (8 <= len(user.password) <= 32):
            logger.error(
                "Invalid password length, Password must be between 8 and 32 characters")
            raise HTTPException(
                status_code=400, detail="Invalid password length, Password must be between 8 and 32 characters")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', user.password):
            logger.error("Password missing special characters")
            raise HTTPException(
                status_code=400, detail="Password must contain at least one special character")

    # If all validations pass, proceed with gRPC call
    stub, channel = await get_grpc_stub()
    try:
        response = await stub.PutUserRPC(user_pb2.PutUserRequest(
            cnic=cnic,
            forename=user.forename,
            surname=user.surname,
            address=user.address,
            email=user.email,
            password=user.password
        ))
        logger.info(f"Response from gRPC server: {response.message}")

        # Broadcast message via WebSocket
        await manager.broadcast(f"User Updated: {user.forename} {user.surname}")

        return {"message": response.message}

    except grpc.aio.AioRpcError as e:
        logger.error(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail=e.details())
    finally:
        await channel.close()

# -------------------------------------------------------------------------------->
# DELETE ------------------------------------------------------------------------->
# -------------------------------------------------------------------------------->


@app.delete("/users/{cnic}", dependencies=[Depends(JWTBearer())])
async def delete_user(cnic: int, token: str = Depends(JWTBearer())):
    """
    Deletes a user by CNIC.

    PARAMS:
    - **cnic**: The CNIC of the user.
    - **token**: JWT token for authentication.

    RETURNS:
    - **Response Message of user deleted, not found or not authenticated**
    """

    logger.info(f"Deleting user with CNIC: {cnic}")

    # Decode the JWT token
    decoded_token = decode_jwt(token)
    if decoded_token.get("cnic") != cnic:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    stub, channel = await get_grpc_stub()
    try:
        response = await stub.DeleteUserRPC(user_pb2.DeleteUserRequest(cnic=cnic))
        logger.info(f"Response from gRPC server: {response.message}")

        # Broadcast message via WebSocket
        await manager.broadcast(f"User Deleted")

        return {"message": response.message}
    except grpc.aio.AioRpcError as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail=e.details())
    finally:
        await channel.close()


@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    """
    Handles validation exceptions.
    """

    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "details": exc.errors()},
    )
