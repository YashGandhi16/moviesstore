from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie, Review
from .models import Order, Item
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from django.contrib import admin

from .utils import calculate_cart_total
def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart =Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html', {'template_data': template_data})


def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('cart.index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    request.session['cart'] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html',
        {'template_data': template_data})

@staff_member_required
def user_engagement(request):
    buyers = (get_user_model().objects
              .annotate(movies_purchased=Sum("order__item__quantity"))
              .filter(movies_purchased__gt=0))
    top = buyers.order_by("-movies_purchased", "pk").first()
    tops = (buyers.filter(
        movies_purchased=top.movies_purchased).order_by("username", "pk")
        if top is not None else []
    )
    template_data = {
        "title": "User Engagement",
        "tops": tops,
    }
    return render(
        request,
        "cart/user_engagement.html",
        {
            **admin.site.each_context(request),
            "title": "User Engagement",
            "template_data": template_data,
        },
    )

@staff_member_required
def movie_statistics(request):

    purchases = (Item.objects
                 .values('movie_id', 'movie__name')
                 .annotate(total=Sum('quantity'))
                 .order_by('-total', 'movie__name', 'movie_id'))
    
    reviews = (Review.objects
                 .values('movie_id', 'movie__name')
                 .annotate(total=Sum('id'))
                 .order_by('-total', 'movie__name', 'movie_id'))
    
    most_purchased_count = (purchases[0]['total'] if purchases else 0)
    most_reviewed_count = (reviews[0]['total'] if reviews else 0)

    template_data = {
        'title': 'Movie Statistics',
        'most_purchased': [
            movie for movie in purchases
            if movie['total'] == most_purchased_count
        ],
        'most_reviewed': [
            movie for movie in reviews
            if movie['total'] == most_reviewed_count
        ],
    }

    return render(
        request,
        'cart/movie_statistics.html',
        {
            **admin.site.each_context(request),
            'title': 'Movie Statistics',
            'template_data': template_data,
        },
    )

