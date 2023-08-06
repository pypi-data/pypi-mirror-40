from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
        name = 'incenp.certbot.ssh',
        version = '0.2.2',
        description = 'Certbot SSH authenticator plugin',
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        license = 'Apache License 2.0',
        author = 'Damien Goutte-Gattat',
        author_email = 'dgouttegattat@incenp.org',
        url = 'https://git.incenp.org/damien/certbot-ssh',

        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7'
        ],

        packages = find_packages(),
        include_package_data = True,

        entry_points = {
            'certbot.plugins': [
                'ssh = incenp.certbot.ssh:Authenticator',
            ]
        }
)
