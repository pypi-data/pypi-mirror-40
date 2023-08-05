import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blog_image_auto_syncer",
    version="0.0.3",
    author="vanjor",
    author_email="vanjor2008@gmail.com",
    description="auto download image from your blog and sync to github",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanjor/blog_image_auto_syncer",
    #packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    packages=["blog_image_auto_syncer", "blog_image_auto_syncer.commands"],

    entry_points={
        "blog_image_auto_syncer.registered_commands": [
            "check = blog_image_auto_syncer.commands.test:main",
        ]
    }
)