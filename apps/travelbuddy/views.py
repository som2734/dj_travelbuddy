from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Users, Trips, Groups
from django.contrib.auth import logout
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'travelbuddy/index.html')

def register(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        conf_password = request.POST['conf_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        b_day=request.POST['b_day']
        print email
        errors = Users.objects.validation(email, password, conf_password, first_name, last_name, b_day)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('/')
        else:
            print ('should be creating a user now...')
            pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            Users.objects.create(email=email, pw_hash=pw_hash, first_name=first_name, last_name=last_name, b_day=b_day)
            messages.success(request, 'You have registered successfully!')
            return redirect('/')

def login(request):
    if request.method == "POST":
        print ('should be logging in now....')
        email = request.POST['email']
        password = request.POST['password']
        print ('Login credentials entered')
        result = Users.objects.login(email, password)
        if type(result) == list:
            print ('returned result is not object')
            for error in result:
                messages.error(request, error)
            return redirect('/')
        else:
            print "we should be successful..."
            request.session['logged_user'] = result.id
            return redirect('/profile')

def log_out(request):
    current_user = Users.objects.get(id=request.session['logged_user'])
    logout(request)
    return redirect('/')

def add_trip(request):
    return render(request, 'travelbuddy/add_trip.html')

def process_trip(request):
    userid = Users.objects.get(id=request.session['logged_user'])
    if request.method == "POST":
        destination = request.POST['destination']
        plan = request.POST['plan']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        new_trip=Trips.objects.create(user=userid, destination=destination, plan=plan, start_date=start_date, end_date=end_date)
        new_trip.id
        trip_owner = Trips.objects.get(user=userid.id)
        context={'new_trips':new_trip, 'other_trips': other_trips}
        print new_trip.id

    return redirect('/profile', context)

def profile(request):
    userid = Users.objects.get(id=request.session['logged_user'])
    messages.success(request, 'Welcome, {}!'.format(userid.first_name))
    print userid.first_name
    other_trips = Trips.objects.exclude(user=userid)
    my_trips = Trips.objects.filter(user=userid)
    print my_trips
    context = {'my_trips':my_trips, 'other_trips':other_trips}
    return render(request, 'travelbuddy/profile.html', context)

def join_trip(request, id):
    user = Users.objects.get(id=request.session['logged_user'])
    trip_id = Trips.objects.get(id=id)
    trip_attend = Trips.objects.filter(user=user)
    trip_owner = Groups.objects.filter(guest=user)
    owner = trip_id.user.id
    trip_members = Groups.objects.filter(trip=trip_id)
    print "owner"
    print owner
    print "trips user is going on"
    print trip_attend
    print "groups user is in"
    print trip_owner
    print ('*****************************')
    group = Groups.objects.filter(guest=user)
    print group
    if request.POST['submit'] == 'Join':
        for group in trip_members:
            if user.id == group.guest.id:
                print user.id
                messages.info(request, 'You are already incldued on this trip!')
                print ('I am already in this trip!')
                return redirect('/trip_details/' + id)
        new_guest = Groups.objects.create(guest=user, trip=trip_id, )
    return redirect('/trip_details/' + id)


def trip_details(request, id=None):
    if id != None:
        trip_id = Trips.objects.filter(id=id)
        members = Groups.objects.filter(trip=id)
        context={'trip_id':trip_id, 'members':members}
        return render(request, 'travelbuddy/trip_details.html', context)

'''
we're going to display one user's trips on one section of our page
and everyone else's trips (excluding the individual user) on a different section
so, if our user is Bob, we have Bob's trips and everyone who is not Bob's trips
def notBob(request, bob_id):
    bob = Users.objects.get(id=bob_id)
    bob_trips = Trips.objects.filter(user=bob)
    not_bob_trips = Trips.objects.exclude(user=bob)
    context = {
    'bob_trips': bob_trips,
    'not_bob_trips': not_bob_trips
    }
    return render(stuff, context)
-----------------
named route in a link
we have a user object called 'user'
<a href="{% url 'trips:my_trip' user_id=user.id %}"
in the main urls.py
url(r'^', include('apps.trips.urls', namespace='trips'))
in apps/trips/urls.py
url(r'^my_trip/(?P<user_id>\d+)$', views.my_trip, name='my_trip')
'''
