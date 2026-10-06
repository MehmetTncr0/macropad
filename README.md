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
