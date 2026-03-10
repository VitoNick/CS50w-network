from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Follower, Post, User


def index(request):
    posts = Post.objects.all()

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'page_obj': page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def get_modal_content(request):
    return render(request, 'network/new_post_modal.html')


@login_required
@require_POST
def create_post(request):
    content = request.POST.get("content", "").strip()
    image = request.FILES.get("image")

    if not content and not image:
        return JsonResponse({
            "success": False,
            "error": "Post must have content or an image."
        }, status=400)

    Post.objects.create(
        owner=request.user,
        contents=content,
        images=image
    )

    return JsonResponse({
        "success": True,
        "message": "Post created successfully!"
    })


def profile(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "network/profile.html", {
            "error": "User not found."
        })

    posts = profile_user.posts.all()  # type: ignore[attr-defined]

    is_following = (
        request.user.is_authenticated
        and request.user != profile_user
        and Follower.objects.filter( 
            user=profile_user, follower=request.user
        ).exists()
    )

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
        "is_following": is_following,
    })


@login_required
@require_POST
def toggle_follow(request, username):
    try:
        target = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if request.user == target:
        return JsonResponse({"error": "You cannot follow yourself."}, status=400)

    obj, created = Follower.objects.get_or_create( 
        user=target, follower=request.user
    )
    if not created:
        obj.delete()  # If following, unfollow

    return HttpResponseRedirect(reverse("profile", args=[username]))
    

@login_required
def following_posts(request):
    following_users = request.user.following.values_list('user', flat=True)
    posts = Post.objects.filter(owner__in=following_users)
    return render(request, "network/following.html", {
        "posts": posts
    })