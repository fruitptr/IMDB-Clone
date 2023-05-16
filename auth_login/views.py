import json

from django.db.models import Count
from django.shortcuts import render, redirect
from movie.models import Movie, Actor
from auth_login.models import User, Producer, Critic, NormalUser
from auth_login.models import Comment
from django.db.models import F, ExpressionWrapper, Q, Func, Value, FloatField
from django.db.models.functions import Replace, Cast, Coalesce
from datetime import datetime as dt
import datetime
import zoneinfo
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# from django.contrib.auth.models import User
# Create your views here.


def index(request): #THIS IS FOR INDEX.HTML
    if request.user.is_authenticated:
        if request.user.user_type != 'producer':
            popular_movies = Movie.objects.all().order_by('-view_count')[:9]
            top_rated_movies = Movie.objects.all().annotate(user_avg=Coalesce('user_avg_rating', 0.0)).order_by('-user_avg')[:5]

            most_reviewed_movies = Comment.objects.all().values('movie_id').annotate(entry_count=Count('movie_id')).values('movie_id', 'entry_count').order_by()
            random_movies = Movie.objects.all().order_by('?')[:6]

            discover_movies = random_movies[:6]
            _carousel = random_movies[:12]

            top_actors = Actor.objects.all().order_by('-view_count')[:3]

            entry_count = most_reviewed_movies.count()
            most_reviewed_movies = sorted(list(most_reviewed_movies), key=lambda x: x['entry_count'], reverse=True)
            if entry_count < 5:
                most_reviewed_movies = most_reviewed_movies[:entry_count]
            else:
                most_reviewed_movies = most_reviewed_movies[:5]

            most_reviewed_data = []

            for _movie in most_reviewed_movies:
                most_reviewed_data.append(Movie.objects.get(id=_movie['movie_id']))

            return render(request, 'index.html', {'most_reviewed': most_reviewed_data, 'top_rated': top_rated_movies,
                                                  'popular_movies': popular_movies, 'spotlight_actors': top_actors,
                                                  'discover_movies': discover_movies, 'carousel': _carousel})
        else:
            return render(request, 'producerlandingpage.html')
    else:
        popular_movies = Movie.objects.all().order_by('-view_count')[:9]
        top_rated_movies = Movie.objects.all().order_by('-user_avg_rating')[:5]

        most_reviewed_movies = Comment.objects.all().values('movie_id').annotate(entry_count=Count('movie_id')).values(
            'movie_id', 'entry_count').order_by()
        random_movies = Movie.objects.all().order_by('?')[:6]

        discover_movies = random_movies[:6]
        _carousel = random_movies[:12]

        top_actors = Actor.objects.all().order_by('-view_count')[:3]

        entry_count = most_reviewed_movies.count()
        most_reviewed_movies = sorted(list(most_reviewed_movies), key=lambda x: x['entry_count'], reverse=True)
        if entry_count < 5:
            most_reviewed_movies = most_reviewed_movies[:entry_count]
        else:
            most_reviewed_movies = most_reviewed_movies[:5]

        most_reviewed_data = []

        for _movie in most_reviewed_movies:
            most_reviewed_data.append(Movie.objects.get(id=_movie['movie_id']))

        return render(request, 'index.html', {'most_reviewed': most_reviewed_data, 'top_rated': top_rated_movies,
                                              'popular_movies': popular_movies, 'spotlight_actors': top_actors,
                                              'discover_movies': discover_movies, 'carousel': _carousel})


