## Project Overview

This project is an **e-commerce platform** designed with scalability, maintainability, and modularity in mind. It leverages **Hexagonal Architecture** to ensure a clean separation of concerns and adopts **Aspect-Oriented Programming** principles for managing cross-cutting concerns efficiently.

The platform incorporates modern best practices, such as the use of `Optional` to eliminate null references and `Result` to handle operation outcomes consistently. These choices contribute to a robust and developer-friendly codebase, facilitating future enhancements and reducing technical debt.

## Hexagonal Architecture

This project follows the **Hexagonal Architecture** (also known as Ports and Adapters Architecture) for the construction of each microservice. This approach promotes a decoupled design, ensuring that business logic is isolated from external dependencies such as databases, APIs, or frameworks.

### Key Principles:
- **Framework Independence**: Business logic does not depend on any specific framework.
- **Ease of Testing**: Use cases and core logic can be tested without relying on external infrastructure.
- **Adaptability**: It is straightforward to switch external dependencies (e.g., migrating from an SQL database to a NoSQL database).

### Application in the Project:
- **Domain Layer**: Contains the core business logic and use cases.
- **Application Layer**: Coordinates use cases and acts as an intermediary between the domain layer and external interfaces. This layer manages application services and orchestrates operations.
- **Infrastructure Layer**: Contains concrete implementations of external dependencies such as databases, external APIs, and specific adapters. This layer directly interacts with external frameworks and libraries.
- **Ports**: Interfaces defining how external layers interact with business logic.
- **Adapters**: Concrete implementations of ports, such as HTTP controllers, database repositories, or external API integrations.

This architecture ensures that microservices are highly maintainable, scalable, and easy to extend.

## Aspect-Oriented Programming and Best Practices

In addition to the hexagonal architecture, this project follows **Aspect-Oriented Programming** principles to handle cross-cutting concerns such as logging, exception handling, service performance, and more. This approach helps maintain clean and modular code.

### Best Practices Implemented:
- **Use of Optional**: To avoid null values and explicitly handle the absence of data.
- **Use of Result**: To clearly represent the success or failure of operations, improving readability and error handling.

These practices ensure more robust, readable, and maintainable code.

## Installation
### Prerequisites
- Python 3.12
- Docker and Docker Compose

### Steps for local environment (specific microservice)
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   cd apps/microservice-name
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   # Linux:
   source env/bin/activate
   # Windows:
   .\env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environments:
   - Update the `.env` file with your credentials.
   - Use .env.example to fill all the environments variables
5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Access the API documentation at: `http://127.0.0.1:8000/docs`

### Docker Setup (all components)
1. Update the `.env` file with the corresponding variables
2. Build and run the application using Docker Compose:
   ```bash
   docker-compose up --build

### Docker Setup (specific microservice)
1. (root project) cd apps/microservice-name
2. Update the `.env` file with the corresponding variables
3. Build and run the application using Docker Compose:
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```
4. Access the API documentation at: `http://127.0.0.1:{PORT}/docs`

### Testing (specific microservice)
1. (root project) cd apps/microservice-name
2. Update the `.env` file with the corresponding variables
3. Build and run the application using Docker Compose:
   ```bash
   docker-compose -f docker-compose.test.yml up --build
   ```

## API Endpoints
### User Module
- `GET /users/client/{id}`: Find client by id
- `PATCH /users/client/{id}`: Modify a client
- `PATCH /users/manager/{id}`: Modify a manager
- `GET /users/manager/{id}`: Find manager by id
- `GET /users/manager/all`: Get all managers
- `GET /users/client/me`: Get client info
  
### Auth Module
- `POST /auth/sign_up`: Register user
- `POST /auth/log_in`: Log in a user
- `POST /auth/create_manager`: Creata a manager
- `POST /auth/create_superadmin`: Create superadmin (initial setup)

### Product Module
- `GET /products`: Get all products
- `GET /products/{product_id}`: Get product by id
- `POST /products`: Create a product
- `PUT /products`: Update product data
- `DELETE /products`: Delete product data

### Inventory Module
- `GET /inventories/{product_id}`: Get product inventory
- `PUT /inventories/{product_id}`: Update inventory

### Cart Module
- `POST /cart/add_product`: Add a product to the cart
- `POST /cart/add_one`: Add one to a product in the cart
- `POST /cart/remove_one`: Remove one to a product in the cart
- `POST /cart/add_product`: Add a product to the cart
- `GET /cart/`: Get the cart

### Order Module
- `POST /orders/create`: Create an order
- `PUT /orders/cancel`: Cancel an order
- `PUT /orders/complete`: Complete an order
- `GET /orders/all/`: Get all orders
- `GET /orders/one/`: Get an order


### Report Module
- `GET /reports/sales/total/`: Get the total amount of sales
- `GET /reports/sales/{product_id}/`: Get the total amount of sales by a product
- `GET /reports/profit/total/`: Get the total amount of profit
- `GET /reports/products/top/`: Get the top ten most saled products
- `GET /reports/customer/top/`: Get the top ten customers with more money spent

## Business Rules
1. Users can only perform actions allowed by their roles.
2. Products can only be added to the cart if stock is available.
3. Passwords must be encrypted.
4. All endpoints are asynchronous.
