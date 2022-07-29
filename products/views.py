import stripe
from .models import Product
from django.conf import settings
from rest_framework import status
from django.shortcuts import redirect
from .serializers import (
                        ProductSerializer,
                        CheckoutSerializer
                        )
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import (
                                    CreateAPIView,
                                    RetrieveAPIView,
                                    GenericAPIView,
                                    )

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


class RetrieveProductView(RetrieveAPIView):
    """
    Retrieves a single Product
    """

    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            product_id = kwargs['pid']
            print("PRODUCT ID = ", product_id )
            product = Product.objects.get(id=product_id)
            serializer = self.serializer_class(product)
            response = {
                'data': serializer.data
            }
            print(response)
            return Response(response, status=status.HTTP_200_OK)

        except Product.DoesNotExist as p:
            print("Product does not exist")
            response = {
                'error': "Product Does Not Exist"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print("Exception ", e)
            response = {
                'error': "Product Does Not Exist"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CreateCheckoutSession(GenericAPIView):

    serializer_class = CheckoutSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print("checkout called", request.data.get('product_id'))
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                product = Product.objects.get(id=serializer.data.get('product_id'))
                print("pid  = ", serializer.data.get("product_id"))
                print("qty  = ", serializer.data.get("qty"))

                checkout_session = stripe.checkout.Session.create(
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'unit_amount': int(product.price)*100,
                                'product_data': {
                                    'name': product.title
                                }
                            },
                            'quantity': serializer.data.get('qty')
                        }
                    ],
                    mode='payment',
                    success_url='https://www.google.com/',
                    cancel_url='https://www.youtube.com/',
                )
                return redirect(checkout_session.url)
        except Exception as e:
            response = {
                'error': str(e)
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



