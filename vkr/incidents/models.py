from django.db import models
from django.contrib.auth.models import User


class Basis(models.Model):
    description = models.CharField("Описание", max_length=200)

    def __str__(self) -> str:
        return self.description

    class Meta:
        verbose_name = "Базис"
        verbose_name_plural = "Базисы"


class Critery(models.Model):
    description = models.CharField("Описание", max_length=200)

    def __str__(self) -> str:
        return self.description

    class Meta:
        verbose_name = "Критерий"
        verbose_name_plural = "Критерии"


class Strategy(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Стратегия"
        verbose_name_plural = "Стратегии"


class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username

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
    results = models.JSONField("Результаты")

    creator_id = models.ForeignKey(Expert, on_delete=models.CASCADE,
                                   related_name="authored_incidents")
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

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
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    basis = models.ForeignKey(Basis, on_delete=models.CASCADE)
    basis_number = models.PositiveSmallIntegerField()


class IncidentCritery(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    critery = models.ForeignKey(Critery, on_delete=models.CASCADE)
    critery_number = models.PositiveSmallIntegerField()


class IncidentStrategy(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    strategy_number = models.PositiveSmallIntegerField()


class IncidentExpert(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    expert_number = models.PositiveSmallIntegerField()
