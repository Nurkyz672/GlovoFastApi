from .views import (UserProfileAdmin,AddressAdmin,CategoryAdmin,ContactAdmin,CourierProductAdmin,
                    OrderAdmin,ProductAdmin,ReviewAdmin,StoreAdmin,StoreMenuAdmin)
from fastapi import  FastAPI
from sqladmin import Admin
from mysite.database.db import engine





def setup_admin(myproject:FastAPI):
    admin = Admin(myproject,engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(AddressAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ContactAdmin)
    admin.add_view(CourierProductAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(StoreAdmin)
    admin.add_view(StoreMenuAdmin)
