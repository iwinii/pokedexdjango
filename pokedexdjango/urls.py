from django.urls import path
from . import views

app_name = 'pokedexdjango'
urlpatterns = [
    path('', views.pokemon_list, name='home'),
    path('pokemon/list', views.pokemon_list, name='pokemon_list'),
    path('pokemon/details/<int:id>/', views.pokemon_details, name='pokemon_details'),
    path('user_info/', views.user_info, name='user_info'),
    path('top_10/', views.top_10, name='top_10'),
    path('top_10_pokemons/', views.top_10_pokemons, name='top_10_pokemons'),
    path('top_10_not_legendary/', views.top_10_not_legendary, name='top_10_not_legendary'),
    path('top_10_water/', views.top_10_water, name='top_10_water'),
    path('top_10_attack/', views.top_10_attack, name='top_10_attack'),
    path('top_10_defence/', views.top_10_defence, name='top_10_defence'),
    path('top_10_hp/', views.top_10_hp, name='top_10_hp'),
    path("register/", views.register, name="register"),
    path("pokemon/list/favourite/", views.favourite_pokemons, name="favourite_pokemons"),
]
