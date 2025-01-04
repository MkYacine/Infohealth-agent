# Infohealth Agent

A conversational AI system designed to assist patients with medication management and deprescription guidance. The agent follows medical protocols and guidelines to provide personalized advice while ensuring patient safety.

## To do:
- Add logging in the LLM call functions 
- Implement validation tests
- Implement railguard with async calling with extraction chain
- Implement tree for AC meds
- Change workflow input to take user's list of meds.


## Features
- Structured conversation flows based on medical protocols
- Safe and controlled responses for medication guidance
- Token usage monitoring and conversation state management
- Modular design for easy addition of new medication workflows

## Tech Stack
- Python
- LLM API integration
- Streamlit (demo interface)

## Project Structure
- Agent core logic for conversation management
- Medication-specific workflow definitions
- Input validation and safety checks
- State management for conversation tracking

## Development
This is an ongoing project aimed at providing medical guidance through a conversational interface. The current implementation serves as a proof of concept, with plans to expand medication coverage and deploy as a web service.

## Safety Note
This agent is designed to complement, not replace, professional medical advice. All medication guidance follows established medical protocols and guidelines.