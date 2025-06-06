# Generated by Django 5.1.1 on 2024-10-12 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0013_coursestudent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examitem',
            name='class_name',
        ),
        migrations.RemoveField(
            model_name='examitem',
            name='course',
        ),
        migrations.RemoveField(
            model_name='homeworkgrade',
            name='homework_item',
        ),
        migrations.RemoveField(
            model_name='homeworkgrade',
            name='student',
        ),
        migrations.RemoveField(
            model_name='homeworkitem',
            name='class_name',
        ),
        migrations.RemoveField(
            model_name='homeworkitem',
            name='course',
        ),
        migrations.CreateModel(
            name='GradeItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_name', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('homework', 'Homework'), ('exam', 'Exam'), ('quiz', 'Quiz')], max_length=10)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grades.course')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.DecimalField(decimal_places=2, max_digits=5)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grades.student')),
                ('grade_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grades.gradeitem')),
            ],
        ),
        migrations.DeleteModel(
            name='ExamGrade',
        ),
        migrations.DeleteModel(
            name='ExamItem',
        ),
        migrations.DeleteModel(
            name='HomeworkGrade',
        ),
        migrations.DeleteModel(
            name='HomeworkItem',
        ),
    ]
