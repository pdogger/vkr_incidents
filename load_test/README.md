```sh
docker run --name vkr-pg -p 5432:5432 -e POSTGRES_USER=vkrvkr -e POSTGRES_PASSWORD=vkrvkr -e POSTGRES_DB=vkrdb -d postgres:13.3
docker run \
    -v $(pwd):/var/loadtest \
    --net host \
    -it yandex/yandex-tank
```
# Insert csrf token and cookies into headers in make_ammo.py
https://overload.yandex.net/702670 - list
https://overload.yandex.net/702673 - get
https://overload.yandex.net/702686 - assess
https://overload.yandex.net/702701 - mixed