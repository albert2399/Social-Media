from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount, Comment
from itertools import chain
import random
from django.http import JsonResponse

# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)


    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)
    
    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    self_post = Post.objects.filter(user=request.user)
    feed.append(self_post)

    feed_list = list(chain(*feed))

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestion_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestion_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestion_list:
        username_profile.append(users.email)

    for username in username_profile:
        profile_lists = Profile.objects.filter(email=username)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    comments = Comment.objects.all()
    return render(request, 'index (1).html', {'user_profile':user_profile, 'comments':comments , 'feed':feed_list, 'suggestions_username_profile_list':suggestions_username_profile_list[:4]})

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        perfil = Profile.objects.get(user=request.user)

        new_post = Post.objects.create(user=user, image=image, caption=caption, perfil=perfil)
        new_post.save()

        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='signin')
def delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user.username)

    if request.method == 'POST':
        post.delete()
        return redirect(request.META['HTTP_REFERER'])
    
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile_list = []

        for user in username_object:
            profile = Profile.objects.get(user=user)
            username_profile_list.append(profile)
    return render(request, 'search.html', {'user_profile':user_profile, 'username_profile_list':username_profile_list})

@login_required(login_url='signin')
def followers(request, pk):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    follower_list = FollowersCount.objects.filter(user=pk).values_list('follower', flat=True)
    user_following = pk

    profile_followers = []

    for follower in follower_list:
        follower_user = User.objects.get(username=follower)
        follower_profile = Profile.objects.get(user = follower_user)
        profile_followers.append(follower_profile)
    

    return render(request, 'followers.html', {'profile_followers':profile_followers, 'user_profile': user_profile, 'user_following':user_following})

@login_required(login_url='signin')
def following(request, pk):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    follower_list = FollowersCount.objects.filter(follower=pk).values_list('user', flat=True)
    user_following = pk

    profile_followers = []

    for follower in follower_list:
        follower_user = User.objects.get(username=follower)
        follower_profile = Profile.objects.get(user = follower_user)
        profile_followers.append(follower_profile)
    

    return render(request, 'following.html', {'profile_followers':profile_followers, 'user_profile': user_profile, 'user_following':user_following})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.likes = post.likes+1
        post.save()
        return redirect(request.META['HTTP_REFERER'])
    
    else:
        like_filter.delete()
        post.likes = post.likes-1
        post.save()
        return redirect(request.META['HTTP_REFERER'])
    

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_length = len(user_posts)

    follower = request.user.username
    user = pk
    isFollowing = True

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
        isFollowing = True

    elif follower == user:
        button_text = 'Account Settings'
        isFollowing = True

    else:
        button_text = 'Follow'
        isFollowing = False

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))




    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_posts_length': user_posts_length,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following,
        'isFollowing':isFollowing,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profiles/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profiles/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.porfile_img
            name = request.POST['name']
            lastname = request.POST['lastname']
            email = request.POST['email']
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.first_name = name
            user_profile.last_name = lastname
            user_profile.email = email
            user_profile.porfile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            name = request.POST['name']
            lastname = request.POST['lastname']
            email = request.POST['email']
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.first_name = name
            user_profile.last_name = lastname
            user_profile.email = email
            user_profile.porfile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')

    return render(request, 'setting.html', {'user_profile':user_profile})

@login_required(login_url='signin')
def advanced(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.background
            user_profile.background = image

            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')

            user_profile.background = image

            user_profile.save()

        return redirect('advanced-settings')
    
    return render(request, 'advanced_settings.html', {'user_profile':user_profile})

@login_required(login_url='signin')
def privacy(request):
    user_profile = Profile.objects.get(user=request.user)

    # if request.method == 'POST':

    #     if request.FILES.get('image') == None:
    #         image = user_profile.background
    #         user_profile.background = image

    #         user_profile.save()
    #     if request.FILES.get('image') != None:
    #         image = request.FILES.get('image')

    #         user_profile.background = image

    #         user_profile.save()

    #     return redirect('privacy')
    
    return render(request, 'privacy.html', {'user_profile':user_profile})

@login_required(login_url='signin')
def posts(request, pk):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_post_list = Post.objects.filter(user=pk)

    comments = Comment.objects.all()

    

    return render(request, 'index.html', {'user_post_list':user_post_list, 'user_profile':user_profile, 'comments':comments})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'This email is already registered')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'This username is already registered')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_porfile = Profile.objects.create(user=user_model, id_user=user_model.id, email=user_model.email)
                new_porfile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password do not Match')
            return redirect('signup')
        
    else:    
        return render(request, 'signup.html')
    
def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or password incorrect')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def add_comment(request, post_id):
    if request.method == 'POST':

        comment_text = request.POST['comment']
        user = request.user.username
        comment = Comment.objects.create(content=comment_text, post_id=post_id, user=user)
        comment.save()
        return redirect(request.META['HTTP_REFERER'])
    

    return render(request, 'index (1).html')

@login_required(login_url='signin')
def del_comment(request, comment_id):
    user=request.user.username
    id = request.POST.get('comentario.id')
    comment = Comment.objects.get(id=comment_id, user=user)
    
    if request.method == 'POST':
        if request.user.username == comment.user:
            comment.delete()
            return redirect(request.META['HTTP_REFERER'])

    
    return render(request, {'comment': comment})

@login_required(login_url='signin')
def like_list(request, post_id):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    like_lists = LikePost.objects.filter(post_id=post_id).values_list('username', flat=True)
    user_liking = post_id

    post_likes = []

    for like in like_lists:
        like_user = User.objects.get(username=like)
        follower_profile = Profile.objects.get(user = like_user)
        post_likes.append(follower_profile)
    

    return render(request, 'likes.html', {'post_likes':post_likes, 'user_profile': user_profile, 'user_liking':user_liking})

@login_required(login_url='signin')
def private(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':

        switch_value = request.POST.get('switch_value')
        if switch_value == 'on':
            user_profile.private = True

        elif switch_value == 'off':
            user_profile.private = False
        user_profile.save()

    return JsonResponse({'success': True})