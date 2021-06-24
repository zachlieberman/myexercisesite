from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
import requests

from django.urls import reverse, reverse_lazy

from .models import Recommended

from django.utils import timezone

from .models import Workout, Favorite, Nutrition, NutriForm, UserProfile, PublicPost


from django.contrib.auth.mixins import LoginRequiredMixin

import string

import math
#import pyjq

# Create your views here.

@login_required
def view_articles_sports(request):
    key = 'ncLbnGcrUevjK2JUZlDnsEakJ0WsynTk'
    url = 'https://api.nytimes.com/svc/topstories/v2/sports.json?api-key='+key

    r = requests.get(url)
    json_results = r.json()
    #copyright = pyjq.all('copyright', json_results)
    copyright = {key: value for key, value in json_results.items() if key=='copyright'}
    results = {key: value for key, value in json_results.items() if key=='results'}

    context = {'copyright': copyright['copyright'],
               'results': results['results']}

    return render(request, 'account/nyt_articles.html', context)

@login_required
def view_articles_health(request):
    key = 'ncLbnGcrUevjK2JUZlDnsEakJ0WsynTk'
    url = 'https://api.nytimes.com/svc/topstories/v2/health.json?api-key='+key

    r = requests.get(url)
    json_results = r.json()
    #copyright = pyjq.all('copyright', json_results)
    copyright = {key: value for key, value in json_results.items() if key=='copyright'}
    results = {key: value for key, value in json_results.items() if key=='results'}

    context = {'copyright': copyright['copyright'],
               'results': results['results']}

    return render(request, 'account/nyt_articles.html', context)

@login_required
def view_articles_nutrition(request):
    key = 'ncLbnGcrUevjK2JUZlDnsEakJ0WsynTk'
    url = 'https://api.nytimes.com/svc/topstories/v2/food.json?api-key='+key

    r = requests.get(url)
    json_results = r.json()
    #copyright = pyjq.all('copyright', json_results)
    copyright = {key: value for key, value in json_results.items() if key=='copyright'}
    results = {key: value for key, value in json_results.items() if key=='results'}

    context = {'copyright': copyright['copyright'],
               'results': results['results']}

    return render(request, 'account/nyt_articles.html', context)


@login_required
def delete_favorite(request):
    try:
        to_compare = request.POST['to_remove'].split()[1]
        #Favorite.objects.filter(user=to_compare).filter(current_user=request.user).delete()
        Favorite.objects.filter(user=to_compare).filter(current_user=request.user).delete()

        return render(request, 'account/delete_favorite.html')

    except:
        return profile(request)

@login_required
def delete_workout(request):
    to_remove = request.POST.get('remove')

    #Favorite.objects.filter(user=to_compare).filter(current_user=request.user).delete()
    #w = Workout.objects.filter(id=to_remove).delete()
    w = Workout.objects.filter(id=to_remove)
    if UserProfile.objects.filter(user=request.user).count() != 0:
        u = UserProfile.objects.filter(user=request.user)[0]
        u.points -= w[0].duration.total_seconds()
        u.save()
    if w[0].partner_username and len(w[0].partner_username)>0:
        partnerID = User.objects.filter(username = w[0].partner_username)[0].id
        if UserProfile.objects.filter(user=partnerID).count() != 0:
            u2 = UserProfile.objects.get(user=partnerID)
            u2.points -= w[0].duration.total_seconds()
            u2.save()
    w.delete()    
    return render(request, 'account/delete_workout.html')

@login_required
def delete_nutrition(request):
    to_remove = request.POST.get('remove')

    #Favorite.objects.filter(user=to_compare).filter(current_user=request.user).delete()
    Nutrition.objects.filter(id=to_remove).delete()

    return render(request, 'account/delete_nutrition.html')


