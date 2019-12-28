from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/' , views.login_user  , name="login"),
    path('logout/' , views.logout_user  , name="logout"),
    path('' , views.summary  , name="summary"),
    path('404' , views.not_found , name="404"),
    path('401' , views.unauthorized , name="401"),
    path('generate_users/' , views.call_users_generator , name='user-generator'),
    path('generate_items/' , views.call_items_generator , name='item-generator'),

    # user crud paths

    path('users/' , views.user_list , name="users-list"),
    path('user/create/' , views.user_create , name="user-create"),
    path('user/<id>/show/' , views.user_show , name="user-show"),
    #path('user/update/' , views.user_update , name="user-update"),
    path('user/<id>/update/' , views.user_update , name="user-update"),
    path('user/<id>/delete/' , views.user_delete , name="user-delete" ),

    # branch crud paths
    path('branches/' , views.branch_list , name="branches-list"),
    path('branch/create/' , views.branch_create , name="branch-create"),
    path('branch/<id>/update/' , views.branch_update , name="branch-update"),
    path('branch/<id>/delete/' , views.branch_delete , name="branch-delete" ),

    # tag crud paths

    path('tags/', views.tag_list, name="tags-list"),
    path('tag/create/', views.tag_create, name="tag-create"),
    path('tag/<id>/update/', views.tag_update, name="tag-update"),
    path('tag/<id>/delete/', views.tag_delete, name="tag-delete"),

    # item crud paths

    path('items/', views.item_list, name="items-list"),
    path('item/create/', views.item_create, name="item-create"),
    path('item/<id>/show/' , views.item_show , name="item-show"),
    path('item/<id>/update/', views.item_update, name="item-update"),
    path('item/<id>/delete/', views.item_delete, name="item-delete"),


]


"""


# item crud paths

path('items/', views.item_list, name="items-list"),
path('item/create/', views.item_create, name="item-create"),
path('item/<id>/show/' , views.item_show , name="item-show"),
path('item/<id>/update/', views.item_update, name="item-update"),
path('item/<id>/delete/', views.item_delete, name="item-delete"),

"""