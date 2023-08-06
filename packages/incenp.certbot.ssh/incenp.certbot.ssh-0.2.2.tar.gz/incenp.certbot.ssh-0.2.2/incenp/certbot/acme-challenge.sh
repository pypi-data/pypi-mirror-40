#!/bin/sh

# The plugin calls this script with 'clean' as first argument once
# the validation process is over.
if [ "x$1" = xclean ]; then
    rm -rf /var/www/*/.well-known/acme-challenge
    exit
fi

# For the validation itself, the plugin calls this script without
# arguments and feeds it with lines according to the following
# format:
#
# domain keyauth
#
# where `domain` is the domain to validate, and `keyauth` is a
# key authorization string (draft-ietf-acme-acme-01, §7.1) of
# the form `token.account_key`.
#
# To complete the challenge, write the key authorization string
# into a file `.well-known/acme-challenge/token`, available
# through HTTP on the requested domain.
while read domain keyauth ; do
    token=$(echo $keyauth | cut -d. -f1)
    logger -t ACME "Validating $domain with token $token"
    mkdir -p /var/www/$domain/.well-known/acme-challenge
    echo $keyauth > /var/www/$domain/.well-known/acme-challenge/$token
done
