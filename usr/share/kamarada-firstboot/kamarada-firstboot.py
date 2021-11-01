#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from os.path import abspath, dirname, join, realpath
import gettext
import locale


domain = 'kamarada-firstboot'
whereAmI = abspath(dirname(realpath(__file__)))
localedir = join(whereAmI, '../locale')

locale.setlocale(locale.LC_ALL, '')
locale.bindtextdomain(domain, localedir)

gettext.bindtextdomain(domain, localedir)
gettext.textdomain(domain)
_ = gettext.gettext


def onBtnPortugueseClicked(button):
    locale.setlocale(locale.LC_ALL, 'pt_BR.utf8') # Currently, this line does nothing (https://stackoverflow.com/q/69791625/1657502)
    headerBar.set_title('Bem-vindo')
    headerBar.set_subtitle('')
    stack.set_visible_child(grdTryInstall)
    headerBar.set_show_close_button(True)
    btnBack.set_visible(True)

def onBtnEnglishClicked(button):
    locale.setlocale(locale.LC_ALL, 'en_US.utf8') # Currently, this line does nothing (https://stackoverflow.com/q/69791625/1657502)
    headerBar.set_title('Welcome')
    headerBar.set_subtitle('')
    stack.set_visible_child(grdTryInstall)
    headerBar.set_show_close_button(True)
    btnBack.set_visible(True)

def onBtnBackClicked(button):
    locale.setlocale(locale.LC_ALL, 'en_US.utf8') # Currently, this line does nothing (https://stackoverflow.com/q/69791625/1657502)
    headerBar.set_title('Bem-vindo')
    headerBar.set_subtitle('Welcome')
    stack.set_visible_child_full('grdLanguage', Gtk.StackTransitionType.SLIDE_RIGHT)
    headerBar.set_show_close_button(False)
    btnBack.set_visible(False)


builder = Gtk.Builder()
builder.set_translation_domain(domain)
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

stack = builder.get_object('stack')
stack.add_named(grdLanguage, 'grdLanguage')
stack.add_named(grdTryInstall, 'grdTryInstall')

mainWindow = builder.get_object('mainWindow')
mainWindow.connect('destroy', Gtk.main_quit)
mainWindow.show()

Gtk.main()