#VIEW SO THAT WHEN USER CLICKS FAVORITED USER, THEY CAN SEE NEW PAGE WITH THEIR WORKOUTS
@login_required
def view_favorite(request):

        favorited_user = request.POST.get('clicked')

        if favorited_user is None:
            none_true = True
        else:
            none_true = False

        if not none_true:
            user = User.objects.all().filter(username=favorited_user)[0]
            
            workouts = Workout.objects.filter(date__lte=timezone.now()).order_by('-date').filter(Q(user=user)|Q(partner_username=user.username)).filter(is_private=False)

            context={'all_workouts':workouts,
                 'none_true': none_true}
            if UserProfile.objects.filter(user=user.id).count() != 0:
                up = UserProfile.objects.get(user = user.id)
                levelCalculation = levelCalculationHelper(up.points)
                context['username'] = user.username
                context['up'] = up
                context['level'] = levelCalculation[0]
                context['remainder'] = levelCalculation[1]
                context['percentage'] = levelCalculation[2]


        else:
            context = {'none_true': none_true}

        return render(request, 'account/recentWorkouts.html', context)

# @login_required
# class recentWorkouts(generic.ListView):
#     favorited_user = request.POST['favorite_click'].split()[1]
#     user = User.objects.all().filter(user=favorited_user)[0]
#
#     model = Workout
#     template_name = 'account/recentWorkouts.html'
#     context_object_name = 'all_workouts'
#
#     def get_queryset(self):
#         return Workout.objects.filter(date__lte=timezone.now()).order_by('-date').filter(user=user)

#Calculate the level system based on points
pointsRequiredToLevelUp = [40,90,140,210,280,360,450,540,650,760,880,1010,1140,1290,1440]
def levelCalculationHelper(points):
    level = 1
    remainder = points
    percentage = 0
    for i in range(len(pointsRequiredToLevelUp)):
        remainder-=pointsRequiredToLevelUp[i]
        if remainder>=0:
            level+=1
        else:
            remainder+=pointsRequiredToLevelUp[i]
            percentage = math.floor(remainder/pointsRequiredToLevelUp[i]*100)
            remainder = pointsRequiredToLevelUp[i] - remainder
            break
    return [level,remainder,percentage]

