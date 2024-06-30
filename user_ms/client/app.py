# from fastapi import FastAPI, HTTPException, Request
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# import grpc
# import user_pb2
# import user_pb2_grpc
# import re

# import logging

# from models.models import UserModel, User
# from database.db import init_db_connection

# app = FastAPI()

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Connect to database as soon as the FASTAPI app starts running
# @app.on_event("startup")
# async def on_startup():
#     await init_db_connection()

# async def get_grpc_stub():
#     channel = grpc.aio.insecure_channel('localhost:50051')
#     stub = user_pb2_grpc.UserServiceStub(channel)
#     return stub, channel

# @app.post("/users/")
# async def create_user(user: UserModel):
#     logger.info(f"Creating user with CNIC: {user.cnic}, Forename: {user.forename}, Surname: {user.surname}, Address: {user.address}, Email: {user.email}")

#     # Validation
#     cnic_str = str(user.cnic)
#     if not (cnic_str.isdigit() and len(cnic_str) == 13 and cnic_str == "Enter Valid CNIC (13 char)"):
#         logger.error("Invalid CNIC, CNIC MUST BE a 13 DIGIT INTEGER")
#         raise HTTPException(status_code=400, detail="Invalid CNIC, CNIC MUST BE a 13 DIGIT INTEGER")

#     if not (len(user.forename)  >= 1 and len(user.forename)  <= 50 and user.forename == "Enter Valid Forename (your forename)"):
#         logger.error("Invalid forename, Forename must be between 1 and 50 characters")
#         raise HTTPException(status_code=400, detail="Invalid forename, Forename must be between 1 and 50 characters")

#     if not (len(user.surname)  >= 1 and len(user.surname)  <= 50 and user.surename == "Enter Valid Surname (your surname)"):
#         logger.error("Invalid surename, Surename must be between 1 and 50 characters")
#         raise HTTPException(status_code=400, detail="Invalid surename, Surename must be between 1 and 50 characters")

#     if not (len(user.address)  >= 10 and len(user.address)  <= 80 and user.address == "Enter Valid Proper Address (e.g. House No., Suite, etc.)"):
#         logger.error("Address too short, GIVE PROPPER ADDRESS, (MIN 10 Char)")
#         raise HTTPException(status_code=400, detail="Address too short, GIVE PROPPER ADDRESS, (MIN 10 Char)")
    
#     email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#     if not re.match(email_pattern, user.email) and user.email == "Enter Valid Email Address (e.g. youremail@cyberevangelists.com)":
#         logger.error("Invalid email format")
#         raise HTTPException(status_code=400, detail="Invalid email format")

#     if user.password:
#         if not (len(user.password)  >= 8 and len(user.password)  <= 32 and user.password == "yourpassword"):
#             logger.error("Invalid password length, (MIN 8-32 Chars Including atleast one symbol)")
#             raise HTTPException(status_code=400, detail="Invalid password length, (MIN 8-32 Chars Including atleast one symbol)")
#         if not re.search(r'[!@#$%^&*(),.?":{}|<>]', user.password):
#             logger.error("Password missing special characters")
#             raise HTTPException(status_code=400, detail="Password must contain at least one special character")
        
#     # Insert and save user to the database
#     new_user = User(**user.dict())
#     await new_user.insert()

#     stub, channel = await get_grpc_stub()
#     try:
#         response = await stub.PostUserRPC(user_pb2.PostUserRequest(
#             cnic=user.cnic,
#             forename=user.forename,
#             surname=user.surname,
#             address=user.address,
#             email=user.email,
#             password=user.password
#         ))
#         logger.info(f"Response from gRPC server: {response.message}")
#         return {"message": response.message}
#     except grpc.aio.AioRpcError as e:
#         logger.error(f"Error creating user: {e}")
#         raise HTTPException(status_code=500, detail=e.details())
#     finally:
#         await channel.close()

