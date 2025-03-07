# Release Building Instructions

## 1. Setting Up a Python/Debian Package Builder

Build the container (make sure you are in the root of this repository).

```sh
# Pull the trixie image
$ podman image pull docker.io/library/debian:trixie

# Build our pkgtest container
$ podman run -d -ti \
    --name styledterm-builder \
    -v $(pwd):/root/styledterm \
    docker.io/library/debian:trixie

# Enter it
$ podman exec -ti styledterm-builder /bin/bash
```

In the container:

```sh
# Get the depdencies we need for building python packages
$ apt-get -y update && apt-get -y upgrade
$ apt-get -y install \
    python3-setuptools \
    python3-build \
    python3-venv \
    debhelper \
    dh-python \
    python3-all \
    python3-setuptools \
    pybuild-plugin-pyproject
```

## 2. Building

Enter the container and build things:

```sh
podman exec -ti styledterm-builder /bin/bash

# 1. Build the debian package
$ ( cd /root/styledterm/ && dpkg-buildpackage -b -us -uc )
# 2. Move the .deb file into _RELEASES
$ mv /root/python3-styledterm_*.deb /root/styledterm/_RELEASES

# 3. Build the python packages:
( cd /root/styledterm/ && python3 -m build )
# 4. Move the dist files into _RELEASES
mv /root/styledterm/dist/*.whl /root/styledterm/_RELEASES
mv /root/styledterm/dist/*.tar.gz /root/styledterm/_RELEASES
```

Then on the host:

```sh
# 5. Clean up
$ git clean -fxd -e _RELEASES
```

