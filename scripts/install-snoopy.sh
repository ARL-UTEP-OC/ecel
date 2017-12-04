#!/bin/bash
set -e

ECEL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
INSTALL_DIR="$ECEL_DIR"/plugins/collectors/snoopy/snoopy_install

### Install snoopy
#
mkdir -p "$INSTALL_DIR"
rm -f "$INSTALL_DIR"/snoopy-install.sh &&
wget -O "$INSTALL_DIR/"snoopy-install.sh https://github.com/a2o/snoopy/raw/install/doc/install/bin/snoopy-install.sh &&
chmod 755 "$INSTALL_DIR"/snoopy-install.sh &&
cd "$INSTALL_DIR"
bash "$INSTALL_DIR"/snoopy-install.sh snoopy-2.4.6_mod.tar.gz

### Configure snoopy
cp "$ECEL_DIR"/plugins/collectors/snoopy/config/snoopy.ini /etc/snoopy.ini

#We only want snoopy to run when ecel says so
echo SNOOPY: Disabling snoopy
bash snoopy-disable
