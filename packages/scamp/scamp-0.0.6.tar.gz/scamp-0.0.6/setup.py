import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scamp",
    version="0.0.6",
    author="Marc Evanstein",
    author_email="marc@marcevanstein.com",
    description="An algorithmic composition framework that manages the flow of musical time, plays back notes via "
                "fluidsynth or though osc, and quantizes and saves the result to music notation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarcTheSpark/scamp",
    packages=setuptools.find_packages(),
    install_requires=['pymusicxml', 'expenvelope', 'clockblocks', 'pyfluidsynth', 'sf2utils', 'python-osc'],
    extras_require={
        'lilypond': 'abjad',
        'midistream': 'python-rtmidi'
    },
    package_data={
        'scamp': ['settings/*', 'soundfonts/*']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
