znbstatic
=====================================================

Custom Django storage backend.

Features
------------------------------------------------------------------------------

- Storage of assets managed by collectstatic on Amazon Web Services S3.
- Versioning using a variable from Django's settings (https://example.com/static/css/styles.css?v=1.2)

Installation Notes
------------------------------------------------------------------------------

Using a Docker container with some Python 3 packages for initial tests.

Change to the directory where the Dockerfile is and build the image from there. Note the use of $(date) to use today's date as part of the image's name.

.. code-block:: bash

  $ docker build --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t alexisbellido/znbstatic-$(date +%Y%m%d) .

Then run the container and make sure you don't map over the /root directory because that's where ssh key from the host is stored if you use a temporary container. 

.. code-block:: bash

  $ docker run -it --rm --mount type=bind,source=$PWD,target=/root/project alexisbellido/znbstatic-20190107:latest docker-entrypoint.sh /bin/bash
  

Installing and Uninstalling Packages
------------------------------------------------------------------------------

Installing in editable mode from local directory.

.. code-block:: bash

  $ pip install -e /path/to/znbstatic/

You can remove the -e to install the package in the corresponding Python path, for example: /env/lib/python3.7/site-packages/znbstatic.

List installed packages and uninstall.

.. code-block:: bash

  $ pip list
  $ pip uninstall znbstatic

Installing from git using https.

.. code-block:: bash

  $ pip install git+https://github.com/requests/requests.git#egg=requests
  $ pip install git+https://github.com/alexisbellido/znbstatic.git#egg=znbstatic


Distribute as a setuptools-based Package
------------------------------------------------------------------------------

This can be run from a host or a container. My tests have been on a container.

.. code-block:: bash

  $ pip install setuptools wheel
  $ pip install twine

Run this from the same directory where setup.py is located.

.. code-block:: bash

  $ python setup.py sdist bdist_wheel

Upload to Test PyPi at `<https://test.pypi.org>`_.

  $ twine upload --repository-url https://test.pypi.org/legacy/ dist/*

The package is now available at `<https://test.pypi.org/project/znbstatic/>`_ and can be installed with pip.

.. code-block:: bash

  $ pip install -i https://test.pypi.org/simple/ znbstati

Upload to the real PyPi at `<https://pypi.org>`_.

.. code-block:: bash

  $ twine upload dist/*

The package is now available at `<https://pypi.org/project/znbstatic/>`_ and can be installed with pip.

.. code-block:: bash

  $ pip install znbstatic

Additional Resources
------------------------------------------------------------------------------

  * `packaging projects <https://packaging.python.org/tutorials/packaging-projects>`_.
  * `setuptools <https://setuptools.readthedocs.io/en/latest/setuptools.html>`_.
  * `pip install <https://pip.pypa.io/en/stable/reference/pip_install>`_ documentation.

Amazon S3
-----------------------------------------------

Some notes to use S3 for storing Django files.

Cross-origin resource sharing (CORS) defines a way for client web applications that are loaded in one domain to interact with resources in a different domain.

More on `S3 access permissions <https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-access-control.html>`_.

Option 1 (preferred): Resource-based policy.

A bucket configured to be allow publc read access and full control by a IAM user that will be used from Django.

Create a IAM user. Write down the arn and user credentials (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY).

Don't worry about adding a user policy as you will be using a bucket policy to refer to this user by its arn.

Create an S3 bucket at url-of-s3-bucket.

Assign it the following CORS configuration in the permissions tab.

.. code-block:: bash

  <?xml version="1.0" encoding="UTF-8"?>
  <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <CORSRule>
      <AllowedOrigin>*</AllowedOrigin>
      <AllowedMethod>GET</AllowedMethod>
      <MaxAgeSeconds>3000</MaxAgeSeconds>
      <AllowedHeader>Authorization</AllowedHeader>
  </CORSRule>
  </CORSConfiguration>

and the following bucket policy (use the corresponding arn for the bucket and for the IAM user that will have full control).

.. code-block:: bash

  {
      "Version": "2012-10-17",
      "Id": "name-of-bucket",
      "Statement": [
          {
              "Sid": "PublicReadForGetBucketObjects",
              "Effect": "Allow",
              "Principal": "*",
              "Action": "s3:GetObject",
              "Resource": "arn:aws:s3:::name-of-bucket/*"
          },
          {
              "Sid": "FullControlForBucketObjects",
              "Effect": "Allow",
              "Principal": {
                  "AWS": "arn:aws:iam::364908532015:user/name-of-user"
              },
              "Action": "s3:*",
              "Resource": [
                  "arn:aws:s3:::name-of-bucket",
                  "arn:aws:s3:::name-of-bucket/*"
              ]
          }
      ]
  }
  

Option 2: user policy.

A user configured to control an specific bucket.

Create an S3 bucket at url-of-s3-bucket.

Assign it the following CORS configuration in the permissions tab.

.. code-block:: bash

  <?xml version="1.0" encoding="UTF-8"?>
  <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <CORSRule>
      <AllowedOrigin>*</AllowedOrigin>
      <AllowedMethod>GET</AllowedMethod>
      <MaxAgeSeconds>3000</MaxAgeSeconds>
      <AllowedHeader>Authorization</AllowedHeader>
  </CORSRule>
  </CORSConfiguration>

Create a user in IAM and assign it to this policy.

.. code-block:: bash

  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Sid": "Stmt1394043345000",
              "Effect": "Allow",
              "Action": [
                  "s3:*"
              ],
              "Resource": [
                  "arn:aws:s3:::url-of-s3-bucket/*"
              ]
          }
      ]
  }

Then create the user credentials (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY) to connect from Django.