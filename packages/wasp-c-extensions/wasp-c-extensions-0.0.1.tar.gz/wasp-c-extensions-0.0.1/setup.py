
import os
from setuptools import setup, find_packages, Extension

from wasp_c_extensions.version import __package_data__


def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()


__pypi_data__ = __package_data__['pypi']
__extension__ = __package_data__['extensions'] if 'extensions' in __package_data__ else None


if __name__ == "__main__":
	setup(
		name=__package_data__['package'],
		version=__package_data__['numeric_version'],
		author=__package_data__['author'],
		author_email=__package_data__['author_email'],
		maintainer=__package_data__['maintainer'],
		maintainer_email=__package_data__['maintainer_email'],
		description=__package_data__['brief_description'],
		license=__package_data__['license'],
		keywords=__pypi_data__['keywords'],
		url=__package_data__['homepage'],
		packages=find_packages(),
		include_package_data=\
			__pypi_data__['include_package_data'] if 'include_package_data' in __pypi_data__ else True,
		long_description=read(__package_data__['readme_file']),
		classifiers=__pypi_data__['classifiers'],
		install_requires=read('requirements.txt').splitlines(),
		zip_safe=__pypi_data__['zip_safe'] if 'zip_safe' in __pypi_data__ else False,
		scripts=__package_data__['scripts'] if 'scripts' in __package_data__ else [],
		extras_require=__pypi_data__['extra_require'] if 'extra_require' in __pypi_data__ else {},
		ext_modules=[Extension(
			x['module_name'],
			x['sources'],
			include_dirs=x['include_dirs'] if 'include_dirs' in x else None,
			libraries=x['libraries'] if 'libraries' in x else None,
			library_dirs=x['library_dirs'] if 'library_dirs' in x else None,
			define_macros=[
				tuple(y) for y in x['define_macros']
			] if 'define_macros' in x else None,
			depends=x['depends'] if 'depends' in x else None
		) for x in __extension__] if __extension__ is not None else None
	)
