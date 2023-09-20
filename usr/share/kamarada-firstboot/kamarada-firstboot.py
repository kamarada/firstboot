#!/usr/bin/python3

from os.path import abspath, dirname, expanduser, join, realpath
import subprocess
import sys
import threading

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gdk, Gtk


whereAmI = abspath(dirname(realpath(__file__)))


APPLICATION_WINDOW = join(whereAmI, 'kamarada-firstboot.ui')
BACKGROUND_PICTURE = '/usr/share/wallpapers/Ribeirao-Capivari/contents/images/3840x2160.jpg'
CUSTOM_CSS_STYLESHEET = join(whereAmI, 'kamarada-firstboot.css')
RESULT_FILE = expanduser('~/.config/kamarada-firstboot')


class FirstBootBackgroundWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._canClose = False
        self.connect('close-request', self.onCloseRequest)

        self.background_picture = Gtk.Picture.new_for_filename(BACKGROUND_PICTURE)
        self.background_picture.set_keep_aspect_ratio(False)
        self.set_child(self.background_picture)

        self.fullscreen()

    def closeFromApp(self):
        self._canClose = True
        self.close()

    def onCloseRequest(self, user_data):
        return ~self._canClose


@Gtk.Template(filename=APPLICATION_WINDOW)
class FirstBootMainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'FirstBootMainWindow'

    btnBack = Gtk.Template.Child()
    btnEnglish = Gtk.Template.Child()
    btnPortuguese = Gtk.Template.Child()
    btnReboot = Gtk.Template.Child()
    btnShutdown = Gtk.Template.Child()
    grdLanguage = Gtk.Template.Child()
    grdTryInstall = Gtk.Template.Child()
    headerBar = Gtk.Template.Child()
    imgEnglish = Gtk.Template.Child()
    imgInstall = Gtk.Template.Child()
    imgPortuguese = Gtk.Template.Child()
    imgTry = Gtk.Template.Child()
    lbInstallButton = Gtk.Template.Child()
    lbInstallInfo = Gtk.Template.Child()
    lbTryButton = Gtk.Template.Child()
    lbTryInfo = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    subtitle = Gtk.Template.Child()
    title = Gtk.Template.Child()

    def __init__(self, firstboot_app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.firstboot_app = firstboot_app

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(CUSTOM_CSS_STYLESHEET)
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.imgPortuguese.set_filename(join(whereAmI, 'png/BR.png'))

        self.imgEnglish.set_filename(join(whereAmI, 'png/international-english.png'))

        self.imgTry.set_filename(join(whereAmI, 'png/try.png'))

        self.imgInstall.set_filename(join(whereAmI, 'png/install.png'))

        self.stack.add_named(self.grdLanguage, 'grdLanguage')
        self.stack.add_named(self.grdTryInstall, 'grdTryInstall')

        self.connect('close-request', self.onCloseRequest)

        self.translateInterface()

    def launchInstaller(self):
        subprocess.run([
            'LANG=' + self.firstboot_app.getLanguage() +
            ' QT_QPA_PLATFORMTHEME="gtk2"' +
            ' kdesu -c /usr/bin/calamares'
        ], shell=True)
        self.show()

    def translateInterface(self):
        # Maybe there is a better way to translate the interface
        # https://stackoverflow.com/q/69791625/1657502
        if (self.firstboot_app.getLanguage() == 'en_US'):
            self._yes = 'Yes'
            self._no = 'No'
            self._shutdownDialogText = 'Your computer is going to shutdown.'
            self._rebootDialogText = 'Your computer is going to reboot.'
            self._areYouSure = 'Are you sure you want to continue?'
            self.btnBack.set_label('Back')
            self.btnShutdown.set_tooltip_text('Shutdown')
            self.btnReboot.set_tooltip_text('Reboot')
            self.lbTryButton.set_label('Try Linux Kamarada')
            self.lbInstallButton.set_label('Install Linux Kamarada')
            self.lbTryInfo.set_label('You can try Linux Kamarada without making any changes to your computer, directly from this live medium.')
            self.lbInstallInfo.set_label('Or, if you\'re ready, you can install Linux Kamarada alongside (or instead of) your current operating system.')
        elif (self.firstboot_app.getLanguage() == 'pt_BR'):
            self._yes = 'Sim'
            self._no = 'Não'
            self._shutdownDialogText = 'Seu computador será desligado.'
            self._rebootDialogText = 'Seu computador será reiniciado.'
            self._areYouSure = 'Tem certeza de que quer continuar?'
            self.btnBack.set_label('Voltar')
            self.btnShutdown.set_tooltip_text('Desligar')
            self.btnReboot.set_tooltip_text('Reiniciar')
            self.lbTryButton.set_label('Experimentar o Linux Kamarada')
            self.lbInstallButton.set_label('Instalar o Linux Kamarada')
            self.lbTryInfo.set_label('Você pode experimentar o Linux Kamarada sem fazer quaisquer alterações no seu computador, diretamente desta mídia live.')
            self.lbInstallInfo.set_label('Ou, se estiver pronto, você poderá instalar o Linux Kamarada juntamente com, ou no lugar do, seu sistema operacional atual.')

    @Gtk.Template.Callback()
    def onBtnPortugueseClicked(self, button):
        self.firstboot_app.setLanguage('pt_BR')
        self.translateInterface()
        self.btnBack.show()
        self.title.set_label('Bem-vindo')
        self.subtitle.set_label('')
        self.btnShutdown.show()
        self.btnReboot.show()
        self.stack.set_visible_child(self.grdTryInstall)

    @Gtk.Template.Callback()
    def onBtnEnglishClicked(self, button):
        self.firstboot_app.setLanguage('en_US')
        self.translateInterface()
        self.btnBack.show()
        self.title.set_label('Welcome')
        self.subtitle.set_label('')
        self.btnShutdown.show()
        self.btnReboot.show()
        self.stack.set_visible_child(self.grdTryInstall)

    @Gtk.Template.Callback()
    def onBtnBackClicked(self, button):
        self.firstboot_app.setLanguage('en_US')
        self.btnBack.hide()
        self.title.set_label('Bem-vindo')
        self.subtitle.set_label('Welcome')
        self.btnShutdown.hide()
        self.btnReboot.hide()
        self.stack.set_visible_child_full('grdLanguage', Gtk.StackTransitionType.SLIDE_RIGHT)

    @Gtk.Template.Callback()
    def onBtnShutdownClicked(self, button):
        dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.QUESTION,
                                   modal=True,
                                   transient_for=self,
                                   text = self._shutdownDialogText,
                                   secondary_text = self._areYouSure)
        dialog.add_buttons(self._yes, Gtk.ResponseType.YES, self._no, Gtk.ResponseType.NO)
        dialog.set_default_response(Gtk.ResponseType.NO)
        dialog.connect('response', self.onShutdownDialogResponse)
        dialog.present()

    def onShutdownDialogResponse(self, dialog, response):
        if (response == Gtk.ResponseType.YES):
            self.firstboot_app.writeResultAndExit('Shutdown')
        else:
            dialog.close()

    @Gtk.Template.Callback()
    def onBtnRebootClicked(self, button):
        dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.QUESTION,
                                   modal=True,
                                   transient_for=self,
                                   text = self._rebootDialogText,
                                   secondary_text = self._areYouSure)
        dialog.add_buttons(self._yes, Gtk.ResponseType.YES, self._no, Gtk.ResponseType.NO)
        dialog.set_default_response(Gtk.ResponseType.NO)
        dialog.connect('response', self.onRebootDialogResponse)
        dialog.present()

    def onRebootDialogResponse(self, dialog, response):
        if (response == Gtk.ResponseType.YES):
            self.firstboot_app.writeResultAndExit('Reboot')
        else:
            dialog.close()

    @Gtk.Template.Callback()
    def onBtnTryClicked(self, button):
        self.firstboot_app.writeResultAndExit('Try')

    @Gtk.Template.Callback()
    def onBtnInstallClicked(self, button):
        # https://askubuntu.com/a/1486389/560233
        self.hide()
        timer = threading.Timer(1, self.launchInstaller)
        timer.start()

    def onCloseRequest(self, user_data):
        if self.firstboot_app.getAction():
            return False
        dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.QUESTION,
                                   modal=True,
                                   transient_for=self,
                                   text = self._rebootDialogText,
                                   secondary_text = self._areYouSure)
        dialog.add_buttons(self._yes, Gtk.ResponseType.YES, self._no, Gtk.ResponseType.NO)
        dialog.set_default_response(Gtk.ResponseType.NO)
        dialog.connect('response', self.onRebootDialogResponse)
        dialog.present()
        return True


class FirstBootApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setLanguage('en_US')
        self.setAction('')

        self.connect('activate', self.onActivate)

    def getAction(self):
        return self._action

    def getLanguage(self):
        return self._language

    def onActivate(self, app):
        self.background_window = FirstBootBackgroundWindow(application=self)
        self.background_window.present()

        self.main_window = FirstBootMainWindow(self, application=self)
        self.main_window.set_transient_for(self.background_window)
        self.main_window.present()

    def setAction(self, value):
        self._action = value

    def setLanguage(self, value):
        self._language = value

    def writeResultAndExit(self, action):
        self.setAction(action)
        with open(RESULT_FILE, 'w+') as resultFile:
            resultFile.write(self._language + '\n' + self._action)
        self.main_window.close()
        self.background_window.closeFromApp()
        sys.exit()


app = FirstBootApp(application_id="com.linuxkamarada.FirstBoot")
app.run(sys.argv)
