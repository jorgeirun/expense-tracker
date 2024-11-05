from flask import Flask, jsonify
import strawberry
from strawberry.flask.views import GraphQLView
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


DATABASE_URL = "sqlite:///db.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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

    @strawberry.field
    def list_expenses(self) -> list[ExpenseType]:
        db = SessionLocal()
        expenses = db.query(Expense).all()
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


# Create the GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)



# Flask application setup
app = Flask(__name__)
app.add_url_rule("/graphql/expenses", view_func=GraphQLView.as_view("graphql_view", schema=schema))

if __name__ == "__main__":
    app.run(debug=True)

