A simple redis lock.
=========================

Installation
---------------

.. code-block:: sh

    pip install simple-redis-lock


Usage
-------

.. code-block:: py

    from simple_redis_lock import simple_lock
    import your_redis_client

    with simple_lock(your_redis_client, 'my_lock_name', ex=30) as lock:
        if lock:
            print('do something')
        else:
            print('do not get lock, return')
