# EGE Django Theme

```
pip install ege-theme
```

Em ```settings.py```:

Adicione a aplicação,```ege_theme```, à variável de configuração ```INSTALLED_APPS``` antes das aplicações do django:

```
INSTALLED_APPS = 'ege_theme',
                 'django.contrib.admin',
                 'django.contrib.auth',
                 ......................
```
  
Certifique-se de que está setada a variável ```STATIC_URL = '/static/'```.
