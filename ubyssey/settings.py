# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&t7b#38ncrab5lmpe#pe#41coa-8ctwuy@tm0!x8*n_r38x_m*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dispatch',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
