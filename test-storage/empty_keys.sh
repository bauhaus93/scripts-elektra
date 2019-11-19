#!/bin/sh

echo ">> MOUNT"
sudo kdb mount test.toml user/tests/storage toml

echo ">> SET NULL"
kdb set user/tests/storage/null

echo ">> CHECK NULL"
kdb get user/tests/storage/null
kdb meta-ls user/tests/storage/null


echo ">> SET EMPTY"
kdb set user/tests/storage/empty ''

echo ">> CHECK EMPTY"
kdb get user/tests/storage/empty
kdb meta-ls user/tests/storage/empty


echo ">> FILE"
cat ~/.config/test.toml
echo ">> FILE END"

echo ">> CLEANUP"
kdb rm -r user/tests/storage
sudo kdb umount user/tests/storage
