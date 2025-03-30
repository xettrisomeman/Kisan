from typing import Annotated, List
from fastapi import APIRouter, status, Depends, Request, HTTPException
from sqlalchemy import select, and_, delete
from sqlalchemy.orm import Session
from datetime import datetime

from schema import GoodsBuy
from database import get_db
from models import User, Goods, OrderItem, OrderRequest, History

from exceptions import NotFoundException

router = APIRouter(prefix="/order", tags=["order"])


@router.post("/buy", status_code=status.HTTP_201_CREATED)
def buy_goods(
    request: Request,
    goods_buy: GoodsBuy,
    db: Annotated[Session, Depends(get_db)],
):
    buyer = db.scalars(select(User).where(User.email == goods_buy.buyer_email)).first()
    seller = db.scalars(
        select(User).where(User.email == goods_buy.seller_email)
    ).first()
    good = db.scalars(select(Goods).where(Goods.id == goods_buy.idx)).first()

    if good.quantity < goods_buy.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient quantity for {good.name}. Available: {good.quantity}",
        )

    total_price = good.price * goods_buy.quantity

    order_item = OrderItem(
        buyer_id=buyer.id,
        goods_id=good.id,
        name=good.name,
        quantity=goods_buy.quantity,
        price=good.price,
        subtotal=total_price,
        status="pending",
    )

    order_request = OrderRequest(
        farmer_id=seller.id,
        goods_id=good.id,
        name=good.name,
        buyer_email=goods_buy.buyer_email,
        quantity=goods_buy.quantity,
        subtotal=total_price,
        status="pending",
    )

    buyer_history = History(
        user_id=buyer.id,
        name="Sent Buy Order",
        good_name=order_item.name,
        quantity=order_item.quantity,
        price=order_item.price,
        buyer_email=goods_buy.buyer_email,
        seller_email=goods_buy.seller_email,
        created_at=datetime.utcnow(),
    )

    db.add(order_item)
    db.add(order_request)
    db.add(buyer_history)
    db.commit()
    db.refresh(order_item)

    return order_item


@router.put("/accept/{order_item_id}", status_code=status.HTTP_200_OK)
def accept_buy_order(
    request: Request,
    order_item_id: int,
    seller_email: str,
    db: Annotated[Session, Depends(get_db)],
):
    seller = db.scalars(select(User).where(User.email == seller_email)).first()

    order_item = db.scalars(
        select(OrderItem).where(OrderItem.id == order_item_id)
    ).first()

    good = db.scalars(select(Goods).where(Goods.id == order_item.goods_id)).first()

    buyer = db.scalars(select(User).where(User.id == order_item.buyer_id)).first()

    if good.quantity < order_item.quantity:
        raise HTTPException(
            status_code=422,
            detail="Cannot accept. The quantity requested is more than available.",
        )

    order_request = db.scalars(
        select(OrderRequest)
        .where(
            OrderRequest.buyer_email == buyer.email,
            OrderRequest.goods_id == order_item.goods_id,
            OrderRequest.name == order_item.name,
            OrderRequest.quantity == order_item.quantity,
        )
        .order_by(OrderRequest.created_at.desc())
    ).first()

    order_request.status = "accepted"
    order_item.status = "accepted"
    good.quantity -= order_item.quantity

    seller_history = History(
        user_id=seller.id,
        name="Accepted Buy Order",
        good_name=order_item.name,
        quantity=order_item.quantity,
        price=good.price,
        buyer_email=buyer.email,
        seller_email=seller.email,
        created_at=datetime.utcnow(),
    )

    buyer_history = History(
        user_id=buyer.id,
        name="Buy Order Accepted",
        good_name=order_item.name,
        quantity=order_item.quantity,
        price=good.price,
        buyer_email=buyer.email,
        seller_email=seller.email,
        created_at=datetime.utcnow(),
    )

    db.add(seller_history)
    db.add(buyer_history)
    db.commit()

    return {"name": order_item.name}


