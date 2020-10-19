from django.contrib.auth.views import LogoutView
from django.shortcuts import render

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Post


def index(request):
    # context = {
    #     'posts': Post.objects.order_by('-date')
    #     if request.user.is_authenticated else []
    # }
    response = render(request, 'blog/index.html')  # django.http.HttpResponse
    if request.user.is_authenticated:
        refresh = TokenObtainPairSerializer.get_token(request.user)
        response.set_cookie(key='access', value=str(refresh.access_token))
        response.set_cookie(key='refresh', value=str(refresh))
    return response


class PostsApiView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        posts = Post.objects.order_by('-date')
        return Response(data=[{
            'title': post.title,
            'content': post.content,
            'date': post.date,
            'user': post.user.username,
        } for post in posts])


class TokenLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super(TokenLogoutView, self).dispatch(request, *args, **kwargs)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response
