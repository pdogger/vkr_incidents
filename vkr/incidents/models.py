from django.contrib.auth.models import User
from django.db import models


class Criteria(models.Model):
    description = models.CharField("Описание", max_length=200)

    def __str__(self) -> str:
        return self.description

    class Meta:
        verbose_name = "Критерий ранжирования"
        verbose_name_plural = "Критерии ранжирования"


class Expert(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.get_full_name() + f" ({self.user.get_username()})"

    class Meta:
        verbose_name = "Эксперт"
        verbose_name_plural = "Эксперты"


class Status(models.Model):
    name = models.CharField("Наименование", max_length=100)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Incident(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    created_at = models.DateTimeField("Создан")
    results = models.TextField("Результаты", null=True, blank=True)

    creator = models.ForeignKey(
        Expert, verbose_name="Инициатор", on_delete=models.CASCADE,
        related_name="authored_incidents",
    )
    status = models.ForeignKey(Status, verbose_name="Статус", on_delete=models.CASCADE)

    criteries = models.ManyToManyField(Criteria, through="IncidentCriteria")
    experts = models.ManyToManyField(Expert, through="IncidentExpert")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Инцидент"
        verbose_name_plural = "Инциденты"


class Basis(models.Model):
    incident = models.ForeignKey(Incident, verbose_name="Инцидент", on_delete=models.CASCADE)

    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    number = models.PositiveSmallIntegerField("Номер")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Базис инцидента"
        verbose_name_plural = "Базисы инцидента"
        unique_together = ('incident', 'name')


class Strategy(models.Model):
    incident = models.ForeignKey(Incident, verbose_name="Инцидент", on_delete=models.CASCADE)

    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    number = models.PositiveSmallIntegerField("Номер")
    is_solution = models.BooleanField('Является решением', default=False)

    class Meta:
        verbose_name = "Стратегия устранения инцидента"
        verbose_name_plural = "Стратегии устранения инцидента"
        unique_together = ('incident', 'name')


class IncidentCriteria(models.Model):
    incident = models.ForeignKey(Incident, verbose_name="Инцидент", on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, verbose_name="Критерий", on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField("Номер")

    class Meta:
        verbose_name = "Критерий ранжирования инцидента"
        verbose_name_plural = "Критерии ранжирования инцидента"
        unique_together = ('incident', 'criteria')


class IncidentExpert(models.Model):
    incident = models.ForeignKey(Incident, verbose_name="Инцидент", on_delete=models.CASCADE)
    expert = models.ForeignKey(Expert, verbose_name="Эксперт", on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField("Номер")
    scores = models.TextField("Оценки", null=True, blank=True)

    class Meta:
        verbose_name = "Эксперт по инциденту"
        verbose_name_plural = "Эксперты по инциденту"
        unique_together = ('incident', 'expert')
