Certbot-ssh - Certbot SSH authenticator plugin
==============================================

Certbot-ssh is a plugin for the
[Certbot](https://github.com/certbot/certbot) ACME client that performs
HTTP01 challenge validation on a remote computer through a SSH
connection.

Rationale
---------
The Certbot client assumes it runs on the machine that serves web pages
for the requested domain.

That is not always desirable or even possible.

The *manual* authenticator (`--manual`) allows to run the client on a
separate machine; it is then up to the system administrator to make sure
the web server responds appropriately to the HTTP01 challenge, by
putting a specific value into a specific file under the
`.well-known/acme-challenge` directory of the web server. This can be
quite tedious, especially if you require a cert for many domains.

This plugin provides an automatized version of the “manual” process.
Upon receiving the challenge data from the ACME server, it will execute
a script on a remote machine through a SSH connexion, and feed it with
the challenge data. It is then up to the script to write the challenge
tokens at the appropriate place.

A [sample script](incenp/certbot/acme-challenge.sh) is provided. This
script assumes the webroot of a requested *domain* is under a
`/var/www/domain` directory; you will probably need to adjust it
according to the layout of your own web server.

Usage
-----
Install the package:

    $ python setup.py install --user

Tweak the `acme-challenge.sh` script if needed, then upload it to your
server. Put it somewhere in the `PATH` of the user account you use for
SSH connection. Remove the `.sh` extension and make sure the script is
executable.

Then you may call Certbot:

    certbot certonly \
      --authenticator incenp.certbot.ssh:ssh \
      --incenp.certbot.ssh:ssh-server user@server.example.com \
      ...

Note that the client will attempt to write to some system directories on
the local machine (`/etc/letsencrypt`, `/var/lib/letsencrypt`). Use the
`--config-dir`, `--work-dir`, and `--logs-dir` options to specify other
directories if you want to run the client from a non-root account.


Copying
-------
Certbot-ssh is distributed under the same terms as Certbot itself, that
is, the Apache License version 2.0. The full license is included in the
[COPYING file](COPYING) of the source distribution.


Homepage and repository
-----------------------
The project is located at https://incenp.org/dvlpt/certbot-ssh.html. The
latest source code is available at https://git.incenp.org/damien/certbot-ssh.
