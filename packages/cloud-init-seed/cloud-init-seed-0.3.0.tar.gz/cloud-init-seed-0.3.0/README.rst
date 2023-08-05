cloud-init seed creation tool
=============================
.. image:: https://travis-ci.org/toabctl/cloud-init-seed.svg
    :target: https://travis-ci.org/toabctl/cloud-init-seed

`cloud-init-seed` is a command line tool to create seed images
which can be used together with `cloud-init`_. This is eg. useful when using
Cloud images (which contain `cloud-init`) together with `libvirt`_ (which does
not have a metadata server which is usually used together with cloud-init).

.. note::
   `cloud-init` in the image must have the `nocloud`_ datasource enabled.

Requirements and installation
-----------------------------
- mkisofs or genisoimage (`zypper in mkisofs` for openSUSE or `apt install genisoimage` for Debian)
- when using virtual envs, just install via pip `pip3 install cloud-init-seed`

Usage
-----
Create a seed image::

  cloud-init-seed create

Now the `seed.img` file can be attached to a libvirt instance as a CDROM drive.


.. _cloud-init: https://cloudinit.readthedocs.io/en/latest/
.. _nocloud: https://cloudinit.readthedocs.io/en/latest/topics/datasources/nocloud.html
.. _libvirt: https://libvirt.org/
