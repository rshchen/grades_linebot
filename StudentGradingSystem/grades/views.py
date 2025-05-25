import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models, IntegrityError   
from django.db.utils import IntegrityError as DbIntegrityError
from .models import Teacher, Manager, Student, Course, GradeItem, Grade
from .forms import CourseForm, GradeItemForm, GradeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd



# 首頁
def index(request):
    return render(request, 'grades/index.html')

################################################
    
def logout_view(request):
    logout(request)  # 結束 Django session
    return redirect('/')  # 登出後重定向到首頁或其他頁面
################################################

# 管理員頁面
@login_required
def manager(request):
    # 取得目前登入用戶的 email
    user_email = request.user.email

    if not Manager.objects.filter(email=user_email).exists():
        # 如果當前用戶的 email 不在 Manager 表中
        message = "您不具備管理員身份，請通知廠商"
        is_manager = False
    else:
        # 獲取當前用戶的管理員資料
        manager = Manager.objects.get(email=user_email)
        message = f"您好，{manager.name}管理員"  # 顯示管理員的名字
        is_manager = True

    # 將訊息和管理員身份傳遞給模板
    return render(request, 'grades/manager.html', {'message': message, 'is_manager': is_manager})

# 學生資料管理
def validate_email(email):
    """檢查電子郵件格式的簡單函數"""
    if not email:  # 如果電子郵件為空，視為有效
        return True
    try:
        from django.core.validators import validate_email as django_validate_email
        from django.core.exceptions import ValidationError

        django_validate_email(email)
        return True
    except ValidationError:
        return False

@login_required
def student_management(request):
    user_email = request.user.email

    if not Manager.objects.filter(email=user_email).exists():
        message = "您不具備管理員身份，請通知廠商"
        is_manager = False
        students = []
    else:
        message = "學生資料管理頁面"
        is_manager = True
        students = Student.objects.all()  # 獲取所有學生資料

        if request.method == "POST" and request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']

            # 檢查文件是否為 CSV 檔案
            if not csv_file.name.endswith('.csv'):
                messages.error(request, '請上傳CSV檔案格式')
                return redirect('student_management')

            try:
                # 讀取並解析 CSV 檔案
                decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
                csv_reader = csv.reader(decoded_file)
                next(csv_reader)  # 跳過標題行

                csv_student_ids = []
                csv_class_names = set()

                for row in csv_reader:
                    if len(row) != 5:
                        messages.error(request, 'CSV 格式錯誤，請檢查資料。')
                        continue

                    class_name, seat_number, student_id, name, student_email = map(str.strip, row)

                    if not student_id:
                        messages.error(request, "缺少學號，跳過該行。")
                        continue

                    if seat_number.isdigit():
                        seat_number = int(seat_number)
                    else:
                        messages.error(request, f"座號 '{seat_number}' 不是有效的數字，跳過該行。")
                        continue

                    if not name:
                        messages.error(request, "姓名不能為空，跳過該行。")
                        continue

                    if not validate_email(student_email):
                        messages.error(request, f"學生信箱 '{student_email}' 格式不正確，跳過該行。")
                        continue

                    csv_student_ids.append(student_id)
                    csv_class_names.add(class_name)

                    # 直接將 class_name 設為字串
                    Student.objects.update_or_create(
                        student_id=student_id,
                        defaults={
                            'class_name': class_name,  # 直接使用 class_name 字串
                            'seat_number': seat_number,
                            'name': name,
                            'student_email': student_email,
                        }
                    )

                # 刪除不再存在的學生
                Student.objects.exclude(student_id__in=csv_student_ids).delete()

                messages.success(request, '學生資料已成功匯入。')
            except Exception as e:
                messages.error(request, f'處理檔案時發生錯誤: {e}')

    return render(request, 'grades/student_management.html', {
        'message': message,
        'is_manager': is_manager,
        'students': students  # 傳遞學生資料
    })



