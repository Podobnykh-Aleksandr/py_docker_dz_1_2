# Для запуска проекта Stocks-Products в Docker контейнере необходимо выполнить следующие шаги:
## Создание образа:
docker build . --tag=some_image
## Запуск контейнера:
docker run -d -p 7978:6060 --name=container_stocks_products some_image
## Проверка работоспособности контейнера:
curl localhost:7978/api/v1/
## Должен быть получен ответ вида:
{"products":"http://localhost:7978/api/v1/products/","stocks":"http://localhost:7978/api/v1/stocks/"}
