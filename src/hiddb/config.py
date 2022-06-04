environment = 'dev'
api_domain = 'hiddb.dev'
db_domain = 'hiddb.dev'

if environment not in ['local', 'dev', 'prod']:
    raise ValueError(f"HIDDB_SDK_PY_ENV")
    
if not api_domain:
    raise ValueError(f"HIDDB_SDK_PY_DOMAIN")

if not db_domain:
    raise ValueError(f"HIDDB_SDK_PY_DOMAIN")

secure = environment != 'local'
protocol = 'https' if secure else 'http'
subdomain = '' if environment == 'local' else 'api.'

base_api_url = f'{protocol}://{subdomain}{api_domain}'