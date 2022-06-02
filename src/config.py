import os
from dotenv import load_dotenv

load_dotenv()

environment = os.getenv('HIDDB_SDK_PY_ENV')
domain = os.getenv('HIDDB_SDK_PY_DOMAIN')

if environment not in ['local', 'dev', 'prod']:
    raise ValueError(f"HIDDB_SDK_PY_ENV")
    
if not os.getenv('HIDDB_SDK_PY_DOMAIN'):
    raise ValueError(f"HIDDB_SDK_PY_DOMAIN")

secure = environment != 'local'
protocol = 'https' if secure else 'http'
subdomain = '' if environment == 'local' else 'api.'
baseDbUrl = f'{protocol}://{subdomain}{domain}'