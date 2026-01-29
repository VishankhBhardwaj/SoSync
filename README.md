# Sentinel — AI Emergency SOS Assistant

A production-ready emergency response system that uses AI to assess emergency situations and automatically place phone calls via Twilio when immediate assistance is required. The application detects user location through browser geolocation, uses an AI agent to determine if an emergency call is warranted, and triggers a real-time phone call with a synthesized emergency message including the user's situation and location.

## Overview

Sentinel is designed as a reliable, safety-first emergency assistance tool. The system combines browser-based geolocation, deterministic reverse geocoding, and an AI-powered decision agent to provide rapid emergency response capabilities. The AI agent is strictly limited to decision-making and call initiation—it does not provide medical or safety advice, ensuring clear separation of concerns and reducing liability risks.

## Key Features

- **Automatic Location Detection**: Uses browser geolocation API to detect user coordinates
- **Deterministic Reverse Geocoding**: Converts GPS coordinates to human-readable addresses using Nominatim (OpenStreetMap)
- **AI-Powered Decision Making**: LangChain agent evaluates emergency situations using Groq's GPT-OSS-120B model
- **Automated Emergency Calls**: Places real-time phone calls via Twilio with text-to-speech emergency messages
- **Panic Mode**: One-click emergency activation for situations where the user cannot speak
- **Minimal Frontend**: Streamlit-based UI designed for reliability and quick access during emergencies
- **Docker-Ready**: Containerized deployment for consistent environments

## Architecture

### System Flow

```
User Input → Location Detection → Reverse Geocoding → AI Agent Evaluation
                                                              ↓
                                                    Emergency Detected?
                                                              ↓
                                                    Yes → Twilio Call Initiated
                                                              ↓
                                                    Synthesized Message Delivered
```

### Component Breakdown

1. **Frontend (Streamlit)**
   - Captures user input and location via browser geolocation
   - Provides minimal, reliable UI for emergency situations
   - Displays location confirmation and call status

2. **Location Processing (`utils.py`)**
   - Receives GPS coordinates from browser
   - Performs reverse geocoding using Nominatim (deterministic, not LLM-based)
   - Falls back to raw coordinates if geocoding fails

3. **AI Agent (`app.py`, `tools.py`)**
   - LangChain agent with tool-calling capabilities
   - Evaluates user input against emergency criteria
   - Strictly limited to decision-making and call initiation
   - Uses Groq's GPT-OSS-120B model for fast inference

4. **Call Execution (`make_call.py`)**
   - Twilio integration for phone call placement
   - Generates TwiML for text-to-speech message delivery
   - Includes user situation and resolved address in call message

## Tech Stack

- **Frontend Framework**: Streamlit
- **AI/ML Framework**: LangChain, LangChain Groq
- **LLM Provider**: Groq (GPT-OSS-120B model)
- **Telephony**: Twilio API
- **Geocoding**: Geopy (Nominatim/OpenStreetMap)
- **Language**: Python 3.10+
- **Containerization**: Docker

## Prerequisites

- Python 3.10 or higher
- Twilio account with API credentials
- Groq API key
- Browser with geolocation permissions enabled
- Docker (optional, for containerized deployment)

## Setup Instructions

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Sos
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   
   Create a `.env` file in the project root with the following variables:
   ```env
   GROQ_API_KEY=your_groq_api_key
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   SOS_TARGET_NUMBER=target_phone_number_for_emergency_calls
   ```

   **Important**: Never commit your `.env` file to version control. Ensure it's listed in `.gitignore`.

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

   The application will be available at `http://localhost:8501`

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t sentinel-sos .
   ```

2. **Run the container**
   ```bash
   docker run -p 8501:8501 --env-file .env sentinel-sos
   ```

   Alternatively, pass environment variables directly:
   ```bash
   docker run -p 8501:8501 \
     -e GROQ_API_KEY=your_key \
     -e TWILIO_ACCOUNT_SID=your_sid \
     -e TWILIO_AUTH_TOKEN=your_token \
     -e TWILIO_PHONE_NUMBER=your_number \
     -e SOS_TARGET_NUMBER=target_number \
     sentinel-sos
   ```

3. **Access the application**
   
   Navigate to `http://localhost:8501` in your browser

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | API key for Groq LLM service | Yes |
| `TWILIO_ACCOUNT_SID` | Twilio account identifier | Yes |
| `TWILIO_AUTH_TOKEN` | Twilio authentication token | Yes |
| `TWILIO_PHONE_NUMBER` | Twilio phone number (E.164 format) | Yes |
| `SOS_TARGET_NUMBER` | Target phone number for emergency calls (E.164 format) | Yes |

