from django.shortcuts import render
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError

from .services import create_transaction, get_all_transactions, creates_user
from .serializers import TransactionSerializer, UserSerializer
# Create your views here.


class UserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = creates_user(**serializer.validated_data)

            return Response({
                'id': user.id,
                'email': user.email
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            Response({'Error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e.args)
            Response({'Error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransactionView(APIView):

    def get(self, request) -> Response:
        transactions = get_all_transactions(request.user.id)
        paginator = LimitOffsetPagination()
        paginator.default_limit = 5
        result = paginator.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request) -> Response:
        # Step 1 - Read data from request
        user = request.user
        value = request.data.get('value')
        kind = request.data.get('kind')

        try:
            transaction = create_transaction(user=user, value=value, kind=kind)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'Error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'Error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
