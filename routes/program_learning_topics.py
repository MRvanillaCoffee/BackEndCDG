from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Program, ProgramLearningTopic
from schemas import ProgramLearningTopicCreate, ProgramLearningTopicOut


router = APIRouter(
    prefix="/programs/{program_id}/learning-topics",
    tags=["Program Learning Topics"]
)


@router.get("/", response_model=list[ProgramLearningTopicOut])
def get_learning_topics(program_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ProgramLearningTopic)
        .filter(ProgramLearningTopic.program_id == program_id)
        .order_by(ProgramLearningTopic.sort_order)
        .all()
    )


@router.post("/", response_model=ProgramLearningTopicOut)
def add_learning_topic(
    program_id: int,
    data: ProgramLearningTopicCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    topic = ProgramLearningTopic(program_id=program_id, **data.model_dump())
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


@router.delete("/{topic_id}")
def delete_learning_topic(program_id: int, topic_id: int, db: Session = Depends(get_db)):
    topic = (
        db.query(ProgramLearningTopic)
        .filter(
            ProgramLearningTopic.id == topic_id,
            ProgramLearningTopic.program_id == program_id
        )
        .first()
    )
    if not topic:
        raise HTTPException(status_code=404, detail="Learning topic not found")

    db.delete(topic)
    db.commit()
    return {"message": "Learning topic deleted successfully"}
