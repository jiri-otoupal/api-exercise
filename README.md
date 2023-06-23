# Car Reservation API

This is a Car Reservation API that allows users to reserve cars for upcoming rides. The API is built using Python 3.6+ and the FastAPI framework. It
utilizes JSON format for communication and stores data in memory. The application provides endpoints for adding, updating, removing, and retrieving
cars, as well as reserving cars for rides and retrieving upcoming reservations. The API documentation is accessible at `localhost:8000/doc`.

### Requirements

To run this application, you need to have the following software installed:

    Python 3.6+
    Docker

#### Installation

Clone the repository:

    `$ git clone https://github.com/jiri-otoupal/api-exercise.git`
    \
    `$ cd api-exercise`

Create a virtual environment and activate it:

`$ python3 -m venv venv`\
`$ source venv/bin/activate`

Install the dependencies:

`$ pip install -r requirements.txt`

Run the application:

    $ python -m uvicorn main:app

    The API will be accessible at http://localhost:8000.

Endpoints
Add Car

    URL: /car/add

    Method: PUT

    Request Body:

    {
      "make": "Toyota",
      "model": "Camry",
      "uid": "C001"
    }

Response:

    {
      "message": "Car added successfully"
    }

Update Car

    URL: /car/update/{uid}

    Method: POST

    URL Parameters:
        identifier: The unique identifier of the car to update

    Request Body:

    {
      "make": "Toyota",
      "model": "Corolla"
    }

Response:

    {
      "message": "Car updated successfully"
    }

Remove Car

    URL: /car/rm/{uid}

    Method: DELETE

    URL Parameters:
        identifier: The unique identifier of the car to remove

    Response:


    {
      "message": "Car removed successfully"
    }

Get All Cars

    URL: /car/list

    Method: GET

    Response:


    {
      "cars": [
        {
          "make": "Toyota",
          "model": "Camry",
          "uid": "C001"
        },
        {
          "make": "Honda",
          "model": "Civic",
          "uid": "C002"
        }
      ]
    }

Reserve Random Car

    URL: /car/reserve

    Method: POST

    Request Body:

    {
      "reserved-since": "2023-06-22T10:00:00",
      "reserved-minutes: 1
    }

Response:

    {
      "message": "Car {UID} {Model} {Make} reserved successfully",
      "reservation": {
        "car": {
          "make": "Toyota",
          "model": "Camry",
          "uid": "C001"
        },
        "reserved-since": "2023-06-22T10:00:00",
        "reserved-minutes: 1
      }
    }

Reserve Car

    URL: /car/reserve/{uid}

    Method: POST

    Request Body:

    {
      "reserved-since": "2023-06-22T10:00:00",
      "reserved-minutes: 1
    }

Response:

    {
      "message": "Car reserved successfully",
      "reservation": {
        "car": {
          "make": "Toyota",
          "model": "Camry",
          "uid": "C001"
        },
        "reserved-since": "2023-06-22T10:00:00",
        "reserved-minutes: 1
      }
    }

### Testing

To run the automated tests, execute the following command:

`$ python -m unittest discover -s tests`

### Docker

You can also run the application using Docker. Make sure you have Docker installed and follow these steps:

    Build the Docker image:

`$ docker build -t car-reservation-api .`

Run the Docker container:

`$ docker run -d -p 8000:8000 car-reservation-api`

The API will be accessible at http://localhost:8000.