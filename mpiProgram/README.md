mpirun -H master,uslave1,uslave2 python CSP.py 4

###install these:
sudo apt-get install python-xlsxwriter
sudo apt-get install python-xlrd
sudo apt-get install python-openpyxl
sudo apt-get install python-matplotlib

###VM set with local master
File->Host Network Manager-> Create -> Manually (192.168.33.1, 255.255.255.0)

Adapter 1: NAT
Adapter 2: Host-only (wybieramy to co stworzylismy wyzej), promiscuous mode: allow all
Taki sam Mac Address na obu adapterach
Na OBU adapterach zaznaczony Cable Connected (Ważne!)

konfiguracja interfejsow sieciowych odbywa sie w innej lokalizacji niz dotychczas na linuxie:
/etc/netplan/50-cloud-init.yaml (bezpiecznie zrobic backup)

np:

networks:
   ethernets:
        enp0s3:
            dhcp4: true
        enp0s8:
	    addresses: [192.16833.100/24]
	    optional: true
	    dhcp4: no
	    dhcp6: no
	    nameservers:
                addresses: [8.8.8.8,8.8.4.4]
   version 2
   renderer: networkd

->analogicznie w drugim nodzie