def loginuser(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:

            username = request.POST.get('usernamehehe', None)
            password = request.POST.get('password', None)

            user_auth = authenticate(request, username=username, password=password)

            if user_auth:
                login(request, user_auth)
            return redirect('/')


def registeruser(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        password = request.POST.get('password', None)
        email = request.POST.get('email', None)
        user_type = request.POST.get('user_type', None)

        user_type = "normal" if user_type == 'regular' else user_type

        user_obj = User(username=username, first_name=first_name, last_name=last_name, email=email, user_type=user_type)
        user_obj.set_password(password)

        user_obj.save()

        if user_type == 'normal':
            NormalUser.objects.create(user_id=user_obj)
        elif user_type == 'critic':
            Critic.objects.create(user_id=user_obj, critic_organization="Default")
        elif user_type == 'producer':
            Producer.objects.create(user_id=user_obj, name=username)

        return redirect('/')

@csrf_exempt
def changepassword(request):
    if request.method == 'POST':
        oldpassword = request.POST.get('enter_old_password', None)
        newpassword = request.POST.get('enter_new_password', None)
        confirmpassword = request.POST.get('enter_confirm_password', None)

        user_obj = request.user

        if user_obj.check_password(oldpassword) == True:
            user_obj.set_password(newpassword)
            user_obj.save()
        else:
            redirect('/')

    return redirect('/')

def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')




def actorslist(request): # THIS IS FOR CELEBRITYLIST.HTML

    actor_list = Actor.objects.all().order_by('-view_count')
    total_actors = actor_list.count()
    top_actors = Actor.objects.all().order_by('-view_count')[:3]
    for act in actor_list:
        print(act.get_age())
    if request.method == 'POST':
        search_name = request.POST.get('search_name', None)
        search_country = request.POST.get('search_country', None)
        min_age = request.POST.get('search_min_age', None)
        max_age = request.POST.get('search_max_age', None)
        min_yob = request.POST.get('search_min_yob', None)
        max_yob = request.POST.get('search_max_yob', None)


        min_age = int(min_age) if min_age else None
        max_age = int(max_age) if max_age else None
        search_name = search_name if search_name else None
        search_country = search_country if search_country else None
        min_yob = min_yob if min_yob else None
        max_yob = max_yob if max_yob else None

        print(min_age, max_age)

        if isinstance(min_age, int) and isinstance(max_age, int):
            print("bruih")
            cr_dt = dt.now(tz=zoneinfo.ZoneInfo('UTC')).date()
            actor_list_q = actor_list.annotate(actor_age=Func(cr_dt, F('date_of_birth'), function='age'))
            actor_list_id = []
            for actor in actor_list_q:
                if datetime.timedelta(days=min_age*365) <= actor.actor_age <= datetime.timedelta(days=max_age*365):
                    actor_list_id.append(actor.id)
            print(actor_list_id)
            actor_list = Actor.objects.filter(id__in=actor_list_id)
        if search_name:
            actor_list = actor_list.filter(Q(name__icontains=search_name) | Q(name__iexact=search_name))
        if search_country:
            actor_list = actor_list.filter(Q(country__icontains=search_country) | Q(country__iexact=search_country))
        if min_yob and max_yob:
            actor_list = actor_list.filter(date_of_birth__year__range=[min_yob, max_yob])


    return render(request, 'celebritylist.html', {'actor_list': actor_list, 'total_actors':total_actors, 'top_actors':top_actors})


def actordata(request, actor_id): # THIS IS FOR CELEBRITYSINGLE.HTML (NOT DONE AT ALL)

    actor = Actor.objects.get(id=actor_id) #CHANGE THIS
    actor_id = actor.id
    actor_movies = Movie.objects.filter(cast__contains=[actor_id])
    notable_movies = actor_movies.order_by('-view_count')[:3]

    return render(request, 'celebritysingle.html', {'actor_movies':actor_movies, 'actor':actor, 'notable_movies':notable_movies})

def moviedata(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie_cast = movie.cast
    cast_object = Actor.objects.filter(id__in=movie_cast)
    movie_comments = Comment.objects.filter(movie_id=movie_id)
    is_reviewed = False
    favourited = False

    if request.user.is_authenticated:
        if Comment.objects.filter(user_id=request.user.id, movie_id=movie_id).exists():
            is_reviewed = True
        if NormalUser.objects.filter(user_id=request.user.id).exists():
            if NormalUser.objects.filter(user_id=request.user.id, favourite_list__contains=[int(movie_id)]):
                favourited=True

    return render(request, 'moviesingle.html', {'movie':movie, 'cast_object':cast_object, 'movie_comments':movie_comments,
                                                'review_done': is_reviewed, 'fav':favourited})


def loadprofile(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'normal':
            return render(request, 'userprofile.html')
        else:
            return redirect('/')
    else:
        return redirect('/')


def showfavourites(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'normal':
            favourites_list = NormalUser.objects.get(user_id=request.user.id).favourite_list

            fav_obj = [Movie.objects.get(id=mid) for mid in favourites_list]
            return render(request, 'userfavoritegrid.html', {'fav': fav_obj})
        else:
            return redirect('/')
    else:
        return redirect('/')


def showrated(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'normal':
            # favourites_list = NormalUser.objects.get(user_id=request.user.id).favourite_list
            comments = Comment.objects.filter(user_id=request.user.id).distinct('movie_id')
            # fav_obj = [Movie.objects.get(movie_id=mid) for mid in favourites_list]
            return render(request, 'userrate.html', {'comments': comments})
        else:
            return redirect('/')
    else:
        return redirect('/')

def movieslist(request):
    movie_list = Movie.objects.all().order_by('-view_count')
    total_movies = movie_list.count()
    if request.method == 'POST':
        search_movie_name = request.POST.get('search_movie_name', None)
        search_director = request.POST.get('search_director', None)
        search_producer = request.POST.get('search_producer', None)
        search_genre = request.POST.get('search_genre', None)
        min_user_rating = request.POST.get('search_min_user_rating', None)
        max_user_rating = request.POST.get('search_max_user_rating', None)
        min_critic_rating = request.POST.get('search_min_critic_rating', None)
        max_critic_rating = request.POST.get('search_max_critic_rating', None)
        min_budget = request.POST.get('search_min_budget', None)
        max_budget = request.POST.get('search_max_budget', None)
        min_runtime = request.POST.get('search_min_runtime', None)
        max_runtime = request.POST.get('search_max_runtime', None)
        min_year_released = request.POST.get('search_min_year_released', None)
        max_year_released = request.POST.get('search_max_year_released', None)
        search_actor = request.POST.get('search_actor', None)

        min_user_rating = float(min_user_rating) if min_user_rating else None
        max_user_rating = float(max_user_rating) if max_user_rating else None
        search_movie_name = search_movie_name if search_movie_name else None
        search_director = search_director if search_director else None
        search_producer = search_producer if search_producer else None
        min_critic_rating = float(min_critic_rating) if min_critic_rating else None
        max_critic_rating = float(max_critic_rating) if max_critic_rating else None
        search_genre = search_genre if search_genre else None
        int_min_budget = int(min_budget.replace(',', '')) if min_budget else None
        int_max_budget = int(max_budget.replace(',', '')) if max_budget else None
        min_runtime = int(min_runtime) if min_runtime else None
        max_runtime = int(max_runtime) if max_runtime else None
        min_year_released = min_year_released if min_year_released else None
        max_year_released = max_year_released if max_year_released else None

        if min_runtime and max_runtime:
            min_runtime = datetime.timedelta(minutes=min_runtime)
            max_runtime = datetime.timedelta(minutes=max_runtime)
            movie_list = movie_list.filter(runtime__range=[min_runtime, max_runtime])

        if search_actor:
            actor_list = [int(actor.id) for actor in Actor.objects.filter(Q(name__icontains=search_actor) | Q(name__iexact=search_actor))]
            movie_list = movie_list.filter(cast__contains=actor_list)

        if search_movie_name:
            movie_list = movie_list.filter(Q(movie_name__icontains=search_movie_name) | Q(movie_name__iexact=search_movie_name))
        if search_director:
            movie_list = movie_list.filter(Q(director__icontains=search_director) | Q(director__iexact=search_director))
        if search_producer:
            movie_list = movie_list.filter(Q(producer_name__icontains=search_producer) | Q(producer_name__iexact=search_producer))
        if search_genre:
            movie_list = movie_list.filter(Q(genre__icontains=search_genre) | Q(genre__iexact=search_genre))
        if min_year_released and max_year_released:
            movie_list = movie_list.filter(year_released__year__range=[min_year_released, max_year_released])
        if int_min_budget and int_max_budget:
            movie_list = movie_list.annotate(real_budget=Cast(Replace('budget', Value(','), Value('')), FloatField())).filter(real_budget__range=[min_budget, max_budget])
        if min_user_rating and max_user_rating:
            movie_list = movie_list.filter(user_avg_rating__gte=min_user_rating, user_avg_rating__lte=max_user_rating)
        if min_critic_rating and max_critic_rating:
            movie_list = movie_list.filter(critic_avg_rating__gte=min_critic_rating, critic_avg_rating__lte=max_critic_rating)
    return render(request, 'moviegrid.html', {'movie_list':movie_list, 'total_movies':total_movies})


def producerlandingpage(request):
        return render(request, 'producerlandingpage.html', {})


def produceractorlist(request):
    actor_list = Actor.objects.all().order_by('-view_count')
    for act in actor_list:
        print(act.get_age())
    if request.method == 'POST':
        search_name = request.POST.get('search_name', None)
        search_country = request.POST.get('search_country', None)
        min_age = request.POST.get('search_min_age', None)
        max_age = request.POST.get('search_max_age', None)
        min_yob = request.POST.get('search_min_yob', None)
        max_yob = request.POST.get('search_max_yob', None)

        min_age = int(min_age) if min_age else None
        max_age = int(max_age) if max_age else None
        search_name = search_name if search_name else None
        search_country = search_country if search_country else None
        min_yob = min_yob if min_yob else None
        max_yob = max_yob if max_yob else None

        if min_age and max_age:
            cr_dt = dt.now(tz=zoneinfo.ZoneInfo('UTC')).date()
            actor_list_q = actor_list.annotate(actor_age=Func(cr_dt, F('date_of_birth'), function='age'))
            actor_list_id = []
            for actor in actor_list_q:
                if datetime.timedelta(days=min_age * 365) <= actor.actor_age <= datetime.timedelta(days=max_age * 365):
                    actor_list_id.append(actor.id)
            actor_list = Actor.objects.filter(id__in=actor_list_id)
        if search_name:
            actor_list = actor_list.filter(Q(name__icontains=search_name) | Q(name__iexact=search_name))
        if search_country:
            actor_list = actor_list.filter(Q(country__icontains=search_country) | Q(country__iexact=search_country))
        if min_yob and max_yob:
            actor_list = actor_list.filter(date_of_birth__year__range=[min_yob, max_yob])

    return render(request, 'produceractorlist.html', {'actor_list': actor_list})


def createmovie(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'producer':
            movie_name = request.POST.get('enter_movie_name', None)
            director = request.POST.get('enter_director', None)
            producer = Producer.objects.get(user_id=request.user.id)
            genre = request.POST.get('search_genre', None)
            release_date = request.POST.get('enter_year_released', None)
            runtime = request.POST.get('enter_runtime', None)
            budget = request.POST.get('enter_budget', None)
            description = request.POST.get('enter_description', None)
            cast = request.POST.get('enter_cast', None)
            cover_art = request.FILES['enter_cover_art']
            trailer_url = request.POST.get('enter_movie_trailer_url', None)

            movie_cast = list(map(int, cast.split(',')))
            runtime = datetime.timedelta(minutes=int(runtime))
            release_date = dt.strptime(release_date, '%Y-%m-%d')


            Movie.objects.create(movie_name=movie_name, description=description, budget=budget, genre=genre,
                                 year_released=release_date, movie_trailer_url=trailer_url, director=director,
                                 cast=movie_cast, runtime=runtime, cover_art=cover_art, producer_name=producer)

            return redirect('/')


@csrf_exempt
def update_view_count(request):
    mres_data = json.loads(request.body)
    movie_id= mres_data['movie_id']
    print(f'{movie_id=}')
    movie_obj = Movie.objects.filter(id=movie_id)
    if movie_obj:
        movie_obj.update(view_count=F('view_count') + 1)
    return JsonResponse({'detail': 'done'}, status=200)


def createreview(request, movie_id):
    if request.user.is_authenticated:
        if request.user.user_type != 'producer':
            rating = request.POST.get('rating')
            comment = request.POST.get('enter_comment_text')

            rating = int(rating)

            movie_data = Movie.objects.filter(id=movie_id)
            user_obj = User.objects.get(id=request.user.id)

            if request.user.user_type == 'critic':
                cr_avg = movie_data[0].critic_avg_rating
                if not cr_avg:
                    movie_data.update(critic_avg_rating=rating)
                else:
                    num_comments = Comment.objects.filter(movie_id=movie_id).select_related('user_id').annotate(user_type=F('user_id__user_type')).filter(user_type='critic').count()
                    total = num_comments * cr_avg
                    new_avg = (total + rating) / (num_comments + 1)
                    movie_data.update(critic_avg_rating=new_avg)
                Comment.objects.create(user_id=user_obj, movie_id=movie_data[0], comment_text=comment, rating=rating)
            else:
                cr_avg = movie_data[0].user_avg_rating
                if not cr_avg:
                    movie_data.update(user_avg_rating=rating)
                else:
                    num_comments = Comment.objects.filter(movie_id=movie_id).select_related('user_id').annotate(
                        user_type=F('user_id__user_type')).filter(user_type='normal').count()
                    total = num_comments * cr_avg
                    new_avg = (total + rating) / (num_comments + 1)
                    movie_data.update(user_avg_rating=new_avg)
                Comment.objects.create(user_id=user_obj, movie_id=movie_data[0], comment_text=comment, rating=rating)
    return redirect(f'/data/movie/{movie_id}')

@csrf_exempt
def add_movie_to_favourite(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'normal':
            res_data = json.loads(request.body)
            movie_id = res_data['movie_id']

            print(request.user.id, 'hi')
            user_data = NormalUser.objects.get(user_id=request.user.id)
            if int(movie_id) not in user_data.favourite_list:
                print("adding")
                user_data.favourite_list.append(int(movie_id))
                user_data.save()
    return JsonResponse({'detail': 'Done'}, status=200)

@csrf_exempt
def remove_movie_from_favourite(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'normal':
            res_data = json.loads(request.body)
            movie_id = res_data['movie_id']

            user_data = NormalUser.objects.get(user_id=request.user.id)
            if int(movie_id) in user_data.favourite_list:
                print("removing")
                user_data.favourite_list.remove(int(movie_id))
                user_data.save()
    return JsonResponse({'detail': 'Done'}, status=200)


def searchdb(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', None)
        type = request.POST.get('type', None)

        if search_query and type:
            if type == 'movie':
                print('???????')
                search_result = Movie.objects.filter(Q(movie_name__iexact=search_query) | Q(movie_name__icontains=search_query))
                return render(request, 'moviegrid.html', {'movie_list': search_result})
            elif type == 'actor':
                search_result = Actor.objects.filter(Q(name__iexact=search_query) | Q(name__icontains=search_query))
                return render(request, 'celebritylist.html', {'actor_list': search_result})
        else:
            return redirect('/')
