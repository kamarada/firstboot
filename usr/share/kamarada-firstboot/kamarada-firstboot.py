#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from os.path import abspath, dirname, expanduser, join, realpath
#import gettext
#import locale
# Waiting for: https://stackoverflow.com/q/69791625/1657502


#domain = 'kamarada-firstboot'
whereAmI = abspath(dirname(realpath(__file__)))
#localedir = join(whereAmI, '../locale')

#locale.setlocale(locale.LC_ALL, '')
#locale.bindtextdomain(domain, localedir)

#gettext.bindtextdomain(domain, localedir)
#gettext.textdomain(domain)
#_ = gettext.gettext

resultFilePath = '~/.config/kamarada-firstboot'
resultFilePath = expanduser(resultFilePath)

selectedLanguage = 'en_US'
selectedAction = ''


def onBtnPortugueseClicked(button):
    #locale.setlocale(locale.LC_ALL, 'pt_BR.utf8') # Currently, this line does nothing (https://stackoverflow.com/q/69791625/1657502)
    global selectedLanguage
    selectedLanguage = 'pt_BR'
    btnBack.set_label('Voltar')
    btnBack.set_visible(True)
    headerBar.set_title('Bem-vindo')
    headerBar.set_subtitle('')
    headerBar.set_show_close_button(True)
    btnTry.set_label('Experimentar o Linux Kamarada')
    lbTry.set_label('Você pode experimentar o Linux Kamarada sem fazer quaisquer alterações no seu computador, diretamente desta mídia live.')
    btnInstall.set_label('Instalar o Linux Kamarada')
    lbInstall.set_label('Ou, se estiver pronto, você poderá instalar o Linux Kamarada juntamente com, ou no lugar do, seu sistema operacional atual.')
    stack.set_visible_child(grdTryInstall)

def onBtnEnglishClicked(button):
    #locale.setlocale(locale.LC_ALL, 'en_US.utf8') # Currently, this line does nothing (https://stackoverflow.com/q/69791625/1657502)
    global selectedLanguage
    selectedLanguage = 'en_US'
    btnBack.set_label('Back')
    btnBack.set_visible(True)
    headerBar.set_title('Welcome')
    headerBar.set_subtitle('')
    headerBar.set_show_close_button(True)
    btnTry.set_label('Try Linux Kamarada')
    lbTry.set_label('You can try Linux Kamarada without making any changes to your computer, directly from this live medium.')
    btnInstall.set_label('Install Linux Kamarada')
    lbInstall.set_label('Or, if you\'re ready, you can install Linux Kamarada alongside (or instead of) your current operating system.')
    stack.set_visible_child(grdTryInstall)

def onBtnBackClicked(button):
    #locale.setlocale(locale.LC_ALL, 'en_US.utf8') # Currently, this line does nothing (https://stackoverflow.com/q/69791625/1657502)
    global selectedLanguage
    selectedLanguage = 'en_US'
    btnBack.set_visible(False)
    headerBar.set_title('Bem-vindo')
    headerBar.set_subtitle('Welcome')
    headerBar.set_show_close_button(False)
    stack.set_visible_child_full('grdLanguage', Gtk.StackTransitionType.SLIDE_RIGHT)

def onCloseButtonClicked(widget, event):
    global selectedAction
    if selectedAction:
        return False
    dialog = Gtk.MessageDialog(transient_for=mainWindow,
                               modal=True,
                               buttons=Gtk.ButtonsType.OK_CANCEL)
    if (selectedLanguage == 'en_US'):
        dialog.props.text = 'If you quit, your computer is going to be restarted.\n\nAre you sure you want to continue?'
    elif (selectedLanguage == 'pt_BR'):
        dialog.props.text = 'Se você sair, seu computador será reiniciado.\n\nTem certeza de que quer continuar?'
    response = dialog.run()
    dialog.destroy()
    if (response == Gtk.ResponseType.OK):
        selectedAction = 'Reboot'
        writeResult()
        return False
    # Otherwise keep the application open
    return True

def onBtnTryClicked(button):
    global selectedAction
    selectedAction = 'Try'
    writeResult()
    mainWindow.close()

def onBtnInstallClicked(button):
    print('Install')
    # TODO Launch installer

def writeResult():
    resultFile = open(resultFilePath, 'w+')
    resultFile.write(selectedAction + '\n' + selectedLanguage)
    resultFile.close()

builder = Gtk.Builder()
#builder.set_translation_domain(domain)
builder.add_from_file(join(whereAmI, 'kamarada-firstboot.ui'))

headerBar = builder.get_object('headerBar')

grdLanguage = builder.get_object('grdLanguage')

btnPortuguese = builder.get_object('btnPortuguese')
btnPortuguese.connect('clicked', onBtnPortugueseClicked)

btnEnglish = builder.get_object('btnEnglish')
btnEnglish.connect('clicked', onBtnEnglishClicked)

grdTryInstall = builder.get_object('grdTryInstall')

btnBack = builder.get_object('btnBack')
btnBack.connect('clicked', onBtnBackClicked)

lbTry = builder.get_object('lbTry')

btnTry = builder.get_object('btnTry')
btnTry.connect('clicked', onBtnTryClicked)

lbInstall = builder.get_object('lbInstall')

btnInstall = builder.get_object('btnInstall')
btnInstall.connect('clicked', onBtnInstallClicked)

stack = builder.get_object('stack')
stack.add_named(grdLanguage, 'grdLanguage')
stack.add_named(grdTryInstall, 'grdTryInstall')

mainWindow = builder.get_object('mainWindow')
mainWindow.connect('delete-event', onCloseButtonClicked)
mainWindow.connect('destroy', Gtk.main_quit)
mainWindow.show()

Gtk.main()
