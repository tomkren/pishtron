# pishtron

Tohle je můj soubor s vtipy-tipy-tricky, kamaráde!



## Hodí se vědět


### Vlastní příkaz

sudo nano .bash_aliases
a tam dát např:
alias temp='/opt/vc/bin/vcgencmd measure_temp'

### On startup script do crontabu

Pro editaci crontabu v nanu dáme (bez sudo, chcem pro uživatele pi, ne root):
crontab -e
A pak na konec souboru přidáme řádek (např):
@reboot cd /home/pi/; ./scripts/on_startup.sh


## Sprovoznovani TFGP

### Java 8
V pohodě, na pi je defaultně, a je tam právě jedna alternativa pro javu, tzn v poho.
Kdyby nebyla tak se dá vybrat, asi dobrý před installem mavenu dat správnou: 
sudo update-alternatives --config java

### maven
Citlivky to můžou dělat nějak manuálně 
(spousta tuorialů de vygooglit, asi kvůli velikosti jsem pochopil), 
mě fungovalo ok klasický:
sudo apt-get install maven

## testovačka
cd TFGP
mvn clean verify


## Co jsem tu zatim nastavoval atd

 - Aby ty okraje zmizely v: sudo nano /boot/config.txt 
   (jde ekvivalentně v configu disable overlay myslim)
 - Aby se forcenul jack na output v: sudo raspi-config
 - Aby bylo SSH 
 - .. a heslo na pi ucet jiny nez default (t..)
 - crontab @reboot ...
 - 




## Co chci udelat

 - Rozchodit lego robota krz python jako na zero
 - Udělat temp_logger cytřejc, aby "komprimoval" (tzn nevypisoval) po sobě jdoucí stejný teploty
