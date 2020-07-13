from werkzeug.security import generate_password_hash

__all__ = ['main', 'metadata', 'console']
__author__ = 'Tkachenko Igor'
__author_url__ = 'https://github.com/foozzi'
__version__ = '0.1.1'

users = {
    "login": generate_password_hash("test5"),
    "password": generate_password_hash("test5")
}