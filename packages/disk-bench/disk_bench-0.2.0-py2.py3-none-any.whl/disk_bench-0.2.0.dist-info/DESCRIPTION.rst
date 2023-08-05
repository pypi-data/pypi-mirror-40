.. default-role:: code

Disk Bench
##########

Designed to run similar tests as Crystal Disk Mark using fio with user friendly output options.

Tests ran:

* Sequential read/write w/ 1MB block size
* Random read/write w/ 512K block size
* Queue depth 32 random read/write 4K blocks size

Install
=======

::

    # system install
    $ sudo pip3 install disk-bench

    # user install
    $ pip3 install --user disk-bench

Usage
=====

::

    $ disk-bench --help

    # Default runs fio w/ --loops=3 and --size=1G
    $ disk-bench /mnt/disk-to-test/whatever

    # Show CSV output (for easy copy/paste into Excel or Google Sheets)
    $ disk-bench /mnt/disk-to-test/whatever --style=csv

    # Quick
    $ disk-bench /mnt/disk-to-test/whatever --loops=1 --size=1M


Changelog
=========

0.2.0 released 2018-12-21
-------------------------

- change tests we run and output format (df6ac7b_)

.. _df6ac7b: https://github.com/rsyring/disk-bench/commit/df6ac7b


0.1.4 released 2018-12-21
-------------------------

- fix cli direct flag (74aa304_)

.. _74aa304: https://github.com/rsyring/disk-bench/commit/74aa304


0.1.3 released 2018-12-21
-------------------------

- support non-direct IO (f5ba899_)

.. _f5ba899: https://github.com/rsyring/disk-bench/commit/f5ba899


0.1.2 released 2018-12-20
-------------------------

- fix some packaging issues (f908a1d_)

.. _f908a1d: https://github.com/rsyring/disk-bench/commit/f908a1d


0.1.1 released 2018-12-20
-------------------------

- fix pypi name (10d6115_)

.. _10d6115: https://github.com/rsyring/disk-bench/commit/10d6115

0.1.0 released 2018-12-20
-------------------------

- add tox & CI (12cfca5_)
- fix json bytes/text for Python 3.5 (475e3ee_)
- add tox improve package (ee8efc4_)

.. _12cfca5: https://github.com/rsyring/disk-bench/commit/12cfca5
.. _475e3ee: https://github.com/rsyring/disk-bench/commit/475e3ee
.. _ee8efc4: https://github.com/rsyring/disk-bench/commit/ee8efc4



