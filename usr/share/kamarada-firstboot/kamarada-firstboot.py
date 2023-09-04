#!/usr/bin/python3

import gi
import sys
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk
from os.path import abspath, dirname, exists, expanduser, join, realpath


whereAmI = abspath(dirname(realpath(__file__)))


APPLICATION_WINDOW = join(whereAmI, 'kamarada-firstboot.ui')
CUSTOM_CSS_STYLESHEET = join(whereAmI, 'kamarada-firstboot.css')


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

    resultFilePath = expanduser('~/.config/kamarada-firstboot')
    selectedLanguage = 'en_US'
    selectedAction = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

        # Check if returning from the installer
        if (exists(self.resultFilePath)):
            with open(self.resultFilePath, 'r') as resultFile:
                firstLine = resultFile.readline()
                secondLine = resultFile.readline()
                if (secondLine == 'Install'):
                    # Returning from the installer (maybe it failed)
                    # Presents the previously selected language
                    if (firstLine == 'pt_BR\n'):
                        self.onBtnPortugueseClicked(self.btnPortuguese)
                    elif (firstLine == 'en_US\n'):
                        self.onBtnEnglishClicked(self.btnEnglish)

    def getStrYes(self):
        return 'Yes' if (self.selectedLanguage == 'en_US') else 'Sim'

    def getStrNo(self):
        return 'No' if (self.selectedLanguage == 'en_US') else 'Não'
    
    def writeResultAndClose(self, action):
        self.selectedAction = action
        with open(self.resultFilePath, 'w+') as resultFile:
            resultFile.write(self.selectedLanguage + '\n' + self.selectedAction)
        self.close()

    @Gtk.Template.Callback()
    def onBtnPortugueseClicked(self, button):
        # Maybe there is a better way to translate the interface
        # https://stackoverflow.com/q/69791625/1657502
        self.selectedLanguage = 'pt_BR'
        self.btnBack.set_label('Voltar')
        self.btnBack.show()
        self.title.set_label('Bem-vindo')
        self.subtitle.set_label('')
        self.btnShutdown.set_tooltip_text('Desligar')
        self.btnShutdown.show()
        self.btnReboot.set_tooltip_text('Reiniciar')
        self.btnReboot.show()
        self.lbTryButton.set_label('Experimentar o Linux Kamarada')
        self.lbInstallButton.set_label('Instalar o Linux Kamarada')
        self.lbTryInfo.set_label('Você pode experimentar o Linux Kamarada sem fazer quaisquer alterações no seu computador, diretamente desta mídia live.')
        self.lbInstallInfo.set_label('Ou, se estiver pronto, você poderá instalar o Linux Kamarada juntamente com, ou no lugar do, seu sistema operacional atual.')
        self.stack.set_visible_child(self.grdTryInstall)

    @Gtk.Template.Callback()
    def onBtnEnglishClicked(self, button):
        self.selectedLanguage = 'en_US'
        self.btnBack.set_label('Back')
        self.btnBack.show()
        self.title.set_label('Welcome')
        self.subtitle.set_label('')
        self.btnShutdown.set_tooltip_text('Shutdown')
        self.btnShutdown.show()
        self.btnReboot.set_tooltip_text('Reboot')
        self.btnReboot.show()
        self.lbTryButton.set_label('Try Linux Kamarada')
        self.lbInstallButton.set_label('Install Linux Kamarada')
        self.lbTryInfo.set_label('You can try Linux Kamarada without making any changes to your computer, directly from this live medium.')
        self.lbInstallInfo.set_label('Or, if you\'re ready, you can install Linux Kamarada alongside (or instead of) your current operating system.')
        self.stack.set_visible_child(self.grdTryInstall)

    @Gtk.Template.Callback()
    def onBtnBackClicked(self, button):
        selectedLanguage = 'en_US'
        self.btnBack.hide()
        self.title.set_label('Bem-vindo')
        self.subtitle.set_label('Welcome')
        self.btnShutdown.hide()
        self.btnReboot.hide()
        self.stack.set_visible_child_full('grdLanguage', Gtk.StackTransitionType.SLIDE_RIGHT)

    @Gtk.Template.Callback()
    def onBtnShutdownClicked(self, button):
        dialog = Gtk.MessageDialog(transient_for=self,
                                   modal=True,
                                   message_type=Gtk.MessageType.QUESTION)
        if (self.selectedLanguage == 'en_US'):
            dialog.props.text = 'Your computer is going to shutdown.'
            dialog.props.secondary_text = 'Are you sure you want to continue?'
        elif (self.selectedLanguage == 'pt_BR'):
            dialog.props.text = 'Seu computador será desligado.'
            dialog.props.secondary_text = 'Tem certeza de que quer continuar?'
        dialog.add_buttons(self.getStrYes(), Gtk.ResponseType.YES, self.getStrNo(), Gtk.ResponseType.NO)
        dialog.set_default_response(Gtk.ResponseType.NO)
        dialog.connect('response', self.onShutdownDialogResponse)
        dialog.present()

    def onShutdownDialogResponse(self, dialog, response):
        if (response == Gtk.ResponseType.YES):
            self.writeResultAndClose('Shutdown')
        else:
            dialog.close()

    @Gtk.Template.Callback()
    def onBtnRebootClicked(self, button):
        dialog = Gtk.MessageDialog(transient_for=self,
                                   modal=True,
                                   message_type=Gtk.MessageType.QUESTION)
        if (self.selectedLanguage == 'en_US'):
            dialog.props.text = 'Your computer is going to reboot.'
            dialog.props.secondary_text = 'Are you sure you want to continue?'
        elif (self.selectedLanguage == 'pt_BR'):
            dialog.props.text = 'Seu computador será reiniciado.'
            dialog.props.secondary_text = 'Tem certeza de que quer continuar?'
        dialog.add_buttons(self.getStrYes(), Gtk.ResponseType.YES, self.getStrNo(), Gtk.ResponseType.NO)
        dialog.set_default_response(Gtk.ResponseType.NO)
        dialog.connect('response', self.onRebootDialogResponse)
        dialog.present()

    def onRebootDialogResponse(self, dialog, response):
        if (response == Gtk.ResponseType.YES):
            self.writeResultAndClose('Reboot')
        else:
            dialog.close()

    @Gtk.Template.Callback()
    def onBtnTryClicked(self, button):
        self.writeResultAndClose('Try')

    @Gtk.Template.Callback()
    def onBtnInstallClicked(self, button):
        self.writeResultAndClose('Install')

    def onCloseRequest(self, user_data):
        if self.selectedAction:
            return False
        dialog = Gtk.MessageDialog(transient_for=self,
                                   modal=True,
                                   message_type=Gtk.MessageType.QUESTION)
        if (self.selectedLanguage == 'en_US'):
            dialog.props.text = 'If you quit, your computer is going to reboot.'
            dialog.props.secondary_text = 'Are you sure you want to continue?'
        elif (self.selectedLanguage == 'pt_BR'):
            dialog.props.text = 'Se você sair, seu computador será reiniciado.'
            dialog.props.secondary_text = 'Tem certeza de que quer continuar?'
        dialog.add_buttons(self.getStrYes(), Gtk.ResponseType.YES, self.getStrNo(), Gtk.ResponseType.NO)
        dialog.set_default_response(Gtk.ResponseType.NO)
        dialog.connect('response', self.onRebootDialogResponse)
        dialog.present()
        return True


class FirstBootApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def do_activate(self):
        self.win = FirstBootMainWindow(application=self)
        self.win.present()


app = FirstBootApp(application_id="com.linuxkamarada.FirstBoot")
app.run(sys.argv)