@router.delete("/cancel/buy/{order_item_id}", status_code=status.HTTP_200_OK)
def cancel_buy_order(
    request: Request,
    order_item_id: int,
    email: str,
    db: Annotated[Session, Depends(get_db)],
):
    user = db.scalars(select(User).where(User.email == email)).first()

    order_item = db.scalars(
        select(OrderItem).where(
            OrderItem.buyer_id == user.id,
            OrderItem.id == order_item_id,
        )
    ).first()

    order_request = db.scalars(
        select(OrderRequest).where(
            OrderRequest.buyer_email == email,
            OrderRequest.goods_id == order_item.goods_id,
            OrderRequest.name == order_item.name,
            OrderRequest.quantity == order_item.quantity,
        )
    ).first()

    buyer_history = History(
        user_id=user.id,
        name="Cancelled Buy Request",
        good_name=order_item.name,
        quantity=order_item.quantity,
        price=order_item.price,
        created_at=datetime.utcnow(),
    )

    db.add(buyer_history)

    if order_request:
        db.delete(order_request)

    db.delete(order_item)
    db.commit()

    return {"name": order_item.name}


# @router.delete("/cancel/incoming/{order_item_id}", status_code=status.HTTP_200_OK)
# def cancel_incoming_buy_order(
#     request: Request,
#     order_item_id: int,
#     buyer_email: str,
#     seller_email: str,
#     db: Annotated[Session, Depends(get_db)],
# ):
#     buyer = db.scalars(select(User).where(User.email == buyer_email)).first()
#     order_item = db.scalars(
#         select(OrderItem).where(
#             OrderItem.buyer_id == buyer.id,
#             OrderItem.id == order_item_id,
#         )
#     ).first()

#     order_request = db.scalars(
#         select(OrderRequest).where(
#             OrderRequest.buyer_email == email,
#             OrderRequest.goods_id == order_item.goods_id,
#             OrderRequest.name == order_item.name,
#             OrderRequest.quantity == order_item.quantity,
#         )
#     ).first()

#     buyer_history = History(
#         user_id=user.id,
#         name="Cancelled Buy Request",
#         good_name=order_item.name,
#         quantity=order_item.quantity,
#         price=order_item.price,
#         created_at=datetime.utcnow(),
#     )

#     seller_history = History(
#         user_id=user.id,
#         name="Incoming Order Cancelled",
#         good_name=order_item.name,
#         quantity=order_item.quantity,
#         price=order_item.price,
#         created_at=datetime.utcnow(),
#     )

#     user.histories.append(buyer_history)

#     if order_request:
#         db.delete(order_request)
#         db.delete(order_item)
#     db.delete(order_item)
#     db.commit()

#     return {"name": order_request.name}


@router.get("/show/buy_requests/pending", status_code=status.HTTP_200_OK)
def show_buy_request_pending_orders(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    buyer_email: str,
):
    user = db.scalars(select(User).where(User.email == buyer_email)).first()

    buy_orders = db.scalars(
        select(OrderItem)
        .where(OrderItem.buyer_id == user.id, OrderItem.status == "pending")
        .order_by(OrderItem.created_at.desc())
    ).all()

    return buy_orders


@router.get("/show/incoming_requests/pending", status_code=status.HTTP_200_OK)
def show_incoming_order_requests_pending_orders(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    seller_email: str,
):
    user = db.scalars(select(User).where(User.email == seller_email)).first()

    buy_orders = db.scalars(
        select(OrderRequest)
        .where(OrderRequest.farmer_id == user.id, OrderRequest.status == "pending")
        .order_by(OrderRequest.created_at.desc())
    ).all()

    return buy_orders


@router.get("/show/history", status_code=status.HTTP_200_OK)
def show_history(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    email: str,
):
    user = db.scalars(select(User).where(User.email == email)).first()

    user_history = db.scalars(
        select(History)
        .where(History.user_id == user.id)
        .order_by((History.created_at.desc()))
    ).all()

    return user_history
