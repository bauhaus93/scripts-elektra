#!/bin/sh


sudo kdb rm -r user/tests/toml
sudo kdb umount user/tests/toml
rm -f ~/.config/config.toml

find $1 -name "*.toml" | xargs -I % sh -c '''
    echo "### Mounting file %":
    sudo kdb mount config.toml user/tests/toml toml && \
    cat % > `kdb file user/tests/toml` && \
    # kdb ls user/tests/toml;
    kdb rm -r user/tests/toml
    sudo kdb umount user/tests/toml
    rm -f ~/.config/config.toml'''
