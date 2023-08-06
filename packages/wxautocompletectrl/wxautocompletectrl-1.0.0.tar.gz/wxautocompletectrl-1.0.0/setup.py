import setuptools

classifiers = """
    Development Status :: 5 - Production/Stable
    License :: OSI Approved :: BSD License
    Intended Audience :: Developers
    Programming Language :: Python :: 3.4
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: Implementation :: CPython
    Operating System :: OS Independent
"""

setuptools.setup(
    name='wxautocompletectrl',
    version='1.0.0',
    description='AutocompleteTextCtrl for wxPython',
    long_description='Text control that uses a HtmlListBox for suggestions',
    keywords='wxpython autocomplete',
    author='Toni Ruža',
    author_email='toni.ruza@gmail.com',
    url='https://bitbucket.org/raz/wxautocompletectrl',
    license='BSD-2-Clause',
    platforms=['any'],
    install_requires=[
        "wxpython",
    ],
    python_requires=">=3.4",
    classifiers=[s.strip() for s in classifiers.splitlines() if s],
    zip_safe=True,
    py_modules=['wxautocompletectrl']
)
