# Recoil - IoC simplified

**This is still in concept stage. No implementation exists yet**

Recoil is designed to be a simplified inversion-of-control (IoC) framework for Python3.6 and higher, based on the ideas
behind Java's Spring Framework (namely `spring-context`, `spring-beans`, etc.)

It is designed to be simple, easy to learn, fast to use, but powerful when you need it, and aims to provide utilities
for wiring up a Python application using tagged components (similar to Java annotations) and configuration classes.
The recoil runner context will then manage dependency injection for you on startup, creating singletons of each
class you tag.

Many of the features will be implemented in Cython where possible to reduce the execution overhead as much as possible,
however, pure-Python implementations will also be provided for convenience for those without access to a C compiler.
