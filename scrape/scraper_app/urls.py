from django.urls import path
from . import views

urlpatterns = [
    path('scrape-jobs/', views.scrape_jobs, name='scrape_jobs'),
    path('search-candidates/', views.search_candidates, name='search_candidates'),
    path('edit-candidate/<int:candidate_id>/', views.edit_candidate, name='edit_candidate'),
    path('delete-candidate/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),
    path('calculate-average-salary/', views.calculate_average_salary, name='calculate_average_salary'),
]