# 教師資料管理
@login_required
def teacher_management(request):
    user_email = request.user.email

    if not Manager.objects.filter(email=user_email).exists():
        message = "您不具備管理員身份，請通知廠商"
        is_manager = False
        teachers = []
    else:
        message = "教師資料管理頁面"
        is_manager = True
        teachers = Teacher.objects.all()  # 獲取所有教師資料

        if request.method == "POST" and request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']

            # 檢查文件是否為 CSV 檔案
            if not csv_file.name.endswith('.csv'):
                messages.error(request, '請上傳CSV檔案格式')
                return redirect('teacher_management')

            try:
                # 讀取並解析 CSV 檔案
                decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
                csv_reader = csv.reader(decoded_file)
                next(csv_reader)  # 跳過標題行

                csv_teacher_emails = []

                for row in csv_reader:
                    if len(row) != 2:
                        messages.error(request, 'CSV 格式錯誤，請檢查資料。')
                        continue

                    name, email = map(str.strip, row)

                    if not name:
                        messages.error(request, "教師姓名不能為空，跳過該行。")
                        continue

                    if not validate_email(email):
                        messages.error(request, f"教師信箱 '{email}' 格式不正確，跳過該行。")
                        continue

                    csv_teacher_emails.append(email)

                    Teacher.objects.update_or_create(
                        email=email,
                        defaults={'name': name}
                    )

                Teacher.objects.exclude(email__in=csv_teacher_emails).delete()

                messages.success(request, '教師資料已成功匯入。')
            except Exception as e:
                messages.error(request, f'處理檔案時發生錯誤: {e}')

    return render(request, 'grades/teacher_management.html', {
        'message': message,
        'is_manager': is_manager,
        'teachers': teachers  # 傳遞教師資料
    })



#############################################################


#教師頁面
@login_required
def teacher(request):
    user_email = request.user.email

    if not Teacher.objects.filter(email=user_email).exists():
        message = "您不具備老師身份，請通知管理員"
        is_teacher = False
    else:
        # 獲取當前用戶的老師資料
        teacher = Teacher.objects.get(email=user_email)
        message = f"{teacher.name}老師，您好"
        is_teacher = True

    return render(request, 'grades/teacher.html', {'message': message, 'is_teacher': is_teacher})

# 創建課程
@login_required
def create_course(request):
    user_email = request.user.email

    # 檢查是否為老師
    try:
        teacher = Teacher.objects.get(email=user_email)
    except Teacher.DoesNotExist:
        return redirect('teacher')


    if request.method == 'POST':
        course_name = request.POST.get('course_name')

        # 創建新的課程，只新增課程名稱
        course = Course.objects.create(name=course_name, teacher=teacher)

        messages.success(request, '課程已成功創建！')
        return redirect('course_list')

    return render(request, 'grades/create_course.html',{'messages' : messages})


# 編輯課程名稱
@login_required
def edit_course_name(request, course_id):
    user_email = request.user.email
    
    # 檢查是否為老師
    try:
        teacher = Teacher.objects.get(email=user_email)
    except Teacher.DoesNotExist:
        return redirect('teacher')

    # 查找該老師的課程
    course = get_object_or_404(Course, id=course_id, teacher=teacher)

    if request.method == 'POST':
        # 更新課程名稱
        course_name = request.POST.get('course_name')
        course.name = course_name
        course.save()
        messages.success(request, '課程名稱已成功更新！')
        return redirect('edit_course_name', course_id=course.id,)

    return render(request, 'grades/edit_course_name.html', {
        'course': course,
    })

#編輯課程學生名單
@login_required
def edit_course_students(request, course_id):
    user_email = request.user.email


    # 確保當前使用者是這門課程的老師
    try:
        teacher = Teacher.objects.get(email=user_email)
    except Teacher.DoesNotExist:
        return redirect('teacher')


    # 查找該老師的課程
    course = get_object_or_404(Course, id=course_id, teacher=teacher)

    if request.method == 'POST':
        # 更新選擇的學生
        selected_students_ids = request.POST.getlist('students')
        if selected_students_ids:
            students = Student.objects.filter(id__in=selected_students_ids)
            course.students.set(students)  # 更新學生，會新增和移除對應的學生
            messages.success(request, '課程學生名單已成功更新！')
            return redirect('edit_course_students', course_id=course.id)

    # 獲取所有學生資料，並根據班級分組
    students = Student.objects.all()
    students_by_class = {}
    for student in students:
        students_by_class.setdefault(student.class_name, []).append(student)

    return render(request, 'grades/edit_course_students.html', {
        'course': course,
        'students_by_class': students_by_class,
    })

