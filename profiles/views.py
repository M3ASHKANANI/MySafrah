from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Follow, Clue, Favorite, Profile, Traveltype, Post
from django.http import JsonResponse
from .forms import ProfileForm, UserProfileForm, PostForm


def posts_list(request,pk):
	profile_obj = Profile.objects.get(pk=pk)
	post_obj2 =  profile_obj.post_set.all()
	return post_obj2


def profile(request, pk):
	if request.user.is_anonymous:

		return redirect('signin')
	profile_obj = Profile.objects.get(pk=pk)
	posts = posts_list(request, profile_obj.id)
	if request.method == "POST":
		message = request.POST.get("message")
		Clue.objects.create(user=pk, message=message)
		profile_obj = Profile.objects.get(pk=request.user)
		posts = posts_list(request, profile_obj.id)
		messages.success(request, "New clue generated for your stalkers!")



	context = {
		"profile": Profile.objects.get(pk=pk),
		"posts": posts,
	}
	return render(request, 'profile.html', context)

def search_users(request):
	if request.user.is_anonymous:
		return redirect('signin')

	prey_list = []
	preys = request.user.stalker.all()
	for prey in preys:
		prey_list.append(prey.prey)

	users = User.objects.none()

	query = request.GET.get('q')
	if query:
		users = User.objects.filter(username__icontains=query)

	context = {
		"users":users,
		"prey_list":prey_list
	}
	return render(request, 'search_users.html', context)

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

	clue_list = Clue.objects.filter(
		Q(user__in=prey_list)|
		Q(user=request.user)
		).distinct()

	# favorite_list = []
	# favorites = user.favorite_set.all()
	# for fav in favorites:
	#     favorite_list.append(fav.clue)

	favorite_list = user.favorite_set.all().values_list('clue_id', flat=True)

	context = {
		"feed": clue_list,
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
		form = PostForm(request.POST)
		if form.is_valid():
			post_obj = form.save(commit=False)
			post_obj.profile = profile_obj
			post_obj.user = request.user
			post_obj.save()

			return redirect("profile", pk=pk)
		print (form.errors)
	
	context = {
		"form": form,
		"profile": profile_obj,
	}
	return render(request, "create_post.html", context)







