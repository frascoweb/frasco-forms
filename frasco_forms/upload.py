from wtforms import FileField as BaseFileField, ValidationError
from flask_wtf.file import FileRequired
from werkzeug import secure_filename, FileStorage
from frasco import current_app, url_for
import os
import uuid


__all__ = ('file_upload_backend', 'create_upload_backend', 'url_for_upload',
           'FileField', 'FileRequired', 'FileAllowed')


upload_backends = {}


def file_upload_backend(name):
    def decorator(cls):
        upload_backends[name] = cls
        return cls
    return decorator


def create_upload_backend(name):
    if isinstance(name, str):
        return upload_backends[name]()
    return name


def url_for_upload(filename, backend=None, **kwargs):
    if not backend:
        backend = current_app.features.forms.get_default_upload_backend()
    elif isinstance(backend, str):
        backend = create_upload_backend(backend)
    return backend.url_for(filename, **kwargs)


class FileField(BaseFileField):
    def __init__(self, label=None, validators=None, auto_save=True, upload_dir=None, upload_backend=None,\
                 uuid_prefix=None, keep_filename=None, subfolders=None, **kwargs):
        super(FileField, self).__init__(label, validators, **kwargs)
        self.file = None
        self.auto_save = auto_save
        self.upload_dir = upload_dir
        self._upload_backend = upload_backend
        self.uuid_prefix = uuid_prefix
        self.keep_filename = keep_filename
        self.subfolders = subfolders

    @property
    def upload_backend(self):
        if not self._upload_backend:
            self._upload_backend = current_app.features.forms.options["upload_backend"]
        if isinstance(self._upload_backend, str):
            self._upload_backend = create_upload_backend(self._upload_backend)
        return self._upload_backend

    def process_formdata(self, valuelist):
        if not valuelist:
            return
        self.file = valuelist[0]
        self.data = None
        if not self.has_file():
            return

        self.data = self.generate_filename(self.file.filename)
        if self.upload_dir:
            self.data = os.path.join(self.upload_dir, self.data)
        if self.auto_save:
            self.save_file()

    def generate_filename(self, filename):
        uuid_prefix = self.uuid_prefix
        if uuid_prefix is None:
            uuid_prefix = current_app.features.forms.options["upload_uuid_prefixes"]
        keep_filename = self.keep_filename
        if keep_filename is None:
            keep_filename = current_app.features.forms.options["upload_keep_filenames"]
        subfolders = self.subfolders
        if subfolders is None:
            subfolders = current_app.features.forms.options["upload_subfolders"]

        if uuid_prefix and not keep_filename:
            _, ext = os.path.splitext(filename)
            filename = str(uuid.uuid4()) + ext
        else:
            filename = secure_filename(filename)
            if uuid_prefix:
                filename = str(uuid.uuid4()) + "-" + filename

        if subfolders:
            if uuid_prefix:
                parts = filename.split("-", 4)
                filename = os.path.join(os.path.join(*parts[:4]), filename)
            else:
                filename = os.path.join(os.path.join(*filename[:4]), filename)

        return filename

    def save_file(self):
        self.upload_backend.save(self.file, self.data)

    def has_file(self):
        # compatibility with Flask-WTF
        if not isinstance(self.file, FileStorage):
            return False
        return self.file.filename not in [None, '', '<fdopen>']


class FileAllowed(object):
    def __init__(self, extensions, message=None):
        self.extensions = extensions
        self.message = message

    def __call__(self, form, field):
        if not field.has_file():
            return

        filename = field.file.filename.lower()
        ext = filename.rsplit('.', 1)[-1]
        if ext in self.extensions:
            return

        message = self.message
        if message is None:
            message = field.gettext("File type not allowed")
        raise ValidationError(message)


@file_upload_backend("local")
class LocalStorageBackend(object):
    def __init__(self, path=None):
        self._path = path

    @property
    def path(self):
        if self._path is None:
            return current_app.features.forms.options["upload_dir"]
        return self._path

    def save(self, file, filename):
        pathname = os.path.join(self.path, filename)
        dirname = os.path.dirname(pathname)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        file.save(pathname)

    def url_for(self, filename, **kwargs):
        return url_for("static_upload", filename=filename, **kwargs)