# Hospicloud API

API to manage medical history from patients, checkups between patients and doctors, and create custom medical prescription templates.

## Getting Started

These instructions will give you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Requirements for the software and other tools to build, test and push

#### Docker & Docker Compose

1\. Follow the instructions found in the [official docs](https://docs.docker.com/get-docker/) to install Docker.

2\. After installing Docker, follow the steps found in the [official docs](https://docs.docker.com/compose/install/) to install Docker Compose.

#### Python

Make sure to install the latest version found on the [official docs](https://www.python.org/downloads/) or at least version **3.7+**

### Installing

Once you have installed the prerequisites above, run this command to get a copy of the project:

```git
git clone https://github.com/HospiCloud-Team/hospicloud-backend-api.git
```

#### Development

In order to start development, follow these steps:

1\. Create a python environment: 

```
python3 -m venv <name_of_virtual_environment>
```

2\. Access the newly created environment:

**MacOS / Linux**

```
source <name_of_virtual_environment>/bin/activate
```

**Windows**

```
source <name_of_virtual_environment>/bin/activate
```

3\. Install the dependencies using the `requirements.txt` file found on the given service.

```
pip install -r requirements.txt
```

## Running the tests

In order to run the tests, execute the following command at the root of the project, followed by the path of the specified service:

```
pytest <service_path> -v
```

## Usage

In order to start the services of the API, run the following command at the root of the project:

```
docker-compose up --build
```

## Built With

- [Fastapi](https://github.com/tiangolo/fastapi) - Modern, fast, web framework for building APIs with Python 3.6+ based on standard Python type hints
- [Sqlalchemy](https://github.com/sqlalchemy/sqlalchemy) - Python SQL Toolkit and Object Relational Mapper
- [Pytest](https://github.com/pytest-dev/pytest) -  Framework to easily write small tests, yet scales to support complex functional testing for applications and libraries
- [Pydantic](https://github.com/samuelcolvin/pydantic) - Data parsing and validation using Python type hints 