# 顯示課程學生名單
@login_required
def show_course_members(request, course_id):
    user_email = request.user.email

    # 確保當前使用者是這門課程的老師
    try:
        teacher = Teacher.objects.get(email=user_email)
    except Teacher.DoesNotExist:
        return redirect('teacher')

    # 查找該老師的課程
    course = get_object_or_404(Course, id=course_id, teacher=teacher)

    # 獲取課程成員
    students = course.students.all()

    return render(request, 'grades/show_course_members.html', {
        'course': course,
        'students': students,
    })

################################################################

# 老師個人課程列表
@login_required
def course_list(request):
    user_email = request.user.email

    # 檢查是否為老師
    try:
        teacher = Teacher.objects.get(email=user_email)
    except Teacher.DoesNotExist:
        return redirect('teacher')

    # 取得老師所創建的課程
    teacher = Teacher.objects.get(email=user_email)
    courses = Course.objects.filter(teacher=teacher)

    return render(request, 'grades/course_list.html', {'courses': courses, 'teacher': teacher})

# 更新課程順序
@csrf_exempt
def update_course_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order = data.get('order', [])
        for index, course_id in enumerate(order):
            Course.objects.filter(id=course_id).update(order=index)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)
    

# 刪除課程
@login_required
def delete_course(request, course_id):
    user_email = request.user.email

    # 檢查是否為老師
    try:
        teacher = Teacher.objects.get(email=user_email)
    except Teacher.DoesNotExist:
        return redirect('teacher')

    # 確保老師只能刪除自己的課程
    course = get_object_or_404(Course, id=course_id, teacher=teacher)

    if request.method == 'POST':
        course.delete()
        messages.success(request, '課程已成功刪除！')
        return redirect('course_list')

    return render(request, 'grades/delete_course.html', {'course': course})
    

################################################################

# 管理成績頁面
@login_required
def manage_grades(request, course_id):
    user_email = request.user.email

    # 檢查是否為老師
    try:
        teacher = Teacher.objects.get(email=user_email)
    except Teacher.DoesNotExist:
        return redirect('teacher')

    course = get_object_or_404(Course, id=course_id)

    # 取得類別篩選的選項，並篩選成績項目
    selected_category = request.GET.get('category', '')  # 從GET參數中取得選擇的類別

    if selected_category:  # 如果選擇了某個類別，篩選成績項目
        grade_items = GradeItem.objects.filter(course=course, category=selected_category)
    else:
        grade_items = GradeItem.objects.filter(course=course)  # 顯示所有成績項目

    # 匯出Excel
    if 'export' in request.GET:
        return export_grades_to_excel(course, grade_items)

    # 匯入Excel
    if request.method == 'POST' and 'import' in request.POST:
        if 'excel_file' not in request.FILES:
            messages.error(request, '請上傳一個Excel檔案')
            return redirect('manage_grades', course_id=course.id)

        excel_file = request.FILES['excel_file']
        success, message = import_grades_from_excel(excel_file, course)
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)  # 使用 error 標籤
        return redirect('manage_grades', course_id=course.id)

    # 表單提交處理，新增成績項目
    if request.method == 'POST' and 'add_grade_item' in request.POST:
        form = GradeItemForm(request.POST)
        if form.is_valid():
            grade_item = form.save(commit=False)
            grade_item.course = course
            # 設置 order 為當前課程中最大 order 值加一
            max_order = GradeItem.objects.filter(course=course).aggregate(max_order=models.Max('order'))['max_order']
            grade_item.order = (max_order or 0) + 1
            try:
                grade_item.save()
                messages.success(request, '成績項目已成功新增')
            except DbIntegrityError as e:
                if 'UNIQUE constraint failed' in str(e) or '23505' in str(e):
                    messages.error(request, '成績項目名稱已存在，請使用不同的名稱')
                else:
                    messages.error(request, '發生錯誤，請稍後再試')
            return redirect('manage_grades', course_id=course.id)
    else:
        form = GradeItemForm()

    return render(request, 'grades/manage_grades.html', {
        'course': course,
        'grade_items': grade_items,
        'form': form,
        'category_choices': GradeItem.GRADE_CATEGORY_CHOICES,  # 傳遞類別選項到模板
        'selected_category': selected_category,  # 傳遞當前選擇的類別到模板
    })


