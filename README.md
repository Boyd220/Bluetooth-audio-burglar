# Information Security - [Bluetooth audio burglar]

###Installatie handleiding
Python2 en Python3 worden ondersteund, de libraries voor Python2 en Python3 zijn anders. Deze handleiding gaat uit van Python3 en een Arch Linux installatie, alhoewel deze libraries ook op een Raspbian installatie binnen te halen zijn via pip.
####Benodigde Python libraries
gobject,dbus,glib,optparse zijn de libraries die nodig zijn voor de correcte werking. Deze zijn op Arch te installeren via pacman: pacman -S python python-gobject python-dbus python-optparse dbus-glib
####Extra Tools
Bluetoothctl is nodig voor het scannen naar apparaten hier voor voldoen de standaard Arch bluetooth tools deze zijn te installeren via pacman: pacman -S bluez
###Gebruikers handleiding
Start bluetoothctl en voer hierin: "power on" en dan "scan on" de bluetooth deamon zal naar apparaten gaan scannen. Start nu het Python script "https://github.com/AP-Elektronica-ICT/infsec-1617-anonymous/blob/master/src/pyCon.py", voor meer informatie is er de -h optie deze geeft de mogelijke opties weer. Standaard zal het python script met alle bluetooth apparaten verbinden, dit zal een hoop mensen in de buurt irriteren met verbindingverzoeken hierdoor raden wij de -a optie aan zodat er alleen met audio apparaten wordt verbonden.

## Beschrijving Project

####De aanloop
Dit project begon als de "Raspberry pi bluetooth alerter". Het idee was om te visualiseren wanneer er een bepaald bluetoothprotocol werd gevonden met daarnaast een bestand dat wordt gemaakt met alle gedetecteerde bluetoothprotocollen, vervolgens zou dit bestand gemaild worden naar de gebruiker. Dit idee is echter na een tijdje de prullenbak in verdwenen. Samen met een ander groepje (Kenny en Gillian) kwamen we erachter dat je een speciale dongle nodig had voor de pi om bluetoothprotocollen te herkennen. Deze was niet beschikbaar op school en is vrij prijzig om zelf aan te schaffen. Uiteindelijk hebben we met ons eindproduct wel een klein beetje van de oorspronkelijk opdracht waargemaakt omdat we kunnen herkennen of het apparaat een audio sink is.

####Het nieuwe idee
Hierna kwamen we op het idee om geluid af te spelen via bluetooth en een verbinding te forceren tussen iedere bluetooth audio device dat wordt gedetecteerd. Dus het idee van ‘Bluetooth audio burglar’ was geboren. Het idee is simpel, er wordt een script gerunt die bekijkt welke bluetoothverbindingen er beschikbaar zijn. Hij kijkt hierin specifiek of het bluetooth apparaat audio kan afspelen. Vervolgens, als hij een audioapparaat ziet, probeert hij te pairen en connecteren en pushed daarna gelijk een mp3 file om af te spelen. Daarnaast kunnen we met meerdere speakers verbinden en daarop een geluidsbestand afspelen. Het nut hiervan? Niet veel buiten dat er te zien is hoe slecht sommige bluetooth devices beveiligd zijn.

####De uitwerking
#####Stap 1
Nadat de pi correct geinstalleerd was en de updates waren uitgevoerd konen we beginnen met eerst überhaupt een bluetoothverbinding op te zetten tussen apparaten. Dit bleek nog lastiger te zijn dan verwacht. We konden in het begin vaak wel naar apparaten zoeken, pairen lukte ook nog maar bij connecteren ging het mis. Na lang doorzoeken kwamen we erachter dat de ‘pulseaudio’ van de pi dwarszat. Deze moest gerund worden in sudo om het bluetoothprogramma en pulseaudio te laten samenwerken. Uiteindelijk konden we dus na dit ook connecteren met een bluetoothapparaat. Daarna een mp3 file afspelen was niet echt een probleem. Voor het afspelen van de mp3 file gebruikten we mplayer. Nu moesten we al deze manuele handelingen nog zien te automatiseren.

