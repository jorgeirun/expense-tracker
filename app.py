from flask import Flask
import strawberry
from strawberry.flask.views import GraphQLView
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional

# DB setup
DATABASE_URL = "sqlite:///db.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, index=True)
    description = Column(String, index=True)
    date = Column(Date, nullable=False)
    category = Column(Integer)

# Create the database table
Base.metadata.create_all(bind=engine)


# GraphQL Types
@strawberry.type
class ExpenseType:
    id: int
    amount: float
    description: str
    date: str
    category: str

# GraphQL Queries
@strawberry.type
class Query:
    # Get by ID
    @strawberry.field
    def get_expense(self, id: int) -> ExpenseType:
        db = SessionLocal()
        expense = db.query(Expense).filter(Expense.id == id).first()
        db.close()
        return ExpenseType(
            id=expense.id,
            amount=expense.amount,
            description=expense.description,
            date=str(expense.date),
            category=expense.category
        ) if expense else None

    # List all
    @strawberry.field
    def list_expenses(self, limit: Optional[int] = 10, offset: Optional[int] = 0) -> list[ExpenseType]:
        db = SessionLocal()
        expenses = db.query(Expense).offset(offset).limit(limit).all()
        db.close()
        return [
            ExpenseType(
                id=expense.id,
                amount=expense.amount,
                description=expense.description,
                date=str(expense.date),
                category=expense.category
            )
            for expense in expenses
        ]

    # Search Expenses
    @strawberry.field
    def search_expenses(
        self,
        description: Optional[str] = None,
        category: Optional[str] = None,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0
    ) -> list[ExpenseType]:
        db = SessionLocal()
        
        query = db.query(Expense)
        
        if description:
            query = query.filter(Expense.description.ilike(f"%{description}%"))
        if category:
            query = query.filter(Expense.category == category)

        expenses = query.offset(offset).limit(limit).all()
        db.close()

        return [
            ExpenseType(
                id=expense.id,
                amount=expense.amount,
                description=expense.description,
                date=str(expense.date),
                category=expense.category
            )
            for expense in expenses
        ]

# GraphQL Mutations
# Create
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_expense(self, amount: float, description: str, date: str, category: str) -> ExpenseType:
        db = SessionLocal()
        # Convert the input date string to a Python date object
        expense_date = datetime.strptime(date, "%Y-%m-%d").date()
        expense = Expense(amount=amount, description=description, date=expense_date, category=category)
        db.add(expense)
        db.commit()
        db.refresh(expense)
        db.close()
        return ExpenseType(
            id=expense.id,
            amount=expense.amount,
            description=expense.description,
            date=str(expense.date),
            category=expense.category
        )
    
    # Edit
    @strawberry.mutation
    def update_expense(
        self,
        id: int,
        amount: Optional[float] = None,
        description: Optional[str] = None,
        date: Optional[str] = None,
        category: Optional[str] = None
    ) -> ExpenseType:
        db = SessionLocal()
        expense = db.query(Expense).filter(Expense.id == id).first()

        if expense is None:
            db.close()
            raise ValueError("Expense not found")

        # Update fields only if new values are provided
        if amount is not None:
            expense.amount = amount
        if description is not None:
            expense.description = description
        if date is not None:
            expense.date = datetime.strptime(date, "%Y-%m-%d").date()
        if category is not None:
            expense.category = category

        db.commit()
        db.refresh(expense)
        db.close()
        
        return ExpenseType(
            id=expense.id,
            amount=expense.amount,
            description=expense.description,
            date=str(expense.date),
            category=expense.category
        )

    # Delete
    @strawberry.mutation
    def delete_expense(self, id: int) -> str:
        db = SessionLocal()
        expense = db.query(Expense).filter(Expense.id == id).first()

        # If the expense is not found, return an error message
        if expense is None:
            db.close()
            return "Expense not found"

        # Delete the expense
        db.delete(expense)
        db.commit()
        db.close()
        
        return "Expense deleted successfully"



# Create the GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Flask application setup
app = Flask(__name__)
app.add_url_rule("/graphql/expenses", view_func=GraphQLView.as_view("graphql_view", schema=schema))

# Main
if __name__ == "__main__":
    app.run(debug=True)
