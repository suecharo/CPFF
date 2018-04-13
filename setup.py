from setuptools import setup


def main():
    setup(
        name="KPHMMER",
        version="1.0.1",
        description="KPHMMER: Hidden Markov Model generator for detecting KEGG PATHWAY-specific genes",
        author="Hirotaka Suetake",
        author_email="hirotaka.suetake@riken.jp",
        license="MIT",
        keywords=["Life Science", "Bioinfomatics", "HMMER", "KEGG"],
        packages=["KPHMMER"],
        zip_safe=False,
        include_package_data=True,
        install_requires=[
            "numpy",
            "PyYAML",
            "scipy",
            "requests"
        ],
        scripts=["bin/kphmmer"],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Scientific/Engineering :: Bio-Informatics",
        ]
    )


if __name__ == "__main__":
    main()
