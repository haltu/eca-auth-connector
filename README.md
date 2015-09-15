# Auth Connector Service

The Connector Service is used for adding authentication methods for users in the system.

New user is invited to the system as Invitee. The invitation happens by the Invitator. Invitator must be existing user in the system.

Each user can have multiple authentication methods in use from the set of supported methods.

The Connector Service is using Auth Proxy to authenticate users. The connections are stored in the Auth Data Service.

The Connector Service does not have any interfaces. It is used be the users with a browser.

