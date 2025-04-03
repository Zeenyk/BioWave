# BioWave

## Overview  
BioWave is a web-based application designed to remotely control and monitor the **BioBench bioreactor** (BioFlex) over a **Local Area Network (LAN)**. Unlike the existing Windows-only software, BioWave provides a **cross-platform, mobile-friendly interface**, making it more accessible for chemists and students who may not be tech-savvy.

## General Objectives

* [ ] Make a dynamic web app that can remotely connect to the bio reactor BioBench like the BioFlex Windows Software. 
* [ ] It works on the same LAN (Local Area Network), allowing the user to insert operations with or without time stamps, visualize data and generally control it.
* [ ] The app should be user friendly both from desktop and mobile as the majority of the chemists students don't are generally skilled with computers.

***

### Wiki

#### Frontend
- **Styling**: TailwindCSS / Bootstrap
- **Visualization**: Chart.js / D3.js (for real-time data)

#### Backend
- **Language**: Python / C++ / Java
- **Communication**: WebSockets (for real-time updates)
- **Database**: MariaDB (for storing logs)

These are the two manuals from the BioBench company regarding the bio reactor BioFlex:

- [BioBench Manual](./documentation/manuals/BioBenchManual.pdf)  
- [BioFlex Manual](./documentation/manuals/BioFlexManual.pdf) 

***

## Features  
  * [ ] **Remote Control** – Send commands to BioFlex via LAN.  
  * [ ] **Real-Time Monitoring** – Visualize sensor data (pH, temperature, O₂, etc.).  
  * [ ] **Scheduled Operations** – Queue timed commands (e.g., "Stir at 300 RPM at 12:00").  
  * [ ] **Mobile-Friendly UI** – Responsive design for phones & tablets.  
  * [ ] **Data Logging** – Export experiment data as CSV/PDF.  
  * [ ] **User Authentication** – Secure access control (if needed).  

***

## Setup  
### Prerequisites  
- Python X.XX+
- BioFlex connected to LAN  

### Installation  
**1. Clone** the repo:  
  ```bash  
  git clone https://github.com/Zeenyk/BioWave.git
  ```
**2. Everytime** you want to work on the repo, you have to run this command on the current directory in VSCode
  ```bash  
  git pull
  ```
**3.** Every group has to **create a branch**: a single branch represent the implementation of something new. You can keep pushing updates in the branch and then, when the new feature is full implemented, you can merge the branch to the main one.
   
***



### Work Subdivision ( Credits )

* Antonio Roggio --> Documentation, UI / UX, Frontend
* Luca Fabris --> Documentation, UI / UX, Frontend
* Suad Bojagic --> UI / UX, Frontend (Helper)
* Federico Peselli --> Documentation, Backend & Logics
* Leonardo Taverna --> Backend & Logics
* Matteo Turello --> Backend & Logics (Helper)
* Daniele Toniolo --> Fullstack
* Sami Sufiane --> Fullstack (Helper) 
***



