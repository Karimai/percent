# Percent App
## Table of Contents:
1. [Introduction](#1-introduction)
2. [DevStack](#2-devstack)
3. [Features](#3-features)
4. [Installation and Setup](#4-installation-and-setup)
5. [Usage](#5-usage)
6. [API Endpoints](#6-api-endpoints)
7. [Known Issues](#7-known-issues)
8. [Contributing](#8-contributing)
9. [Future Features](#9-future-features)



## 1. Introduction
Welcome to Percent! a simple graphical tools illustrates what percentage of life passed for individuals in different countries. This app allows users to register, sign in, add their residences with specific date ranges and purpose of residing in a particular country. The app then provides a visual representation of the time spent in different countries using a diagram.

## 2. DevStack
The percent app is build using the following technologies:
- FastAPI: A modern, fast, web framework for building APIs with Python.
- Poetry: A dependency management tool for Python projects.
- JWT: JSON Web Tokens for secure user authentication.
- PostgresSQL:
- SQLAlchemy: A powerful and flexible ORM (Object-Relational Mapping) for interacting with the database.
- Alembic: A database migration tool to manage the evolution of the database schema.
- Pydantic: A data validation and parsing library used to define data schemas.
- JavaScript: Used for enhancing for app's frontend interactivity.
- Docker and Docker Compose: For containerization and simplifying the deployment process.
- Matplotlib: A Python library for creating visualizations and diagram.

## 3. Features
The initial version of the Percent app includes the following features:
- User Registration and Login: Users can creat new accounts and log in securely using JWT-based authentication.
- Residence: Users can add their residences in different countries with specific start and end dates and provide a reason for residing there (e.g. Matherlands, Work, Study, or Travel)
- Edit Residences: User can edit or delete residences later.

## 4. Installation and Setup
Set up needs the following steps:
1. Clone the repository from Github: `git clone git@github.com:Karimai/percent.git`
2. Install Poetry: Follow instructions on [poetry docs](https://python-poetry.org/docs/) for installation.
3. Alternatively, you can use Docker. Ensure Docker and Docker Compose are installed. By running the `docker-compose up --build`, you can bring up the app in container and browse the app with [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## 5. Usage
Visit [http://localhost:8000/](http://localhost:8000/) in your browser to access the app.

## 6. API-endpoints
The main of APIs are listed as follow:
* /login
* /user/logout
* /user/register/
* /residence/residences
* /residence/newresidence
* /diagram
* /docs: for documentation.

## 7. Known-issues
It is an initial version and there are a lot of points for improvements:
- some sanity check in entrance a new residence. Even time are not checking at the moments. The end time can be before the start time.
- keep the access_token has a security issue. It should be removed.
- Need a User Profile page.
- User should be able to choose different type of graph type.
- Use Dependency Injection for user login. Now I use http middleware.
- Access token should not be kept in the cookie and it should be kept in request header. Currently it is relying on server-side session. Pass the access token as an Authentication header in the request.

## 8. Contributing
Contributions to the Percent app are welcome! You can help me to make it better if you write to me your suggestions or report bugs that you found during your surf.

## 9. Future Features
- Add Present checkbox in the new residence page
- A lot of improvement in diagram page.

## 10. License
The Percent app is licensed under the MIT License. Feel free to use, modify, and distribute the app according to the license.


