# accounts.decorators.py

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def student_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="login"
):
    """Décorateur pour les vues qui vérifie que l'utilisateur connecté est un 
    étudiant, redirige vers la page de connexion si nécessaire."""

    actual_decorator = user_passes_test(
        lambda user: user.is_active and user.type,
        login_url=login_url, redirect_field_name=redirect_field_name,
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def teacher_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="login"
):
    """Décorateur pour les vues qui vérifie que l'utilisateur connecté est un enseignant,
    et redirige vers la page de connexion si nécessaire."""

    actual_decorator = user_passes_test(
        lambda user: user.is_active and user.type,
        login_url=login_url, redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def staff_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="login"
):
    """Décorateur pour les vues qui vérifie que l'utilisateur connecté est un staff/admin,
    et redirige vers la page de connexion si nécessaire."""

    actual_decorator = user_passes_test(
        lambda user: user.is_active and user.is_staff,
        login_url=login_url, redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def superuser_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="login"
):
    """Décorateur pour les vues qui vérifie que l'utilisateur connecté est un superutilisateur,
    et redirige vers la page de connexion si nécessaire."""

    actual_decorator = user_passes_test(
        lambda user: user.is_active and user.is_superuser,
        login_url=login_url, redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
