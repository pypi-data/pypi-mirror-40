import os.path
from os import listdir
from .dir import make_dir, delete_dir
from .get_basename import get_basename


class Path:
	def __init__(self, string, show_size=False, show_full_path=False):
		self._string = string
		self._size = None
		self._show_size = show_size
		self._show_full_path = show_full_path

	def __str__(self):
		return self.string

	def __repr__(self):
		if self._show_full_path:
			string = self.path
		else:
			string = self.name
		if self._show_size:
			size, unit = self.get_size()
			return f'{self.type}: {string} - {round(size, 3)} {unit}'
		else:
			return f'{self.type}: {string}'

	@classmethod
	def get_current_directory(cls, show_size=False):
		return cls(string='.', show_size=show_size)

	@property
	def parent_directory(self):
		return self+'..'

	@property
	def string(self):
		return self._string

	@property
	def path(self):
		return self.string

	@property
	def value(self):
		return self.string

	@property
	def name_and_extension(self):
		return get_basename(path=self.path)

	full_name = name_and_extension

	@property
	def extension(self):
		extension_with_dot = os.path.splitext(self.path)[1]
		if len(extension_with_dot) > 0:
			return extension_with_dot[1:]
		else:
			return extension_with_dot

	@property
	def name(self):
		return self.name_and_extension.rsplit('.', 1)[0]

	def get_absolute(self):
		return os.path.abspath(self.path)

	@property
	def absolute(self):
		return self.get_absolute()

	def get_size_bytes(self):
		if self.is_file():
			return os.path.getsize(self.path)
		else:
			return sum([x.size_bytes for x in self.list()])

	@property
	def size_bytes(self):
		if self._size is None:
			self._size = self.get_size_bytes()
		return self._size

	def get_size_kb(self, binary=True):
		if binary:
			return self.size_bytes/(2**10)
		else:
			return self.size_bytes/1e3

	def get_size_mb(self, binary=True):
		if binary:
			return self.size_bytes/(2**20)
		else:
			return self.size_bytes/1e6

	def get_size_gb(self, binary=True):
		if binary:
			return self.size_bytes/(2**30)
		else:
			return self.size_bytes/1e6

	def get_size(self, binary=True):
		main_unit = 'B' if binary else 'b'
		if self.size_bytes <= 1e3:
			return (self.size_bytes, 'B')
		elif self.size_bytes <= 1e6:
			return (self.get_size_kb(binary=binary), 'K'+main_unit)
		elif self.size_bytes <= 1e9:
			return (self.get_size_mb(binary=binary), 'M' + main_unit)
		else:
			return (self.get_size_gb(binary=binary), 'G' + main_unit)

	def exists(self):
		return os.path.exists(self._string)

	def is_file(self):
		if not self.exists():
			raise ValueError(f'Path {self.string} does not exist!')
		return os.path.isfile(self.string)

	def is_directory(self):
		if not self.exists():
			raise ValueError(f'Path {self.string} does not exist!')
		return not os.path.isfile(self.string)

	@property
	def type(self):
		if self.is_file():
			return 'file'
		else:
			return 'directory'



	def __add__(self, other):
		if isinstance(other, str):
			other_string = other
		elif isinstance(other, Path):
			other_string = other.string
		else:
			raise TypeError(f'{other} is a {type(other)} but it should either be string or {Path}')
		self_string = '' if self.string=='.' else self.string

		return self.__class__(
			string=os.path.join(self_string, other_string),
			show_size=self._show_size, show_full_path=self._show_full_path
		)

	def _sort_key(self):
		return (self.type, self.string)

	def __lt__(self, other):
		return self._sort_key() < other._sort_key()

	def __gt__(self, other):
		return self._sort_key() > other._sort_key()

	def __le__(self, other):
		return self._sort_key() <= other._sort_key()

	def __ge__(self, other):
		return self._sort_key() >= other._sort_key()

	def __eq__(self, other):
		return self._sort_key() == other._sort_key()

	def __ne__(self, other):
		return self._sort_key() != other._sort_key()

	def list(self, show_size=None, show_full_path=None):
		if self.is_file(): raise NotADirectoryError(f'{self.name} is not a directory!')
		if show_size is not None:
			self._show_size = show_size
		if show_full_path is not None:
			self._show_full_path = show_full_path

		if not self.is_directory():
			raise TypeError('{self} is not a directory!')
		result = [self+x for x in listdir(self.string)]
		result.sort()
		return result

	@property
	def directories(self):
		return [x for x in self.list() if x.is_directory()]

	@property
	def files(self):
		return [x for x in self.list() if x.is_file()]

	def get(self, full_name):
		return [x for x in self.list() if x.full_name==full_name][0]

	def make_directory(self, name, ignore_if_exists=True):
		make_dir(path=(self+name).path, ignore_if_exists=ignore_if_exists)

	def delete_directory(self, name):
		delete_dir(path=(self+name).path)

	# aliases
	ls = list
	dir = list
	md = make_directory
	make_dir = make_directory
	del_dir = delete_directory
	delete_dir = delete_directory


