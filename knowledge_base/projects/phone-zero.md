<!-- markdownlint-disable MD003 MD007 MD022 MD032 -->

---

title: Phone Zero
type: project
category: accessibility-device
status: active
repository: https://github.com/mitselek/touch-tone
language: C++
last_updated: 2025-09
experience: personal-project
organization: Personal Project
role: Hardware/Software Engineer
duration: 2025 to present

prototype_version: v0.2.0
project_stage: proof-of-concept

---

<!-- markdownlint-enable MD003 MD007 MD022 MD032 -->

# Phone Zero

**Accessibility Phone for Elderly Blind Users - IoT Device with Cellular Connectivity**

Phone Zero is a custom desktop phone designed specifically for elderly blind users, featuring large tactile buttons instead of a screen. The device integrates ESP32 microcontroller with GSM/4G cellular connectivity, demonstrating expertise in embedded systems, IoT hardware, and accessibility-focused design.

## Project Status

**Current Stage:** Proof of Concept (Prototype v0.2.0)  
**Last Updated:** September 2025  
**Progress:** ~20% toward functional prototype  
**Key Achievement:** GSM communication validated on ESP32-WROOM-32 + SIM900A platform

## Technology Stack

### Hardware Platform

- **ESP32-WROOM-32** - Main microcontroller (DoiT ESP32 DevKit v1)
  - 4MB Flash memory
  - Hardware UART2 for reliable communication
  - WiFi/Bluetooth capability (unused in this application)
- **SIM900A GSM/GPRS Module** - Cellular connectivity
  - Quad-band GSM
  - Voice calling and SMS capabilities
  - AT command interface
- **JZK XL4015 DC-DC Converter** - Power management
  - 4-38V input, 1.25-36V output
  - Max 5A current
  - Powers both ESP32 and GSM module from single supply
- **8 Tactile Push Buttons** - User interface
  - Large buttons for accessibility
  - Internal pull-up resistors
  - Instant speed dial functionality

### Firmware

- **Language:** C++ (Arduino framework)
- **Platform:** PlatformIO IDE
- **Communication:** Hardware UART (Serial2)
- **Storage:** ESP32 Preferences (non-volatile flash)
- **AT Commands:** GSM protocol implementation

### Future Hardware Considerations

- **4G Modules:** SIM7670G or A7670 (evaluated for v0.3.0)
- **Audio Processing:** CS48L32-CWZR (echo cancellation)
- **Audio System:** MAX98357A I2S amplifier + speaker
- **Power:** LiPo battery for extended off-grid operation

## Core Features

### Implemented (v0.2.0) ✅

- **Speed Dial System:** 8 buttons for instant calling
- **SMS Programming:** Remote configuration via authorized numbers
  - `SET 1 +1234567890` - Program button
  - `LIST` - Get current numbers
  - `STATUS` - Check device status
  - `SMS "text" +number` - Relay messages
- **Call Management:**
  - Initiate voice calls
  - Detect incoming calls
  - Answer calls
  - Hang up calls
- **Persistent Storage:** Phone numbers saved to ESP32 flash
- **Security:** Authorized number whitelist
- **Memory Management:** Automatic SMS cleanup for privacy
- **Network Monitoring:** Signal quality and registration status

### Validated Capabilities ✅

- GSM communication (calls, SMS)
- Hardware UART ESP32↔SIM900A
- Button input detection and debouncing
- Persistent storage using ESP32 Preferences
- SMS command parsing
- Single power supply solution
- Audio output (tested via earphone jack)

### Not Yet Implemented ❌

- Microphone integration
- Speaker amplifier
- Audio processing (echo cancellation)
- Battery backup system
- Physical enclosure
- Extended reliability testing (1+ week operation)
- Complete accessibility features (vibration feedback, audio alerts)

## Design Philosophy

### Accessibility First

- **No Visual Interface:** Designed for blind users
- **Large Tactile Buttons:** Easy to locate and press by touch
- **Audio Feedback:** Planned sound confirmation for operations
- **Vibration Feedback:** Hardware-level haptic alerts (planned)
- **Button-based Call Answering:** Any button accepts incoming calls
- **Battery Status via SMS:** Notifications at 100%, 75%, 50%, 25%, 10%, 5%

### Technical Requirements

- **Always-on Design:** Mains-powered with battery backup
- **Stationary Device:** Desktop/bedside placement
- **Single-piece Unit:** Integrated design with USB-C backup power
- **Low Power Mode:** Optimized battery consumption during outages
- **Reliable Operation:** Designed for non-technical users

## Technical Achievements

### Hardware Integration

- **UART Communication Success:** Hardware Serial2 eliminates Arduino SoftwareSerial limitations
- **Power Architecture:** Single DC-DC converter successfully powers both modules
- **Shared Ground:** Common ground ensures reliable ESP32-GSM communication
- **Automatic Power-Up:** Hardware modification (R13 solder) + GPIO27 control enables SIM900A auto-startup

### Software Framework

