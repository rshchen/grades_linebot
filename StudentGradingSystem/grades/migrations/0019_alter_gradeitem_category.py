# Generated by Django 5.1.2 on 2024-10-16 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0018_alter_gradeitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gradeitem',
            name='category',
            field=models.CharField(choices=[('homework', '作業'), ('exam', '段考'), ('quiz', '小考'), ('general performance', '平時成績')], max_length=30),
        ),
    ]
