#!/bin/bash

test -e /etc/debian_version && DIST="Debian"
grep Ubuntu /etc/lsb-release &> /dev/null && DIST="Ubuntu"

if [[ $DIST == Ubuntu || $DIST == Debian ]]; then
    update='sudo DEBIAN_FRONTEND=noninteractive apt-get update'
    install='sudo DEBIAN_FRONTEND=noninteractive apt-get -y install'
    remove='sudo DEBIAN_FRONTEND=noninteractive apt-get -y remove'
    pkginst='sudo dpkg -i'
    # Prereqs for this script
    if ! which lsb_release &> /dev/null; then
        $install lsb-release
    fi
fi

function amc {
    if [[ updated != true ]]; then
        $update
        updated="true"
    fi
    
    $install auto-multiple-choice
    echo 'Installed AMC'
}

function amc_code {
    if [[ updated != true ]]; then
        $update
        updated="true"
    fi

    #dependências AMC
    $install debhelper gettext libnetpbm10-dev libxml-libxml-perl dblatex xsltproc docbook-xml docbook-xsl librsvg2-bin netpbm texlive-pictures pkg-config libopencv-dev libpoppler-glib-dev libcairo2-dev libpango1.0-dev texlive-latex-recommended texlive-xetex lmodern texlive-lang-french texlive-lang-japanese texlive-lang-chinese libxml-writer-perl libxml-perl
    $install liblocale-gettext-perl libxml-simple-perl libxml-writer-perl libgtk3-perl libio-compress-perl libcompress-zlib-perl libgraphics-magick-perl libdbd-sqlite3-perl libdbi-perl libfile-mimeinfo-perl libtext-csv-perl texlive-latex-base texlive-latex-recommended texlive-plain-generic texlive-latex-extra texlive-fonts-extra imagemagick netpbm ghostscript poppler-utils libarchive-zip-perl librsvg2-common unzip libglib-object-introspection-perl libclone-perl liblocale-codes-perl

    #Argparse perl
    $install libgetopt-argparse-perl
    
    #clone AMC
    cd ..
    git clone https://gitlab.com/jojo_boulix/auto-multiple-choice.git
    cd auto-multiple-choice


    #compile AMC
    make version_files
    make

    echo 'Installed AMC source code'
}

function dependencies {
    if [[ updated != true ]]; then
        $update
        updated="true"
    fi

    $install git
    $install php
    $install evince

    #Install Browser
    $install firefox
    echo 'Installed Firefox'

    # Install Additional Software
    $install graphviz aspell ghostscript clamav php7.4-pspell php7.4-curl php7.4-gd php7.4-intl php7.4-mysql php7.4-xml php7.4-xmlrpc php7.4-ldap php7.4-zip php7.4-soap php7.4-mbstring
}

function moodle {

    if [[ updated != true ]]; then
        $update
        updated="true"
    fi

    #Install Apache
    $install apache2
    sudo service apache2 restart

    #Download Moodle
    cd /opt 
    sudo git clone git://git.moodle.org/moodle.git
    cd moodle
    sudo git branch --track MOODLE_310_STABLE origin/MOODLE_310_STABLE
    sudo git checkout MOODLE_310_STABLE

    #Copy local reposioty to /var/www/html/
    sudo cp -R /opt/moodle /var/www/html/
    sudo mkdir /var/moodledata
    sudo chown -R www-data /var/moodledata
    sudo chmod -R 777 /var/moodledata
    sudo chmod -R 0755 /var/www/html/moodle

    echo 'Installed Moodle'

    #Copy config file
    sudo cp -R /home/vagrant/amc-testbed/config.php /var/www/html/moodle

    echo 'Configured Moodle'
}

function mysql {

    if [[ updated != true ]]; then
        $update
        updated="true"
    fi

    #Install MySQL
    $install mysql-client 
    $install mysql-server
    sudo service mysql restart

    echo 'Installed MySQL'

    #Script SQL 
    sudo mysql -u root < /home/vagrant/amc-testbed/db.sql    

    echo 'Created database'
}

function usage {
    printf '\nUsage: %s [-a]\n\n' $(basename $0) >&2

    printf 'options:\n' >&2
    printf -- ' -a: install AMC\n' >&2
    printf -- ' -c: install AMC source code\n' >&2
    printf -- ' -d: install dependencies\n' >&2
    printf -- ' -m: install Moodle\n' >&2
    printf -- ' -s: install mySQL\n' >&2
    
    exit 2
}

if [[ $# -eq 0 ]]; then
    usage
else
    while getopts 'acdms' OPTION
    do
        case $OPTION in
        a)    amc;;
        c)    amc_code;;
        d)    dependencies;;
        m)    moodle;;
        s)    mysql;;
        ?)    usage;;
        esac
    done
    shift $(($OPTIND - 1))
fi
