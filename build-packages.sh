#! /bin/bash

set -e

CNTR=styledterm-builder

# 1. Build the debian package
podman exec -w /root/styledterm $CNTR dpkg-buildpackage -b -us -uc
# 2. Move the .deb file into _RELEASES
podman exec -t $CNTR sh -c "mv /root/python3-styledterm_*.deb /root/styledterm/_RELEASES"

# 3. Build the python packages:
podman exec -w /root/styledterm $CNTR python3 -m build
# 4. Move the dist files into _RELEASES
podman exec -t $CNTR sh -c "mv /root/styledterm/dist/*.whl /root/styledterm/_RELEASES"
podman exec -t $CNTR sh -c "mv /root/styledterm/dist/*.tar.gz /root/styledterm/_RELEASES"

# 5. Clean up
git clean -fxd -e _RELEASES
