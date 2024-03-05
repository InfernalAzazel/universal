import os

APP_NAME = os.environ.get("APP_NAME", "universal")
MONGODB_HOST = os.getenv('MONGODB_HOST', '127.0.0.1')
MONGODB_DATABASE_NAME = os.getenv('MONGODB_DATABASE_NAME', APP_NAME)
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME', 'spb0122003')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'dcaGRzkJpuKsHgMs8hoS')

TZ_INFO = os.getenv('TZ_INFO', 'Asia/Shanghai')
JWT_SECRET = os.getenv('JWT_SECRET', '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_MINUTES = int(os.getenv('JWT_MINUTES', '60'))



