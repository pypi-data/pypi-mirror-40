#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import shutil
import subprocess
from pathlib import Path
from distutils.spawn import find_executable

import cv2

aruco_images_dir = (Path(__file__).parent / 'aruco_6x6_250').as_posix()
extendscript_dir = (Path(__file__).parent / 'extendscript').as_posix()


def generate_marker_images():
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    if not os.path.exists(aruco_images_dir):
        os.mkdir(aruco_images_dir)

    for i in range(250):
        marker_i = cv2.aruco.drawMarker(dictionary, i, 250)
        cv2.imwrite(os.path.join(aruco_images_dir, f'aruco6x6_{i}.jpg'), marker_i)


def build_extendscript():
    assert find_executable('npm') is not None, 'npm not installed. this is necessary to build scripts that will work on Illustrator.'

    install_depencencies = subprocess.Popen(['npm', 'install'], cwd=extendscript_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    install_depencencies.wait()
    build = subprocess.Popen(['npm', 'run', 'build'], cwd=extendscript_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    build.wait()


def installOnMac():

    assert any(['Illustrator' in app_name for app_name in os.listdir('/Applications')]), 'Illustrator is not installed. this is mendatory'

    generate_marker_images()
    build_extendscript()

    script_dirname_candidates = ('Scripts', 'スクリプト')
    scripts_dir_candidates = []
    for dirname in script_dirname_candidates:
        scripts_dir_candidates += list(Path('/Applications/').glob(f'*Illustrator*/Presets*/**/{dirname}'))

    scripts_dir = scripts_dir_candidates[0]
    shutil.copytree(aruco_images_dir, os.path.join(scripts_dir, aruco_images_dir.split('/')[-1]))
    shutil.copy(os.path.join(extendscript_dir, 'dist', 'ArucoDesign.js'), scripts_dir)