# 匯入成績到 Excel
def import_grades_from_excel(excel_file, course):
    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        return False, f'無法讀取Excel檔案: {str(e)}'

    required_columns = ['學號']
    if not all(col in df.columns for col in required_columns):
        return False, 'Excel檔案格式不正確，缺少必要的欄位：學號'

    for index, row in df.iterrows():
        student_id = row['學號']
        student = Student.objects.filter(student_id=student_id).first()
        if not student:
            continue

        for grade_item in GradeItem.objects.filter(course=course):
            column_name = grade_item.name
            if column_name in row.index:
                grade_value = row[column_name]
                if pd.notna(grade_value):
                    try:
                        # 檢查成績是否為數字，忽略文字欄位
                        grade_value = float(grade_value)
                    except ValueError:
                        return False, f'成績值無效：{grade_value} 不是有效的數字'
                else:
                    grade_value = None  # 將成績設為空白

                grade, created = Grade.objects.get_or_create(student=student, grade_item=grade_item)
                if grade.grade != grade_value:
                    grade.grade = grade_value
                    try:
                        grade.save()
                        print(f'成績已更新: 學號={student_id}, 項目={column_name}, 成績={grade_value}')
                    except ValidationError as e:
                        return False, f'儲存成績時發生錯誤：{str(e)}'
                else:
                    print(f'成績未變更: 學號={student_id}, 項目={column_name}, 成績={grade_value}')
    
    return True, '成績已成功匯入'

# 匯出成績到 Excel
def export_grades_to_excel(course, grade_items):
    # 準備數據
    data = []
    for student in course.students.all():
        student_data = {
            '班級': student.class_name,
            '座號': student.seat_number,
            '學號': student.student_id,
            '姓名': student.name,
        }
        for grade_item in grade_items:
            grade = Grade.objects.filter(student=student, grade_item=grade_item).first()
            student_data[grade_item.name] = grade.grade if grade else ''
        data.append(student_data)

    # 創建DataFrame
    df = pd.DataFrame(data)

    # 創建HttpResponse
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={course.name}_grades.xlsx'

    # 將DataFrame寫入Excel
    df.to_excel(response, index=False)

    return response

# 更新成績項目順序
@csrf_exempt
def update_grade_item_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order = data.get('order', [])
        for index, grade_item_id in enumerate(order):
            GradeItem.objects.filter(id=grade_item_id).update(order=index)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)




# 編輯項目成績名稱
@login_required
def edit_grade_item(request, course_id, grade_item_id):
    user_email = request.user.email
    # 檢查是否為老師
    try:
        teacher = Teacher.objects.get(email=user_email)
    except Teacher.DoesNotExist:
        return redirect('teacher')
        
    course = get_object_or_404(Course, id=course_id)
    grade_items = GradeItem.objects.filter(course=course)
    grade_item = get_object_or_404(GradeItem, id=grade_item_id)
    if request.method == 'POST':
        form = GradeItemForm(request.POST, instance=grade_item)
        if form.is_valid():
            form.save()
            return redirect('manage_grades', course_id=course_id)
    else:
        form = GradeItemForm(instance=grade_item)

    return render(request, 'grades/edit_grade_item.html', {
        'form': form,
        'course_id': course_id,
    })

