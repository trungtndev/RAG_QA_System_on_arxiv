"""
Django settings for arxiv_rag project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

RESOURCES_DIR = Path('resources')
MEDIA_DIR = RESOURCES_DIR / 'media'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x3z=*u#rq-f=8ga=m78l9vt%(6inbxb$1ep76ewk#@ov6#v=58'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rag_core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.global_exception.GlobalExceptionMiddleware',
]

ROOT_URLCONF = 'arxiv_rag.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'arxiv_rag.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    "qdrant": {
        "url": None,
        "host": None,
        "port": None,
        'https': True,
        'location': ":memory:",
    }
}

RAG_CONFIG = {

    "DENSE_EMBEDDING": {
        "model_name": "hiieu/halong_embedding",
        "model_kwargs": {
            "device": "cuda",
            "trust_remote_code": True,
        },
        "encode_kwargs": {
        },
        "multi_process": False,
        "show_progress": False
    },

    "SPARSE_EMBEDDING": {
        "model_name": "Qdrant/BM25",
    },
    "QDRANT_VECTORSTORE": {
        "vector_name": "dense",
        "sparse_vector_name": "sparse",
        "retrieval_mode": "hybrid",  # dense, sparse, hybrid
        "collection_name": "pdf_collection",

    },

    "RETRIEVER": {
        "search_type": "similarity",
        "search_kwargs": {
            "k": 10,
        },
    },

    "LLM": {
        "model_id": "AITeamVN/Vi-Qwen2-1.5B-RAG",
        "model_kwargs": {
            "trust_remote_code": True,
        },
        "pipeline_kwargs": {
            "temperature": 1,
            "max_new_tokens": 200,
        },
        "task": "text-generation",
        "device": 0,
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
