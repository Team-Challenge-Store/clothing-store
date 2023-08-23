# Clothing Store API Documentation

Welcome to the documentation for the Clothing Store API. This API provides functionalities for user registration and authentication within the context of a clothing store application.

## Base URL

The base URL for the API is: `https://molfaryura.pythonanywhere.com/`

## Authentication

The API does not require authentication for user registration.

## Endpoints

### Register User

- **URL:** `/register`
- **Method:** POST
- **Description:** Register a new user account.
- **Request Body:**
  ```json
  {
    "username": "string (1-100 characters)",
    "email": "valid-email@example.com",
    "password": "string (8+ characters with at least one uppercase, one lowercase, one number, and one special symbol)",
    "repeat_password": "same-as-password"
  }
  ```
- **Response:**

  - **Success (HTTP 201):**
    ```json
    {
      "message": "User registered successfully",
      "username": "username",
      "email": "user@example.com"
    }
    ```
  - **Error (HTTP 400):**
    ```json
    {
      "error": "Description of the error"
    }
    ```
  - **Server Error (HTTP 500):**
    ```json
    {
      "error": "An unexpected error occurred"
    }
    ```
    ```json
    {
      "error": "DatabaseError"
    }
    ```

## Notes

- Ensure that you are sending valid JSON data in the request body.
- Password must meet the specified complexity requirements.
- Username and email must meet specified validation criteria.
