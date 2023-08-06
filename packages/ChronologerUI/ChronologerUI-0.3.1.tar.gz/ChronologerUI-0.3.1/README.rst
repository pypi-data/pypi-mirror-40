.. image:: https://img.shields.io/badge/dynamic/json.svg?url=https://api.bitbucket.org/2.0/repositories/saaj/chronologer/pipelines/?page=1%26pagelen=1%26sort=-created_on%26target.ref_name=frontend&label=build&query=$.values[0].state.result.name&colorB=blue
   :target: https://bitbucket.org/saaj/chronologer/addon/pipelines/home#!/results/branch/frontend/page/1
.. image:: https://badge.fury.io/py/ChronologerUI.svg
   :target: https://pypi.org/project/ChronologerUI/

==============
Chronologer UI
==============

.. figure:: https://bitbucket.org/saaj/chronologer/raw/53816c9dfba77791492438c0f7eb14fc96fae998/source/resource/clui/image/logo/logo240.png
   :alt: Chronologer

Chronologer UI is a `Qooxdoo`_ application written in ECMAScript 5.1.


.. _qooxdoo: http://www.qooxdoo.org/


Building frontend
=================
The frontend requires Qoodxoo 5 SDK which requires Python 2. The SDK can be installed like::

  wget -q -P /tmp https://github.com/qooxdoo/qooxdoo/archive/branch_5_0_x.zip
  mkdir -p /usr/share/javascript/qooxdoo
  unzip -q -d /usr/share/javascript/qooxdoo /tmp/branch_5_0_x.zip
  mv /usr/share/javascript/qooxdoo/qooxdoo-branch_5_0_x \
     /usr/share/javascript/qooxdoo/qooxdoo-5.0.3-sdk

To install dependencies::

  ./generate.py load-library

To make a development build and serve it locally::

  ./generate.py && ./generate.py source-server

To run the test suite in terminal:

  ./generate.py test-console && ./generate.py testsuite

To make the Python distribution package::

  python3 setup.py sdist

Credits
=======
Logo is contributed by `lightypaints`_.


.. _lightypaints: https://www.behance.net/lightypaints

