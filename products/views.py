import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .models import Product
from django.conf import settings
from rest_framework import status
from django.shortcuts import redirect
from .serializers import (
                        ProductSerializer,
                        CheckoutSerializer,
                        OrderSerializer
                        )
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import (
                                    RetrieveAPIView,
                                    GenericAPIView,
                                    )

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.ENDPOINT_SECRET_KEY

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
            product = Product.objects.get(id=product_id)
            serializer = self.serializer_class(product)
            response = {
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        except Product.DoesNotExist as p:
            response = {
                'error': "Product Does Not Exist"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            response = {
                'error': "Product Does Not Exist"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CreateCheckoutSession(GenericAPIView):

    serializer_class = CheckoutSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                product = Product.objects.get(id=serializer.data.get('product_id'))

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
                    metadata={
                        "product_id": serializer.data.get("product_id"),
                        "qty": serializer.data.get("qty"),
                        "unit_price": int(product.price)*100,
                    },
                    mode='payment',
                    success_url='http://localhost:4200/shopping/product/1?success=true',
                    cancel_url='http://localhost:4200/shopping/product/1',
                )
                return redirect(checkout_session.url)
        except Exception as e:
            response = {
                'error': str(e)
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        prod_id = session['metadata']['product_id']
        qty = session['metadata']['qty']
        unit_price = session['metadata']['unit_price']
        payment_status = "completed"

        customer_email = session['customer_details']['email']
        customer_name = session['customer_details']['name']
        customer_country = session['customer_details']['address']['country']
        customer_state = session['customer_details']['address']['state']
        customer_city = session['customer_details']['address']['city']
        customer_addr_line1 = session['customer_details']['address']['line1']
        customer_addr_line2 = session['customer_details']['address']['line2']
        customer_postal_code = session['customer_details']['address']['postal_code']

        order = {
            'email': customer_email,
            'name': customer_name,
            'country': customer_country,
            'state': customer_state,
            'city': customer_city,
            'addr_line1': customer_addr_line1,
            'addr_line2': customer_addr_line2,
            'postal_code': customer_postal_code,
            'product_id': prod_id,
            'qty': qty,
            'unit_price': unit_price,
            'payment_status': payment_status
        }

        serializer = OrderSerializer(data=order)
        if serializer.is_valid():
            serializer.save()
        else:
            response = {
                'errors': serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # Passed signature verification
    return HttpResponse(status=200)



