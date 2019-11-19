#!/bin/sh

echo ">> MOUNT"
sudo kdb mount test.toml user/tests/storage toml type

echo ">> SHOW"

echo "SET TO TRUE"
kdb set user/tests/storage/bool/value true
echo ">> FILE"
cat ~/.config/test.toml
echo ">> FILE END"
echo "GET"
kdb get user/tests/storage/bool/value

echo "SET TYPE TO BOOELAN"
kdb meta-set user/tests/storage/bool/value type boolean
kdb set user/tests/storage/bool/value 1
echo "GET"
kdb get user/tests/storage/bool/value

echo "SET TO FALSE"
kdb set user/tests/storage/bool/value false
echo "GET"
kdb get user/tests/storage/bool/value

echo ">> SET NON-BOOLEAN"
kdb set user/tests/storage/bool/value 'non boolean'
echo "RETVAL: $?"

echo ">> GET PREV VALID VALUE"
kdb get user/tests/storage/bool/value

echo ">> FILE"
cat ~/.config/test.toml
echo ">> FILE END"

echo ">> CLEANUP"
kdb rm -r user/tests/storage
sudo kdb umount user/tests/storage
