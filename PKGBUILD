# Maintainer: Antonio Medeiros <linuxkamarada@gmail.com>

pkgname=(kamarada-firstboot)
pkgbase=firstboot
pkgver=20250907
pkgrel=1
pkgdesc='Kamarada Firstboot'
arch=(any)
url='https://github.com/kamarada/firstboot'
license=('GPL-3.0')
depends=(
    'calamares'
    'gnome-shell'
    'kdesu'
    'python'
    'python-gobject'
    'sed'
    'sudo'
    'systemd'
)
makedepends=('git')
source=('git+https://github.com/kamarada/firstboot.git#branch=testing')
sha256sums=('SKIP')

package() {
    cd "${pkgbase}"

    mkdir -p "$pkgdir/usr/bin"
    install -m0755 usr/bin/kamarada-firstboot "$pkgdir/usr/bin/"

    mkdir -p "$pkgdir/usr/lib/systemd/system"
    install -m0755 usr/lib/systemd/system/kamarada-firstboot.service "$pkgdir/usr/lib/systemd/system/"

    mkdir -p "$pkgdir/usr/sbin"
    install -m0755 usr/sbin/kamarada-setup "$pkgdir/usr/sbin/"

    mkdir -p "$pkgdir/usr/share/kamarada-firstboot/png"
    install -m0644 usr/share/kamarada-firstboot/kamarada-firstboot.{css,py,ui} "$pkgdir/usr/share/kamarada-firstboot/"
    install -m0644 usr/share/kamarada-firstboot/png/* "$pkgdir/usr/share/kamarada-firstboot/png/"
}
