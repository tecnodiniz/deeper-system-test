# Functional Users System CRUD

A full-stack application for managing user data with complete CRUD (Create, Read, Update, Delete) functionality.

## Overview

This project consists of a Flask backend with MongoDB database integration and a frontend built with modern web technologies. The system provides a complete interface for managing user data through a responsive and intuitive UI.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- Complete CRUD operations for user management
- MongoDB database integration
- RESTful API architecture
- Responsive frontend interface
- Data import functionality

## Requirements

### Backend

- Python 3.6+
- MongoDB
- Flask

### Frontend

- Node.js
- npm or yarn

## Installation

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/functional-users-system.git
   cd functional-users-system/backend
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Create a `.env` file in the backend directory:

   ```
   MONGO_URI=mongodb://localhost:27017
   FLASK_APP=app.py
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start MongoDB service:

   ```bash
   # On Linux
   sudo systemctl start mongod

   # On macOS with Homebrew
   brew services start mongodb-community

   # On Windows, ensure the MongoDB service is running
   ```

6. Import initial data:
   ```bash
   python parser.py
   ```
   This will import the data from `udata.json` into your MongoDB users database. Make sure the database is empty before running the parser. I added a safeguard to prevent duplicate data insertion. If you access the app before running the parser and add a user, the collection will contains data, you'll need to delete all existing entries to ensure the collection is empty.

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Usage

### Running the Backend

From the backend directory, run:

```bash
python app.py
```

Or if you've set `FLASK_APP` in your `.env` file:

```bash
flask run
```

The backend API will be available at http://127.0.0.1:5000

The backend serves the app with Flask, but you can interact with it through the Vue 3 frontend.

### Running the Frontend

From the frontend directory, run:

```bash
npm run dev
```

This will start the development server for the frontend.

## API Endpoints

The following API endpoints are available:

- `GET /` - This is the main route of the application.
- `GET /api/users` - Retrieve all users
- `GET /api/users/{id}` - Retrieve a specific user
- `POST /api/users/new` - Create a new user
- `PUT /api/users/{id}` - Update a user
- `DELETE /api/users/{id}` - Delete a user
