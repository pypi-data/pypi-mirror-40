import setuptools

setuptools.setup(
    name="chrome_trex_gym",
    version="0.0.4",
    author="Badr Youbi Idrissi",
    author_email="badryoubiidrissi@gmail.com",
    description="A gym environement for the chrome trex game",
    url="https://github.com/BadrYoubiIdrissi/chrome-trex-gym.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)