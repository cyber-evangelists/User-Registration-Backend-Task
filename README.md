# NADRA-User-Registration 🪪

This project demonstrates a FastAPI application using Beanie ODM (Object Document Mapper) for MongoDB. The project is containerized using Docker and Docker Compose for easy setup and deployment. [Its also deployed on Docker-Hub](https://hub.docker.com/r/saadarazzaq/nadra-user-registration-api) 🐳🙂

## Project Demonstration 📹

[![Product Reviews API](https://github.com/SaadARazzaq/Product-Reviews-API/assets/123338307/7960274c-5ac1-4726-96d2-367c99bf0896)](https://www.loom.com/share/aab52275625246529cbf4de2c00d6402?sid=a43c4124-d721-4e33-a045-93947a31368b)

## FlowChart of Microservices:

<img width="1140" alt="Screenshot 2024-06-30 at 5 42 59 PM" src="https://github.com/cyber-evangelists/NADRA-User-Registration-Backend-Task/assets/173667240/ce831755-7877-4b8f-82ae-019863696904">


## Project Structure 🧱

<img width="275" alt="Screenshot 2024-06-30 at 5 00 35 PM" src="https://github.com/cyber-evangelists/NADRA-User-Registration-Backend-Task/assets/173667240/6b9e7931-eb2f-4a4f-9377-fb0dc5f292b0">

- **protos/user.proto**: Defines the overall structure of the app schema and functionalities in a `universal syntax`. Its the very first step when working with grpcs. After defining the user.proto file, run the command (given in user.proto file) in the terminal to generate compiler constructed `user_pb2.py` and `user_pb2_grpc.py` files.
- **routes/auth_handler.py**: Defines the `encoding` and `decoding` of `JWT Tokens`.
- **routes/auth_bearer.py**: Defines the `JWT_Bearer` Class and verifies `JWT Tokens`.
- **routes/app.py**: Contains the `API end points`, `JWT Authentication`, and proper `API Validations` for handling User APIS.
- **server/models.py**: Defines the `User` and `UserModel` and `UserUpdateModel` models using `Beanie` and `Pydantic`.
- **app/server/db.py**: Contains the `database initialization logic`.
- **server/app.py**: Contains the `gRPC calls`, `DB initiallization on startup`, and `User Data storage in DB` from the endpoints.
- **main.py**: The entry point for running the `Uvicorn server`.
- **Dockerfile**: The `Dockerfile` for building the routes/server images.
- **docker-compose.yml**: `Docker Compose file` for setting up the `FastAPI` and `MongoDB services`.
- **requirements.txt**: Python dependencies required for the project.

**Note: Most of the files are redundant and not defined explicitly above e.g. routes/models.py is not defined above as same file with same code is present in the server/models.py**

## Features Loaded ⚙️

1. User Registration CRUD Operations:
• Create new user registration.
• Read user information.
• Update user information.
• Delete user registration.

2. JWT Authentication:
- Implemented secure JWT authentication for user login and access control.

3. Database Integration:
- Used Beanie (MongoDB ODM) to store and manage user information.

4. Dockerization:
- Containerized the application using Docker for easy deployment and scalability. [Its also deployed on Docker-Hub](https://hub.docker.com/r/saadarazzaq/nadra-user-registration-api) 🐳🙂

5. Swagger Documentation:
- Provided comprehensive Swagger documentation for the API.

6. PEP8 Standards of code:
- Followed PEP8 Standards of Python syntax

## Major Tasks Performed: 🛠️

1. Setup FastAPI Project:
- Initialized a new FastAPI project.
- Configured the project structure for microservices.

2. User Registration CRUD Endpoints:
- Implemented endpoints for creating, reading, updating, and deleting user registrations.
- Ensured validation and error handling.

3. JWT Authentication:
- Implemented JWT authentication for secure access.
- Created login and token generation endpoints.
- Secured CRUD endpoints using JWT authentication.
  
4. Database Configuration:
- Setup MongoDB connection.
- Created pydantic models and schemas for user information.
- Integrated MongoDB with FastAPI for data operations.
  
5. Dockerization:
- Created Dockerfile for the FastAPI application.
- Setup Docker Compose for multi-container setup (including MongoDB).

6. Swagger Documentation:
- Added Swagger documentation for all the endpoints.
- Ensured all routes, models, and authentication are properly documented.

7. Code Structure:
- Ensured modularity while coding.
- Followed PEP8 standards of coding throughout the project.

## Getting Started 🏃

### Prerequisites 📋

- `Docker Desktop` installed and up and running on your machine.

### Installation 🛠️

1. Clone the repository:

    ```sh
    git clone https://github.com/cyber-evangelists/NADRA-User-Registration-Backend-Task/new/main?filename=README.md
    cd project-dir
    ```

2. Build and start the Docker containers:

    ```sh
    docker-compose up --build
    ```

3. The FastAPI application will be available at `http://localhost:8000`.
   

### API Endpoints ⚡

<img width="748" alt="Screenshot 2024-06-30 at 5 29 10 PM" src="https://github.com/cyber-evangelists/NADRA-User-Registration-Backend-Task/assets/173667240/fbf20811-3bda-44df-8a69-d491bcc6bae6">

<img width="730" alt="Screenshot 2024-06-30 at 5 31 39 PM" src="https://github.com/cyber-evangelists/NADRA-User-Registration-Backend-Task/assets/173667240/1edaeb14-863f-4e8e-a559-5688b1432279">

<img width="727" alt="Screenshot 2024-06-30 at 5 32 14 PM" src="https://github.com/cyber-evangelists/NADRA-User-Registration-Backend-Task/assets/173667240/599103d1-c19e-47c1-887e-a867e8c5ed3a">

<img width="735" alt="Screenshot 2024-06-30 at 5 32 40 PM" src="https://github.com/cyber-evangelists/NADRA-User-Registration-Backend-Task/assets/173667240/9d65be82-d4d0-427d-a46c-60d32c4a7864">

<img width="729" alt="Screenshot 2024-06-30 at 5 33 06 PM" src="https://github.com/cyber-evangelists/NADRA-User-Registration-Backend-Task/assets/173667240/0755b766-590e-4e81-84c6-cc8822714162">

<img width="344" alt="Screenshot 2024-06-30 at 5 50 27 PM" src="https://github.com/cyber-evangelists/NADRA-User-Registration-Backend-Task/assets/173667240/f473ab63-d9ed-462b-b18e-b375d3391d5e">

### Model Schemas 🧩

<img width="1157" alt="Screenshot 2024-06-30 at 5 26 26 PM" src="https://github.com/cyber-evangelists/NADRA-User-Registration-Backend-Task/assets/173667240/da0c7def-e27a-4eb7-a628-aa469d29f012">

### Notes 📒

- Ensure MongoDB is running and accessible for the FastAPI application to function correctly.
- The mongo_url in server/db.py is set to connect to a MongoDB instance at host.docker.internal.

---

```bash
This project was made with 💖 by Saad Abdur Razzaq under the supervision of Sir Husnain
```
