from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('index', views.index_redir),

    path('register', views.register),
    path('logout', views.logout),
    path('login', views.login),
    path('logregister', views.logregister),

    path('animals/<int:render_id>', views.animal),
    path('families/<int:render_id>', views.family),
    path('aniclasses/<int:render_id>', views.aniclass),
    path('biomes/<int:render_id>', views.biome),
    path('users/<int:render_id>', views.user_profile),

    path('add_biome', views.add_biome),
    path('add_biome_exe', views.add_biome_exe),
    path('add_class', views.add_class),
    path('add_class_exe', views.add_class_exe),
    path('add_family', views.add_family),
    path('add_family_exe', views.add_family_exe),
    path('add_animal', views.add_animal),
    path('add_animal_exe', views.add_animal_exe),

    path('comment', views.comment),
]