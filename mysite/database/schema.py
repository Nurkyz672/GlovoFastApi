from pydantic import EmailStr
from typing import Optional
from datetime import date,datetime
from pydantic import BaseModel


class UserProfileSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

class Login(BaseModel):
    username: str
    password: str


class  UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    age: Optional[int]
    phone_number: Optional[int]


class  UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    age: Optional[int]
    phone_number: Optional[int]
    date_registered: date



class CategoryInputSchema(BaseModel):
    category_name: str


class CategoryOutSchema(BaseModel):
    id: int
    category_name: str



class StoreInputSchema(BaseModel):
    category_id: int
    store_name: str
    store_image: Optional[str]
    description: Optional[str]
    owner_id: int


class StoreOutSchema(BaseModel):
    id: int
    category_id: int
    store_name: str
    store_image: Optional[str]
    description: Optional[str]
    owner_id: int
    created_date: date



class ContactInputSchema(BaseModel):
    store_id: int
    contact_name: str
    contact_number: Optional[str]


class ContactOutSchema(BaseModel):
    id: int
    store_id: int
    contact_name: str
    contact_number: Optional[str]



class AddressInputSchema(BaseModel):
    store_id: int
    address_name: str


class AddressOutSchema(BaseModel):
    id: int
    store_id: int
    address_name: str



class StoreMenuInputSchema(BaseModel):
    store_id: int
    menu_name: str


class StoreMenuOutSchema(BaseModel):
    id: int
    store_id: int
    menu_name: str



class ProductInputSchema(BaseModel):
    store_id: int
    product_name: str
    product_image: Optional[str]
    product_description: Optional[str]
    price: int
    quantity: int


class ProductOutSchema(BaseModel):
    id: int
    store_id: int
    product_name: str
    product_image: Optional[str]
    product_description: Optional[str]
    price: int
    quantity: int



class OrderInputSchema(BaseModel):
    users_id: int
    product_id: int
    deliver_address: str
    quantity: int


class OrderOutSchema(BaseModel):
    id: int
    users_id: int
    product_id: int
    deliver_address: str
    quantity: int
    created_at: date



class CourierProductInputSchema(BaseModel):
    users_id: int
    order_id: int


class CourierProductOutSchema(BaseModel):
    id: int
    users_id: int
    order_id: int



class ReviewInputSchema(BaseModel):
    client_id: int
    store_id: Optional[int]
    courier_id: Optional[int]
    rating: int
    text: str


class ReviewOutSchema(BaseModel):
    id: int
    client_id: int
    store_id: Optional[int]
    courier_id: Optional[int]
    rating: int
    text: str
    created_date: date