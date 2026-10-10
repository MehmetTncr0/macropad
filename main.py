from machine import Pin, PWM, I2C
import time
import framebuf

class SSD1306(framebuf.FrameBuffer):
    def __init__(self,width,height,external_vcc):
        self.width=width
        self.height=height
        self.external_vcc=external_vcc
        self.pages = self.height//8
        self.buffer=bytearray(self.pages*self.width)
        super().__init__(self.buffer,self.width,self.height,framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        for cmd in (
            0xAE,0xD5,0x80,0xA8,self.height-1,0xD3,0x00,
            0x40,0x8D,0x14 if not self.external_vcc else 0x10,
            0x20,0x00,0xA1,0xC8,0xDA,0x12 if self.height == 64 else 0x02,
            0x81,0xCF if not self.external_vcc else 0x9F,
            0xD9,0xF1 if not self.external_vcc else 0x22,
            0xDB,0x40,0xA4,0xA6,0xAF):
            self.write_cmd(cmd)
        self.fill(0)
        self.show()
    def show(self):
        for page in range(self.pages):
            self.write_cmd(0xB0+page)
            self.write_cmd(0x00)
            self.write_cmd(0x10)
            self.write_data(self.buffer[self.width*page:self.width*(page+1)])

class SSD1306_I2C(SSD1306):
    def __init__(self,width,height,i2c,addr=0x3C,external_vcc=False):
        self.i2c=i2c
        self.addr = addr
        self.temp = bytearray(2)
        super().__init__(width,height,external_vcc)

    def write_cmd(self,cmd):
        self.temp[0]=0x00
        self.temp[1]=cmd
        self.i2c.writeto(self.addr,self.temp)

    def write_data(self,buf):
        self.i2c.writeto(self.addr,b'\x40'+buf)


i2c = I2C(0,sda = Pin(8),scl=Pin(9),freq=400000)
oled = SSD1306_I2C(128,64,i2c,addr=0x3c)
PIN_NUMBERS= [12,13,14,15,16,17,18,19,20,21,22,26]
switches = {pin_no:Pin(pin_no,Pin.IN,Pin.PULL_UP)for pin_no in PIN_NUMBERS}
previous_states = {pin_no:1 for pin_no in PIN_NUMBERS}

RED,GREEN,BLUE = 5,27,28
redpwm = PWM(Pin(RED),freq=1000)
greenpwm = PWM(Pin(GREEN),freq=1000)
bluepwm = PWM(Pin(BLUE),freq=1000)

encoderclk = Pin(7,Pin.IN,Pin.PULL_UP)
encoderdt = Pin(10,Pin.IN,Pin.PULL_UP)
encodersw = Pin(11,Pin.IN,Pin.PULL_UP)

last_clk = encoderclk.value()
prev_sw_state = 1

rgb_mode = 0
color_index = 0
colorpalette = [
    ("Kirmizi",255,0,0),
    ("Yesil",0,255,0),
    ("Mavi",0,0,255),
    ("Sari",255,255,0),
    ("Turkuaz",0,255,255),
    ("Mor",255,0,255),
    ("Beyaz",255,255,255),
]
rainbow_hue=0
last_rgb_uptade = time.ticks_ms()

current_notification = ""
notification_end_time = 0
volume_pct=50
audio_output_index=0
AUDIO_OUTPUTS=["Kulaklık","Hoparlör","Bluetooth"]

def set_rgb(r,g,b):
    redpwm.duty_u16(65535-int(r*65535/255))
    greenpwm.duty_u16(65535-int(g*65535/255))
    bluepwm.duty_u16(65535-int(b*65535/255))

def hsv_to_rgb(h,s,v):
    h = h%360
    c = v*s
    x = c*(1-abs((h/60)%2 - 1))    
    m = v-c
    if h<60: r, g, b=c,x,0
    elif h<120:r,g,b=x,c,0
    elif h<180:r,g,b=0,c,x
    elif h<240:r,g,b=0,x,c
    elif h<300:r,g,b=x,0,c
    else :r,g,b=c,0,x
    return int((r+m)*255),int((g+m)*255),int((b+m)*255)

def trigger_notification(text):
    global current_notification,notification_end_time
    current_notification = text
    notification_end_time=time.ticks_add(time.ticks_ms(),2500)

def draw_default_screen():
    oled.fill(0)
    oled.text("MACROPAD v1.0",0,0)
    oled.text("-------------",0,10)
    oled.text("Saat : 14:30",0,10)
    oled.text("Tarih : 11.10.2026",0,38)
    oled.text("Hava : 22C Acik",0,52)
    oled.show()

def draw_notification_screen(text):
    oled.fill(0)
    oled.text("--- BILDIRIM ---",0,0)
    lines= text.split("\n")
    if len(lines)==1:
        oled.text(lines[0],0,28)
    else:
        oled.text(lines[0],0,22)
        oled.text(lines[1],0,40)
    oled.show()

print("Sistem aktif")
draw_default_screen()

while True:
    now = time.ticks_ms()
    if rgb_mode ==0:
        name,r,g,b= colorpalette[color_index]
        set_rgb(r,g,b)
    else:
        if time.ticks_diff(now,last_rgb_uptade)>20:
            rainbow_hue= (rainbow_hue+2)%360
            r,g,b = hsv_to_rgb(rainbow_hue,1.0,2.0)
            set_rgb(r,g,b)
            last_rgb_uptade = now

    current_clk =encoderclk.value()
    if current_clk != last_clk and current_clk ==0:
        if encoderdt.value() != current_clk:
            volume_pct = min(100,volume_pct+5)
        else:
            volume_pct = max(0,volume_pct-5)
        trigger_notification(f"Ses Seviyesi:\n {volume_pct}")
    last_clk= current_clk

    sw_state= encodersw.value()
    if sw_state ==0 and prev_sw_state ==1:
        audio_output_index =(audio_output_index+1)%len(AUDIO_OUTPUTS)
        trigger_notification("Cikis cihazi:\n"+ AUDIO_OUTPUTS[audio_output_index])
        time.sleep_ms(20)
    prev_sw_state = sw_state

    for pin_no, switch_pin in switches.items():
        curr_st=switch_pin.value()
        if curr_st != previous_states[pin_no]:
            time.sleep_ms(15)
            if switch_pin.value()==curr_st:
                previous_states[pin_no]= curr_st

                if curr_st == 0: 
                    if pin_no == 12:
                        trigger_notification("Tirnak Isareti (\")\nYazildi")
                    elif pin_no == 13:
                        trigger_notification("Google Aciliyor...")
                    elif pin_no == 14:
                        trigger_notification("YouTube Aciliyor...")
                    elif pin_no == 15:
                        trigger_notification("Pencere Degisti\n(Alt + Tab)")
                    elif pin_no == 16:
                        rgb_mode = 1 - rgb_mode
                        mode_str = "RGB Stream" if rgb_mode == 1 else "Tek Renk"
                        trigger_notification("RGB Mod:\n" + mode_str)
                    elif pin_no == 17:
                        if rgb_mode == 0:
                            color_index = (color_index + 1) % len(colorpalette)
                            c_name = colorpalette[color_index][0]
                            trigger_notification("Renk Seçildi:\n" + c_name)
                        else:
                            trigger_notification("Uyari: RGB Stream\nModu Aktif!")
                    elif pin_no == 18:
                        trigger_notification("Medya:\nBaslat / Durdur")
                    elif pin_no == 19:
                        trigger_notification("Mikrofon:\nSessize Alindi")
                    elif pin_no == 20:
                        trigger_notification("Ses:\nTamamen Kapatildi")
                    elif pin_no == 21:
                        trigger_notification("Medya:\nSonraki Parca")
                    elif pin_no == 22:
                        trigger_notification("Ekran Goruntusu\nAlindi (Win+Shift+S)")
                    elif pin_no == 26:
                        trigger_notification("Komut Satiri\nAciliyor...")

    if time.ticks_diff(notification_end_time, now) > 0:
        draw_notification_screen(current_notification)
    else:
        draw_default_screen()

    time.sleep_ms(2)
