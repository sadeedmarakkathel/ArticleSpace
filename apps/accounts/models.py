from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'ADMIN'
    EDITOR = 'EDITOR'
    VIEWER = 'VIEWER'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (EDITOR, 'Editor'),
        (VIEWER, 'Viewer'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=VIEWER,
    )

    def is_admin(self):
        return self.role == self.ADMIN

    def is_editor(self):
        return self.role == self.EDITOR

    def is_viewer(self):
        return self.role == self.VIEWER

    def __str__(self):
        return f"{self.username} ({self.role})"
