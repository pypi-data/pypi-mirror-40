# auth against the server itself, basic only
# integers are sleep secs
# This setup, run with --loops=2 should result in 3 jobs, one 401, two 200:
story = [
    {
        'cpeid': 'cpe_401',
        'url': 'SELF/cpe_401/user/pass?sleep=1000',
        'user': 'foo',
        'password': 'barbar',
    },
    0.01,
    {
        'cpeid': 'cpe_200',
        'url': 'SELF/cpe_200/user/passwordx',
        'user': 'user',
        'password': 'passwordx',
    },
]
