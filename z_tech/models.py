from django.db import models
from django.shortcuts import resolve_url

from accounts.models import Profile


class Tech(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=10)
    url = models.URLField()

    # 연도별 로드맵
    year = models.PositiveIntegerField(default=0)
    # 올해 모은 돈
    money = models.PositiveIntegerField(default=0)
    # 올해 목표 저축액
    goal = models.PositiveIntegerField(default=0)

    # 진행도
    class Percent(models.IntegerChoices):
        zero = 0
        one = 10
        two = 20
        three = 30
        four = 40
        five = 50
        six = 60
        seven = 70
        eight = 80
        nine = 90
        ten = 100

    percent = models.IntegerField(choices=Percent.choices, default='zero')

    # 돈을 모아야 하는 이유
    reason = models.CharField(max_length=100)

    # 돈을 어떻게 벌고 있는지
    # 매달 들어오는 돈
    deposit = models.PositiveIntegerField(default=0)
    # 현재까지 번 돈
    gather = models.PositiveIntegerField(default=0)
    # 올해 예상 수입
    expectation = models.PositiveIntegerField(default=0)

    # 수익 타입
    Type = (
        ('fixed', '고정 수입'),
        ('non-fixed', '비고정 수입'),
        ('interest', '이자'),
        ('dividend', '배당금'),
    )

    type = models.CharField(max_length=30, choices=Type, default='fixed',)

    # 지출
    item = models.CharField(max_length=10)
    # 지출 금액
    spending = models.PositiveIntegerField(default=0)

    # 지출 태그
    Tag = (
        ('purpose', '목적성 저축'),
        ('housing', '주거비'),
        ('fixed-expenses', '고정 지출'),
        ('variable-spending', '비고정 지출'),
    )

    tag = models.CharField(max_length=30, choices=Tag, default='purpose',)

    def __str__(self):
        return f'{self.name} : {self.url}'

    def get_absolute_url(self):
        return resolve_url('z_tech:detail', pk=self.pk)
