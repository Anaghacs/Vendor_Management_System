Vendor Management System API Documentation:

Welcome to the manual documentation for the Vendor Management System API. This document provides detailed information about the API endpoints, request and response formats, authentication methods, and usage examples.


We have also implemented an interactive Swagger API documentation for the Vendor Management System API. You can access it by visiting the following URL:
[Swagger API Documentation](http://127.0.0.1:8000/api/docs/)

The Swagger documentation provides an interactive interface for exploring and testing the API endpoints. Feel free to use it alongside this manual documentation for a comprehensive understanding of the API.


Overview:
The Vendor Management System API allows you to manage vendors, track purchase orders, and calculate vendor performance metrics. Below is a summary of the available endpoints:

/api/token/: JWT access token.
/api/refresh/token/: JWT refresh token.
/api/vendors/: Manage vendor profiles.
/api/purchase_orders/: Manage purchase orders.
/api/purchase_orders/{po_id}/acknowledge/: Acknowledge a purchase order by the vendor.
/api/vendors/{vendor_id}/performance/: Retrieve vendor performance metrics.

JWT Authentication:
To access protected endpoints in the Vendor Management System API, you need to include a JWT access token in the authorization header of your requests. Follow the steps below to obtain and include the token:

1) Obtain Access Token:
    Endpoint: POST /api/token/
    Description: Retrieve a JWT access token by providing valid credentials.
    Parameters:
        username (string): User's username.
        password (string): User's password.
    Example Request Body:
        {
            "username": "example_user",
            "password": "example_password"
        }
    Example Response (Success):
        {
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
        }
    Include Token in Requests:
        Add the obtained access token to the authorization header of subsequent requests.
        Example:
            Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

### Error Handling:
The Vendor Management System API follows standard HTTP status codes to indicate the success or failure of requests. Below are some common error responses that users might encounter:

- **400 Bad Request:** Indicates that the request was malformed or contained invalid parameters.
- **401 Unauthorized:** Indicates that the request requires authentication but no valid credentials were provided.
- **403 Forbidden:** Indicates that the server understood the request but refuses to authorize it.
- **404 Not Found:** Indicates that the requested resource could not be found.
- **500 Internal Server Error:** Indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.

Each error response may include additional information in the response body to provide more context about the error.

2) Vendor Endpoints:

    1) List Vendors:
        Endpoint: GET /api/vendors/
        Description: Retrieve a list of all vendors.
        Response: Status Code: 200 (OK)
        Content-Type: application/json
        Body:
            [
        {
            "id": 1,
            "name": "Vendor A",
            "contact_details": "Contact A",
            "address": "Address A",
            "vendor_code": "A123",
            "on_time_delivery_rate": 90.0,
            "quality_rating_avg": 4.5,
            "average_response_time": 2.5,
            "fulfillment_rate": 95.0
        },
        {
            "id": 2,
            "name": "Vendor B",
            "contact_details": "Contact B",
            "address": "Address B",
            "vendor_code": "B456",
            "on_time_delivery_rate": 85.0,
            "quality_rating_avg": 4.2,
            "average_response_time": 3.0,
            "fulfillment_rate": 92.0
        }
    ]
    2) Create Vendor:
        Endpoint: POST /api/vendors/
        Description: Create a new vendor.
        Parameters:
            name (string): Vendor's name.
            contact_details (string): Contact information of the vendor.
            address (string): Physical address of the vendor.
            vendor_code (string): A unique identifier for the vendor.
        
        Example Request Body:
            {
                "name": "New Vendor",
                "contact_details": "New Contact",
                "address": "New Address",
                "vendor_code": "NV123"
            }
        Response:
            Status Code: 201 (Created)
            Content-Type: application/json
            Body:
                {
                    "id": 3,
                    "name": "New Vendor",
                    "contact_details": "New Contact",
                    "address": "New Address",
                    "vendor_code": "NV123",
                    "on_time_delivery_rate": 0.0,
                    "quality_rating_avg": 0.0,
                    "average_response_time": 0.0,
                    "fulfillment_rate": 0.0
                }
    3) Retrieve Vendor:
        Endpoint: GET /api/vendors/{vendor_id}/
        Description: Retrieve details of a specific vendor.
        Parameters:
            vendor_id (integer): Unique identifier of the vendor.
        Example:
        Request: GET /api/vendors/1/
        Response:
            {
                "id": 1,
                "name": "Vendor A",
                "contact_details": "Contact A",
                "address": "Address A",
                "vendor_code": "A123",
                "on_time_delivery_rate": 90.0,
                "quality_rating_avg": 4.5,
                "average_response_time": 2.5,
                "fulfillment_rate": 95.0
            }
    4) Update Vendor:
        Endpoint: PUT /api/vendors/{vendor_id}/
        Description: Update details of a specific vendor.
        Parameters:
            vendor_id (integer): Unique identifier of the vendor.
        Example Request Body:
            {
                "name": "Updated Vendor A",
                "contact_details": "Updated Contact A",
                "address": "Updated Address A",
                "vendor_code": "UA123"
            }
        Example:
            Request: PUT /api/vendors/1/
            Response:
                {
                    "id": 1,
                    "name": "Updated Vendor A",
                    "contact_details": "Updated Contact A",
                    "address": "Updated Address A",
                    "vendor_code": "UA123",
                    "on_time_delivery_rate": 90.0,
                    "quality_rating_avg": 4.5,
                    "average_response_time": 2.5,
                    "fulfillment_rate": 95.0
                }
    5) Delete Vendor:
        Endpoint: DELETE /api/vendors/{vendor_id}/
        Description: Delete a specific vendor.
        Parameters:
            vendor_id (integer): Unique identifier of the vendor.
        Example:
            Request: DELETE /api/vendors/1/
            Response:
                Status Code: 204 (No Content)            
        
