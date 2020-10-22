from django.contrib.auth.views import LogoutView

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from social_django.utils import load_strategy

from .models import Post


def index(request):
    response = render(request, 'blog/index.html')  # django.http.HttpResponse
    if request.user.is_authenticated:
        social = request.user.social_auth.get(provider='google-oauth2')
        expiration_datetime = social.expiration_datetime()
        access_token = social.get_access_token(load_strategy())
        # refresh_token = social.refresh_token(load_strategy())
        refresh = TokenObtainPairSerializer.get_token(request.user)
        response.set_cookie(key='access', value=str(refresh.access_token))
        response.set_cookie(key='refresh', value=str(refresh))
    return response


class RefreshApiView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        data_from_frontend = request.data
        social = request.user.social_auth.get(provider='google-oauth2')
        expiration_datetime = social.expiration_datetime()
        social.refresh_token(load_strategy())
        access_token = social.get_access_token(load_strategy())
        return Response({'new_token': access_token})


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
