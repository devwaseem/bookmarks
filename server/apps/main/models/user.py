import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager[AbstractUser]):
    """Manager class for User."""

    use_in_migrations = True

    def create_user(
        self,
        email: str,
        password: str,
        **extra_fields,
    ) -> "User":
        """Create a Normal User."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self,
        email=None,
        password=None,
        **extra_fields,
    ) -> "User":
        """Create a SuperUser with all the privileges."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields) -> "User":
        """Create and save a user with the given username, email, and password."""  # noqa: E501
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = User(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """User class."""

    internal_id = models.AutoField(primary_key=True)
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    username = None  # type:ignore
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []
    objects = UserManager()  # type:ignore
