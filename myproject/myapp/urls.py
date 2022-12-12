from django.urls import path, include
from . import views

app_name = 'myapp'

urlpatterns = [
    # defであれば下のようにOK
    # path('', views.Index, name='index'),
    # classであればしたのように
    path('', views.Index.as_view(), name='index'),
    #nameのpost_createはボタンとか作るときのhtmlでlinkを使うための名称
    path('post_create', views.PostCreate.as_view(), name='post_create'),
    path('post_detail/<int:pk>', views.PostDetail.as_view(), name='post_detail'),
    path('post_update/<int:pk>', views.PostUpdate.as_view(), name='post_update'),
    path('post_delete/<int:pk>', views.PostDelete.as_view(), name='post_delete'),
    path('post_list', views.PostList.as_view(), name='post_list'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('like/<int:post_id>./', views.Like_add, name='like_add'),
    path('category_list', views.CategoryList.as_view(), name='category_list'),
    path('category_detail/<str:name_en>', views.CategoryDetail.as_view(), name='category_detail'),
    path('search', views.Search, name='search'),
]
