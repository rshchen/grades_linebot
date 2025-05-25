from django.db import models
from django.core.exceptions import ValidationError


# 9. 管理員資料
class Manager(models.Model):
    name = models.CharField(max_length=100)  # 管理員姓名
    email = models.EmailField()  # 管理員信箱

    def __str__(self):
        return self.name
        
# 8. 老師資料
class Teacher(models.Model):
    name = models.CharField(max_length=100)  # 老師姓名
    email = models.EmailField()  # 老師信箱

    def __str__(self):
        return self.name
        

# 學生
class Student(models.Model):
    class_name = models.CharField(max_length=50)  # 班級名稱
    seat_number = models.IntegerField()  # 座號
    student_id = models.CharField(max_length=36, unique=True)  # 學號，唯一
    name = models.CharField(max_length=100)  # 學生姓名
    student_email = models.EmailField()  # 學生信箱
    parent_email = models.EmailField(blank=True, null=True)  # 家長信箱，可以為空
    line_user_id = models.CharField(max_length=255,  unique=True, blank=True, null=True)  # 儲存LINE的user_id
    last_category = models.CharField(max_length=30, blank=True, null=True)  # 最近選擇的成績類型


    def __str__(self):
        return f"{self.name} ({self.class_name})"


# 課程
class Course(models.Model):
    name = models.CharField(max_length=100)  # 課程名稱
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # 課程的老師
    students = models.ManyToManyField(Student, blank=True)  # 課程的學生，可以為空
    order = models.IntegerField(default=0)  # 課程的順序

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


# 課程和學生的中介資料表
class CourseStudent(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)  # 選課的時間

    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.name}"





# 成績項目名稱，類似作業或考試
class GradeItem(models.Model):
    GRADE_CATEGORY_CHOICES = [
        ('homework', '作業'),
        ('exam', '段考'),
        ('quiz', '小考'),
        ('general performance',  '平時成績'),
        ('overall score', '總成績'),
    ]
    name = models.CharField(max_length=100)  # 成績項目名稱 (例如作業或考試名稱)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # 關聯到課程
    class_name = models.CharField(max_length=50)  # 班級名稱
    category = models.CharField(max_length=30, choices=GRADE_CATEGORY_CHOICES)  # 成績類型
    order = models.PositiveIntegerField(default=0)  # 成績項目的順序

    class Meta:
        ordering = ['order']
        unique_together = ('name', 'course')  # 確保每個課程中的成績項目名稱是唯一的
        
    def __str__(self):
        return f"{self.name} - {self.category} ({self.class_name}, {self.course})"

# 學生成績
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # 關聯到學生
    grade_item = models.ForeignKey(GradeItem, on_delete=models.CASCADE)  # 關聯到成績項目
    grade = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)  # 成績
    
    def __str__(self):
        return f"{self.student.name} - {self.grade_item.name} ({self.grade_item.category}): {self.grade}"



# OTP 資料庫
class OTPVerification(models.Model):
    line_user_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
