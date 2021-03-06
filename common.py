#!/usr/bin/env python
# -*- coding: utf-8 -*-
# common.py
#
# Author: Yann KOETH
# Created: Wed Jul 16 19:11:21 2014 (+0200)
# Last-Updated: Thu Jul 24 10:33:48 2014 (+0200)
#           By: Yann KOETH
#     Update #: 148
#

import cv2
import os
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QGraphicsBlurEffect, QGraphicsPixmapItem

from tree import Tree

class CustomException(Exception):
    pass

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

def setPickerColor(color, colorPicker):
    """Set the color picker color.
    """
    css = 'QWidget { background-color: %s; border-width: 0; \
        border-radius: 2px; border-color: #555; border-style: outset; }'
    colorPicker.setStyleSheet(css % color.name())

def checkerboard(size):
    """Create a checkboard.
    """
    h, w = size.height(), size.width()
    c0 = (191, 191, 191, 255)
    c1 = (255, 255, 255, 255)
    blocksize = 8
    coords = np.ogrid[0:h,0:w]
    idx = (coords[0] // blocksize + coords[1] // blocksize) % 2
    vals = np.array([c0, c1], dtype=np.uint8)
    return np2Qt(vals[idx])

def np2Qt(image):
    """Convert numpy array to QPixmap.
    """
    height, width, bytesPerComponent = image.shape
    bytesPerLine = 4 * width

    if bytesPerComponent == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
    qimg = QImage(image.data, width, height,
                  bytesPerLine, QImage.Format_ARGB32)
    return QPixmap.fromImage(qimg)

def fitImageToScreen(pixmap):
    """Fit pixmap to screen.
    """
    resolution = QDesktopWidget().screenGeometry()
    h, w = resolution.width(), resolution.height()
    w = min(pixmap.width(), w)
    h = min(pixmap.height(), h)
    return pixmap.scaled(QtCore.QSize(w, h), QtCore.Qt.KeepAspectRatio)

def blurPixmap(pixmap, radius):
    effect = QGraphicsBlurEffect()
    effect.setBlurRadius(radius)
    buffer = QPixmap(pixmap)
    item = QGraphicsPixmapItem(buffer)
    item.setGraphicsEffect(effect)
    output = QPixmap(pixmap.width(), pixmap.height())
    painter = QtGui.QPainter(output)
    scene = QtWidgets.QGraphicsScene()
    view = QtWidgets.QGraphicsView(scene)
    scene.addItem(item)
    scene.render(painter)
    return output

def scaleRect(rect, scale):
    """Scale 'rect' with a factor of 'scale'.
    """
    x, y, w, h = rect
    return (x * scale, y * scale, w * scale, h * scale)

def getObjectsTree(qTreeView, table, indexes, extract):
    """Create an object tree representation from QTreeView.
    """
    tree = Tree()
    model = qTreeView.model()
    extracted = tree.fromQStandardItemModel(model, table, indexes, extract)
    return tree, extracted
