FROM registry.fedoraproject.org/fedora:27
LABEL \
    name="dogtagpki/pki-ci:f27_105" \
    maintainer="Christian Heimes <cheimes@redhat.com>" \
    vendor="Dogtag PKI" \
    url="http://dogtagpki.org/"

# PYTHONCOERCECLOCALE warning
ENV LC_ALL=C.UTF-8

# update all packages
RUN dnf install -y dnf-plugins-core \
    && dnf copr -y enable @pki/10.5 \
    && dnf -y update

# install base dependencies and DS
RUN dnf install -y \
        make \
        rpm-build \
        sudo \
        389-ds-base

# install PKI build dependencies
RUN dnf builddep -y pki-core

# build env
ENV BUILDDIR="/tmp/workdir" \
    BUILDUSER="builduser" \
    BUILDUSER_UID=1000 \
    BUILDUSER_GID=1000
VOLUME ["${BUILDDIR}"]
EXPOSE 389 8080 8443

# https://raw.githubusercontent.com/fedora-cloud/Fedora-Dockerfiles/master/systemd/systemd/Dockerfile
ENV container docker
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
    rm -f /lib/systemd/system/multi-user.target.wants/*; \
    rm -f /etc/systemd/system/*.wants/*; \
    rm -f /lib/systemd/system/local-fs.target.wants/*; \
    rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
    rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
    rm -f /lib/systemd/system/basic.target.wants/*; \
    rm -f /lib/systemd/system/anaconda.target.wants/*;

# cleanup
RUN dnf clean all

VOLUME [ "/sys/fs/cgroup", "/tmp", "/run" ]
CMD ["/sbin/init"]
STOPSIGNAL SIGRTMIN+3