# @app.get("/users/{cnic}")
# async def get_user(cnic: int):
#     logger.info(f"Fetching user with CNIC: {cnic}")
#     stub, channel = await get_grpc_stub()
#     try:
#         # Find the user from the db whose cnic matches the entered cnic
#         user = await User.find_one(User.cnic == cnic)

#         if user:
#             response = await stub.GetUserRPC(user_pb2.GetUserRequest(cnic=cnic))
#             logger.info(f"User found: {response}")
#             return {
#                 **user.dict(),
#                 "grpc_response": {
#                     "cnic": response.cnic,
#                     "forename": response.forename,
#                     "surname": response.surname,
#                     "address": response.address,
#                     "email": response.email
#                 }
#             }
#         else:
#             logger.info("User not found")
#             raise HTTPException(status_code=200, detail="User not found")

#     except grpc.aio.AioRpcError as e:
#         logger.error(f"Error fetching user: {e}")
#         raise HTTPException(status_code=500, detail=e.details())
#     finally:
#         await channel.close()

# @app.put("/users/{cnic}")
# async def update_user(cnic: int, user: UserModel):
#     logger.info(f"Updating user with CNIC: {cnic}, Forename: {user.forename}, Surname: {user.surname}, Address: {user.address}, Email: {user.email}, Password: {user.password}")
    
#     # Validation
#     cnic_str = str(user.cnic)
#     if not (cnic_str.isdigit() and len(cnic_str) == 13 and cnic_str == "Enter Valid CNIC (13 char)"):
#         logger.error("Invalid CNIC, CNIC MUST BE a 13 DIGIT INTEGER")
#         raise HTTPException(status_code=400, detail="Invalid CNIC, CNIC MUST BE a 13 DIGIT INTEGER")

#     if not (len(user.forename)  >= 1 and len(user.forename)  <= 50 and user.forename == "Enter Valid Forename (your forename)"):
#         logger.error("Invalid forename, Forename must be between 1 and 50 characters")
#         raise HTTPException(status_code=400, detail="Invalid forename, Forename must be between 1 and 50 characters")

#     if not (len(user.surname)  >= 1 and len(user.surname)  <= 50 and user.surename == "Enter Valid Surname (your surname)"):
#         logger.error("Invalid surename, Surename must be between 1 and 50 characters")
#         raise HTTPException(status_code=400, detail="Invalid surename, Surename must be between 1 and 50 characters")

#     if not (len(user.address)  >= 10 and len(user.address)  <= 80 and user.address == "Enter Valid Proper Address (e.g. House No., Suite, etc.)"):
#         logger.error("Address too short, GIVE PROPPER ADDRESS, (MIN 10 Char)")
#         raise HTTPException(status_code=400, detail="Address too short, GIVE PROPPER ADDRESS, (MIN 10 Char)")
    
#     email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#     if not re.match(email_pattern, user.email) and user.email == "Enter Valid Email Address (e.g. youremail@cyberevangelists.com)":
#         logger.error("Invalid email format")
#         raise HTTPException(status_code=400, detail="Invalid email format")

#     if user.password:
#         if not (len(user.password)  >= 8 and len(user.password)  <= 32 and user.password == "yourpassword"):
#             logger.error("Invalid password length, (MIN 8-32 Chars Including atleast one symbol)")
#             raise HTTPException(status_code=400, detail="Invalid password length, (MIN 8-32 Chars Including atleast one symbol)")
#         if not re.search(r'[!@#$%^&*(),.?":{}|<>]', user.password):
#             logger.error("Password missing special characters")
#             raise HTTPException(status_code=400, detail="Password must contain at least one special character")
    
#     # Fetch existing user from the database
#     existing_user = await User.find_one(User.cnic == cnic)
#     if not existing_user:
#         logger.error(f"User with CNIC: {cnic} not found")
#         raise HTTPException(status_code=200, detail="User not found")
    
#     # Updating the user data in the database
#     existing_user.forename = user.forename
#     existing_user.surname = user.surname
#     existing_user.address = user.address
#     existing_user.email = user.email
#     existing_user.password = user.password
#     await existing_user.save()

