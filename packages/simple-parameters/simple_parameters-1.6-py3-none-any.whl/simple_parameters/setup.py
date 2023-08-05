import setuptools

setuptools.setup(
    name = 'SimpleParameters',
    version = '1.5',
    description = 'Simple parsing of parameters supplied on the command line',
    long_description= 'Allows to create json file with details of the parameters available on the command line for any application. It then handles the user parsing of these parameters by setting the required flags which you can directly consume in your application',

    author='crazybusy',
    author_email = 'upscprep48@gmail.com',
    url = 'https://github.com/crazybusy/SimpleParameters',

    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: Free for non-commercial use"
        ]
)
