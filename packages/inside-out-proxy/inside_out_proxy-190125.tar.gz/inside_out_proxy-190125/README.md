# Inside Out HTTP Job Proxy

> "Don't call us, we call you!"

(https://en.wiktionary.org/wiki/Hollywood_principle)

Allows to stream jobs from a long polling server to the proxy, which turns them into outgoing HTTP Requests.


# Proxy

Specific options:

    inside_out_proxy --help

All options

    inside_out_proxy --helpfull

## Example:

    inside_out_proxy --user=foo --password="$PW" --jobserver="https://..."


# Testserver

Included is a test server which allows to check the correct working of the
client.

    inside_out_proxy_test_jobserver --help

shows its options.


## Testrun

### Periodic Jobs

This will start the testserver on localhost port 8089, returning jobs from
playbook "prod":

```bash
inside_out_proxy_test_jobserver --playbook prod --loops=1000 --debug
```

Now we connect the proxy with default settings:

```bash
inside_out_proxy --debug

```

### Speed Test

When we connect with user speed and a password which the testserver accepts, it
will load the client with jobs for perf tests:

```
# server:
inside_out_proxy_test_jobserver --speed_user_password=foo --debug

# client:
inside_out_proxy --debug --user=speed --password=foo
```



DVCS URL: /scm/hg/AX/inside_out_proxy

