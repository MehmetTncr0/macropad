# 🎹 12-Key RP2040 Macropad (v1.0)

A 12-key (3x4 layout) mechanical macropad powered by the **Raspberry Pi Pico**, featuring an OLED display, rotary encoder, and an analog potentiometer. 

Designed for macro execution, volume control, layer switching, and media controls.

---

## 🛠️ Features & Hardware

* **Brain:** Raspberry Pi Pico (RP2040)
* **Keys:** 12x Mechanical Switches (3x4 Matrix)
* **Display:** 0.96" SSD1306 OLED (I2C)
* **Controls:** 
  * 1x EC11 Rotary Encoder (with push button)
  * 1x 10k Potentiometer (analog input)
* **PCB Specs:** 2-Layer FR4 | 1.6mm thickness | Dual-sided GND plane

---

## 📦 Bill of Materials (BOM)

| Component | Reference | Quantity | Description |
| :--- | :--- | :--- | :--- |
| Raspberry Pi Pico | U1 | 1 | Microcontroller Board |
| 0.96" I2C OLED | DISP1 | 1 | 128x64 Display |
| Mechanical Switches | SW1–SW12 | 12 | Key Switches (3x4 layout) |
| Rotary Encoder | ROT1 | 1 | EC11 Encoder with Switch |
| Potentiometer | RV1 | 1 | 10k Linear Potentiometer |

---

## 🔧 Design & Status

* **KiCad Routing:** 0 DRC Errors / 0 DRC Warnings.
* **Trace Widths:** 0.2mm for signals, 0.4–0.5mm for power lines.
* **Firmware Target:** KMK Firmware / CircuitPython.
*<img width="799" height="775" alt="_5" src="https://github.com/user-attachments/assets/d69b513c-6884-48ec-8864-6578356bbc1e" />
<img width="792" height="779" alt="_4" src="https://github.com/user-attachments/assets/424e70a7-2bad-44ab-85c1-beae511e8cf8" />
<img width="521" height="514" alt="_3" src="https://github.com/user-attachments/assets/a64772e1-b03d-4e38-baab-4109c34281d4" />
<img width="532" height="522" alt="_2" src="https://github.com/user-attachments/assets/51f7f4ff-6bd4-4b74-b53e-3165fd5550fe" />
<img width="921" height="512" alt="_1" src="https://github.com/user-attachments/assets/68563cd2-cf58-41ea-81c8-593440b6b18d" />
<img width="502" height="595" alt="_7" src="https://github.com/user-attachments/assets/761311fa-5b90-40d1-bbfc-6993df33389d" />
<img width="476" height="550" alt="_6" src="https://github.com/user-attachments/assets/1701399c-775a-4dee-bb3a-663b48664fe7" />



