A simple redis lock.
=========================

Installation
---------------

.. code-block:: sh

    pip install simple-redis-lock


Usage
-------

.. code-block:: py

    from simple_redis_lock import SimpleLock
    import your_redis_client

    with SimpleLock(your_redis_client, 'my_lock_name', ex=30):
        print('do something')