# 刪除成績項目
@login_required
def delete_grade_item(request, course_id, grade_item_id):
    user_email = request.user.email
    # 檢查是否為老師
    try:
        teacher = Teacher.objects.get(email=user_email)
    except Teacher.DoesNotExist:
        return redirect('teacher')
        
    grade_item = get_object_or_404(GradeItem, id=grade_item_id)
    grade_item.delete()
    return redirect('manage_grades', course_id=course_id)

################################################################

# 管理學生項目成績頁面
@login_required
def manage_student_grades(request, course_id, grade_item_id):
    user_email = request.user.email
    # 檢查是否為老師
    try:
        teacher = Teacher.objects.get(email=user_email)
    except Teacher.DoesNotExist:
        return redirect('teacher')
        
    grade_item = get_object_or_404(GradeItem, id=grade_item_id)
    students = grade_item.course.students.all()

    if request.method == 'POST':
        if 'grades' in request.POST:
            grades_input = request.POST.get('grades')
            if grades_input:
                grades_list = grades_input.splitlines()  # 按行分割輸入的成績
                
                # 檢查成績數量與學生數量是否相符
                if len(grades_list) != students.count():
                    messages.warning(request, '輸入的成績數量與學生數量不符！請重新確認。')
                else:
                    for student, grade_value in zip(students, grades_list):
                        grade_value = grade_value.strip()  # 去除前後空白
                        grade, created = Grade.objects.get_or_create(student=student, grade_item=grade_item)
                        if grade_value:  # 確保不為空
                            try:
                                grade.grade = float(grade_value)  # 嘗試轉換為浮點數
                            except ValueError:
                                continue  # 如果轉換失敗，則跳過該成績
                        else:
                            grade.grade = None  # 將成績設為空白
                        grade.save()
                    
                    # 添加成功消息
                    messages.success(request, '成績已成功更新！')
        elif 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            success, message = import_grades_from_excel(excel_file, grade_item)
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)

    return render(request, 'grades/manage_student_grades.html', {
        'grade_item': grade_item,
        'students': students,
    })


# 處理單一學生成績修改
@login_required
def edit_student_grade(request, grade_item_id, student_id):
    user_email = request.user.email
    # 檢查是否為老師
    try:
        teacher = Teacher.objects.get(email=user_email)
    except Teacher.DoesNotExist:
        return redirect('teacher')
    
    grade_item = get_object_or_404(GradeItem, id=grade_item_id)
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        single_grade = request.POST.get('single_grade')
        grade, created = Grade.objects.get_or_create(student=student, grade_item=grade_item)
        if single_grade:
            try:
                # 將成績轉換為浮點數
                single_grade = float(single_grade)
                grade.grade = single_grade
                grade.save()
                messages.success(request, f'{student.name} 的成績已成功更新為 {single_grade}！')
            except ValueError:
                messages.warning(request, '成績輸入無效，請輸入一個有效的數字。')
        else:
            grade.grade = None  # 將成績設為空白
            grade.save()
            messages.success(request, f'{student.name} 的成績已成功清空！')

    return redirect('manage_student_grades', course_id=grade_item.course.id, grade_item_id=grade_item_id)
#################################################################

# 學生頁面
@login_required
def student(request):
    user_email = request.user.email
    student = Student.objects.filter(student_email=user_email).first()
    
    if not student:
        message = "未找到學生資料"
        return render(request, 'grades/student.html', {'message': message})

    courses = student.course_set.all()  # 獲取學生所修的課程
    grade_items = []
    grade_category = request.POST.get("grade_category", "homework")  # 預設選擇 homework

    if request.method == "POST":
        course_id = request.POST.get("course")
        if course_id:
            course = Course.objects.get(id=course_id)
            grade_items = GradeItem.objects.filter(course=course, category=grade_category).prefetch_related('grade_set')

            # 為每個成績項目檢查學生的成績
            for grade_item in grade_items:
                student_grade = None
                for grade in grade_item.grade_set.all():
                    if grade.student.id == student.id:
                        student_grade = grade.grade
                        break  # 找到成績後結束迴圈
                # 將成績或 "尚無成績" 的結果加入到每個 grade_item 中
                grade_item.student_grade = student_grade if student_grade is not None else "尚無成績"

    return render(request, 'grades/student.html', {
        'message': f"您好，{student.name}同學",
        'courses': courses,
        'grade_items': grade_items,
        'student': student,  # 傳遞學生物件以便在模板中使用
        'grade_category': grade_category,  # 傳遞當前選擇的成績類型
    })

