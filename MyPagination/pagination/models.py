from django.db import models


class SchoolInfo(models.Model):
    id = models.AutoField(primary_key=True)  # 使用 AutoField 字段
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        # 创建字段索引
        indexes = [models.Index(fields=['name'], name='school_name')]
        # 按字段排序，保证分页一致性
        ordering = ('-name',)


class StudentInfo(models.Model):
    id = models.AutoField(primary_key=True)  # 使用 AutoField 字段
    name = models.CharField(max_length=10)
    year = models.IntegerField()
    email = models.EmailField(unique=True, db_index=True)  # 创建字段索引
    school = models.ForeignKey(SchoolInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + self.email

    class Meta:
        # 按字段排序，保证分页一致性
        ordering = ('-name',)
