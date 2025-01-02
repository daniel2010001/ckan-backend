from datetime import timedelta
from pathlib import Path
from urllib.parse import ParseResult
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read environment variables from .env file
env = environ.Env()
environ.Env.read_env()

# Define the environment variables
SECRET_KEY: str = env.str(
    "SECRET_KEY",
    default="django-insecure-@zrjon_5sg0z*rutv+)7x2n_lg#v9+4^(dyc-&14q1%35c*_gw",
)
DEBUG: bool = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", [])

DATABASES = {
    "default": env.db(
        "DATABASE_URL", default="postgres://user:password@localhost:5432/dbname"
    )
}

CORS_ALLOWED_ORIGINS = env.list("CLIENTS_URL", default=["http://localhost:5173"])

CKAN_URL: ParseResult = env.url("CKAN_URL", default="http://localhost:5000")
CKAN_API_KEY: str = env.str("CKAN_API_KEY", default="your-ckan-api-key")

AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ["apps.users.utils.CustomBackend"]

MEDIA_URL = "/media/"
MEDIA_ROOT = (BASE_DIR / "media").absolute()

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",  # Django REST Framework
    "rest_framework_simplejwt",  # Autenticación JWT
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "apps.ckan",
    "apps.users",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
}

SIMPLE_JWT = {
    # Sliding token configuration
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=10),
    # "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=2),
    # Access and refresh token configuration
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    # Blacklist configuration
    "ROTATE_REFRESH_TOKENS": False,  # Rotar tokens de refresco en lugar de borrarlos
    "BLACKLIST_AFTER_ROTATION": False,  # Borrar tokens de refresco después de rotar
    "UPDATE_LAST_LOGIN": False,  # Actualizar la última fecha de inicio de sesión luego de rotar
    # JWT authentication configuration
    "AUTH_TOKEN_CLASSES": (  # Clases de token a utilizar para la autenticación
        "rest_framework_simplejwt.tokens.AccessToken",
        "rest_framework_simplejwt.tokens.SlidingToken",
    ),
    "LEEWAY": 0,  # Tiempo de espera para la validación de token
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "es"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