@login_required
def profile(request):

    context = {}

    #ACCESSES THE USERNAME OF THE USER THAT REQUESTED THE FUNCTION
    for user in User.objects.all():
        if user.username == request.user.username:
            current=user.username
            break

    try:
        #IF (1) THE CURRENT USER HAS NOT YET FAVORITED THAT PAGE, (2) THE USER HAS NOT YET FAVORITED 5 ACCOUNTS, AND (3) THE USER IS NOT TRYING TO FAVORITE THEMSELVES
        if (Favorite.objects.filter(current_user=request.user).filter(user=request.POST['user']).count() == 0) \
                and (Favorite.objects.filter(current_user=request.user).count() < 5) \
                and (request.POST['user'] != current):

            #CREATE A NEW UNIQUE FAVORITE OBJECT WITH PRIMARY KEY="FAVORITED USER" + "CURRENT USER"
            f = Favorite.objects.create(user=request.POST['user'], current_user=request.user, id=request.POST['user']+'_'+request.user.username)
            f.save()

            #FILTER TO FIND ONLY THE CURRENT USER'S FAVORITES, THEN PASS THAT LIST TO THE HTML FILE TO RENDER
            favorites_list = Favorite.objects.filter(user__in=User.objects.values('username')).filter(current_user=request.user)
            all_logs = Workout.objects.all().filter(user=request.user).filter(date__lte=timezone.now()).order_by('-date')[:5]

            if UserProfile.objects.filter(user=request.user).count() != 0:
                up = UserProfile.objects.get(email=request.user.email)
                levelCalculation = levelCalculationHelper(up.points)
                context = {'favorites_list': favorites_list, 'up': up, 'level':levelCalculation[0],'user_name': up.user.username,
                           'remainder':levelCalculation[1],'percentage':levelCalculation[2], 'all_logs': all_logs}

            else:
                context = {'favorites_list': favorites_list, 'all_logs': all_logs}

            #context = {'favorites_list': favorites_list}
            return render(request, 'account/profile.html', context)

        elif request.POST['user'] == current or Favorite.objects.filter(current_user=request.user).filter(user=request.POST['user']).count() != 0:
            favorites_list = Favorite.objects.filter(user__in=User.objects.values('username'),
                                                     current_user=request.user)
            all_logs = Workout.objects.all().filter(user=request.user).filter(date__lte=timezone.now()).order_by('-date')[:5]

            if UserProfile.objects.filter(user=request.user).count() != 0:
                up = UserProfile.objects.get(email=request.user.email)
                levelCalculation = levelCalculationHelper(up.points)
                context = {'favorites_list': favorites_list, 'up': up, 'user_name': up.user.username,
                           'level': levelCalculation[0], 'remainder': levelCalculation[1],
                           'percentage': levelCalculation[2],'all_logs': all_logs,
                           'error_msg': 'You may not add yourself to your favorites, add the same user to your favorites twice, or resumbit this form. '
                                        'Search for another user to try again!'
                           }

            else:
                context = {'favorites_list': favorites_list, 'user_name': request.user.username, 'all_logs': all_logs, 'error_msg': 'You may not add yourself to your favorites,'
                                                                                                              ' add the same user to your favorites twice,'
                                                                                                                                    ' or submit this form twice. '
                                                                                                              'Search for another user to try again!'}

            return render(request, 'account/profile.html', context)


        elif Favorite.objects.filter(current_user=request.user).count() >= 5:
            favorites_list = Favorite.objects.filter(user__in=User.objects.values('username'),
                                                     current_user=request.user)
            all_logs = Workout.objects.all().filter(user=request.user).filter(date__lte=timezone.now()).order_by('-date')[:5]

            if UserProfile.objects.filter(user=request.user).count() != 0:
                up = UserProfile.objects.get(email=request.user.email)
                levelCalculation = levelCalculationHelper(up.points)
                context = {'favorites_list': favorites_list, 'up': up, 'user_name': up.user.username,
                           'level': levelCalculation[0], 'remainder': levelCalculation[1],
                           'percentage': levelCalculation[2],'all_logs': all_logs,
                           'error_msg': 'You may only have up to 5'
                                        ' favorites. Remove a favorite'
                                        ' to add another.'
                           }

            else:
                context = {'favorites_list': favorites_list, 'user_name': request.user.username, 'all_logs': all_logs, 'error_msg': 'You may only have up to 5 '
                                                                                                              'favorites. Remove a favorite '
                                                                                                              'to add another.'}

            return render(request, 'account/profile.html', context)

        #OTHERWISE, DO NOT CREATE ANY NEW FAVORITES -- JUST RENDER THE PAGE WITH CURRENT USER'S EXISTING FAVORITES
        else:

            favorites_list = Favorite.objects.filter(user__in=User.objects.values('username'),
                                                     current_user=request.user)
            all_logs = Workout.objects.all().filter(user=request.user).filter(date__lte=timezone.now()).order_by('-date')[:5]

            if UserProfile.objects.filter(user=request.user).count() != 0:
                up = UserProfile.objects.get(email=request.user.email)
                levelCalculation = levelCalculationHelper(up.points)
                context = {'favorites_list': favorites_list, 'up': up, 'user_name': up.user.username, 'all_logs': all_logs, 'level':levelCalculation[0],'remainder':levelCalculation[1],'percentage':levelCalculation[2]}

            else:
                context = {'favorites_list': favorites_list, 'user_name': request.user.username, 'all_logs': all_logs}

            return render(request, 'account/profile.html', context)

    except:

        favorites_list = Favorite.objects.filter(user__in=User.objects.values('username'),
                                                 current_user=request.user)
        all_logs = Workout.objects.all().filter(user=request.user).filter(date__lte=timezone.now()).order_by('-date')[:5]

        if UserProfile.objects.filter(user=request.user).count() != 0:
            up = UserProfile.objects.get(email=request.user.email)
            levelCalculation = levelCalculationHelper(up.points)
            context = {'favorites_list': favorites_list, 'up': up, 'user_name': up.user.username, 'all_logs': all_logs, 'level':levelCalculation[0],'remainder':levelCalculation[1],'percentage':levelCalculation[2]}

        else:
            context = {'favorites_list': favorites_list, 'user_name': request.user.username, 'all_logs': all_logs}

        return render(request, 'account/profile.html', context)


