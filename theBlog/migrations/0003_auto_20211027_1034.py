# Generated by Django 3.2.7 on 2021-10-27 04:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('theBlog', '0002_alter_post_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='postLikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='theBlog.customuser')),
                ('nickName', models.CharField(blank=True, max_length=20, null=True)),
                ('profilePhoto', models.ImageField(blank=True, null=True, upload_to='Profile Photo/')),
                ('religion', models.CharField(blank=True, choices=[('Christianity', 'Christianity'), ('Islam', 'Islam'), ('Atheist', 'Atheist'), ('Hinduism', 'Hinduism'), ('Buddhism', 'Buddhism'), ('Ethnic', 'Ethnic'), ('Sikhism', 'Sikhism'), ('Spiritism', 'Spiritism'), ('Judaism', 'Judaism'), ('Jainism', 'Jainism'), ('Shinto', 'Shinto'), ('Cao Dai', 'Cao Dai'), ('Zoroastrianism', 'Zoroastrianism'), ('Tenrikyo', 'Tenrikyo'), ('Animism', 'Animism'), ('Neo-Paganism', 'Neo-Paganism'), ('Unitarian', 'Unitarian'), ('Rastafari', 'Rastafari'), ('Other', 'Other')], max_length=20, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=20, null=True)),
                ('highSchool', models.CharField(blank=True, max_length=100, null=True)),
                ('college', models.CharField(blank=True, max_length=100, null=True)),
                ('university', models.CharField(blank=True, max_length=100, null=True)),
                ('worksAt', models.CharField(blank=True, max_length=100, null=True)),
                ('parmanentAddress', models.CharField(blank=True, max_length=200, null=True)),
                ('currentAddress', models.CharField(blank=True, max_length=200, null=True)),
                ('about', models.CharField(blank=True, max_length=500, null=True)),
                ('followers', models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
