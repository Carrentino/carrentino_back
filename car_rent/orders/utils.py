from rest_framework import status
from rest_framework.response import Response


def check_order_status(order, expected_status, requested_status):
    if order.status != expected_status:
        return (False, Response({"error": f"Для изменения на статус {requested_status}, заявка должна находиться в статусе {expected_status}"}, status=status.HTTP_409_CONFLICT))
    return (True, None)
