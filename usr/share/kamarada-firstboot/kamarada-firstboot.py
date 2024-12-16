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
BACKGROUND_PICTURE = '/usr/share/backgrounds/kamarada/cambirela-light.jpg'
# TODO Get background from GSettings
# Path: org.gnome.desktop.background
# Key: picture-uri
CUSTOM_CSS_STYLESHEET = join(whereAmI, 'kamarada-firstboot.css')
RESULT_FILE = expanduser('~/.config/kamarada-firstboot')


class FirstBootBackgroundWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._can_close = False
        self.connect('close-request', self.on_close_request)

        self.background_picture = Gtk.Picture.new_for_filename(BACKGROUND_PICTURE)
        self.background_picture.set_keep_aspect_ratio(False)
        self.set_child(self.background_picture)

        self.fullscreen()

    def close_from_app(self):
        self._can_close = True
        self.close()

    def on_close_request(self, user_data):
        return ~self._can_close


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
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.imgPortuguese.set_filename(join(whereAmI, 'png/BR.png'))

        self.imgEnglish.set_filename(join(whereAmI, 'png/international-english.png'))

        self.imgTry.set_filename(join(whereAmI, 'png/try.png'))

        self.imgInstall.set_filename(join(whereAmI, 'png/install.png'))

        self.stack.add_named(self.grdLanguage, 'grdLanguage')
        self.stack.add_named(self.grdTryInstall, 'grdTryInstall')

        self.connect('close-request', self.on_close_request)

        self.translate_interface()

    def launch_installer(self):
        subprocess.run([
            'LANG=' + self.firstboot_app.get_language() +
            ' QT_QPA_PLATFORMTHEME="gtk2"' +
            ' kdesu -c /usr/bin/calamares'
        ], shell=True)
        self.show()

    def translate_interface(self):
        # Maybe there is a better way to translate the interface
        # https://stackoverflow.com/q/69791625/1657502
        if (self.firstboot_app.get_language() == 'en_US'):
            self._yes = 'Yes'
            self._no = 'No'
            self._shutdown_dialog_text = 'Your computer is going to shutdown.'
            self._reboot_dialog_text = 'Your computer is going to reboot.'
            self._are_you_sure = 'Are you sure you want to continue?'
            self.btnBack.set_label('Back')
            self.btnShutdown.set_tooltip_text('Shutdown')
            self.btnReboot.set_tooltip_text('Reboot')
            self.lbTryButton.set_label('Try Linux Kamarada')
            self.lbInstallButton.set_label('Install Linux Kamarada')
            self.lbTryInfo.set_label('You can try Linux Kamarada without making any changes to your computer, directly from this live medium.')
            self.lbInstallInfo.set_label('Or, if you\'re ready, you can install Linux Kamarada alongside (or instead of) your current operating system.')
        elif (self.firstboot_app.get_language() == 'pt_BR'):
            self._yes = 'Sim'
            self._no = 'Não'
            self._shutdown_dialog_text = 'Seu computador será desligado.'
            self._reboot_dialog_text = 'Seu computador será reiniciado.'
            self._are_you_sure = 'Tem certeza de que quer continuar?'
            self.btnBack.set_label('Voltar')
            self.btnShutdown.set_tooltip_text('Desligar')
            self.btnReboot.set_tooltip_text('Reiniciar')
            self.lbTryButton.set_label('Experimentar o Linux Kamarada')
            self.lbInstallButton.set_label('Instalar o Linux Kamarada')
            self.lbTryInfo.set_label('Você pode experimentar o Linux Kamarada sem fazer quaisquer alterações no seu computador, diretamente desta mídia live.')
            self.lbInstallInfo.set_label('Ou, se estiver pronto, você poderá instalar o Linux Kamarada juntamente com, ou no lugar do, seu sistema operacional atual.')

    @Gtk.Template.Callback()
    def on_btn_portuguese_clicked(self, button):
        self.firstboot_app.set_language('pt_BR')
        self.translate_interface()
        self.btnBack.show()
        self.title.set_label('Bem-vindo')
        self.subtitle.set_label('')
        self.btnShutdown.show()
        self.btnReboot.show()
        self.stack.set_visible_child(self.grdTryInstall)

    @Gtk.Template.Callback()
    def on_btn_english_clicked(self, button):
        self.firstboot_app.set_language('en_US')
        self.translate_interface()
        self.btnBack.show()
        self.title.set_label('Welcome')
        self.subtitle.set_label('')
        self.btnShutdown.show()
        self.btnReboot.show()
        self.stack.set_visible_child(self.grdTryInstall)

    @Gtk.Template.Callback()
    def on_btn_back_clicked(self, button):
        self.firstboot_app.set_language('en_US')
        self.btnBack.hide()
        self.title.set_label('Bem-vindo')
        self.subtitle.set_label('Welcome')
        self.btnShutdown.hide()
        self.btnReboot.hide()
        self.stack.set_visible_child_full('grdLanguage', Gtk.StackTransitionType.SLIDE_RIGHT)

    @Gtk.Template.Callback()
    def on_btn_shutdown_clicked(self, button):
        dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.QUESTION,
                                   modal=True,
                                   transient_for=self,
                                   text=self._shutdown_dialog_text,
                                   secondary_text=self._are_you_sure)
        dialog.add_buttons(self._yes, Gtk.ResponseType.YES, self._no, Gtk.ResponseType.NO)
        dialog.set_default_response(Gtk.ResponseType.NO)
        dialog.connect('response', self.on_shutdown_dialog_response)
        dialog.present()

    def on_shutdown_dialog_response(self, dialog, response):
        if (response == Gtk.ResponseType.YES):
            self.firstboot_app.write_result_and_exit('Shutdown')
        else:
            dialog.close()

    @Gtk.Template.Callback()
    def on_btn_reboot_clicked(self, button):
        dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.QUESTION,
                                   modal=True,
                                   transient_for=self,
                                   text=self._reboot_dialog_text,
                                   secondary_text=self._are_you_sure)
        dialog.add_buttons(self._yes, Gtk.ResponseType.YES, self._no, Gtk.ResponseType.NO)
        dialog.set_default_response(Gtk.ResponseType.NO)
        dialog.connect('response', self.on_reboot_dialog_response)
        dialog.present()

    def on_reboot_dialog_response(self, dialog, response):
        if (response == Gtk.ResponseType.YES):
            self.firstboot_app.write_result_and_exit('Reboot')
        else:
            dialog.close()

    @Gtk.Template.Callback()
    def on_btn_try_clicked(self, button):
        self.firstboot_app.write_result_and_exit('Try')

    @Gtk.Template.Callback()
    def on_btn_install_clicked(self, button):
        # https://askubuntu.com/a/1486389/560233
        self.hide()
        timer = threading.Timer(1, self.launch_installer)
        timer.start()

    def on_close_request(self, user_data):
        if self.firstboot_app.get_action():
            return False
        dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.QUESTION,
                                   modal=True,
                                   transient_for=self,
                                   text=self._reboot_dialog_text,
                                   secondary_text=self._are_you_sure)
        dialog.add_buttons(self._yes, Gtk.ResponseType.YES, self._no, Gtk.ResponseType.NO)
        dialog.set_default_response(Gtk.ResponseType.NO)
        dialog.connect('response', self.on_reboot_dialog_response)
        dialog.present()
        return True


class FirstBootApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_language('en_US')
        self.set_action('')

        self.connect('activate', self.on_activate)

    def get_action(self):
        return self._action

    def get_language(self):
        return self._language

    def on_activate(self, app):
        self.background_window = FirstBootBackgroundWindow(application=self)
        self.background_window.present()

        self.main_window = FirstBootMainWindow(self, application=self)
        self.main_window.set_transient_for(self.background_window)
        self.main_window.present()

    def set_action(self, value):
        self._action = value

    def set_language(self, value):
        self._language = value

    def write_result_and_exit(self, action):
        self.set_action(action)
        with open(RESULT_FILE, 'w+') as result_file:
            result_file.write(self._language + '\n' + self._action)
        self.main_window.close()
        self.background_window.close_from_app()
        sys.exit()


app = FirstBootApp(application_id="com.linuxkamarada.FirstBoot")
app.run(sys.argv)
