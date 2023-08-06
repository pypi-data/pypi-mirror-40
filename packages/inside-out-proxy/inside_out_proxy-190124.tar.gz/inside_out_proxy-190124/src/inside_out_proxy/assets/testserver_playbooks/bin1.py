# real digest authing server
# integers are sleep secs
story = [
    {
        'cpeid': 'cpe_401',
        'url': 'https://nghttp2.org/httpbin/digest-auth/auth/user/p',
        'user': 'foo',
        'password': 'barbar',
    },
    # duplicate, must be active:
    {
        'cpeid': 'cpe_401',
        'url': 'https://nghttp2.org/httpbin/digest-auth/auth/user/p',
        'user': 'foo',
        'password': 'barbaz',
    },
    4,
    {
        'cpeid': 'cpe_200',
        'url': 'https://nghttp2.org/httpbin/digest-auth/auth/user/passwordx',
        'user': 'user',
        'password': 'passwordx',
    },
    4,
]
