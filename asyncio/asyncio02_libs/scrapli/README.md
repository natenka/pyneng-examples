## scrapli

Here are examples only for asynchronous transport options. Synchronous
examples are shown in [ssh_telnet/scrapli/](https://github.com/natenka/pyneng-examples/tree/main/ssh_telnet/scrapli)

## Links

* [основы scrapli в книге Python для сетевых инженеров](https://pyneng.readthedocs.io/ru/latest/book/18_ssh_telnet/scrapli.html), [english version](https://pyneng.readthedocs.io/en/latest/book/18_ssh_telnet/scrapli.html)
* [асинхронный транспорт scrapli в книге Advanced Python для сетевых инженеров](https://advpyneng.readthedocs.io/ru/latest/book/17_async_libraries/scrapli.html)
* [scrapli docs](https://carlmontanari.github.io/scrapli/user_guide/basic_usage/)
* [scrapli-cfg](https://scrapli.github.io/scrapli_cfg/user_guide/quickstart/)

## Notes

```
"transport": "asyncssh",
"transport_options": {"encryption_algs": "+aes128-cbc,aes256-cbc"},
~/venv/pyneng-py3-8-0/lib/python3.8/site-packages/scrapli/transport/plugins/asyncssh/transport.py
 118 line: encryption_algs="+aes128-cbc,aes256-cbc",
```

* [173](https://github.com/carlmontanari/scrapli/issues/173)
* [docs](https://github.com/carlmontanari/scrapli/blob/master/docs/api_docs/transport/plugins/asyncssh.md)
* [transport_options](https://github.com/carlmontanari/scrapli/search?q=transport_options)
