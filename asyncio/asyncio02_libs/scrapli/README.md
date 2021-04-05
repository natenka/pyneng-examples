## scrapli

Тут примеры только для асинхронных вариантов транспорта.
Синхронные варианты описаны [в ssh_telnet/scrapli/](https://github.com/natenka/pyneng-examples/tree/main/ssh_telnet/scrapli)

## Полезные ссылки

* [основы scrapli в книге Python для сетевых инженеров](https://pyneng.readthedocs.io/ru/latest/book/18_ssh_telnet/scrapli.html)
* [асинхронный транспорт scrapli в книге Advanced Python для сетевых инженеров](https://advpyneng.readthedocs.io/ru/latest/book/17_async_libraries/scrapli.html)
* [документация scrapli](https://carlmontanari.github.io/scrapli/user_guide/basic_usage/)
* [scrapli-cfg](https://scrapli.github.io/scrapli_cfg/user_guide/quickstart/)

## Проблемы

```
"transport": "asyncssh",
"transport_options": {"encryption_algs": "+aes128-cbc,aes256-cbc"},
~/venv/pyneng-py3-8-0/lib/python3.8/site-packages/scrapli/transport/plugins/asyncssh/transport.py
 118 line: encryption_algs="+aes128-cbc,aes256-cbc",
```
