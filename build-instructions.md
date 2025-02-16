# Build Instructions

## 1. Debian Package Builder

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

# Build it
$ ( cd /root/styledterm/ && dpkg-buildpackage -b -us -uc )

# Move the .deb file back into the accessible directory
$ mv /root/python3-styledterm_*.deb /root/styledterm
```

