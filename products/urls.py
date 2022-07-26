from django.urls import path
from .views import (
                    RetrieveProductView,
                    CreateCheckoutSession
                    )

urlpatterns = [
    path('product/<int:pid>/', RetrieveProductView.as_view(), name="retrieve-single-product"),
    path('checkout',CreateCheckoutSession.as_view(), name="checkout")
]