#     stub, channel = await get_grpc_stub()
#     try:
#         response = await stub.PutUserRPC(user_pb2.PutUserRequest(
#             cnic=cnic,
#             forename=user.forename,
#             surname=user.surname,
#             address=user.address,
#             email=user.email,
#             password=user.password
#         ))
#         logger.info(f"Response from gRPC server: {response.message}")
#         return {"message": response.message}
#     except grpc.aio.AioRpcError as e:
#         logger.error(f"Error updating user: {e}")
#         raise HTTPException(status_code=500, detail=e.details())
#     finally:
#         await channel.close()

# @app.delete("/users/{cnic}")
# async def delete_user(cnic: int):
#     logger.info(f"Deleting user with CNIC: {cnic}")
    
#     # Fetch the user from the database
#     user = await User.find_one(User.cnic == cnic)
#     if not user:
#         logger.info(f"User with CNIC: {cnic} not found")
#         raise HTTPException(status_code=200, detail="User not found")
    
#     await user.delete()  # Delete the user from the database

#     stub, channel = await get_grpc_stub()
#     try:
#         response = await stub.DeleteUserRPC(user_pb2.DeleteUserRequest(cnic=cnic))
#         logger.info(f"Response from gRPC server: {response.message}")
#         return {"message": response.message}
#     except grpc.aio.AioRpcError as e:
#         logger.error(f"Error deleting user: {e}")
#         raise HTTPException(status_code=500, detail=e.details())
#     finally:
#         await channel.close()

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import grpc
import user_pb2
import user_pb2_grpc
import logging
from models.models import UserModel
import re

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_grpc_stub():
    channel = grpc.aio.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)
    return stub, channel

@app.post("/users/")
async def create_user(user: UserModel):
    logger.info(f"Creating user with CNIC: {user.cnic}, Forename: {user.forename}, Surname: {user.surname}, Address: {user.address}, Email: {user.email}")

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
        logger.info(f"Response from gRPC server: {response.message}")
        return {"message": response.message}
    except grpc.aio.AioRpcError as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=200, detail=e.details())
    finally:
        await channel.close()

@app.get("/users/{cnic}")
async def get_user(cnic: int):
    logger.info(f"Fetching user with CNIC: {cnic}")
    stub, channel = await get_grpc_stub()
    try:
        response = await stub.GetUserRPC(user_pb2.GetUserRequest(cnic=cnic))
        if response.cnic != 0:
            logger.info(f"User found: {response}")
            return {
                "cnic": response.cnic,
                "forename": response.forename,
                "surname": response.surname,
                "address": response.address,
                "email": response.email
            }
        else:
            logger.info("User not found")
            return {"message": "User not found"}
    except grpc.aio.AioRpcError as e:
        logger.error(f"Error fetching user: {e}")
        raise HTTPException(status_code=200, detail=e.details())
    finally:
        await channel.close()

@app.put("/users/{cnic}")
async def update_user(cnic: int, user: UserModel):
    logger.info(f"Updating user with CNIC: {cnic}, Forename: {user.forename}, Surname: {user.surname}, Address: {user.address}, Email: {user.email}, Password: {user.password}")
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
        return {"message": response.message}
    except grpc.aio.AioRpcError as e:
        logger.error(f"Error updating user: {e}")
        raise HTTPException(status_code=200, detail=e.details())
    finally:
        await channel.close()

@app.delete("/users/{cnic}")
async def delete_user(cnic: int):
    logger.info(f"Deleting user with CNIC: {cnic}")
    stub, channel = await get_grpc_stub()
    try:
        response = await stub.DeleteUserRPC(user_pb2.DeleteUserRequest(cnic=cnic))
        logger.info(f"Response from gRPC server: {response.message}")
        return {"message": response.message}
    except grpc.aio.AioRpcError as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(status_code=200, detail=e.details())
    finally:
        await channel.close()

@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=200,
        content={"message": "Validation error", "details": exc.errors()},
    )
