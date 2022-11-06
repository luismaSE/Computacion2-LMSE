from celery import Celery

app = Celery("calculo_matriz_celery", broker='redis://localhost:6379/0', backend='redis://localhost:6379',include='calculo_matriz_celery') 