3) Purchase Order Endpoints:

    1) Create Purchase Order:
        Endpoint: POST /api/purchase_orders/
        Description: Create a new purchase order.
        Parameters:
            po_number (string): Purchase Order number (unique).
            vendor (integer): ID of the vendor associated with the purchase order.
            order_date (datetime, optional): Date of the purchase order (default: current date and time).
            delivery_date (datetime, optional): Date of expected delivery.
            items (list): List of items included in the purchase order.
            quantity (integer): Quantity of items.
            status (string): Status of the purchase order (default: 'pending').
            quality_rating (float, optional): Quality rating for the purchase order.
            acknowledgment_date (datetime, optional): Date when the purchase order was acknowledged.
        Example Request Body:
            {
                "po_number": "PO123",
                "vendor": 1,
                "order_date": "2024-05-01T08:00:00Z",
                "delivery_date": "2024-05-10T08:00:00Z",
                "items": [
                    {
                        "name": "Item A",
                        "description": "Description of Item A",
                        "unit_price": 10.00,
                        "quantity": 5
                    },
                    {
                        "name": "Item B",
                        "description": "Description of Item B",
                        "unit_price": 20.00,
                        "quantity": 3
                    }
                ],
                "quantity": 8,
                "status": "pending",
                "quality_rating": 4.5,
                "acknowledgment_date": "2024-05-02T08:00:00Z"
            }
        Response:
            Status Code: 201 (Created)
            Content-Type: application/json
            Body:    
                {
                    "id": 1,
                    "po_number": "PO123",
                    "vendor": 1,
                    "order_date": "2024-05-01T08:00:00Z",
                    "delivery_date": "2024-05-10T08:00:00Z",
                    "items": [
                        {
                            "name": "Item A",
                            "description": "Description of Item A",
                            "unit_price": 10.00,
                            "quantity": 5
                        },
                        {
                            "name": "Item B",
                            "description": "Description of Item B",
                            "unit_price": 20.00,
                            "quantity": 3
                        }
                    ],
                    "quantity": 8,
                    "status": "pending",
                    "quality_rating": 4.5,
                    "acknowledgment_date": "2024-05-02T08:00:00Z"
                }
    2) List Purchase Orders:
        Endpoint: GET /api/purchase_orders/
        Description: Retrieve a list of all purchase orders with an option to filter by vendor.
        Parameters:
            vendor (integer, optional): ID of the vendor to filter purchase orders.
        Example:
            Request: GET /api/purchase_orders/
            Response:   
                {
                    "id": 1,
                    "po_number": "PO123",
                    "vendor": 1,
                    "order_date": "2024-05-01T08:00:00Z",
                    "delivery_date": "2024-05-10T08:00:00Z",
                    "items": [
                        {
                            "name": "Item A",
                            "description": "Description of Item A",
                            "unit_price": 10.00,
                            "quantity": 5
                        },
                        {
                            "name": "Item B",
                            "description": "Description of Item B",
                            "unit_price": 20.00,
                            "quantity": 3
                        }
                    ],
                    "quantity": 8,
                    "status": "pending",
                    "quality_rating": 4.5,
                    "acknowledgment_date": "2024-05-02T08:00:00Z"
                }
    3) Retrieve Purchase Order:
        Endpoint: GET /api/purchase_orders/{po_id}/
        Description: Retrieve details of a specific purchase order.
        Parameters:
            po_id (integer): ID of the purchase order.
        Example:
            Request: GET /api/purchase_orders/1/
            Response:
                {
                    "id": 1,
                    "po_number": "PO123",
                    "vendor": 1,
                    "order_date": "2024-05-01T08:00:00Z",
                    "delivery_date": "2024-05-10T08:00:00Z",
                    "items": [
                        {
                            "name": "Item A",
                            "description": "Description of Item A",
                            "unit_price": 10.00,
                            "quantity": 5
                        },
                        {
                            "name": "Item B",
                            "description": "Description of Item B",
                            "unit_price": 20.00,
                            "quantity": 3
                        }
                    ],
                    "quantity": 8,
                    "status": "pending",
                    "quality_rating": 4.5,
                    "acknowledgment_date": "2024-05-02T08:00:00Z"
                }
    4) Update Purchase Order:
        Endpoint: PUT /api/purchase_orders/{po_id}/
        Description: Update details of a specific purchase order.
        Parameters:
            po_id (integer): ID of the purchase order.
        Example Request Body:
            {
                "po_number": "PO123",
                "vendor": 1,
                "order_date": "2024-05-01T08:00:00Z",
                "delivery_date": "2024-05-10T08:00:00Z",
                "items": [
                    {
                        "name": "Item A",
                        "description": "Description of Item A",
                        "unit_price": 10.00,
                        "quantity": 5
                    },
                    {
                        "name": "Item B",
                        "description": "Description of Item B",
                        "unit_price": 20.00,
                        "quantity": 3
                    }
                ],
                "quantity": 8,
                "status": "completed",
                "quality_rating": 4.7,
                "acknowledgment_date": "2024-05-02T08:00:00Z"
            }
        Example:
        Request: PUT /api/purchase_orders/1/
        Response:
            {
                "id": 1,
                "po_number": "PO123",
                "vendor": 1,
                "order_date": "2024-05-01T08:00:00Z",
                "delivery_date": "2024-05-10T08:00:00Z",
                "items": [
                    {
                        "name": "Item A",
                        "description": "Description of Item A",
                        "unit_price": 10.00,
                        "quantity": 5
                    },
                    {
                        "name": "Item B",
                        "description": "Description of Item B",
                        "unit_price": 20.00,
                        "quantity": 3
                    }
                ],
                "quantity": 8,
                "status": "completed",
                "quality_rating": 4.7,
                "acknowledgment_date": "2024-05-02T08:00:00Z"
            }
    5) Delete Purchase Order:
        Endpoint: DELETE /api/purchase_orders/{po_id}/
        Description: Delete a specific purchase order.
        Parameters:
            po_id (integer): ID of the purchase order.
        Example:
            Request: DELETE /api/purchase_orders/1/
            Response:
                Status Code: 204 (No Content)
            
4) Vendor Performance Endpoints:

    1)  Retrieve a vendor's performance metrics.
        Endpoint: GET/api/vendors/{vendor_id}/performance
        Description: Retrieve specific vendor's performance metrics.
        Parameters:
            vendor_id (integer): Unique identifier of the vendor.
        Example:
            Request: GET/api/vendors/1/performance   
        Response:
            Status Code: 200 (OK)
            Content-Type: application/json
            Body:
                {
                    "vendor_id": 1,
                    "on_time_delivery_rate": 95.0,
                    "quality_rating_avg": 4.8,
                    "average_response_time": 2.3,
                    "fulfillment_rate": 98.0
                }




            

                        




                



