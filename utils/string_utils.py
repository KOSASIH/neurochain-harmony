import re
import hashlib
from urllib.parse import urlparse

class StringUtils:
    def __init__(self):
        pass

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate an email address using a regular expression.

        :param email: The email address to validate.
        :return: True if the email address is valid, False otherwise.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def generate_hash(string: str, algorithm: str = 'sha256') -> str:
        """
        Generate a hash of a given string using a specified algorithm.

        :param string: The string to generate a hash for.
        :param algorithm: The algorithm to use for hashing (default is sha256).
        :return: The hashed string.
        """
        if algorithm == 'sha256':
            return hashlib.sha256(string.encode()).hexdigest()
        elif algorithm == 'md5':
            return hashlib.md5(string.encode()).hexdigest()
        else:
            raise ValueError('Invalid algorithm')

    @staticmethod
    def extract_domain(url: str) -> str:
        """
        Extract the domain from a given URL.

        :param url: The URL to extract the domain from.
        :return: The domain of the URL.
        """
        return urlparse(url).netloc

    @staticmethod
    def slugify(string: str) -> str:
        """
        Convert a given string to a slug format (lowercase, no spaces, etc.).

        :param string: The string to convert to a slug.
        :return: The slugified string.
        """
        return re.sub(r'[^a-zA-Z0-9_-]', '-', string.lower()).strip('-')

    @staticmethod
    def truncate_string(string: str, length: int) -> str:
        """
        Truncate a given string to a specified length.

        :param string: The string to truncate.
        :param length: The length to truncate the string to.
        :return: The truncated string.
        """
        return string[:length] + '...' if len(string) > length else string

    @staticmethod
    def remove_accents(string: str) -> str:
        """
        Remove accents from a given string.

        :param string: The string to remove accents from.
        :return: The string with accents removed.
        """
        return ''.join(c for c in unicodedata.normalize('NFD', string)
                       if unicodedata.category(c) != 'Mn')

    @staticmethod
    def word_count(string: str) -> int:
        """
        Count the number of words in a given string.

        :param string: The string to count the words in.
        :return: The number of words in the string.
        """
        return len(string.split())