##############################################

# Line Bot
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, MessageEvent, TextMessage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from linebot.exceptions import InvalidSignatureError
from decouple import config
from .models import Student, OTPVerification

from django.core.mail import send_mail
from django.conf import settings

from django.utils import timezone
from datetime import timedelta

# 使用 decouple 讀取環境變數
line_bot_api = LineBotApi(config('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(config('LINE_CHANNEL_SECRET'))

# 生成 OTP 並發送郵件
import random
from django.core.mail import send_mail

# 生成 6 位數的 OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# 發送 OTP 到指定的 email
def send_otp_to_email(email, otp):
    subject = '您的驗證碼'
    message = f'您的一次性密碼（OTP）是: {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL  # 使用 settings 中的 DEFAULT_FROM_EMAIL
    
    send_mail(subject, message, from_email, [email])

# 儲存或更新 OTP 到資料庫
def save_otp(user_id, email, otp):
    otp_record, created = OTPVerification.objects.update_or_create(
        line_user_id=user_id,
        defaults={'email': email, 'otp': otp}
    )
    
    # 更新 created_at 時間
    if not created:
        otp_record.created_at = timezone.now()  # 手動更新 created_at
        otp_record.save()  # 保存更改


# 處理從 LINE Bot 發來的 Webhook 請求
@csrf_exempt
def line_webhook(request):
    if request.method == 'POST':
        signature = request.META.get('HTTP_X_LINE_SIGNATURE', '')
        body = request.body.decode('utf-8')
        
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponse(status=403)
        
        return HttpResponse(status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

from linebot.models import CarouselTemplate, CarouselColumn, TemplateSendMessage, MessageAction

# 處理 LINE 的訊息
# 'homework': '作業成績',
# 'quiz': '平時考成績',
# 'exam': '段考成績',
# 'general performance': '平時成績',
# 'overall score': '總成績',
# 'authentication': '認證',
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id  # 獲取 LINE 使用者 ID
    message_text = event.message.text.strip().lower()  # 將訊息轉換為小寫

    # 中英文成績類型映射
    grade_category_map = {
        'homework': '作業成績',
        'quiz': '平時考成績',
        'exam': '段考成績',
        'general performance': '平時成績',
        'overall score': '總成績',
    }

    # 如果訊息內容是 "authentication" 或包含 '@'，則進行 OTP 認證邏輯
    if message_text == "authentication":
        # 如果使用者已經綁定 line_user_id，刪除舊的綁定資料
        try:
            student = Student.objects.get(line_user_id=user_id)
            student.line_user_id = None  # 解除舊的綁定
            student.save()
        except Student.DoesNotExist:
            pass  # 如果不存在就忽略，繼續進行認證

        # 提示輸入 email 進行重新綁定驗證
        reply_text = "請輸入您的 email，我們將寄送驗證信給您！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

    elif '@' in message_text:
        # 如果使用者輸入的是電子郵件地址，查找該 email 是否在 Student 資料表中
        try:
            student = Student.objects.get(student_email=message_text)  # 使用 student_email 欄位查詢
            # 獲取最近的 OTP 紀錄
            try:
                otp_record = OTPVerification.objects.get(line_user_id=user_id)  # 使用 line_user_id 查詢
                time_since_last_otp = timezone.now() - otp_record.created_at

                if time_since_last_otp < timedelta(seconds=30):
                    reply_text = "請在 30 秒後再請求新的驗證碼。"
                else:
                    # 如果找到該 email，生成 OTP 並發送到該 email
                    otp = generate_otp()  # 生成 OTP
                    save_otp(user_id, message_text, otp)  # 儲存或更新 OTP 到資料庫
                    send_otp_to_email(message_text, otp)  # 發送 OTP 到 email
                    reply_text = "已發送驗證碼到您的電子郵件，請輸入驗證碼。"
            
            except OTPVerification.DoesNotExist:
                # 如果沒有找到 OTP 紀錄，則直接生成並發送 OTP
                otp = generate_otp()  # 生成 OTP
                save_otp(user_id, message_text, otp)  # 儲存或更新 OTP 到資料庫
                send_otp_to_email(message_text, otp)  # 發送 OTP 到 email
                reply_text = "已發送驗證碼到您的電子郵件，請輸入驗證碼。"

        except Student.DoesNotExist:
            # 如果該 email 不存在於 Student 資料表中
            reply_text = "此 email 不在我們的資料庫當中，請確認後再試。"
            
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))


    elif message_text.isdigit() and len(message_text) == 6:
        # 如果使用者輸入的是 6 位數的驗證碼
        try:
            otp_record = OTPVerification.objects.get(line_user_id=user_id, otp=message_text)
            # 驗證成功，綁定 line_user_id 和 student_email
            student = Student.objects.get(student_email=otp_record.email)
            student.line_user_id = user_id  # 更新 line_user_id 綁定
            student.save()
            reply_text = f"恭喜恭喜！驗證成功，「{student.name}」同學的帳戶已經綁定！"
        except OTPVerification.DoesNotExist:
            reply_text = "驗證失敗，請確認您的驗證碼是否正確。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

    else:
        # 檢查 line_user_id 是否存在於資料庫中
        try:
            student = Student.objects.get(line_user_id=user_id)

            if message_text in grade_category_map:
                # 儲存最近選擇的成績類型到資料庫
                student.last_category = message_text
                student.save()

                # 顯示課程選擇，使用 CarouselTemplate
                courses = student.course_set.all()
                if courses.exists():
                    columns = []
                    for course in courses:
                        teacher_name = course.teacher.name  # 取得老師的名字
                        columns.append(
                            CarouselColumn(
                                text=f"{teacher_name}老師的{course.name} - {grade_category_map[message_text]}",
                                actions=[
                                    MessageAction(label=f"選擇 {course.name}", text=course.name)
                                ]
                            )
                        )
                    
                    carousel_template = CarouselTemplate(columns=columns)
                    template_message = TemplateSendMessage(
                        alt_text='請選擇課程', template=carousel_template
                    )
                    line_bot_api.reply_message(event.reply_token, template_message)
                else:
                    reply_text = f"「{student.name}」同學目前沒有選修任何課程。"
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

            elif message_text in get_all_course_names():
                course = Course.objects.get(name=message_text)

                # 使用學生最近選擇的成績類型
                grade_category = student.last_category

                # 獲取對應的中文成績類型名稱
                grade_category_chinese = grade_category_map.get(grade_category, grade_category)

                grades = Grade.objects.filter(
                    student=student,
                    grade_item__course=course,
                    grade_item__category=grade_category
                ).order_by('grade_item__order')  # 根據 grade_item 的 order 欄位排序

                if grades.exists():
                    teacher_name = course.teacher.name  # 取得老師的名字
                    reply_text = f"「{student.name}」在「{course.name}」的{grade_category_chinese}如下：\n"  # 使用中文顯示成績類型
                    for grade in grades:
                        reply_text += f"{grade.grade_item.name}: {grade.grade}\n"
                else:
                    reply_text = f"「{student.name}」在「{course.name}」目前沒有{grade_category_chinese}。"

                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

            else:
                reply_text = f"歡迎「{student.name}」 同學使用本成績查詢系統，請利用選單功能查詢成績"
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

        except Student.DoesNotExist:
            # 如果 line_user_id 不存在，提示進行身份驗證
            reply_text = "請點選身份驗證按鈕，進行身份認證。"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))


def get_all_course_names():
    """獲取所有課程名稱的列表"""
    return [course.name for course in Course.objects.all()]
