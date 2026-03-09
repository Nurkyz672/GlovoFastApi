from mysite.database.models import (UserProfile, Address, Category, Contact, CourierProduct,Order,
                                    Product, Store, StoreMenu, Review)
from sqladmin import ModelView



class UserProfileAdmin(ModelView,model=UserProfile):
    column_list = [UserProfile.first_name,UserProfile.last_name]


class AddressAdmin(ModelView,model = Address):
    column_list = [Address.address_name]


class CategoryAdmin(ModelView,model = Category):
    column_list = [Category.id,Category.category_name]


class ContactAdmin(ModelView,model = Contact):
    column_list = [ Contact.contact_name,Contact.contact_number]


class ReviewAdmin(ModelView,model = Review):
    column_list = [ Review.rating,Review.text]


class StoreAdmin(ModelView,model = Store):
    column_list = [Store.store_name,Store.description]


class StoreMenuAdmin(ModelView,model = StoreMenu):
    column_list = [StoreMenu.menu_name,StoreMenu.store_id]


class ProductAdmin(ModelView,model = Product):
    column_list = [Product.product_name,Product.price]


class OrderAdmin(ModelView, model = Order):
    column_list = [Order.users_id,Order.product_id]


class CourierProductAdmin(ModelView,model = CourierProduct):
    column_list = [CourierProduct.users_id,CourierProduct.order_id]