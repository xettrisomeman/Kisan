from typing import List, Optional
from datetime import datetime

from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(200), nullable=False)
    interests: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    order_items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem",
        cascade="all, delete-orphan",
    )
    goods: Mapped[List["Goods"]] = relationship(
        "Goods",
        back_populates="farmer",
        cascade="all, delete-orphan",
    )
    order_requests: Mapped[List["OrderRequest"]] = relationship(
        "OrderRequest",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    histories: Mapped[List["History"]] = relationship(
        "History", cascade="all, delete-orphan"
    )


class Goods(Base):
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    farmer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    previous_price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity_scale: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    farmer: Mapped["User"] = relationship("User", back_populates="goods")
    order_items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem", back_populates="goods"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    buyer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    goods_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("goods.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    goods: Mapped["Goods"] = relationship(back_populates="order_items")


class OrderRequest(Base):
    __tablename__ = "order_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    farmer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    goods_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("goods.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    buyer_email: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(
        String(25),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="order_requests")


class History(Base):
    __tablename__ = "histories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(36), nullable=False)
    good_name: Mapped[str] = mapped_column(String(36), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=True)
    buyer_email: Mapped[str] = mapped_column(String(136), nullable=True)
    seller_email: Mapped[str] = mapped_column(String(136), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped["User"] = relationship("User", back_populates="histories")
