from django.db import models
from django.contrib.auth.models import User


class Basis(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Базис"
        verbose_name_plural = "Базисы"


class Critery(models.Model):
    description = models.CharField("Описание", max_length=200)

    def __str__(self) -> str:
        return self.description

    class Meta:
        verbose_name = "Критерий ранжирования"
        verbose_name_plural = "Критерии ранжирования"


class Strategy(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Стратегия"
        verbose_name_plural = "Стратегии"


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
    results = models.JSONField("Результаты", null=True, blank=True)

    creator = models.ForeignKey(Expert, verbose_name="Инициатор", on_delete=models.CASCADE,
                                related_name="authored_incidents")
    status = models.ForeignKey(Status, verbose_name="Статус", on_delete=models.CASCADE)

    basises = models.ManyToManyField(Basis, through="IncidentBasis")
    criteries = models.ManyToManyField(Critery, through="IncidentCritery")
    strategies = models.ManyToManyField(Strategy, through="IncidentStrategy")
    experts = models.ManyToManyField(Expert, through="IncidentExpert")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Инцидент"
        verbose_name_plural = "Инциденты"


class IncidentBasis(models.Model):
    incident = models.ForeignKey(Incident, verbose_name="Инцидент", on_delete=models.CASCADE)
    basis = models.ForeignKey(Basis, verbose_name="Базис", on_delete=models.CASCADE)
    basis_number = models.PositiveSmallIntegerField("Номер")

    class Meta:
        verbose_name = "Базис инцидента"
        verbose_name_plural = "Базисы инцидента"


class IncidentCritery(models.Model):
    incident = models.ForeignKey(Incident, verbose_name="Инцидент", on_delete=models.CASCADE)
    critery = models.ForeignKey(Critery, verbose_name="Критерий", on_delete=models.CASCADE)
    critery_number = models.PositiveSmallIntegerField("Номер")

    class Meta:
        verbose_name = "Критерий ранжирования инцидента"
        verbose_name_plural = "Критерии ранжирования инцидента"


class IncidentStrategy(models.Model):
    incident = models.ForeignKey(Incident, verbose_name="Инцидент", on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, verbose_name="Стратегия", on_delete=models.CASCADE)
    strategy_number = models.PositiveSmallIntegerField("Номер")

    class Meta:
        verbose_name = "Стратегия устранения инцидента"
        verbose_name_plural = "Стратегии устранения инцидента"


class IncidentExpert(models.Model):
    incident = models.ForeignKey(Incident, verbose_name="Инцидент", on_delete=models.CASCADE)
    expert = models.ForeignKey(Expert, verbose_name="Эксперт", on_delete=models.CASCADE)
    expert_number = models.PositiveSmallIntegerField("Номер")
    scores = models.JSONField("Оценки", null=True, blank=True)

    class Meta:
        verbose_name = "Эксперт по инциденту"
        verbose_name_plural = "Эксперты по инциденту"
