#!/bin/sh

echo ">> MOUNT"
sudo kdb mount test.toml user/tests/storage toml

echo ">> SET"
kdb set user/tests/storage/root "abc"
kdb set user/tests/storage/root/a/b/c "xyz"

echo ">> LIST"
kdb ls user/tests/storage/root

echo ">> FILE"
cat ~/.config/test.toml
echo ">> FILE END"

echo ">> CLEANUP"
kdb rm -r user/tests/storage
sudo kdb umount user/tests/storage
