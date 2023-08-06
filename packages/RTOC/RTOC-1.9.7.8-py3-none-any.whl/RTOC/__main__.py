import sys
import os
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import json
import getopt
import traceback
import time

try:
    from .RTOC import RTOC, RTOC_TCP
    from .RTLogger import RTLogger
    from .data.Daemon import Daemon
except:
    from RTOC import RTOC, RTOC_TCP
    from RTLogger import RTLogger
    from data.Daemon import Daemon


class RTOCDaemon(Daemon):
    def __init__(self, pidfile, port=5050):
        self.pidfile = pidfile
        self.port = 5050

    def run(self):
        # Or simply merge your code with MyDaemon.
        logger = RTLogger(True, self.port)


def main():
    opts, args = getopt.getopt(sys.argv[1:], "hvs:p:r:c:", ["server=","remote=","port=",'config='])
    if len(opts) == 0:
        startRTOC()
    else:
        for opt, arg in opts:
            if opt in ('-p', '--port'):
                port = int(arg)
                break
            else:
                port = 5050
        for opt, arg in opts:
            if opt == '-h':
                print(
                    'RTOC.py [-h, -s] [-r <Remoteadress>]\n -h: Hilfe\n-s (--server) [COMMAND]: TCP-Server ohne GUI\n\t- start: Starts the RTOC-daemon\n\t- stop: Stops the RTOC-daemon\n\t- restart: Restarts the RTOC-daemon\n-r (--remote) <Remoteadresse>: TCP-Client zu RTOC-Server\n-p (--port): Starte TCP-Server auf anderem Port (Standart: 5050)\n-c (--config [OPTION=value]): Configure RTOC, type "-c list" to see all options')
                sys.exit(0)
            elif opt == '-v':
                print("1.9.7.8")
            elif opt in ('-s','--server'):
                if os.name == 'nt':
                    print('Running RTOC as a service is not supported on windows. Running just in background')
                    logger = RTLogger(True, port)
                    #runInBackground()
                    try:
                        while logger.run:
                            time.sleep(1)
                    except:
                        logger.stop()
                    sys.exit(0)
                command = arg
                daemon = RTOCDaemon('/tmp/RTOCDaemon.pid')
                if command == 'stop':
                    daemon.stop()
                elif command == 'restart':
                    daemon.restart()
                elif command == 'start':
                    daemon.start()
                else:
                    print('Unknown server command: '+str(command)+'\nUse "start", "stop" or "restart"')
                    sys.exit(1)
            elif opt in ('-c','--config'):
                configureRTOC(arg)
            elif opt in ("-r", "--remote"):
                remotepath = arg
                startRemoteRTOC(remotepath)
                sys.exit(0)
        #startRTOC(None, port)

def configureRTOC(arg):
    try:
        userpath = os.path.expanduser('~/.RTOC')
        with open(userpath+"/config.json", encoding="UTF-8") as jsonfile:
            config = json.load(jsonfile, encoding="UTF-8")
    except:
        print('No config-file found in ~/.RTOC/\nPlease start RTOC at least once.')
        sys.exit(1)
    if arg == 'list':
        print('This is your current configuration:')
        for key in config.keys():
            if key not in ['csv_profiles','telegram_chat_ids', 'lastSessions', 'grid', 'plotLegendEnabled','blinkingIdentifier','scriptWidget','deviceWidget','signalsWidget','pluginsWidget','eventWidget','newSignalSymbols','plotLabelsEnabled','plotGridEnabled','plotLegendEnabled','signalStyles','plotInverted','plotRate','xTimeBase','timeAxis','systemTray','documentfolder','language']:
                print(key+"\t"+str(config[key]))

    else:
        splitted = arg.split('=')
        if len(splitted)!=2:
            print('Please provide options like this: "python3 -m RTOC -c tcpserver=False\nYour entry didn\'t include a "="')
            sys.exit(1)
        else:
            if splitted[0] not in config.keys():
                print('The config file has no option '+splitted[0])
                sys.exit(1)
            t = type(config[splitted[0]])
            try:
                if t != bool:
                    newValue = t(splitted[1])
                elif splitted[1].lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh','ja','j','jupp','jawohl']:
                    newValue = True
                else:
                    newValue = False

                oldValue = config[splitted[0]]
                config[splitted[0]]=newValue
                with open(userpath+"/config.json", 'w', encoding="utf-8") as fp:
                    json.dump(config, fp,  sort_keys=False, indent=4, separators=(',', ': '))
                print('Option "'+splitted[0]+'" was changed from "'+str(oldValue)+'" to "'+str(newValue)+'"')
            except:
                print('Your entered value "'+splitted[1]+'" is not of the correct type.')
                sys.exit(1)

    # print('This is your new configuration:')
    # for key in config.keys():
    #     if key not in ['csv_profiles','telegram_chat_ids', 'lastSessions', 'grid', 'plotLegendEnabled','blinkingIdentifier','scriptWidget','deviceWidget','signalsWidget','pluginsWidget','eventWidget','newSignalSymbols','plotLabelsEnabled','plotGridEnabled','plotLegendEnabled','signalStyles','plotInverted','plotRate','xTimeBase','timeAxis','systemTray','documentfolder','language']:
    #         print(key+"\t"+str(config[key]))