#####Stap 2
Nu we het principe doorhadden, moesten we er een script voor gaan schrijven om het te laten automatiseren. De keuze stond voor python of bash. Uiteindelijk hebben we het beide in bash en python geprobeerd. De uiteindelijke oplossing is in python geschreven. Boyd probeerde bash te schrijven en Jeroen waagde zich aan python. Bij bash konden we het hele verbindingsproces automatiseren, echter moesten we dan wel hardcoded het macadres van het bluetoothapparaat ingeven. Dit was natuurlijk niet de bedoeling, dus pasten we het aan dat hij alle apparaten hun macadres in een bestand schreef. Uiteindelijk zijn we met bash hier vastgelopen, om dit bestand vervolgens uit te lezen, te pairen en connecteren met dat apparaat en een mp3 file te pushen lukte niet.

Jeroen is er echter wel in geslaagd om een python script te schrijven die scant naar bluetoothsignalen, bepaald welke van deze signalen een audio output heeft, probeert te pairen en connecteren en vervolgens een mp3 file afspeelt.

#### Waarom python over bash?
We gebruiken python omdat we in tegenstelling tot bash direct via dbus kunnen communiceren met de bluetooth deamon. Bij bash moet je via het bluetoothprogramma communiceren naar de d-bus. Dit zorgt voor een directere communicatie tussen ons python script en de hardware. Daarnaast heeft Jeroen ook een persoonlijke voorkeur voor python omdat hij hier redelijk wat ervaring mee heeft. Dit haalde de hoge leercurve weg moesten we iets gebruiken wat we nog niet zo goed kenden. We probeerden echter het ook werkend te krijgen met bash maar nadien opgegeven en volledig voor python gegaan                       

##Code en toelichting op de code
####Variabelen
Hier worden de variabelen gedeclareerd alsook de libraries waar ons script van afhankelijk is.

