from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 將根路徑映射到 views.index
#    path('home/', views.home, name='home'),  # 對應到 home 視圖
    path('manager/', views.manager, name='manager'),  # 管理員頁面
    path('teacher/', views.teacher, name='teacher'),  # 老師頁面
    path('student/', views.student, name='student'),  # 學生頁面
    path('student_management/', views.student_management, name='student_management'),
    path('teacher_management/', views.teacher_management, name='teacher_management'),
    
    path('create_course/', views.create_course, name='create_course'),
        path('courses/', views.course_list, name='course_list'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),

    path('edit_course_name/<int:course_id>/', views.edit_course_name, name='edit_course_name'),
    path('edit_course_students/<int:course_id>/', views.edit_course_students, name='edit_course_students'),
    path('course/<int:course_id>/members/', views.show_course_members, name='show_course_members'),
    
    path('courses/<int:course_id>/manage-grades/', views.manage_grades, name='manage_grades'),
    path('courses/<int:course_id>/edit-grade-item/<int:grade_item_id>/', views.edit_grade_item, name='edit_grade_item'),
    path('courses/<int:course_id>/delete-grade-item/<int:grade_item_id>/', views.delete_grade_item, name='delete_grade_item'),
    path('courses/<int:course_id>/manage-student-grades/<int:grade_item_id>/', views.manage_student_grades, name='manage_student_grades'),
    
    path('accounts/', include('allauth.urls')),
    
    path('edit_student_grade/<int:grade_item_id>/<int:student_id>/', views.edit_student_grade, name='edit_student_grade'),
    
    path('line-webhook/', views.line_webhook, name='line_webhook'),  # Webhook 路徑
    path('update_course_order/', views.update_course_order, name='update_course_order'), # 更新課程順序
    path('update_grade_item_order/', views.update_grade_item_order, name='update_grade_item_order'), # 更新成績項目順序

]
