import os
from typing import Annotated, List
from fastapi import APIRouter, status, Depends, Request
import dspy
from datetime import datetime
from sqlalchemy import select, text, inspect
from sqlalchemy.orm import Session

from schema import GoodsCreate, GoodsDetail, DeleteGoodResponse, GoodsNewCreate
from database import get_db, engine
from models import User, Goods, History

from exceptions import NotFoundException


router = APIRouter(prefix="/goods", tags=["goods"])

lm = dspy.LM("cohere/command-r-plus", api_key=os.environ["COHERE_API_KEY"])
dspy.configure(lm=lm)


@router.get("/show", status_code=status.HTTP_200_OK, response_model=List[GoodsDetail])
def list_goods(request: Request, db: Annotated[Session, Depends(get_db)]):
    stmt = select(Goods)
    result = db.execute(stmt)
    goods = result.scalars().all()
    if not goods:
        raise NotFoundException(detail="No goods found!")
    return goods


@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_goods(
    goods_data: GoodsCreate,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    email: str,
):
    user = db.scalars(select(User).where(User.email == email)).first()

    new_goods = Goods(
        farmer_id=user.id,
        name=goods_data.name,
        description=goods_data.description,
        price=goods_data.price,
        previous_price=goods_data.price,
        quantity=goods_data.quantity,
        quantity_scale=goods_data.quantity_scale,
        farmer=user,
        order_items=[],
    )

    history = History(
        user_id=user.id,
        name="Good Added",
        good_name=new_goods.name,
        quantity=new_goods.quantity,
        price=new_goods.price,
        # buyer_email=buyer.email,
        # seller_email=seller.email,
        created_at=datetime.utcnow(),
    )
    user.goods.append(new_goods)
    user.histories.append(history)
    db.add(new_goods)
    db.commit()
    db.refresh(new_goods)
    return new_goods


@router.put("/edit", status_code=status.HTTP_200_OK, response_model=GoodsDetail)
def edit_goods(
    idx: int,
    goods_data: GoodsNewCreate,
    email: str,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):
    user = db.scalars(select(User).where(User.email == email)).first()

    goods = user.goods

    good_to_change = None
    for good in goods:
        if good.id == idx:
            good_to_change = good
            break

    if good_to_change.price != goods_data.price:
        good_to_change.previous_price = good_to_change.price
        good_to_change.price = goods_data.price
    elif good_to_change.quantity != goods_data.quantity:
        good_to_change.quantity = goods_data.quantity
    else:
        return good
    history = History(
        user_id=user.id,
        name="Good Edited",
        good_name=good_to_change.name,
        quantity=goods_data.quantity,
        price=goods_data.price,
        # buyer_email=buyer.email,
        # seller_email=seller.email,
        created_at=datetime.utcnow(),
    )
    user.histories.append(history)
    db.commit()
    db.add(history)
    db.refresh(good_to_change)
    return good


# text-to-sql (https://huggingface.co/docs/smolagents/en/examples/text_to_sql)
@router.get("/search", status_code=status.HTTP_200_OK)
def search_goods(request: Request, query: str, db: Annotated[Session, Depends(get_db)]):
    examples = [
        "Query: Show me all users\nOutput: SELECT * FROM users;\n\n",
        "Query: Find all goods with a price greater than 10.\nOutput: SELECT * FROM goods WHERE price > 10;\n\n",
    ]

    inspector = inspect(engine)
    information = ""
    for table in ["users", "goods"]:
        columns_info = [
            (col["name"], col["type"]) for col in inspector.get_columns(table)
        ]

        table_description = f"\nTable '{table}':\n"

        table_description += "Columns:\n" + "\n".join(
            [f"  - {name}: {col_type}" for name, col_type in columns_info]
        )
        information += "\n" + table_description

    class OneLineAnswer(dspy.Signature):
        """You are an expert SQL Query Generator. Generate a sqlalcmey query based on provided tables and query."""

        database_schema: str = dspy.InputField()
        examples_query: list[str] = dspy.InputField()
        input_seach_query: str = dspy.InputField()
        sql_output_query: str = dspy.OutputField()

    answer = dspy.Predict(OneLineAnswer)

    sql_query = answer(
        database_schema=information, examples_query=examples, input_seach_query=query
    ).sql_output_query.strip()

    output = db.execute(text(sql_query))
    if not output.scalar_one_or_none():
        raise ValueError("No output.")
    return output


@router.get("/detail/{id}", status_code=status.HTTP_200_OK, response_model=GoodsDetail)
def goods_detail(id: int, request: Request, db: Annotated[Session, Depends(get_db)]):
    good = db.scalars(select(Goods).where(Goods.id == id)).first()
    return good


@router.delete("/delete", response_model=DeleteGoodResponse)
def delete_goods(
    idx: int, email: str, request: Request, db: Annotated[Session, Depends(get_db)]
):
    user = db.scalars(select(User).where(User.email == email)).first()
    good = db.scalars(select(Goods).where(Goods.id == idx)).first()
    if good.farmer.email == email:
        history = History(
            user_id=user.id,
            name="Good Deleted",
            good_name=good.name,
            quantity=good.quantity,
            price=good.price,
            # buyer_email=buyer.email,
            # seller_email=seller.email,
            created_at=datetime.utcnow(),
        )
        user.histories.append(history)
        db.add(history)
        db.delete(good)
        db.commit()
        return {"name": good.name}
    return {"name": "error"}
