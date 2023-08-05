"""
Build script to create a doc-to-pdf convert server as a Windows executable.
"""

import os
import textwrap


setup_params = dict(
	console=['server.py'],
	options=dict(
		py2exe=dict(
			packages=['pkg_resources'],
		),
	),
	script_args=('py2exe',),
)

if __name__ == '__main__':
	from setuptools import setup
	__import__('py2exe')
	code = """
		from jaraco.office import convert
		convert.ConvertServer.start_server()
		"""
	open('server.py', 'w').write(textwrap.dedent(code))
	setup(**setup_params)
	os.remove('server.py')
