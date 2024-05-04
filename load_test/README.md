```sh
docker run --name vkr-pg -p 5432:5432 -e POSTGRES_USER=vkrvkr -e POSTGRES_PASSWORD=vkrvkr -e POSTGRES_DB=vkrdb -d postgres:13.3
docker run \
    -v $(pwd):/var/loadtest \
    --net host \
    -it yandex/yandex-tank
```
https://overload.yandex.net/702670 - list
https://overload.yandex.net/702673 - get
https://overload.yandex.net/702674 - assess
https://overload.yandex.net/702675 - mixed