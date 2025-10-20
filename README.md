# Подготовка виртуальной машины

## Склонируйте репозиторий

Склонируйте репозиторий проекта:

```
git clone https://github.com/kruglikovAlex/mle-pr-final.git
```

## Активируйте виртуальное окружение

Используйте то же самое виртуальное окружение, что и созданное для работы с уроками. Если его не существует, то его следует создать.

Создать новое виртуальное окружение можно командой:

```
python3 -m venv eenv_pr_final
```

После его инициализации следующей командой

```
. env_pr_final/bin/activate
```

установите в него необходимые Python-пакеты следующей командой

```
pip install -r requirements.txt
```

### Скачайте файлы с данными

Для начала работы понадобится три файла с данными: https://disk.yandex.ru/d/XPthmNk_pqEDaQ

## Запустите Jupyter Lab

Запустите Jupyter Lab в командной строке

```
jupyter lab --ip=0.0.0.0 --no-browser
```

# Расчёт рекомендаций

Код для выполнения первой части проекта находится в файле `final_project.ipynb`. Изначально, это шаблон. Используйте его для выполнения первой части проекта.

# Сервис рекомендаций
Каждая инструкция выполняется из директории репозитория mle-pr-final
Если необходимо перейти в поддиректорию, напишите соотвесвтующую команду

Код сервиса рекомендаций находится в файлах `events_service.py`, `features_service.py`, `recommendations.py`, `recommendations_service.py`.

## 1. микросервис mlflow для загрузки актуальной ML модели в микросервис прогнозирования
```python

cd services
cd mlflow_server
# создание виртуального окружения
python3 -m venv .venv_mlflow
source .venv_mlflow/bin/activate
# установки необходимых библиотек 
pip3 install -r requirements.txt
# установка разрешений
sudo chmod +x ./run_mlflow_registry.sh
# запуск сервиса
./run_mlflow_registry.sh
```
(http://127.0.0.1:5000)

## 2. Инструкции для запуска сервиса рекомендаций
```python

cd services\ml_service
# запуск сервиса off-line рекомендаций
uvicorn features_service:app --reload --port 8081 --host 0.0.0.0
# запуск сервиса on-line рекомендаций
uvicorn events_service:app --reload --port 8082 --host 0.0.0.0
# запуск сервиса рекомендаций
uvicorn recommendation_service:app --reload --port 8088 --host 0.0.0.0
# 
```

## 2. FastAPI микросервис в Docker-контейнере

```bash
# команда перехода в нужную директорию
cd services
cd ml_service
# команда для запуска микросервиса в режиме docker compose
docker image build . --tag ml_service_image:1 -f Dockerfile
docker compose up --build
```

# Инструкции для тестирования сервиса

Код для тестирования сервиса находится в файле `/services/ml_service/test_uvicorn/test_service.py`
```python

# запуск кода для тестирования
python3 test_service.py
#
```

# Лог файлы:
/service/test_service.log - логирование результатов тестирования
/service/test_service_offline.log - логирование работы сервиса off-line рекомендаций
/service/test_service_online.log - логирование работы сервиса on-line рекомендаций
/service/test_service_recommend.log - логирование различных методов сервиса рекомендаций (отдельно)