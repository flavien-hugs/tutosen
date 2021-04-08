# [tutosen](https://github.com/flavien-hugs/tutosen.git) - Online Learning Platform

[![tutosen](https://img.shields.io/badge/tutosen-build-orange.svg)](https://www.tutosen.com/)
[![Django Version](https://img.shields.io/badge/Django-Version3-success.svg)](http://www.djangoproject.com)
[![Python Version](https://img.shields.io/badge/Python-3.6-brightgreen.svg)](https://www.python.com)

## Vision

Tuto-Sen est une plateforme web de mise en relation entre enseignants disposant du temps libre et
des étudiants en difficultés d’enseignements pour du tutorat.


## Installation

Nous utilisons ces technologies suivantes:

- Python/Django
- API Rest/djangorestframework
- Html/CSS/Javascript/
- Bootstrap 5.x
- JQuery
- Ajax

Pour pouvoir exécuter l'application, vous devez avoir installé _Python-3.8 ou supérieur_ dans votre système.
Nous utilisons **Pipenv** comme gestionnaire de dépendances, vous pouvez l'installer [ici](https://pipenv.pypa.io/en/latest/install/).

\*Note : Tous les membres de l'équipe doivent l'utiliser.
Une fois installé, vous devez exécuter ces commandes pour configurer le projet :

```shell
pipenv install
```

## Exécuter l'application

Assurez-vous de modifier les informations de la base de données `settings.py`

```bash
python manage.py migrate
python manage.py runserver

ou

make migratedb
```

Amusez-vous bien :) !

## License

Tous les droits sont réservés © [tutosen](https://www.tutosen.com)
