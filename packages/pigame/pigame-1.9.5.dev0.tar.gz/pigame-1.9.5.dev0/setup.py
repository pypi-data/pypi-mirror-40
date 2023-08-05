from setuptools import setup


DESCRIPTION = """Pygame is a Python wrapper module for the
SDL multimedia library. It contains python functions and classes
that will allow you to use SDL's support for playing cdroms,
audio and video output, and keyboard, mouse and joystick input."""
setup(
    name="pigame",
    version="1.9.5.dev0",
    license="LGPL",
    url="https://www.pygame.org",
    author="Pete Shinners, Rene Dudfield, Marcus von Appen, Bob Pendleton, others...",
    author_email="pygame@seul.org",
    description="Python Game Development",
    long_description=DESCRIPTION,
    install_requires=['pygame', 'pygame.snake'],
)
