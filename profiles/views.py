from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Follow, Clue, Favorite, Profile, Traveltype, Post, FacilityRating, Facility
from django.http import JsonResponse
from .forms import ProfileForm, UserProfileForm, PostForm, FacilityForm


def posts_list(request,pk):
	profile_obj = Profile.objects.get(pk=pk)
	post_obj2 =  profile_obj.post_set.all()
	return post_obj2


def profile(request, pk):
	if request.user.is_anonymous:

		return redirect('signin')

	my_list = []
	profile_obj = Profile.objects.get(pk=pk)
	posts = profile_obj.post_set.all()
	for post in posts:
		my_list.append({
			"post":post,
			"facilities_with_rating": post.facilityrating_set.all().values_list('facility', flat=True),
			"ratings": post.facilityrating_set.all(),
			})

	context = {
		"profile": Profile.objects.get(pk=pk),
		"posts": posts,
		"my_list": my_list
	}
	return render(request, 'profile1.html', context)

def search_users(request):
	if request.user.is_anonymous:
		return redirect('signin')

	prey_list = []
	preys = request.user.stalker.all()
	for prey in preys:
		prey_list.append(prey.prey)

	users = User.objects.none()
	posts = Post.objects.none()

	query = request.GET.get('q')
	if query:
		users = User.objects.filter(username__icontains=query)
		posts = Post.objects.filter(
			Q(hotel__icontains=query)|
			Q(country__icontains=query)|
			Q(city__icontains=query)|
			Q(suitablefor__title__icontains=query)
			).distinct()

	context = {
		"users":users,
		"prey_list":prey_list,
		"posts": posts,
	}
	return render(request, 'search_users.html', context)


def search_post(request):
	posts = Post.objects.all()

	query = request.GET.get("q")
	if query:
		posts = post.filter(
			Q(hotel__icontains=query)|
			Q(country__icontains=query)|
			Q(city__icontains=query)|
			Q(suitablefor__icontains=query)
			).distinct()

	context = {
		"posts": posts,
	}
	return render(request, 'search_post.html', context)

def follow(request, pk):
	if request.user.is_anonymous:
		return redirect('signin')

	prey = User.objects.get(pk=pk)
	stalker = request.user

	follow, created = Follow.objects.get_or_create(stalker=stalker, prey=prey)
	if created:
		messages.success(request, "Successfully followed %s!"%(prey))
	else:
		follow.delete()
		messages.success(request, "Unfollowed %s!"%(prey))

	return redirect('search-users')

def followers(request, pk):
	if request.user.is_anonymous:
		return redirect('signin')

	user = request.user
	followers = user.prey.all()
	context = {
		"followers": followers,
	}
	return render(request, 'followers.html', context)

def following(request, pk):
	if request.user.is_anonymous:
		return redirect('signin')

	user = request.user
	following = user.stalker.all()
	context = {
		"following": following,
	}
	return render(request, 'following.html', context)

def feed(request):
	if request.user.is_anonymous:
		return redirect('signin')

	user = request.user
	prey_list = []
	preys = request.user.stalker.all()
	for prey in preys:
		prey_list.append(prey.prey)

	post_list = Post.objects.filter(
		Q(profile__owner__in=prey_list)|
		Q(profile__owner=request.user)
		).distinct()

	# favorite_list = []
	# favorites = user.favorite_set.all()
	# for fav in favorites:
	#     favorite_list.append(fav.clue)

	favorite_list = user.favorite_set.all().values_list('clue_id', flat=True)

	context = {
		"feed": post_list,
		"favorites":favorite_list,
	}
	return render(request, 'feed.html', context)

def favorite(request, pk):
	clue_object = Clue.objects.get(pk=pk)
	new_favorite, created = Favorite.objects.get_or_create(user=request.user, clue=clue_object)

	if created:
		action="favorite"
	else:
		new_favorite.delete()
		action="unfavorite"

	response = {
		"action": action,
	}
	return JsonResponse(response, safe=False)

def editprofile(request , pk):
	profile_obj = Profile.objects.get(pk=pk)
	if not(request.user.is_staff or request.user==profile_obj.owner):
		raise Http404
	form = ProfileForm(instance=profile_obj)
	profile_form = UserProfileForm(instance=profile_obj.owner)
	if request.method == "POST":
		form = ProfileForm(request.POST , request.FILES or None, instance=profile_obj)
		profile_form = UserProfileForm(request.POST , request.FILES or None, instance=profile_obj.owner)

		if form.is_valid() and profile_form.is_valid():
			form.save()
			user = form.save()
			profile = profile_form.save(commit=False)
			profile.owner = user
			profile.save()
			profile_form.save_m2m()
			user.save()

			return redirect("profile", pk=pk)
	context = {
		"edit_form":form,
		'profile_form':profile_form,
		"profile_obj":profile_obj,

	}
	return render(request, "edit.html", context)


def create_post(request, pk):
	form = PostForm()
	profile_obj = Profile.objects.get(pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, request.FILES or None)
		if form.is_valid():
			post_obj = form.save(commit=False)
			post_obj.profile = profile_obj
			post_obj.user = request.user
			post_obj.save()
			form.save_m2m()

			return redirect("profile", pk=pk)
		print (form.errors)
	
	context = {
		"form": form,
		"profile": profile_obj,
	}
	return render(request, "create_post.html", context)

def edit_Facli_rate(request, pk):
	obj = FacilityRating.objects.get(pk=pk)
	form = FacilityForm(instance=obj)
	if request.method == "POST":
		form = FacilityForm(request.POST, instance=obj)
		if form.is_valid():
			form.save()
			return redirect("profile", obj.post.profile.id)
 

	context = {
		"form": form,
		"obj": obj,

	}

	return render(request, "edit_rate.html", context)


def create_facility_rate(request, post_id, facility_id):
	form = FacilityForm()
	post_obj = Post.objects.get(id=post_id)
	facility_obj = Facility.objects.get(id=facility_id)
	if request.method == "POST":
		form = FacilityForm(request.POST)
		if form.is_valid():
			rating = form.save(commit=False)
			rating.post = post_obj
			rating.owner = request.user
			rating.facility = facility_obj
			rating.save()

			return redirect("profile", post_obj.profile.id) 
		print (form.errors)

	context = {
		"form": form,
		"post": post_obj,
		"facility": facility_obj,
	}

	return render(request, "rate_facilities.html", context)

