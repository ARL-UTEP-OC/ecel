#!/bin/bash
set -e

ECEL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
INSTALL_DIR="$ECEL_DIR"/plugins/snoopy

### Install snoopy
#
mkdir -p "$INSTALL_DIR"
rm -f "$INSTALL_DIR"/snoopy-install.sh &&
wget -O "$INSTALL_DIR/"snoopy-install.sh https://github.com/a2o/snoopy/raw/install/doc/install/bin/snoopy-install.sh &&
chmod 755 "$INSTALL_DIR"/snoopy-install.sh &&
cd "$INSTALL_DIR"
bash "$INSTALL_DIR"/snoopy-install.sh stable

### Configure snoopy
#
#TODO: a custom change for the config file; may have to compile this in... need to test
cp "$ECEL_DIR"/plugins/collectors/snoopy/config/snoopy.ini /etc/snoopy.ini
