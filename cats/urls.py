from django.urls import path
from . import views

urlpatterns = [
    path('', views.SceneView.as_view(), name='scene'),
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('my-cats/', views.MyCatsView.as_view(), name='my_cats'),

    path('cat/new/', views.CatCreateView.as_view(), name='cat_create'),
    path('cat/<int:pk>/', views.CatDetailView.as_view(), name='cat_detail'),
    path('cat/<int:pk>/edit/', views.CatUpdateView.as_view(), name='cat_update'),
    path('cat/<int:pk>/delete/', views.CatDeleteView.as_view(), name='cat_delete'),

    path('cat/<int:pk>/comment/', views.add_comment, name='comment_create'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

    path('cat/<int:pk>/react/', views.toggle_reaction, name='cat_react'),
    path('cat/<int:pk>/pet/', views.pet_cat, name='cat_pet'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
]