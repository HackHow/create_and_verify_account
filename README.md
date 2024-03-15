# HTTP APIs for Account and Password Management

#### Design and implement two RESTful HTTP APIs for creating and verifying an account and password.

## Table of Contents

- [Getting Started](#getting-started)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Features and Usage](#features-and-usage)
- [API Documentation](#api-documentation)
- [Technology Choices](#technology-choices)
- [Known Issues and Improvement Plans](#known-issues-and-improvement-plans)
- [Local Setup Tutorial](#local-setup-tutorial)
    - [Local Installation Requirements](#local-installation-requirements)
    - [Running the Application Locally](#running-the-application-locally)
    - [Local API Testing](#local-api-testing)

## Getting Started

1. Download [Docker](https://www.docker.com/products/docker-desktop/)
2. Download a code editor: [PyCharm](https://www.jetbrains.com/pycharm/download/?section=mac)
   or [Visual Studio Code](https://code.visualstudio.com/)
3. Download API testing tool: [Postman](https://www.postman.com/downloads/) **(optional)**

## Installation

```shell
git clone git@github.com:HackHow/senao_networks_interview.git
```

Move to the project directory

```shell
cd senao_networks_interview
```

## Running the Application

### With Docker

Run `docker-compose.yaml`:

```shell
docker-compose up -d
```

> No need to run docker pull <image>, as docker-compose up -d automatically pulls the necessary PostgreSQL and
> custom [Flask App Image](https://hub.docker.com/repository/docker/howard23/senao-networks-interview-flask-app/general)
> Therefore, [Python](https://www.python.org/) installation is not required for project execution!

For local execution instructions, refer to [here](#local-setup-tutorial)

## Features and Usage

- Accessing [http://localhost:5000/](http://localhost:5000/) in a browser displays `Hello World`

  ![CleanShot 2024-03-15 at 01 15 16@2x](https://github.com/HackHow/senao_networks_interview/assets/56557271/64b6a288-95e2-4f0b-9be3-ac426eae4a44)

- Seeing `Hello World` confirms successful service startup. Next, use **Postman** for API testing to ensure responses
  meet expectations
  > Remember, you must register and verify login with the registered account and password to receive successful
  verification responses; otherwise, a "user not found" message will be returned

    - **Create account:**

      ![CleanShot 2024-03-15 at 01 22 04@2x](https://github.com/HackHow/senao_networks_interview/assets/56557271/b9b82725-2e05-40f8-8455-a22df4223b29)

    - **Verify account and password:**

      ![CleanShot 2024-03-15 at 01 22 13@2x](https://github.com/HackHow/senao_networks_interview/assets/56557271/1f34ac80-47f4-4bdd-b3f4-dbe5d54bcf5c)

## API Documentation

- Access [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/) for the Swagger interface:

  ![CleanShot 2024-03-15 at 01 35 39@2x](https://github.com/HackHow/senao_networks_interview/assets/56557271/eaa3cbba-45e6-4885-876c-b07f05ebb4ea)

- This page also allows for API testing. Select the registration API, click **Try it out**, and then **Execute**

  ![CleanShot 2024-03-15 at 01 54 46@2x](https://github.com/HackHow/senao_networks_interview/assets/56557271/910b363b-956a-4382-932e-3ef63667ef25)

## Technology Choices

- Web Framework: [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- Data Storage: [PostgreSQL](https://www.postgresql.org/)
- API document: [Flasgger](https://github.com/flasgger/flasgger)
- Package Management: [Poetry](https://python-poetry.org/docs/)

## Known Issues and Improvement Plans

- **Issues：**
    - The project utilizes direct SQL queries, making DB migrations time-consuming. The workaround of using SQL's **_IF NOT EXISTS_** for table creation is not viable for medium to large-scale or multi-user projects.
    - The verification API, which requires a cooldown after 5 failed attempts, uses a global dictionary with **username
      ** as key for **"last_attempt_time"** and **"attempts"**. There are issues with verifying if a user exists,
      despite **username** being unique.

- **Improvement:**
    - Explore more tools such as [SQLAlchemy](https://www.sqlalchemy.org/) for future projects for its extensive
      resources.
    - A better approach would be using **user_id** as the key to prevent login issues due to incorrect username input.
      Using Redis to store key/value pairs could reduce the unpredictability associated with global variables.

## Local Setup Tutorial

### Local Installation Requirements

In addition to the tools mentioned in [Getting Started](#getting-started), you will need：

- Download the specified [Python](https://www.python.org/) version. This project specifies
  a [version](https://github.com/HackHow/senao_networks_interview/blob/docs/add_user_guide_content/.python-version) (
  It's also recommended to manage versions using [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#unixmacos)).
- Download [Poetry](https://python-poetry.org/docs/#installation) to verify if the application executes correctly on
  your local environment. The recommended download method
  is [Manually (advanced)](https://python-poetry.org/docs/#installing-manually), creating a separate virtual environment
  for Poetry using `venv`.
  > This approach allows you to test application startup and basic functionality. After verifying,
  the entire setup can be easily removed by deleting the directory, making this process clean and reversible.

### Running the Application Locally

1. Install the required packages:
    ```shell
    poetry insall
    ```

2. Based on
   the [.env.example](https://github.com/HackHow/senao_networks_interview/blob/docs/add_user_guide_content/.env.example),
   create a `.env file`, example:
    ```text
   DATABASE_URL=postgresql://postgres:senao@localhost/interview
    POSTGRES_PASSWORD=senao
    POSTGRES_DB=interview
   ```

3. Start the database with `docker-compose.yaml`::
    ```shell
    docker-compose up -d db
    ```

4. Run the application:
    ```shell
    cd app/
    flask --app main run 
    ```

### Local API Testing [pytest](https://docs.pytest.org/en/8.0.x/)

Move to `tests` directory

```shell
cd app/tests/
pyest
```

