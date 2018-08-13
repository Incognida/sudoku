from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError


def validate_number(value):
    if value == 0:
        raise ValidationError("Value must be > 0")


class SudokuTable(models.Model):
    solved_table = ArrayField(
        ArrayField(models.IntegerField(), max_length=9), max_length=9,
    )
