# FastAPI E-Commerce Application

This is a modular e-commerce backend API built with **FastAPI**. The project includes authentication, account management, product management, cart functionality, and user management. The codebase is organized into distinct modules for better scalability and maintainability.

---

## Features

- **Authentication Module**  
  Handles user registration, login, password hashing, and token-based authentication.

- **Users Module**  
  Manages user information and CRUD operations for users.

- **Account Module**  
  Provides functionalities for managing user account details, including updates and preferences.

- **Product Module**  
  Handles product creation, retrieval, and management, including categories.

- **Cart Module**  
  Manages cart functionalities such as adding, removing, and viewing items.

---

## Project Structure

The application is divided into distinct modules for better organization:

```plaintext
project/
│
├── core/                 # Core configurations and settings
│   ├── config.py         # Application configuration settings
│   ├── database.py       # Database configurations and connection
│   ├── security.py       # Security utilities (e.g., hashing, token handling)
│
├── models/               # Database models
│   ├── user.py           # User models
│   ├── product.py        # Product models
│   ├── cart.py           # Cart models
│   └── __init__.py       # Model initialization
│
├── routers/              # API endpoints
│   ├── auth.py           # Authentication routes
│   ├── users.py          # User routes
│   ├── products.py       # Product routes
│   ├── cart.py           # Cart routes
│   └── __init__.py       # Router initialization
│
├── schemas/              # Pydantic schemas for validation
│   ├── auth.py           # Schemas for authentication requests/responses
│   ├── user.py           # Schemas for user data
│   ├── product.py        # Schemas for products
│   ├── cart.py           # Schemas for cart data
│   └── __init__.py       # Schema initialization
│
├── services/             # Business logic
│   ├── auth_service.py   # Logic for authentication
│   ├── user_service.py   # Logic for user management
│   ├── product_service.py# Logic for product management
│   ├── cart_service.py   # Logic for cart operations
│   └── __init__.py       # Service initialization
│
├── utils/                # Utility functions
│   ├── response.py       # Standard response formatting
│   └── __init__.py       # Utility initialization
│
├── tests/                # Test cases
│   ├── test_auth.py      # Test cases for authentication
│   ├── test_users.py     # Test cases for users
│   ├── test_products.py  # Test cases for products
│   ├── test_cart.py      # Test cases for cart
│   └── __init__.py       # Test initialization
│
├── main.py               # Application entry point
├── requirements.txt      # Dependencies
└── README.md             # Project documentation
```

---

## Setup Instructions

### Prerequisites

- Python 3.10 or above
- PostgreSQL installed and running

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yvesHakizimana/fastApi-Ecommerce.git
   cd fastApi-Ecommerce
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the root directory and add the following:
   ```dotenv
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Apply database migrations:
   ```bash
   alembic upgrade head
   ```

6. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

### Access the API

- API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)  
- Alternate Documentation: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) (ReDoc)

---

## Utilities

- **Standardized Responses**:  
  Custom responses are implemented in `utils/response.py` to ensure consistent API response formatting.

---

## Future Enhancements

- Implement order management
- Integrate payment gateways
- Add analytics and reporting

---

## Contributing

Contributions are welcome! Please follow the steps below:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License.

---

With this README file, you provide detailed and structured documentation for your project, helping other developers quickly understand and set up the application.
