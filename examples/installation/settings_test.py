from .settings import *  # noqa


ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB", default="test"),
        "USER": env.str("POSTGRES_USER", default="test"),
        "PASSWORD": env.str("POSTGRES_PASSWORD", default="test"),
        "HOST": env.str("POSTGRES_HOST", default="postgres"),
        "PORT": env.str("POSTGRES_PORT", default="5432"),
        "ATOMIC_REQUESTS": env.bool("POSTGRES_ATOMIC", default=True),
    }
}