![alt tag](https://github.com/AP-Elektronica-ICT/infsec-1617-anonymous/blob/master/doc/img/1.png)

####Scan opzetten
Hier worden de settings bepaald en ‘getrust’, vervolgens wordt de pi klaargemaakt om te scannen naar bluetooth apparaten en meer specifiek, naar degene die een audio output hebben, vervolgens wordt dit kenbaar gemaakt aan de gebruiker. 

![alt tag](https://github.com/AP-Elektronica-ICT/infsec-1617-anonymous/blob/master/doc/img/2.png)
####Pair met alles dat je ziet
De scan gaat vervolgens proberen te pairen met onze hardcoded pincode 0000, hij stuurt dit via dbus naar het apparaat waarmee hij probeert te connecteren. Het apparaat reageert hierop en daarna zijn ze verbonden waarna er een geluidsbestand kan worden afgespeeld. Indien hij niet reageert of het afwijst dan gebeurt er niks en gaat de code verder met het zoeken naar andere apparaten. We hebben het zo gemaakt dat de speaker zegt: “Ready to pair”, vervolgens gaat zoeken en als de pairing succesvol is zegt hij “Pairing succesfull”.

![alt tag](https://github.com/AP-Elektronica-ICT/infsec-1617-anonymous/blob/master/doc/img/3.png)

####Errors opvangen en voer de code uit
Hier wordt opgevangen of het device paired is, alsook wordt er een manager voorgeschreven aan het geconnecteerde apparaat. Daarna word de code ook in een loop gezet zodat hij blijft scannen en proberen connecteren tot hij eindelijk succes heeft.

![alt tag](https://github.com/AP-Elektronica-ICT/infsec-1617-anonymous/blob/master/doc/img/4.png)

##Diagram over ons project

![alt tag](https://github.com/AP-Elektronica-ICT/infsec-1617-anonymous/blob/master/doc/img/diagramma.png)

Hierboven zie je grofweg hoe ons project werkt. In dit plaatje zijn bluetooth, pulseaudio en ons zelfgeschreven script een proces. Deze communiceren dus allemaal via d-bus met elkaar. D-bus vervoerd dus bij wijs van spreken de logica van het python script via de bus naar onze bluetooth dongle, de dongle doet hier iets mee en stuurt vervolgens als hij geconnecteerd is met een apparaat naar pulseaudio het resultaat. Daarna vervoerd pulseaudio een audiofile naar dat geconnecteerde apparaat en speelt het af. 

## Belangrijkste problemen en oplossingen
###Probleem
#### Probleem protocollen detecteren
Zoals aangekaart in de aanloop begon dit project als detecteren welke protocollen er worden gebruikt en dit te visualiseren en loggen. Na wat onderzoek te doen kwamen we erachter dat dit wel mogelijk is, maar dat dit een dure aangelegenheid zal zijn. 
#### Probleem pulseaudio
Voordat we een automatisch script gingen schrijven wilden we eerst manueel een verbinding aanleggen en manueel een mp3 file laten afspelen op het apparaat. Dit leek simpel volgens de documentatie, echter kwam er elke keer een dikke error op het scherm. Het bleek uiteindelijk pulseaudio te zijn die niet met genoeg rechten gestart probeerde te worden. 
#### Handmatig macadres invoeren bij bashscript
Ons geautomatiseerde verbindingsproces lukte allemaal mooi. Echter is het veel mooier en gebruiksvriendelijker als het macadres van het apparaat gedetecteerd word en automatisch word gezet waar hij thuishoort en verbinding probeert te maken.
####Probleem bash of python
We wilden eerst ambitieus beide talen gebruiken om het project te maken, echter zijn we daarvan afgestapt en hebben de focus gelegd op python.
###Oplossing
####Oplossing protocollen detecteren
Omdat het dus duur werd om protocollen te detecteren moesten we een ander idee bedenken. Dit idee is dat we een script gaan schrijven die via bluetooth detecteert of het apparaat muziek kan afspelen, indien dit het geval hiermee te connecteren en vervolgens muziek probeert af te spelen op dit audioapparaat.
#### Oplossing pulseaudio
De oplossing was niet gemakkelijk te vinden, maar was even briljant als simpel. Je killde het huidige pulseaudio proces en deed hem opnieuw opstarten met sudo rechten, na deze handeling wilden bluetooth en pulseaudio wel ineens samenwerken.

####Oplossing handmatig macadres invoeren bij bashscript
Uiteindelijk hebben we het niet opgelost gekregen. We konden de gedetecteerde macadressen wegschrijven in een bestandje, echter specifiek die karakters van het macadres eruit halen die je nodig hebt, was veel moeilijker dan geanticipeerd. Nog een reden waarom we voor python gekozen hebben.
####Oplossing bash of python
Omdat Jeroen meer ervaring heeft met Python en omdat het ons beter leek om het project eerst met überhaupt een taal te laten werken, zijn we uiteindelijk voor python gegaan als taal.

## Gebruikte voorwerpen
Voor dit project hebben we een aantal voorwerpen gebruikt. Hieronder worden deze opgesomd. 
#### Raspberry pi 2
Boyd had al een raspberry pi 2 thuis liggen dus hebben we deze gebruikt voor het project. Hier draait ons pi arch systeem op.
#### Bluetooth dongle
Via aliexpress hebben we een goedkope bluetooth dongle op de kop getikt. Via deze dongle word er gezocht naar beschikbare bluetooth apparaten en word er getracht een verbindging op te zetten.
#### Ethernet kabel
Een ethernet kabel om gemakkelijk een SSH verbinding tussen de laptop en pi te werk te stellen.
#### Mini usb oplader
Om 5v aan de pi te geven zodat hij aan staat.
#### Bluetoothspeaker en bluetoothheadset
Om te testen en verbinding te maken een bluetooth apparaat. Om te beginnen probeerden we met een van deze apparaten te verbinden, later met meerdere.
####SD kaart
Om de pi distributie op te slaan gebruiken we een SD kaartje natuurlijk.

##Gebruikte technologie

####Arch Linux voor de pi
Aangezien Jeroen fan is van Arch zijn we daarom ook gegaan voor de pi distributie van Arch. We vonden het een leuke en alternatieve manier van het project benaderen tegenover onze klasgenoten die bijna allemaal NOOBS gebruiken voor de raspberry pi.

####Bluetooth
We maken gebruik van bluetooth om te connecteren met apparaten. Bluetooth is een gemakkelijk te gebruiken protocol die veel mogelijkheden bied mits er creatief genoeg mee word om gegaan.

####SSH
Om verbinding te leggen met de pi zonder een tv of monitor daarvoor te gebruiken.

####Python
Ons uiteindelijke script is geschreven in python.	

####Bash
We hebben geprobeerd om het script ook te schrijven in bash.

####WinSCP
Om gemakkelijk files over te zetten van onze computer naar de pi gebruiken we het programma WinSCP. Deze zet files gemakkelijk over via ssh naar de pi.

## Documentatie
Onderstaande zijn de meest gebruikte bronnen voor onze informatie.

#### https://en.wikipedia.org/wiki/D-Bus
We zijn in dit project voornamelijk afhankelijk van D-Bus procedure. D-bus zorgt ervoor dat een proces met verschillende sessies en gebruikers met elkaar kunnen communiceren. D-bus versimpelt alle binnenkomende signalen zodat er geen conflicten ontstaan tussen de verschillende sessies, gebruikers en processen. D-bus interpreteert vervolgens het inkomende signaal en heeft het vermogen om dat vervolgens op het aangewezen medium af te spelen. Het is dus wel in te beelden waarom deze procedure van levensbelang is voor ons project goed te laten verlopen

#### GitHub
Via GitHub hebben we een aantal libraries gevonden die we gebruiken om onze pi en het script goed te laten lopen.

#### https://wiki.archlinux.org/index.php/Raspberry_Pi
Met dit hebben we de initiële configuratie uitgevoerd om onze pi in te stellen en users toe te bedelen. We zagen het niet zitten om alles via root user te doen omdat dat best wel een ‘bad habit’ is als je met Linux systemen werkt nu en in de toekomst.

####https://wiki.archlinux.org/index.php/bluetooth 
We gebruiken om de bluetoothdongle aan te sturen bluetoothctl van Linux. Dit programma zetten we aan via het python script en die zegt tegen bluetoothctl dat hij moet gaan scannen en pairen. Zonder bluetoothctl had dit project niet gewerkt, aangezien de geïntegreerde omgeving van Linux voor randapparaten vreselijk in omgang is.

#### https://wiki.archlinux.org/index.php/PulseAudio 
We hebben pulseaudio gebruikt om via een virtuele geluidsinterface op meerdere speakers tegelijk muziek af te spelen. Pulseaudio werkt samen met bluetoothctl om voornamelijk geluidsbestanden via bluetooth correct en op het juiste apparaat af te spelen.

#### https://wiki.archlinux.org/index.php/MPlayer 
Om geluiden af te spelen via de pi gebruikten we mplayer. Mplayer is te vergelijken met vlc voor windows. Het is makkelijk te installeren en te gebruiken. Wij gebruikten het om onze audio files af te spelen via de pi.

#### https://wiki.archlinux.org/index.php/Bluetooth_headset
Met deze informatie hebben we de initiële bluetooth verbinding gelegd tussen een apparaat en de pi. Hier stond in welke librarys je nodig hebt en welke commando’s je moet invoeren om het tot een goed einde te brengen, er stond echter niks in over onze error met pulse-audio.
#### Reddit
Ik weet niet exact meer welke pagina het was, maar zonder deze anonieme held op reddit had de zoektocht naar dat pulse-audio bluetoothctl in de weg zat nog langer geduurd.
#### https://www.kernel.org/doc/ols/2006/ols2006v1-pages-421-426.pdf
#### https://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html
Met deze twee bovenstaande documentaties hebben we de ‘Bluez’ library via een python script samen laten werken met d-bus.

## Groepsleden
#### Boyd Franken
#### Jeroen Rietveld
