from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _

class RoundType(models.TextChoices):
    SEQUENTIAL = 'S', _('Sequential')
    BOARD = 'B', _('Board')

class QuestionType(models.TextChoices):
    NORMAL = 'N', _('Normal')
    MCQ = 'C', _('MCQ')
    ORDERING = 'O', _('Order')

class SlideType(models.TextChoices):
    TEXT = 'T', _('Text')
    IMAGE = 'I', _('Image')

class QuestionClass(models.TextChoices):
    SINGLE_ANSWER = 'S'
    CHOICE_ANSWER = 'C'