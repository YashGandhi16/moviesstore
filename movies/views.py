from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Rating
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

def index(request):

    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()


    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie, is_reported = False)

    avg_score = Rating.objects.filter(movie=movie).aggregate(Avg('score'))['score__avg']
    average_rating = round(avg_score, 1) if avg_score else None

    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(movie=movie, user=request.user).first()

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['average_rating'] = average_rating
    template_data['user_rating'] = user_rating


    return render(request, 'movies/show.html', {'template_data': template_data})



@login_required
def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, movie_id=id)
    review.is_reported = True
    review.save()
    return redirect('movies.show', id=id)



@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)


@login_required
def rate_movie(request, id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=id)
        score = request.POST.get('score')
        if score and score.isdigit() and 1 <= int(score) <= 5:
            Rating.objects.update_or_create(
                movie=movie,
                user=request.user,
                defaults={'score': int(score)}
            )
        return redirect('movies.show', id=id)

@staff_member_required
def top_commenter(request):
    top_user = (User.objects
        .annotate(comment_count=Count('review'))
        .filter(comment_count__gt=0)
        .order_by('-comment_count', 'username')
        .first())

    template_data = {}
    template_data['title'] = 'Top Commenter'
    template_data['top_user'] = top_user
    return render(request, 'movies/top_commenter.html',
    {'template_data': template_data})
