# Ricochet - IoC simplified

**This is still in concept stage. No implementation exists yet**

Ricochet is designed to be an architectural design framework for Python applications which utilises inversion of 
control. Built with the aim of making complex designs simpler to implement, this framework will allow you to specify 
dependencies between components in a simple way and allow the framework to handle wiring the references together.  

It is designed to be simple, easy to learn, fast to use, but powerful when you need it, and aims to provide utilities
for wiring up a Python application using tagged components (similar to Java annotations) and configuration classes.
The recoil runner context will then manage dependency injection for you on startup, creating singletons of each
class you tag.

