# auth against the server itself, basic only
# integers are sleep secs
# This setup is for keeping clients connected.
story = [
    {
        'cpeid': 'cpe_401',
        'url': 'SELF/cpe_401/user/pass?sleep=1000',
        'user': 'foo',
        'password': 'barbar',
    },
    5,
    {
        'cpeid': 'cpe_200',
        'url': 'SELF/cpe_200/user/passwordx',
        'user': 'user',
        'password': 'passwordx',
    },
    5,
]
