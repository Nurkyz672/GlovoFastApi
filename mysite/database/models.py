from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, Date, ForeignKey, Text, DateTime
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import date, datetime

class RoleChoices(str, PyEnum):
    client = "client"
    owner = "owner"
    courier = "courier"



class UserProfile(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.client)
    date_registered: Mapped[date] = mapped_column(Date, default=date.today)
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="users")
    courier_product: Mapped[List["CourierProduct"]] = relationship("CourierProduct",
                                                                   back_populates="users" )
    stores: Mapped[List["Store"]] = relationship("Store", back_populates="owner")
    user_tokens: Mapped[List['RefreshToken']] = relationship( 'RefreshToken',
                                                              back_populates='token_user',
                                                              cascade='all, delete-orphan'
    )


class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token_user: Mapped[UserProfile] = relationship('UserProfile', back_populates='user_tokens')
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)





class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(20), unique=True)
    stores: Mapped[List["Store"]] = relationship("Store", back_populates="category")


class Store(Base):
    __tablename__ = "store"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="stores")
    store_name: Mapped[str] = mapped_column(String(30), unique=True)
    store_image: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["UserProfile"] = relationship("UserProfile", back_populates="stores")
    created_date: Mapped[date] = mapped_column(Date, default=date.today)
    contacts: Mapped[List["Contact"]] = relationship("Contact", back_populates="store")
    addresses: Mapped[List["Address"]] = relationship("Address", back_populates="store")
    store_menus: Mapped[List["StoreMenu"]] = relationship("StoreMenu", back_populates="store")
    products: Mapped[List["Product"]] = relationship("Product", back_populates="store")


class Contact(Base):
    __tablename__ = "contact"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("store.id"))
    store: Mapped["Store"] = relationship("Store", back_populates="contacts")
    contact_name: Mapped[str] = mapped_column(String(30))
    contact_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("store.id"))
    store: Mapped["Store"] = relationship("Store", back_populates="addresses")
    address_name: Mapped[str] = mapped_column(String(100))


class StoreMenu(Base):
    __tablename__ = "store_menu"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("store.id"))
    store: Mapped["Store"] = relationship("Store", back_populates="store_menus")
    menu_name: Mapped[str] = mapped_column(String(30))


class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("store.id"))
    store: Mapped["Store"] = relationship("Store", back_populates="products")
    product_name: Mapped[str] = mapped_column(String(30))
    product_image: Mapped[Optional[str]] = mapped_column(String)
    product_description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="product")


class OrderStatusChoices(str, PyEnum):
    pending = "pending"
    canceled = "canceled"
    delivered = "delivered"



class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    users: Mapped["UserProfile"] = relationship("UserProfile", back_populates="orders")
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    product: Mapped["Product"] = relationship("Product", back_populates="orders")
    status: Mapped[OrderStatusChoices] = mapped_column(Enum(OrderStatusChoices)
                                                       ,default=OrderStatusChoices.pending)
    deliver_address: Mapped[str] = mapped_column(String(100))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[date] = mapped_column(Date, default=date.today)



class CourierStatusChoices(str, PyEnum):
    busy = "busy"
    available = "available"


class CourierProduct(Base):
    __tablename__ = "courier_product"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    users: Mapped["UserProfile"] = relationship("UserProfile", back_populates="courier_product")
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    order: Mapped["Order"] = relationship("Order")
    courier_status: Mapped[CourierStatusChoices] = mapped_column(Enum(CourierStatusChoices),
                                                                 default=CourierStatusChoices.available)


class Review(Base):
    __tablename__ = "review"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    client: Mapped["UserProfile"] = relationship("UserProfile", foreign_keys=[client_id])
    store_id: Mapped[Optional[int]] = mapped_column(ForeignKey("store.id"), nullable=True)
    store: Mapped[Optional["Store"]] = relationship("Store")
    courier_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    courier: Mapped[Optional["UserProfile"]] = relationship("UserProfile", foreign_keys=[courier_id])
    rating: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)