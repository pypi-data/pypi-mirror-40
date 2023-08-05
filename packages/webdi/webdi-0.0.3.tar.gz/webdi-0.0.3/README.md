# A Simple Dependency Injection Container for Web Apps

This module contains a simple dependency injection container that is optimized
for web apps. You define relationships once, and then each request (probably
via middleware) receives a container that references the once-defined
definition to build memoized services for just that request.

Please note: documentation on this project is currently not provided

## Running tests:

`python -m tests`