def login(request):
    return render(request, 'account/login.html')

@login_required
def search_users(request):
    if request.method == "POST":
        user_search = request.POST['user_search']
        users = User.objects.filter(username__startswith=user_search.lower())
        return render(request, 'account/search_users.html',
                      {'user_search':user_search,
                       'users':users})
    else:
        return render(request, 'account/search_users.html')

@login_required
def email(request):
    return render(request, 'account/email.html')


@login_required
def editProfile(request):
    if request.method == "POST":

        for user in User.objects.all():
            if user.username == request.user.username:
                u = user
                break


        fName = request.POST.get('firstName')
        lName = request.POST.get('lastName')
        wt = request.POST.get('weight')
        up = UserProfile(user=u, email=user.email, firstName=fName, lastName=lName, weight=wt)
        #test = UserProfile.objects.create(user=u, email=u.email, firstName=fName, lastName=lName, weight=wt)
        up.save()
        context = {'up': up}
        print(up.firstName + ' ' + up.lastName + ' ' + up.weight + ' ')
        return HttpResponseRedirect(reverse('profile'))

    else:
        print('NONE')
        up = request.user
        context = {'up': up}
        return render(request, 'account/editProfile.html', context)

@login_required
def logWorkout(request):

    if request.method == "GET":
        return render(request, 'account/logWorkout.html')

    #LINES 174-180 MAKE SURE THAT THE PERSON HAS ENTERED A VALID USERNAME FOR THEIR WORKOUT PARTNER
    username_list = []
    for elem in User.objects.values('username'):
        username_list.append(elem['username'])

    if (request.POST.get('workoutPartner') not in username_list) and (request.POST.get('workoutPartner') != ""):
        context = {'error_message': 'You did not enter a valid username.'}
        return render(request, 'account/logWorkout.html', context)

    if request.method == "POST":
        i = 0
        for user in User.objects.all():
            if user.username == request.user.username:
                u = user
                break
            i += 1

        wType = request.POST.get('workoutType')
        partner = request.POST.get('workoutPartner')
        #filter out characters
        dur = request.POST.get('duration').strip(string.ascii_letters)
        nt = request.POST.get('notes')
        private = request.POST.get('private')
        if private == 'on':
            private_true = True

        else:
            private_true = False
        w = Workout.objects.create(user=u, partner_username=partner, workout_type=wType, duration=dur, note=nt, is_private=private_true)
        w.save()

        #add points based on duration (1 pointer per minute)
        if UserProfile.objects.filter(user=request.user).count() != 0:
            #print(request.user)
            up = UserProfile.objects.get(email=request.user.email)
            up.points += int(dur)
            up.save()
        if request.POST.get('workoutPartner') != "":
            partnerID = User.objects.filter(username = partner)[0].id
            if UserProfile.objects.filter(user=partnerID).count() != 0:
                up2 = UserProfile.objects.get(user=partnerID)
                up2.points += int(dur)
                up2.save()
        #print(w)
        #Save points earned in session variable
        request.session['pointsEarned'] = int(dur)
        return redirect('workoutsuccess')

    else:
        print('NONE')
        return render(request, 'account/logWorkout.html')

@login_required
def workoutsuccess(request):
    all_workouts = Workout.objects.all()



    context = {
        'all_workouts':  all_workouts,
    }
    return render(request, "account/workoutsuccess.html", context)


class recentWorkouts(generic.ListView):
    model = Workout
    template_name = 'account/recentWorkouts.html'
    context_object_name = 'all_workouts'

    def get_queryset(self):
        return Workout.objects.filter(date__lte=timezone.now()).order_by('-date').filter(Q(user=self.request.user)|Q(partner_username=self.request.user.username))

