from django.urls import path
from . import views
post_viewset = views.PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

post_detail = views.PostViewSet.as_view({
    'get': 'post_detail'
})
category_list = views.CategoryDetail.as_view()

urlpatterns = [
    path('posts/', post_viewset),
    path('post/<slug:slug>/', post_detail),
    path('recommend/', views.PostViewSet.as_view(
            {
                'get': 'recommend'
            }
        )),
    path('categories/', category_list),
    # path('posts/<int:pk>/', views.PostDetail.as_view()),
    # path('categories/', views.CategoryList.as_view()),
    # path('categories/<int:pk>/', views.CategoryDetail.as_view()),
]