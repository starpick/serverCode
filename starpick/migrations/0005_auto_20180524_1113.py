# Generated by Django 2.0.4 on 2018-05-24 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('starpick', '0004_auto_20180516_0306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token', to='starpick.User')),
            ],
        ),
        migrations.AlterField(
            model_name='like',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='starpick.Entry'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='starpick.User'),
        ),
        migrations.AlterField(
            model_name='pick',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='picks', to='starpick.Entry'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='starpick.Entry'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='pick',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tag', to='starpick.Pick'),
        ),
    ]