class RecentWorkoutView(generic.ListView):
    template_name = 'account/recentWorkout.html'


class OthersWorkoutView(LoginRequiredMixin,generic.ListView):
    #model = Workout
    template_name = 'account/othersWorkout.html'
    context_object_name = 'recentWorkout'
    def get_queryset(self):
        #return Workout.objects.all()
        return Workout.objects.filter(date__lte=timezone.now()).filter(is_private=False).order_by('-date')[0:20]

@login_required
def community(request):
    return render(request, 'account/community.html')

def logout(request):
    return render(request, 'account/logout.html')

@login_required
def log_nutrition(request):
    # create a nutrition instance, associate the form info with that instance (save), redirect to list view
    if request.method == "POST":
        for user in User.objects.all():
            if user.username == request.user.username:
                u = user
                break
        form = NutriForm(request.POST)
        if form.is_valid():
            # grab the text submitted
            nutri_title = form.cleaned_data['title']
            nutri_text = form.cleaned_data['text']
            # create nutrition instance
            logs = Nutrition(user=request.user, title=nutri_title, text=nutri_text)
            logs.save()

            return redirect('nutrisuccess')
    else:
        form = NutriForm()

    all_logs = Nutrition.objects.all().filter(user=request.user)
    # all_logs = Nutrition.objects.filter(date__lte=timezone.now()).order_by('-date')[:2]

    context = {
        'form' : form,
        'all_logs':  all_logs
    }

    return render(request, "account/nutrition.html", context)

@login_required
def nutrisuccess(request):
    all_logs = Nutrition.objects.all().filter(user=request.user)

    context = {
        'all_logs':  all_logs,
    }

    return render(request, "account/nutrisuccess.html", context)

@login_required
def nutrihistory(request):
    all_logs = Nutrition.objects.all().filter(user=request.user)

    context = {
        'all_logs':  all_logs,
    }

    return render(request, "account/nutrihistory.html", context)

def chat(request):
    return render(request, 'account/chat.html')
def room(request, room_name):
    return render(request, 'account/chatRoom.html', {
        'room_name': room_name
    })

@login_required
def submitPost(request):
    """
    A form page to submit a post
    """
    return render(request, 'account/post.html')

@login_required
def myPost(request):
    """
    Shows all posts that the current user made
    """
    myPosts = PublicPost.objects.filter(date__lte=timezone.now(), user = request.user).order_by('-date')
    return render(request, 'account/myPost.html', {'myPost':myPosts})

@login_required
def postHandling(request):
    """
    Handles submitting a post
    """
    try:
        postContent = request.POST['post_content']
        postTitle = request.POST['post_title']
        posting = PublicPost(user = request.user, title = postTitle, content = postContent, date = timezone.now())
        posting.save()
    except (KeyError):
        pass
    
    
    return HttpResponseRedirect(reverse('myPost'))
@login_required
def allPost(request):
    """
    Shows the view for all community posts
    """
    all_posts = PublicPost.objects.filter(date__lte=timezone.now(),is_highlighted = False).order_by('-date')
    highlight_posts = PublicPost.objects.filter(date__lte=timezone.now(),is_highlighted = True).order_by('-date')
    context = {
        'allPosts':  all_posts,
        'highlightPosts': highlight_posts,
    }

    return render(request, 'account/allPost.html', context)
    
def deletePost(request):
    """
    handles deleting posts
    """
    try:
        postID = request.POST['postID']
    except(KeyError):
        pass
    PublicPost.objects.filter(id = postID).delete()
    return HttpResponseRedirect(reverse('myPost'))

class RecommendedList(generic.ListView):
    queryset = Recommended.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

    def load(request):
        return render(request, 'account/index.html')
    

class RecommendedDetail(generic.DetailView):
    model = Recommended
    template_name = 'post_detail.html'
