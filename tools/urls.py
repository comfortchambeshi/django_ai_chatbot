# chat_project/urls.py

from django.contrib import admin
from django.urls import path, include

from .views import *

app_name = "tools"

urlpatterns = [
    path('', chat, name='tools_home'),  # Render the chat interface
    path('chatbot/', chat, name='chatbot'),  # Render the chat interface
    path('webhook/', stripe_webhook, name='webhook'), 
    path('generate_response/', generate_response, name='generate_response'),  # Handle AJAX requests


]