def setStyleSheet(app, myapp):
    if os.name == 'posix':
        type = 'QDarkStyle'
    else:
        type = 'QtModern'

    if type == 'QtModern':
        try:
            import qtmodern.styles
            import qtmodern.windows
            packagedir = os.path.dirname(os.path.realpath(__file__))
            with open(packagedir+"/data/ui/qtmodern.qss", 'r') as myfile:
                stylesheet = myfile.read().replace('\n', '')
            app.setStyleSheet(stylesheet)
            qtmodern.styles.dark(app)
            #mw = qtmodern.windows.ModernWindow(myapp)

            mw = myapp
            return app, mw
        except ImportError:
            tb = traceback.format_exc()
            #print(tb)
            print("QtModern not installed")
            type = 'QDarkStyle'
    if type == 'QDarkStyle':
        try:
            import qdarkstyle
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            app.setStyleSheet(dark_stylesheet)
            return app, myapp
        except ImportError:
            tb = traceback.format_exc()
            #print(tb)
            print("QtModern not installed")
            type == 'qdarkgraystyle'
    if type == 'qdarkgraystyle':
        try:
            import qdarkgraystyle
            dark_stylesheet = qdarkgraystyle.load_stylesheet()
            app.setStyleSheet(dark_stylesheet)
            return app, myapp
        except ImportError:
            tb = traceback.format_exc()
            #print(tb)
            print("QtModern not installed")
    packagedir = os.path.dirname(os.path.realpath(__file__))
    with open(packagedir+"/data/ui/darkmode.html", 'r') as myfile:
        stylesheet = myfile.read().replace('\n', '')
    stylesheet = stylesheet.replace('/data/ui/icons',os.path.join(packagedir,'data','ui','icons').replace('\\','/'))
    #stylesheet = stylesheet.replace('/data/ui/icons','./data/ui/icons')
    app.setStyleSheet(stylesheet)
    return app, myapp


def setLanguage(app):
    try:
        userpath = os.path.expanduser('~/.RTOC')
        with open(userpath+"/config.json", encoding="UTF-8") as jsonfile:
            config = json.load(jsonfile, encoding="UTF-8")
    except:
        config={'language':'en'}
    if config['language'] == 'en':
        translator = QtCore.QTranslator()
        if getattr(sys, 'frozen', False):
            # frozen
            packagedir = os.path.dirname(sys.executable)
        else:
            # unfrozen
            packagedir = os.path.dirname(os.path.realpath(__file__))
        translator.load(packagedir+"/lang/en_en.qm")
        app.installTranslator(translator)
    # more info here: http://kuanyui.github.io/2014/09/03/pyqt-i18n/
    # generate translationfile: % pylupdate5 RTOC.py -ts lang/de_de.ts
    # compile translationfile: % lrelease-qt5 lang/de_de.ts
    # use self.tr("TEXT TO TRANSLATE") in the code

# def runInBackground():
#     app = QtWidgets.QApplication(sys.argv)
#     myapp = RTOC_TCP()
#     app, myapp = setStyleSheet(app, myapp)
#
#     app.exec_()


def startRemoteRTOC(remotepath):
    app = QtWidgets.QApplication(sys.argv)
    try:
        userpath = os.path.expanduser('~/.RTOC')
        with open(userpath+"/config.json", encoding="UTF-8") as jsonfile:
            config = json.load(jsonfile, encoding="UTF-8")
    except:
        config={'language':'en'}
    if config['language'] == 'en':
        print("English language selected")
        translator = QtCore.QTranslator()
        if getattr(sys, 'frozen', False):
            # frozen
            packagedir = os.path.dirname(sys.executable)
        else:
            # unfrozen
            packagedir = os.path.dirname(os.path.realpath(__file__))
        translator.load(packagedir+"/lang/en_en.qm")
        app.installTranslator(translator)
    myapp = RTOC(False)
    myapp.config["tcpserver"] = True

    app, myapp = setStyleSheet(app, myapp)
    print(remotepath)
    myapp.show()
    myapp.pluginsWidget.show()
    myapp.scriptDockWidget.hide()
    myapp.deviceWidget.hide()
    myapp.eventWidgets.show()
    button = QtWidgets.QPushButton()
    button.setCheckable(True)
    button.setChecked(True)
    myapp.toggleDevice('NetWoRTOC', button)
    myapp.logger.getPlugin('NetWoRTOC').start(remotepath)
    myapp.logger.getPlugin('NetWoRTOC').widget.comboBox.setCurrentText(remotepath)
    myapp.logger.getPlugin('NetWoRTOC').widget.streamButton.setChecked(True)
    app.exec_()


def startRTOC(tcp = None, port = None):
    app = QtWidgets.QApplication(sys.argv)
    try:
        userpath = os.path.expanduser('~/.RTOC')
        with open(userpath+"/config.json", encoding="UTF-8") as jsonfile:
            config = json.load(jsonfile, encoding="UTF-8")
    except:
        config={'language':'en'}
    if config['language'] == 'en':
        print("English language selected")
        translator = QtCore.QTranslator()
        if getattr(sys, 'frozen', False):
            # frozen
            packagedir = os.path.dirname(sys.executable)
        else:
            # unfrozen
            packagedir = os.path.dirname(os.path.realpath(__file__))
        translator.load(packagedir+"/lang/en_en.qm")
        app.installTranslator(translator)
        # more info here: http://kuanyui.github.io/2014/09/03/pyqt-i18n/
        # generate translationfile: % pylupdate5 RTOC.py -ts lang/de_de.ts
        # compile translationfile: % lrelease-qt5 lang/de_de.ts
        # use self.tr("TEXT TO TRANSLATE") in the code
    myapp = RTOC(tcp, port)
    app, myapp = setStyleSheet(app, myapp)

    myapp.show()
    app.exec_()


if __name__ == '__main__':
    main()
    sys.exit()