- **Memory Management:** ESP32 Preferences for persistent storage
- **SMS Cleanup:** Automatic deletion prevents memory overflow
- **Privacy Protection:** Messages deleted immediately after processing
- **Button Debouncing:** Software-based reliable input detection
- **Error Handling:** Network recovery mechanisms

### Development Evolution

- **v0.1.x:** Arduino Uno/Nano with SoftwareSerial (communication issues)
- **v0.2.0:** ESP32-WROOM-32 with Hardware UART2 (✅ SUCCESS)

## Relevance to Professional Work

### IoT & Embedded Systems

- Hands-on experience with ESP32 microcontroller platform
- Cellular connectivity implementation (GSM/4G)
- Hardware UART communication protocols
- AT command interface programming
- Power management for battery-operated devices

### Telecom Protocols

- GSM protocol implementation
- SMS sending/receiving
- Voice call management
- Network registration and status monitoring
- Signal quality assessment

### Accessibility Engineering

- Human-centered design for visually impaired users
- Tactile interface design
- Audio feedback systems
- Simplified user experience without visual dependency

### Systems Integration

- Multi-component hardware integration
- Power supply management
- Audio routing (planned)
- Sensor integration (movement detection planned)
- Persistent storage systems

## Project Documentation

### Repository Structure

```text
touch-tone/
├── ESP_GSM/                  # Main firmware (PlatformIO)
│   ├── src/main.cpp         # Complete implementation
│   └── platformio.ini       # Build configuration
├── docs/                    # Comprehensive documentation
│   ├── prototype-v0.2.0/   # Current prototype docs
│   ├── boards/             # Hardware pinouts
│   ├── MVP/                # MVP requirements
│   ├── hardware-requirements.md
│   └── phone-specifications.md
└── private/                # Market research
```

### Key Documents

- **README.md** - Project overview and current status
- **prototype-v0.2.0/README.md** - Detailed v0.2.0 documentation with photos
- **hardware-requirements.md** - Component specifications
- **phone-specifications.md** - Core features and accessibility design
- **MVP/** - Minimum viable product milestones and component lists

### Photo Documentation

- Complete hardware setup (8 photos)
- ESP32 wiring (4 detailed photos)
- SIM900A module connections
- Power supply configuration
- Working prototype in operation

## Development Priorities

### v0.3.0 Roadmap

**Immediate Goals:**

1. Audio system integration (microphone + speaker)
2. Audio amplifier circuit implementation
3. Extended reliability testing (1+ week continuous operation)
4. Hardware organization (move from breadboard to PCB)

**Medium-term Goals:**

1. Echo cancellation (CS48L32-CWZR evaluation)
2. Complete software implementation with robust error handling
3. Physical enclosure design
4. Battery backup system integration

**Long-term Vision:**

1. 4G module upgrade (SIM7670G)
2. Production-ready PCB design
3. 3D printed enclosure
4. Complete accessibility feature set
5. Extended field testing with target users

## Technical Skills Demonstrated

### Programming

- C++ (Arduino framework)
- Embedded systems programming
- Hardware abstraction layers
- Interrupt-driven programming
- State machine design

### Hardware

- ESP32 microcontroller architecture
- GSM/GPRS module integration
- Power management circuits
- Audio signal routing
- Button interface design
- UART communication

### Protocols & Standards

- AT commands (GSM)
- UART (hardware serial)
- I2S (audio, planned)
- GSM cellular standards
- SMS protocols

### Tools & Platforms

- PlatformIO IDE
- Arduino framework
- Hardware UART debugging
- Oscilloscope (for troubleshooting)
- Multimeter (power/signal testing)

## Impact & Learning

### Personal Growth

- First embedded systems project from scratch
- Learned cellular connectivity implementation
- Gained hardware integration experience
- Developed accessibility-focused design mindset
- Overcame Arduino-to-ESP32 migration challenges

### Problem Solving

- **Challenge:** Arduino SoftwareSerial unreliable → **Solution:** Migrated to ESP32 Hardware UART
- **Challenge:** Dual power supplies complex → **Solution:** Single DC-DC converter for both modules
- **Challenge:** SIM900A manual power-up → **Solution:** Hardware mod + GPIO control for auto-startup
- **Challenge:** Memory overflow from SMS → **Solution:** Automatic cleanup after processing

### Future Applications

This project provides practical experience relevant to:

- IoT device development
- eSIM standard implementation (1oT position)
- Cellular connectivity platforms
- Embedded systems for accessibility
- Hardware-software co-design
- Power-optimized battery devices

## Connections

This project demonstrates skills from:

- [[javascript]] - Architecture design patterns transferable from software
- [[node-js]] - Async programming concepts applied to embedded systems
- [[api-development]] - AT command interface similar to REST APIs
- [[system-architecture]] - Multi-component system integration

Related to experiences:

- [[entusiastid-ou-2010-present]] - Platform architecture thinking
- [[poff-web-platform]] - Multi-domain system design patterns

---

**Key Takeaway:** Phone Zero represents hands-on IoT hardware experience with cellular connectivity, embedded systems programming, and accessibility-focused design - directly relevant to eSIM/IoT platform development roles.
