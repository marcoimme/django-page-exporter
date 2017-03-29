.. include:: globals
.. _glossary:


Glossary
====================

.. glossary::

    Administrator
        Special user that can access the administration pages of |project-label|

    Anonymous User
        User not logged into |project-label|

    Authenticated User
        Standard User logged into |project-label| that belongs to at least one Role

    Guest User
        Any user who does not belong to any group, ie they have no privileges.

    Group
        Represents a role in the system. Privileges are granted to a :term:`Group` and any
        :term:`Authenticated User` belongs to one or more  :term:`Group`

    Superuser
        Special user that can access any part of the system

    System Adminstrator
        Host administrator, does not have any role in |project-label|.
        They configure the architectural components like Web Server, Database, Logging...

        .. note:: for security reasons these users do not have any privileges in |project-label|