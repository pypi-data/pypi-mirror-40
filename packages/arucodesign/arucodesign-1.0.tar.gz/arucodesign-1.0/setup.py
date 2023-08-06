import setuptools

setuptools.setup(
    name="arucodesign",
    version="1.0",
    author="Kenichi Nakahara",
    author_email="kenichi.nakahara.082@gmail.com",
    description="Aruco marker detection module, along with assist plugin of Adobe Illustrator to place Aruco markers on the CAD",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'opencv-python',
        'opencv-contrib-python'
    ],
    python_requires='>3.6.0',
    entry_points={
        'console_scripts': ['arucodesign=aruco_design.command_line:installOnMac']
    }
)
