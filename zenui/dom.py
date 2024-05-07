#!/usr/bin/env python3
from .singleton import SingletonMeta

class DOM(metaclass=SingletonMeta):
    """
        Python utility that allows python developers
        to interact with the browser document.
        it returns js code for trynscrypt
    """
    def init(self, id):
        return document.querySelector(id)

    def style(self, id, styles):
        self.init(id).style = styles

    def activeElement(self):
        return document.activeElement

    def documentEventListener(self, event, callback):
        document.addEventListener(event, callback)

    def adoptNode(self, node):
        return document.adoptNode(node)

    def baseURI(self):
        return document.baseURI

    def body(self):
        return document.body

    def close(self):
        return document.close()

    def cookie(self):
        return document.cookie

    def characterSet(self):
        return document.characterSet

    def createAttribute(self, name, value):
        att = document.createAttribute(name)
        att.value = value

    def createComment(self, comment):
        document.createComment(comment)

    def createDocumentFragment(self):
        return document.createDocumentFragment()

    def createElement(self, element):
        return document.createElement(element)

    def createEvent(self, event):
        return document.createEvent(event)

    def createTextNode(self, text):
        return document.createTextNode(text)

    def defaultView(self):
        return document.defaultView

    def designModeOn(self):
        document.designMode = 'on'

    def designModeOff(self):
        document.designMode = 'off'

    def documentElement(self):
        return document.documentElement

    def documentURI(self):
        return document.documentURI

    def domain(self):
        return document.domain

    def embeds(self):
        return document.embeds

    def exeCommand(self, event):
        return document.exeCommand(event)

    def forms(self):
        return document.forms

    def fullScreenElement(self):
        return document.fullscreenElement

    def fullScreenEnabled(self):
        return document.fullscreenEnabled

    def getElementById(self, id):
        return document.getElementById(id)

    def getElementByClassName(self, className):
        return document.getElementsByClassName(className)

    def getElementByName(self, name):
        return document.getElementsByName(name)

    def getElementByTagName(self, tagName):
        return document.getElementsByTagName(tagName)

    def hasFocus(self):
        return document.hasFocus()

    def head(self):
        return document.head

    def images(self):
        return document.images

    def implementation(self):
        return document.implementation

    def importNode(self, node):
        return document.importNode(node, True)

    def lastModified(self):
        return document.lastModified

    def normalize(self):
        document.normalize()

    def open(self):
        document.open()

    def querySelector(self, selector):
        return document.querySelector(selector)

    def querySelectorAll(self, selector):
        return document.querySelectorAll(selector)

    def readyState(self):
        return document.readyState

    def referrer(self):
        return document.referrer

    def removeEventListener(self, event):
        document.removeEventListener(event)

    def scripts(self):
        return document.scripts

    def title(self):
        return document.title

    def URL(self):
        return document.URL

    def write(self, text):
        document.write(text)

    def writeLn(self, text):
        document.writeln(text)

    def abort(self, id, callback):
        self.init(id).addEventListener('abort', callback)

    def afterPrint(self, id, callback):
        self.init(id).addEventListener('afterprint', callback)

    def animationEnd(self, id, callback):
        self.init(id).addEventListener('animationend', callback)

    def animationIteration(self, id, callback):
        self.init(id).addEventListener('animationiteration', callback)

    def animationStart(self, id, callback):
        self.init(id).addEventListener('animationstart', callback)

    def beforePrint(self, id, callback):
        self.init(id).addEventListener('beforeprint', callback)

    def beforeUnload(self, id, callback):
        self.init(id).addEventListener('beforeunload', callback)

    def blur(self, id, callback):
        self.init(id).addEventListener('blur', callback)

    def canPlay(self, id, callback):
        self.init(id).addEventListener('oncanplay', callback)

    def canPlayThrough(self, id, callback):
        self.init(id).addEventListener('canplaythrough', callback)

    def change(self, id, callback):
        self.init(id).addEventListener('change', callback)

    def click(self, id, callback):
        self.init(id).addEventListener('click', callback)

    def contextMenu(self, id, callback):
        self.init(id).addEventListener('contextmenu', callback)

    def copy(self, id, callback):
        self.init(id).addEventListener('copy', callback)

    def cut(self, id, callback):
        self.init(id).addEventListener('cut', callback)

    def dblClick(self, id, callback):
        self.init(id).addEventListener('dblclick', callback)

    def drag(self, id, callback):
        self.init(id).addEventListener('drag', callback)

    def dragEnd(self, id, callback):
        self.init(id).addEventListener('dragend', callback)

    def dragEnter(self, id, callback):
        self.init(id).addEventListener('dragenter', callback)

    def dragLeave(self, id, callback):
        self.init(id).addEventListener('dragleave', callback)

    def dragOver(self, id, callback):
        self.init(id).addEventListener('dragover', callback)

    def dragStart(self, id, callback):
        self.init(id).addEventListener('dragstart', callback)

    def durationChange(self, id, callback):
        self.init(id).addEventListener('durationchange', callback)

    def ended(self, id, callback):
        self.init(id).addEventListener('ended', callback)

    def error(self, id, callback):
        self.init(id).addEventListener('error', callback)

    def focus(self, id, callback):
        self.init(id).addEventListener('focus', callback)

    def focusIn(self, id, callback):
        self.init(id).addEventListener('focusin', callback)

    def fullScreenChange(self, id, callback):
        self.init(id).addEventListener('fullscreenchange', callback)

    def fullScreenError(self, id, callback):
        self.init(id).addEventListener('fullscreenerror', callback)

    def hashChange(self, id, callback):
        self.init(id).addEventListener('hashChange', callback)

    def focus(self, id, callback):
        self.init(id).addEventListener('focus', callback)

    def input(self, id, callback):
        self.init(id).addEventListener('input', callback)

    def invalid(self, id, callback):
        self.init(id).addEventListener('invalid', callback)

    def keyDown(self, id, callback):
        self.init(id).addEventListener('keydown', callback)

    def keyPress(self, id, callback):
        self.init(id).addEventListener('keypress', callback)

    def keyUp(self, id, callback):
        self.init(id).addEventListener('keyup', callback)

    def load(self, id, callback):
        self.init(id).addEventListener('load', callback)

    def loadedData(self, id, callback):
        self.init(id).addEventListener('loadeddata', callback)

    def loadedMetaData(self, id, callback):
        self.init(id).addEventListener('loadedmetadata', callback)

    def loadStart(self, id, callback):
        self.init(id).addEventListener('loadstart', callback)

    def message(self, id, callback):
        self.init(id).addEventListener('message', callback)

    def mouseDown(self, id, callback):
        self.init(id).addEventListener('mousedown', callback)

    def mouseEnter(self, id, callback):
        self.init(id).addEventListener('mouseenter', callback)

    def mouseLeave(self, id, callback):
        self.init(id).addEventListener('mouseleave', callback)

    def mouseMove(self, id, callback):
        self.init(id).addEventListener('mousemove', callback)

    def mouseOver(self, id, callback):
        self.init(id).addEventListener('mouseover', callback)

    def mouseOut(self, id, callback):
        self.init(id).addEventListener('mouseout', callback)

    def mouseUp(self, id, callback):
        self.init(id).addEventListener('mouseup', callback)

    def offline(self, id, callback):
        self.init(id).addEventListener('offline', callback)

    def online(self, id, callback):
        self.init(id).addEventListener('online', callback)

    def open(self, id, callback):
        self.init(id).addEventListener('open', callback)

    def pageHide(self, id, callback):
        self.init(id).addEventListener('pagehide', callback)

    def pageShow(self, id, callback):
        self.init(id).addEventListener('pageshow', callback)

    def paste(self, id, callback):
        self.init(id).addEventListener('paste', callback)

    def pause(self, id, callback):
        self.init(id).addEventListener('pause', callback)

    def play(self, id, callback):
        self.init(id).addEventListener('play', callback)

    def playing(self, id, callback):
        self.init(id).addEventListener('playing', callback)

    def popState(self, id, callback):
        self.init(id).addEventListener('popstate', callback)

    def progress(self, id, callback):
        self.init(id).addEventListener('progress', callback)

    def rateChange(self, id, callback):
        self.init(id).addEventListener('ratechange', callback)

    def resize(self, id, callback):
        self.init(id).addEventListener('resize', callback)

    def reset(self, id, callback):
        self.init(id).addEventListener('reset', callback)

    def scroll(self, id, callback):
        self.init(id).addEventListener('scroll', callback)

    def search(self, id, callback):
        self.init(id).addEventListener('search', callback)

    def seeked(self, id, callback):
        self.init(id).addEventListener('seeked', callback)

    def seeking(self, id, callback):
        self.init(id).addEventListener('seeking', callback)

    def select(self, id, callback):
        self.init(id).addEventListener('select', callback)

    def show(self, id, callback):
        self.init(id).addEventListener('show', callback)

    def stalled(self, id, callback):
        self.init(id).addEventListener('stalled', callback)

    def storage(self, id, callback):
        self.init(id).addEventListener('storage', callback)

    def submit(self, id, callback):
        self.init(id).addEventListener('submit', callback)

    def suspend(self, id, callback):
        self.init(id).addEventListener('suspend', callback)

    def timeUpdate(self, id, callback):
        self.init(id).addEventListener('timeupdate', callback)

    def toggle(self, id, callback):
        self.init(id).addEventListener('toggle', callback)

    def touchCancel(self, id, callback):
        self.init(id).addEventListener('touchcancel', callback)

    def touchEnd(self, id, callback):
        self.init(id).addEventListener('touchend', callback)

    def touchMove(self, id, callback):
        self.init(id).addEventListener('touchmove', callback)

    def touchStart(self, id, callback):
        self.init(id).addEventListener('touchstart', callback)

    def transitionEnd(self, id, callback):
        self.init(id).addEventListener('transitionend', callback)

    def unload(self, id, callback):
        self.init(id).addEventListener('unload', callback)

    def volumeChange(self, id, callback):
        self.init(id).addEventListener('volumechange', callback)

    def waiting(self, id, callback):
        self.init(id).addEventListener('waiting', callback)

    def wheel(self, id, callback):
        self.init(id).addEventListener('wheel', callback)