### Obtaining Credentials

- **Groq API Key**: Sign up at [console.groq.com](https://console.groq.com) and generate an API key
- **Twilio Credentials**: Create an account at [twilio.com](https://www.twilio.com) and obtain Account SID, Auth Token, and a phone number from the console

## Safety & Design Philosophy

### Core Principles

1. **AI Role Limitation**: The AI agent is explicitly restricted to decision-making and call initiation. It does not provide medical advice, safety instructions, or emergency guidance beyond triggering the call mechanism.

2. **Deterministic Geocoding**: Reverse geocoding is handled by Nominatim (OpenStreetMap), not the LLM. This ensures consistent, reliable address resolution without AI hallucination risks.

3. **Minimal Frontend**: The UI is intentionally simple to reduce failure points and ensure quick access during high-stress situations.

4. **Fail-Safe Design**: The system includes fallback mechanisms (e.g., coordinate fallback if geocoding fails) to ensure calls can be placed even under adverse conditions.

5. **Clear Separation of Concerns**: Each component has a single, well-defined responsibility, making the system easier to maintain and audit.

## Limitations

### Twilio Trial Account Restrictions

- **Trial Account Limitations**: Twilio trial accounts can only call verified phone numbers. To call unverified numbers, upgrade to a paid account.
- **Call Costs**: Each emergency call incurs Twilio charges based on your account's pricing tier.

### Browser Permissions

- **Geolocation Required**: The application requires browser geolocation permissions. Users must explicitly grant location access.
- **HTTPS Requirement**: Browser geolocation API typically requires HTTPS in production environments (localhost is exempt for development).

### Network Dependencies

- **API Availability**: The system depends on external services (Groq, Twilio, Nominatim). Network outages or API rate limits may affect functionality.
- **Geocoding Rate Limits**: Nominatim has usage policies and rate limits. For production use, consider using a commercial geocoding service or self-hosted Nominatim instance.

### AI Decision-Making

- **False Positives/Negatives**: The AI agent may incorrectly assess emergency situations. The system should be used as a supplementary tool, not a replacement for direct emergency services.
- **Model Limitations**: The GPT-OSS-120B model, while powerful, may have limitations in understanding context or edge cases.

## Usage

1. **Grant Location Permission**: When prompted, allow the browser to access your location.
2. **Describe Your Situation**: Enter a description of your emergency situation in the text input field.
3. **Send SOS**: Click the "🆘 Send SOS" button to trigger the AI agent evaluation.
4. **Panic Mode**: For immediate emergencies where you cannot type, click "🚨 PANIC SOS" to trigger an emergency call with minimal information.

The AI agent will evaluate your input and automatically place a phone call if an emergency is detected. The call will include your situation description and resolved address.

## Future Improvements

- **Multi-language Support**: Extend emergency messages to support multiple languages
- **SMS Fallback**: Implement SMS notifications as a backup when phone calls fail
- **Emergency Contact Management**: Allow users to configure multiple emergency contacts
- **Location History**: Store recent locations for faster emergency response
- **Integration with Emergency Services**: Direct integration with local emergency dispatch systems (where APIs are available)
- **Offline Mode**: Cache location data and provide basic functionality when network connectivity is limited
- **Enhanced Geocoding**: Integration with commercial geocoding services for improved accuracy and reliability
- **Call Recording & Logging**: Audit trail for emergency calls (with privacy considerations)
- **Voice Input**: Support for voice-to-text input for hands-free operation
- **Mobile App**: Native mobile application for improved reliability and background operation

## Contributing

This project is designed for production use in emergency situations. Contributions should prioritize:
- Reliability and safety
- Clear error handling
- Comprehensive testing
- Documentation updates

## License

[Specify your license here]

## Disclaimer

This software is provided as-is for emergency assistance purposes. It is not a replacement for direct emergency services (e.g., 911, 112). Users should always contact local emergency services directly when possible. The developers assume no liability for the use or misuse of this software.
