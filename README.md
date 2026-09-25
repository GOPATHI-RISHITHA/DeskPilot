Yes — you want **clean Markdown that you can copy directly into GitHub's `README.md` editor**.

Copy everything below:

````markdown
# DeskPilot – AI Operating System Assistant

DeskPilot is an AI-powered desktop assistant designed to interact with a Windows computer using natural-language commands.

It combines a desktop interface, AI-based command understanding, specialized agents, and system tools to help users perform everyday computer tasks through text and voice.

## Overview

DeskPilot acts as an AI layer between the user and the Windows operating system.

Instead of manually navigating through applications, folders, terminals, and other services, users can give commands such as:

- Open Chrome
- Create a folder on the desktop
- Open VS Code
- Show system statistics
- Find emails from Naukri
- Create an email draft
- Send an email
- Search the web for DBMS concepts
- Create a file inside the Study folder

DeskPilot interprets the user's request, selects the appropriate tool or agent, performs the required operation, and provides a response.

## Key Features

### Natural Language Commands

Users can interact with DeskPilot using normal language instead of memorizing commands.

Example:

> Create a folder called Placement on my desktop.

### Voice Commands

DeskPilot supports voice-based interaction.

The voice pipeline is:

```text
User Voice
    ↓
Audio Recording
    ↓
FastAPI Backend
    ↓
Gemini Audio Transcription
    ↓
Natural Language Command
    ↓
AI Orchestrator
    ↓
Appropriate Agent
    ↓
Windows / Web / Gmail Action
    ↓
DeskPilot Response
````

### AI Command Understanding

DeskPilot uses Google's Gemini model to understand natural-language requests and determine which tool should handle each request.

The AI orchestrator connects the language model with the available agents and tools.

### Application Control

DeskPilot can open and close commonly used Windows applications, including:

* Google Chrome
* Microsoft Edge
* Brave
* Firefox
* Visual Studio Code
* Notepad
* Paint
* Calculator
* Command Prompt
* PowerShell
* File Explorer
* Settings
* Task Manager
* Control Panel
* Spotify
* WhatsApp
* Discord

### File Operations

DeskPilot supports file-management operations such as:

* Creating folders
* Creating files
* Listing files
* Searching for files
* Working with the Windows Desktop
* Working with the Study folder

Example:

> Create a DBMS file inside the Study folder.

### Terminal Operations

DeskPilot can execute terminal commands through its terminal agent, allowing users to perform command-line operations through natural-language requests.

### System Control

DeskPilot provides system-level utilities including:

* System statistics
* Volume control
* Brightness control

### Web Research

DeskPilot can perform web research using Gemini with Google Search grounding.

Example:

> Search the web for basic DBMS concepts important for placements.

### Gmail Integration

DeskPilot integrates with Gmail using the Gmail API and OAuth 2.0.

Supported operations include:

* Gmail connection testing
* Searching emails
* Listing unread emails
* Reading emails
* Creating email drafts
* Preparing emails for sending
* Sending emails after confirmation

Example:

> Find emails from Naukri.

### Email Confirmation

DeskPilot uses a confirmation step before sending emails.

```text
User Request
    ↓
Prepare Email
    ↓
Show Recipient / Subject / Body
    ↓
User Confirmation
    ↓
Send Email
```

This provides an additional safety layer before performing an external action.

### Voice Response

DeskPilot provides spoken responses using text-to-speech.

The current interface uses a female English voice when an available female English system voice is detected.

### AI Avatar Interface

DeskPilot uses a floating desktop avatar as its main interaction interface.

The avatar provides different visual states:

* Idle
* Listening
* Thinking
* Speaking
* Completed
* Error

This gives the user visual feedback about the assistant's current state.

## Architecture

DeskPilot follows a modular agent-based architecture.

```text
                    ┌─────────────────────┐
                    │     User Input      │
                    │    Text / Voice     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Electron + React   │
                    │      Frontend       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       FastAPI       │
                    │       Backend       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   AI Orchestrator   │
                    │       Gemini        │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      Application Agent    File Agent     Terminal Agent
             │
             ├──────────────────┐
             │                  │
             ▼                  ▼
       System Agent         Web Agent
             │
             ▼
        Email Agent
             │
             ▼
           Gmail
