# Expense Tracker with Flask, GraphQL, and React

This project is a simple expense tracker application built using Flask for the backend, GraphQL for API querying, and React for the frontend. The backend uses an SQLite database to store and manage expense records, with Strawberry GraphQL providing a flexible API layer.

## Features

- **Backend**: Flask with Strawberry GraphQL for managing CRUD operations on expenses.
- **Database**: SQLite, managed with SQLAlchemy ORM.
- **Frontend**: React (in progress) to provide a user interface for interacting with expenses.

## Project Structure

- **Backend**: Manages data operations and exposes GraphQL endpoints.
- **Frontend**: Displays data to users and allows them to interact with expense records.

## Getting Started

### Prerequisites

- Python 3.7+
- Node.js (for the React frontend)
- Flask and dependencies

### Setup and Installation

#### Backend Setup

1. **Clone the repository:**
   ```git clone <repository-url>```
   ```cd <repository-directory>```

2.	**Create a virtual environment:**
    ```python3 -m venv .venv```
    ```source .venv/bin/activate```

3.	**Install dependencies:**
    ```pip install flask strawberry-graphql sqlalchemy```


4.	**Initialize the SQLite database:**
This will create an SQLite database file (db.db) and set up the expenses table.

#### Running the Backend
1.	Start the Flask server:
```python app.py```
or
``` flask run```

2.	Access the GraphQL Playground:
Navigate to http://127.0.0.1:5000/graphql/expenses in your browser to test GraphQL queries and mutations.


#### Frontend Setup (React)
    In progress


## GraphQL API Documentation

#### Types

	•	ExpenseType: Represents an expense with fields:
	•	id: ID of the expense
	•	amount: Amount spent
	•	description: Description of the expense
	•	date: Date of the expense (as a string)
	•	category: Category of the expense


#### Queries

	•	get_expense(id: Int): Fetches a single expense by ID.
	•	list_expenses(limit: Int, offset: Int): Lists expenses with optional pagination.


#### Mutations

	•	create_expense(amount: Float, description: String, date: String, category: String): Creates a new expense.
	•	update_expense(id: Int, amount: Float, description: String, date: String, category: String): Updates an existing expense.
	•	delete_expense(id: Int): Deletes an expense by ID.

#### Example Queries

#### Create

```
mutation {
  createExpense(amount: 50.0, description: "Grocery shopping", date: "2024-11-01", category: "Food") {
    id
    amount
    description
    date
    category
  }
}
```

#### Search Expenses with Pagination (by description or category)
This search query filters expenses by description and category, returning the first 5 results.

```
query {
  searchExpenses(description: "lunch", limit: 5) {
    id
    amount
    description
    date
    category
  }
}
```

```
query {
  searchExpenses(category: "Food", limit: 5) {
    id
    amount
    description
    date
    category
  }
}
```

#### List Expenses with Pagination
```
query {
  listExpenses(limit: 5, offset: 0) {
    id
    amount
    description
    date
    category
  }
}
```

#### Update Expense
```
mutation {
  updateExpense(id: 1, amount: 75.0) {
    id
    amount
    description
    date
    category
  }
}
```

#### Delete Expense
```
mutation {
  deleteExpense(id: 1)
}
```


## License
This project is licensed under the MIT License - see the LICENSE file for details.
