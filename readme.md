# Dynamic Data Collection API for Farming Practices Using FastAPI

## Objective:
Develop a flexible API using FastAPI that allows for dynamic data collection from farmers regarding their farming practices over a specified number of years. The API should support the creation of varied table configurations based on user needs.

Link for assessment:
[python-data-collection](https://github.com/regrow-coding-challenge/python-data-collection)

## Features & Requirements:

1. **Dynamic Column Configuration:**

- Allow the user to define columns for the data collection table through API requests.
- Support a variety of column types:
    - Four-digit number (e.g., Year)
    - Constrained picklist (e.g., Crop Type with options like corn, wheat, etc.)
    - Constrained float (e.g., Tillage Depth where 0 <= x < 10)
    - Boolean (e.g., Tilled?)
    - Regex validated string (e.g., External Account ID)
    - Slider control mapped to a float (alternative representation in API, since there's no UI)

2. **Dynamic Row Configuration:**

- Provide endpoints to specify the number of years of data to be collected.
- The API should generate the required configuration for the specified number of rows.

3. **Configuration Storage:**

- The API should allow storing, retrieving, updating, and deleting table configurations.
- While data entry values aren't stored, the configuration for each table should be persisted for future use.

4. **Extensibility:**

- The API's design should prioritize scalability and extensibility. Adding new column types or features in the future should be relatively straightforward.

5. **Validation:**

- The API should validate incoming configuration requests to ensure they adhere to the predefined constraints of each column type.

## Implementation Steps:

1. **Database Design:** 

- Create database tables/entities to store the table configurations, which include columns, their types, constraints, and other metadata.

2. **FastAPI Setup:**

- Initialize a FastAPI application.
- Integrate with the database using ORM with SQLAlchemy.

3. **API Development:**

- Implement CRUD (Create, Read, Update, Delete) endpoints for table configurations.
- Add validation logic for various column constraints using FastAPI's request validation features.

4. **Testing:**

- Create unit tests for each endpoint, validating both happy paths and error scenarios.
- Use FastAPI's test client to simulate API calls and verify responses.

5. **Documentation:**

- Utilize FastAPI's automatic Swagger UI and ReDoc integration to provide documentation for the API endpoints and their expected payloads.

## Project Commands

### 1. **Run the Project in Development Mode:**

To start the Uvicorn server in development mode:

```bash
make run
```

This command sets the environment to `development` and runs:

```bash
export ENV=development && uvicorn main:app --reload --host 0.0.0.0
```

### 2. **Clean and Run in Development Mode:**

This command deletes the `database.db` file and then starts the Uvicorn server in development mode:

```bash
make clean-run
```

Executed commands:

```bash
export ENV=development && rm -f database.db && uvicorn main:app --reload --host 0.0.0.0
```

### 3. **Generate Requirements.txt:**

To produce a `requirements.txt` file from the Pipenv environment:

```bash
make generate_requirements_txt
```

The command used is:

```bash
pipenv requirements --dev > requirements.txt
```

### 4. **Run Tests:**

For testing:

```bash
make test
```

This command deletes the `test.db`, sets the environment to `testing`, and then runs pytest:

```bash
rm -f test.db
export ENV=testing && pytest tests -x -vv
```

### 5. **Install Project Dependencies:**

To set up the project's dependencies:

```bash
make install
```

This corresponds to:

```bash
pipenv install --dev
```

