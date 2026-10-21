from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.shortcuts import render
def parse_list_size(raw_value):
    raw_value = (raw_value or "").strip()
    if raw_value == "":
        return None, None
    try:
        size = int(raw_value)
    except ValueError:
        return None, "List size must be a whole number."
    if size < 1:
        return None, "List size must be at least 1."
    return size, None
def top_purchasers(request):
    list_size, error = parse_list_size(request.GET.get("size"))
    users = (
        get_user_model().objects
        .annotate(
            movies_purchased=Sum(
                "order__item__quantity",
                default = 0,
            ),
            orders_placed=Count("order",distinct=True),
        )
        .order_by("-movies_purchased", "username", "pk")
    )
    total_users = users.count()
    if list_size is not None:
        users = users[:list_size]
    context = admin.site.each_context(request)
    context.update({
        "title": "Top purchasers",
        "purchasers": users,
        "total_users": total_users,
        "list_size": list_size,
        "size_value": (
            request.GET.get("size", "")
            if error
            else (list_size or "")
        ),
        "error": error,
    })
    return render(
        request,
        "admin/cart/top_purchasers.html",
        context,
    )