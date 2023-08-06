.. _subscriber_directive:

``subscriber``
--------------

The ``subscriber`` ZCML directive configures an :term:`subscriber`
callable to listen for events broadcast by the Pyramid web
framework.

Attributes
~~~~~~~~~~

``for``
   The class or :term:`interface` that you are subscribing the listener for,
   e.g. :class:`pyramid.events.NewRequest`.  Registering a subscriber for a
   specific class or interface limits the event types that the subscriber
   will receive to those specified by the interface or class.  Default:
   ``zope.interface.Interface`` (implying *any* event type).

``handler``
   A :term:`dotted Python name` which references an event handler
   callable.  The callable should accept a single argument: ``event``.
   The return value of the callable is ignored.

Examples
~~~~~~~~

.. code-block:: xml
   :linenos:

   <subscriber
      for="pyramid.events.NewRequest"
      handler=".subscribers.handle_new_request"
    />

Alternatives
~~~~~~~~~~~~

You can also register an event listener by using the
:meth:`pyramid.config.Configurator.add_subscriber` method.

See Also
~~~~~~~~

See also :ref:`events_chapter`.
