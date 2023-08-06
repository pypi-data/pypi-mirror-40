# Inside Out HTTP Job Proxy

> "Don't call us, we call you!"

(https://en.wiktionary.org/wiki/Hollywood_principle)

Allows to stream jobs from a long polling server to the proxy, which turns them into outgoing HTTP Requests.


# Proxy

All options:

    inside_out_proxy --helpfull

## Example:

    inside_out_proxy --user=foo --password="$PW" --jobserver="https://..."


# Testserver

Included is a test server which allows to check the correct working of the
client.

    ./testserver.py --help

shows its options.


## Testrun

This will start the testserver on localhost port 8089, returning jobs from
playbook "prod":

```bash
./testserver.py --playbook prod --loops=1000 --debug
```

Now we connect the proxy with default settings:

```bash
inside_out_proxy --debug

```





DVCS URL: /scm/hg/AX/inside_out_proxy

