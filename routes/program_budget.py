from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramBudgetIncome, ProgramBudgetExpense
from schemas import (
    ProgramBudgetIncomeCreate, ProgramBudgetIncomeOut,
    ProgramBudgetExpenseCreate, ProgramBudgetExpenseOut
)


income_router = APIRouter(
    prefix="/programs/{program_id}/budget-income",
    tags=["Program Budget Income"]
)

expense_router = APIRouter(
    prefix="/programs/{program_id}/budget-expense",
    tags=["Program Budget Expense"]
)


@income_router.get("/", response_model=list[ProgramBudgetIncomeOut])
def get_budget_income(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ProgramBudgetIncome)
        .filter(ProgramBudgetIncome.program_id == program_id)
        .order_by(ProgramBudgetIncome.sort_order)
        .all()
    )


@income_router.post("/", response_model=ProgramBudgetIncomeOut)
def add_budget_income(program_id: int, data: ProgramBudgetIncomeCreate, db: Session = Depends(get_db)):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    row = ProgramBudgetIncome(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@income_router.delete("/{income_id}")
def delete_budget_income(program_id: int, income_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(ProgramBudgetIncome)
        .filter(ProgramBudgetIncome.id == income_id, ProgramBudgetIncome.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Budget income entry not found")
    db.delete(row)
    db.commit()
    return {"message": "Budget income entry deleted successfully"}


@expense_router.get("/", response_model=list[ProgramBudgetExpenseOut])
def get_budget_expense(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ProgramBudgetExpense)
        .filter(ProgramBudgetExpense.program_id == program_id)
        .order_by(ProgramBudgetExpense.sort_order)
        .all()
    )


@expense_router.post("/", response_model=ProgramBudgetExpenseOut)
def add_budget_expense(program_id: int, data: ProgramBudgetExpenseCreate, db: Session = Depends(get_db)):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    row = ProgramBudgetExpense(program_id=program_id, **data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@expense_router.delete("/{expense_id}")
def delete_budget_expense(program_id: int, expense_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(ProgramBudgetExpense)
        .filter(ProgramBudgetExpense.id == expense_id, ProgramBudgetExpense.program_id == program_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Budget expense entry not found")
    db.delete(row)
    db.commit()
    return {"message": "Budget expense entry deleted successfully"}
