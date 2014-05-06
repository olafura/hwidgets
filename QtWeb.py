import sys

from PySide.QtCore import QObject, Slot, Signal, QUrl
from PySide.QtGui import QApplication
from PySide.QtWebKit import QWebView, QWebSettings
from PySide.QtNetwork import QNetworkRequest

from Battery import Battery
from Wifi import Wifi

import json

class Application(object):

    def show(self):
        self.battery = Battery()
        self.wifi = Wifi()
        self.url = QUrl("qt.html")

        self.web = QWebView()

        self.web.loadFinished.connect(self.onLoad)
        self.web.load(self.url)

        self.web.show()

    def onLoad(self):
        self.page = self.web.page()
        self.page.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        self.frame = self.page.mainFrame()
        self.frame.addToJavaScriptWindowObject("battery", self.battery)
        self.frame.addToJavaScriptWindowObject("wifi", self.wifi)

        self.frame.evaluateJavaScript("isReady()")
        self.wifi.loop.run()


app = QApplication(sys.argv)

webapp = Application()
webapp.show()

sys.exit(app.exec_())
