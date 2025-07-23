import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
nom = '+94710649265'
number = phonenumbers.parse(nom, 'CH')
number2 = phonenumbers.parse(nom, 'RO')
print(geocoder.description_for_number(number, 'en'))
print(carrier.name_for_number(number2,'en'))
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + IPAddr)