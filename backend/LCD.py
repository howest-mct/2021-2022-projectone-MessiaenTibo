from RPi import GPIO
import time
from smbus import SMBus
i2c=SMBus()
i2c.open(1)

class lcd:
    aantal=0
    # rs laag, set_databits_bits, E laag, e hoog
    def sent_instructions(self,value):
        waarde=i2c.read_byte(0x38)
        i2c.write_byte(0x38,waarde&0b11101111)#rs=0
        waarde=i2c.read_byte(0x38)
        i2c.write_byte(0x38,waarde|0b00100000)#e=1
        waarde=i2c.read_byte(0x38)
        lcd.set_data_bits(self,value,1)
        waarde=i2c.read_byte(0x38)
        i2c.write_byte(0x38,waarde&0b11011111)#e=0
        waarde=i2c.read_byte(0x38)
        time.sleep(0.01)
        i2c.write_byte(0x38,waarde|0b00100000)#e=1
        waarde=i2c.read_byte(0x38)
        lcd.set_data_bits(self,value,2)
        waarde=i2c.read_byte(0x38)
        i2c.write_byte(0x38,waarde&0b11011111)#e=0
        waarde=i2c.read_byte(0x38)
        time.sleep(0.01)
    # rs laag, set_databits_bits, E laag, e hoog
    def sent_characters(self,value):
        waarde=i2c.read_byte(0x38)
        global aantal
        if lcd.aantal ==16:
            lcd.set_cursor(self,0,1)
        i2c.write_byte(0x38,waarde|0b00110000)#rs=1 e=1
        waarde=i2c.read_byte(0x38)
        lcd.set_data_bits(self,ord(value),1)
        waarde=i2c.read_byte(0x38)
        i2c.write_byte(0x38,waarde&0b11011111)#e=0
        time.sleep(0.01)
        waarde=i2c.read_byte(0x38)
        i2c.write_byte(0x38,waarde|0b00100000)#e=1
        lcd.set_data_bits(self,ord(value),2)
        waarde=i2c.read_byte(0x38)
        i2c.write_byte(0x38,waarde&0b11011111)#e=0
        time.sleep(0.01)
        waarde=i2c.read_byte(0x38)
        lcd.aantal+=1
    # value=byte, loop trough bits (mask) and set data pins
    def set_data_bits(self,value,nibel):
        nibbel1=value>>4
        nibbel2=value&0x0F
        waarde=i2c.read_byte(0x38)
        if nibel==1:
            # print(nibbel1)
            waarde=waarde|(nibbel1)
            waarde=waarde&(nibbel1|0b11110000)
            i2c.write_byte(0x38,waarde)#eeste deel
        else:
            # print(nibbel2)
            waarde=waarde|(nibbel2)
            waarde=waarde&(nibbel2|0b11110000)
            i2c.write_byte(0x38,waarde)#eeste deel
    # function set, display on, clear, en cursor home
    def lcdInit(self):
        i2c.write_byte(0x38,0)#e=0
        lcd.sent_instructions(self,0b0010)
        lcd.sent_instructions(self,0b00001111)
        lcd.sent_instructions(self,0b00000001)
    # verchilende carakters verzenden
    def write_message(self,velue):
        for i in range(len(velue)):
            lcd.sent_characters(self,velue[i])
    # cursor verzetten
    def set_cursor(self,x,y):
        global aantal
        lcd.aantal=x
        adress=y*0x40+x
        lcd.sent_instructions(self,128|adress)
    
    def clear_screen(self):
        lcd.sent_instructions(self,0b00000001)
        lcd.aantal=0

    def stop(self):
        i2c.close()