```

## Agents

### Application Agent

Handles opening, closing, and checking running applications.

### File Agent

Handles file and folder operations.

### Terminal Agent

Handles terminal command execution.

### System Agent

Handles system-level operations such as volume, brightness, and system statistics.

### Web Agent

Handles web research using Gemini and Google Search.

### Email Agent

Handles Gmail operations such as searching, reading, drafting, and sending emails.

### Calendar Agent

Provides the structure for calendar-related functionality.

### Memory Agent

Provides the structure for storing and retrieving user-related information.

### Voice Agent

Processes uploaded audio and converts speech into text using Gemini.

## Technology Stack

### Frontend

* Electron
* React
* Vite
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### AI

* Google Gemini
* Gemini Tool Calling
* Google Search Grounding

### APIs and Services

* Gmail API
* Google OAuth 2.0

### System Integration

* Windows applications
* PowerShell
* Windows file system

## Project Structure

```text
DeskPilot/
│
├── backend/
│   ├── agents/
│   │   ├── application_agent.py
│   │   ├── calendar_agent.py
│   │   ├── email_agent.py
│   │   ├── file_agent.py
│   │   ├── memory_agent.py
│   │   ├── system_agent.py
│   │   ├── terminal_agent.py
│   │   ├── voice_agent.py
│   │   └── web_agent.py
│   │
│   ├── core/
│   │   ├── ai_orchestrator.py
│   │   ├── config.py
│   │   └── confirmation_manager.py
│   │
│   ├── utils/
│   │   └── helpers.py
│   │
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── electron/
│   │   └── main.js
│   │
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   │
│   ├── index.html
│   ├── package.json
│   └── package-lock.json
│
├── .gitignore
├── README.md
└── .vscode/
```

## Installation

### Prerequisites

* Windows 10/11
* Python 3.10+
* Node.js
* npm
* Git

### Backend Setup

Clone the repository:

```powershell
git clone https://github.com/GOPATHI-RISHITHA/DeskPilot.git
cd DeskPilot
```

Navigate to the backend:

```powershell
cd backend
```

Install Python dependencies:

```powershell
py -m pip install -r requirements.txt
```

Create a `.env` file inside the `backend` folder:

```text
GEMINI_API_KEY=your_gemini_api_key
```

For Gmail functionality, configure Google OAuth 2.0 and place the credentials file inside:

```text
backend/credentials.json
```

Do not commit credentials, tokens, or API keys to GitHub.

### Start the Backend

```powershell
cd backend
py -m uvicorn main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

### Start the Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

The Vite development server runs at:

```text
http://localhost:5173
```

Electron loads the DeskPilot interface from this address.

## API Endpoints

### General

```text
GET  /
POST /api/command
POST /api/voice
```

### Application

```text
POST /api/app/open
POST /api/app/close
GET  /api/app/running
```

### File

```text
POST /api/file/create-folder
POST /api/file/create-file
GET  /api/file/list
GET  /api/file/search
```

### Terminal

```text
POST /api/terminal/run
```

### System

```text
GET  /api/system/stats
POST /api/system/volume
POST /api/system/brightness
```

### Email

```text
POST /api/email/prepare-send
POST /api/email/confirm-send
POST /api/email/cancel-send
```

FastAPI interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Example Commands

### Applications

```text
Open Chrome.
```

```text
Close Chrome.
```

### Files

```text
Create a folder called Placement on my desktop.
```

```text
Create the DBMS file inside the Study folder.
```

### System

```text
Show my system statistics.
```

### Email

```text
Find emails from Naukri.
```

```text
Read the latest email from Google.
```

```text
Create an email draft to rishithagopathi@gmail.com.
```

```text
Send an email to rishithagopathi@gmail.com with subject Test Email and body Hello from DeskPilot.
```

### Web

```text
Search the web for DBMS concepts important for placements.
```

### Voice

Users can speak commands through the DeskPilot microphone interface instead of typing them.

## Security

DeskPilot uses OAuth 2.0 for Gmail authentication.

Sensitive files are excluded from Git using `.gitignore`:

```text
backend/credentials.json
backend/token.json
```

API keys should be stored in environment variables rather than directly inside source code.

Email sending requires explicit confirmation before the message is sent.

## Future Scope

* Wake-word activation
* Calendar automation
* Persistent user memory
* More Windows system controls
* Workflow automation
* Additional application integrations
* Improved multi-step task execution
* Additional AI tools and agents
* Improved privacy and permission controls
* Windows production packaging

## Project Status

DeskPilot is currently under active development.

### Implemented

* AI command understanding
* Windows application control
* File operations
* Terminal operations
* System controls
* Web research
* Voice input
* Voice transcription
* AI-generated responses
* Gmail integration
* Email search
* Email reading
* Email drafting
* Email sending with confirmation
* Desktop avatar interface
* Voice responses

## Team

**DeskPilot – AI Desktop Assistant**

Developed as a final-year major project.

## License

This project is currently intended for academic and educational purposes.

