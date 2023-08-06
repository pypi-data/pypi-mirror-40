# coding: utf-8
import qiniu as _qiniu
from flask import current_app


class prefix(object):
    """
    Make a context of prefix, with which operations with filename will be auto prefixed.

    Example:
        ```
        q = Qiniu(app)

        with prefix('image/'):
            for file in ['foo.png', 'bar.png']:
                q.upload_file(file, f'./{file}')
        ```

        The filenames after upload will be 'image/foo.png', 'image/bar.png'.
    """
    def __init__(self, prefix):
        if isinstance(prefix, str):
            self.prefix = prefix
        else:
            raise ValueError("prefix must be 'str' object")

    def __enter__(self):
        current_app.extensions['qiniu']._prefix = self.prefix

    def __exit__(self, exc_type, exc_val, exc_tb):
        current_app.extensions['qiniu']._prefix = ''


class Qiniu(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['qiniu'] = self
        self._access_key = app.config.get('QINIU_ACCESS_KEY')
        self._secret_key = app.config.get('QINIU_SECRET_KEY')
        self._bucket_name = app.config.get('QINIU_BUCKET_NAME')
        self._bucket_domain = app.config.get('QINIU_BUCKET_DOMAIN', '')
        self._token_expires = app.config.setdefault('QINIU_TOKEN_EXPIRES', 3600)
        self._global_prefix = app.config.setdefault('QINIU_GLOBAL_PREFIX', '')
        self._prefix = ''
        self._auth = _qiniu.Auth(self._access_key, self._secret_key)
        self._bucket = _qiniu.BucketManager(self._auth)

    def _get_token(self, filename, expires=None):
        """Get a upload token.

        :param filename: name of the file after it's uploaded.
        :param expires: expire time of the token.
        :return: the token.
        """
        if expires is None:
            expires = self._token_expires
        return self._auth.upload_token(self._bucket_name, filename, expires)

    def _prefixed_filename(self, filename):
        """Add specific prefix to filename.

        :param filename: origin filename.
        :return: prefixed filename.
        """
        return self._global_prefix + self._prefix + filename

    def upload_file(self, filename, file_path, expires= None):
        """Upload a local file.

        :param filename: name of the file without prefix after it's uploaded.
        :param file_path: location of the file.
        :param expires: upload token expire time.
        :return: a dict like {"hash": "<Hash string>", "key": "<Key string>"};
            a ResponseInfo object.
        """
        filename = self._prefixed_filename(filename)
        token = self._get_token(filename, expires)
        return _qiniu.put_file(token, filename, file_path)

    def upload_data(self, filename, data, expires=None):
        """Upload a file with data in byte.

        :param filename: name of the file without prefix after it's uploaded.
        :param data: bytes.
        :param expires: upload token expire time.
        :return: a dict like {"hash": "<Hash string>", "key": "<Key string>"};
            a ResponseInfo object.
        """
        filename = self._prefixed_filename(filename)
        token = self._get_token(filename, expires)
        return _qiniu.put_data(token, filename, data)

    def fetch_url(self, filename, url):
        """Upload a file which fetched from an URL.

        :param filename: name of the file without prefix after it's uploaded.
        :param url: URL from which to fetch.
        :return: a dict like {"hash": "<Hash string>", "key": "<Key string>"};
            a ResponseInfo object.
        """
        filename = self._prefixed_filename(filename)
        return self._bucket.fetch(url, self._bucket_name, filename)

    def rename_file(self, filename, filename_to):
        """Rename a file.

        :param filename: origin name.
        :param filename_to: new name.
        :return: a dict like {"error": "<errMsg string>"} when fail, or None when succeed;
            a ResponseInfo object.
        """
        filename = self._prefixed_filename(filename)
        return self._bucket.move(self._bucket_name, filename, self._bucket_name, filename_to)

    def delete_file(self, filename):
        """Delete a file.

        :param filename: name of file to delete.
        :return: a dict like {"error": "<errMsg string>"} when fail, or None when succeed;
            a ResponseInfo object.
        """
        filename = self._prefixed_filename(filename)
        return self._bucket.delete(self._bucket_name, filename)
