import environ

BASE_DIR = environ.Path(__file__) - 1

env = environ.Env()

DEBUG = env.bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = []
SECRET_KEY = "none"

INSTALLED_APPS = [
    "djangocms_admin_style",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "cms",
    "menus",
    "treebeard",
    "sekizai",
    "djangocms_text_ckeditor",
    "djangocms_snippet",
    "djangocms_style",
    "djangocms_column",
    "cms_forms",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
    "cms.middleware.utils.ApphookReloadMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR.path("templates"))],
        "OPTIONS": {
            "debug": DEBUG,
            "loaders": ["django.template.loaders.filesystem.Loader", "django.template.loaders.app_directories.Loader",],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "cms.context_processors.cms_settings",
                "sekizai.context_processors.sekizai",
            ],
        },
    }
]

CMS_TEMPLATES = [
    ("base.html", "Base template"),
]

MEDIA_ROOT = str(BASE_DIR("shared/media"))
MEDIA_URL = "/media/"

STATIC_ROOT = str(BASE_DIR("shared/static/"))
STATIC_URL = "/static/"

ROOT_URLCONF = "installation.urls"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR("shared/db.sqlite3"),}}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Warsaw"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [("en-us", "English")]

TEST_RUNNER = "common.pytestrunner.PytestTestRunner"

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": "plugin_forms",}}

CMS_CACHE_DURATIONS = {
    "content": 60 * 60,
    "menus": 60 * 60,
    "permissions": 60 * 60,
}

# You can customize registered form plugins
from cms_forms import config_defaults  # noqa

CMS_FORMS_REGISTER_PLUGINS = True
CMS_FORM_PLUGINS = config_defaults.FORM_PLUGINS[:]
CMS_FIELD_PLUGINS = config_defaults.FIELD_PLUGINS[:]
CMS_WIDGET_PLUGINS = config_defaults.WIDGET_PLUGINS[:]
CMS_CHOICE_OPTION_PLUGINS = config_defaults.CHOICE_OPTION_PLUGINS[:]
CMS_CHOICE_FIELD_PLUGINS = config_defaults.CHOICE_FIELD_PLUGINS[:]
CMS_BUTTON_PLUGINS = config_defaults.BUTTON_PLUGINS[:]
