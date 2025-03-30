from typing import Optional, List
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, validator, ConfigDict, EmailStr


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    location: str
    interests: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    location: str
    interests: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class OrderItemBase(BaseModel):
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    subtotal: float = Field(..., gt=0)
    status: str = Field(..., description="Order status (e.g., 'pending', 'completed')")


class GoodsCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    quantity_scale: str = Field(
        ..., description="Unit of measurement (e.g., 'kg', 'lb', 'unit')"
    )


class OrderItemCreate(OrderItemBase):
    goods_id: int


class OrderItemResponse(OrderItemBase):
    id: int
    buyer_id: int
    goods_id: int

    model_config = ConfigDict(from_attributes=True)


class OrderItemsDetail(OrderItemResponse):
    model_config = ConfigDict(from_attributes=True)

    goods: List[GoodsCreate]


class GoodsResponse(GoodsCreate):
    id: int
    farmer_id: int
    created_at: datetime
    updated_at: datetime
    previous_price: float

    model_config = ConfigDict(from_attributes=True)


class GoodsDetail(GoodsResponse):
    model_config = ConfigDict(from_attributes=True)

    farmer: UserResponse
    order_items: List[OrderItemBase] = []


class DeleteGoodResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class GoodsNewCreate(BaseModel):
    price: float
    quantity: int


class GoodsBuy(BaseModel):
    buyer_email: str
    seller_email: str
    idx: int
    quantity: int
