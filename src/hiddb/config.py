environment = 'dev'
domain = 'hiddb.dev'

if environment not in ['local', 'dev', 'prod']:
    raise ValueError(f"HIDDB_SDK_PY_ENV")
    
if not domain:
    raise ValueError(f"HIDDB_SDK_PY_DOMAIN")

secure = environment != 'local'
protocol = 'https' if secure else 'http'
subdomain = '' if environment == 'local' else 'api.'
baseDbUrl = f'{protocol}://{subdomain}{domain}'