import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="socket_chatroom",
	version="0.1.0",
	author="WangTanxu",
	author_email="a913536021@qq.com",
	description="test",
	long_description=long_description,
	long_description_content_type="text/markdown",
	# url="https://github.com/pypa/sampleproject",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)