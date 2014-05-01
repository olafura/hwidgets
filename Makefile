.PHONY: init
all :
	echo "prufa"

#MONO = $(shell sudo apt-get install ubuntu-mono)
SHELL = /bin/bash

copy :
	@echo "Copying icons from the ubuntu-mono theme"
	@cp /usr/share/icons/ubuntu-mono-dark/status/24/nm-* web/assets
	@cp /usr/share/icons/ubuntu-mono-dark/status/24/gpm-* web/assets

mono :
	@echo "Checking if ubuntu-mono theme is installed"
	@if [ "$(shell dpkg -l | grep -c 'ubuntu-mono ')" == "0" ];\
	then\
		sudo apt-get install ubuntu-mono;\
	fi


pcouchdb :
	@echo "Checking if python-couchdb is installed"
	@if [ "$(shell dpkg -l | grep -c 'python-couchdb ')" == "0" ];\
	then\
		sudo apt-get install python-couchdb;\
	fi

couchdb :
	@echo "Checking if couchdb is installed"
	@if [ "$(shell dpkg -l | grep -c 'couchdb ')" == "0" ];\
	then\
		sudo apt-get install couchdb;\
	fi

dbus :
	@echo "Checking if dbus-python is installed"
	@if [ "$(shell dpkg -l | grep -c 'python-dbus ')" == "0" ];\
	then\
		sudo apt-get install python-dbus;\
	fi

upower :
	@echo "Checking if upower is installed"
	@if [ "$(shell dpkg -l | grep -c 'upower ')" == "0" ];\
	then\
		sudo apt-get install upower;\
	fi

gobject :
	@echo "Checking if python-gobject is installed"
	@if [ "$(shell dpkg -l | grep -c 'python-gobject ')" == "0" ];\
	then\
		sudo apt-get install python-gobject;\
	fi

network :
	@echo "Checking if python-networkmanager is installed"
	@if [ "$(shell dpkg -l | grep -c 'python-networkmanager ')" == "0" ];\
	then\
		sudo apt-get install python-networkmanager;\
	fi

pinit :
	@echo "Initialize CouchDB"
	@python initialize.py

gitinit :
	@echo "Get all the submodules for git"
	@git submodule init
	@git submodule update

init : mono copy dbus upower network couchdb pcouchdb gitinit pinit
