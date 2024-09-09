# How_I_Built_Supply_Chain_Optimization_Using_AI_Agent
How I Built Supply Chain Optimization Using AI Agents

## Introduction

Full Article : [https://medium.com/@learn-simplified/how-about-an-ai-agent-that-builds-complete-software-projects-all-local-8ddda106011c

Imagine a world where your company's payment processing department runs like a well-oiled machine, handling vendor payments with the precision of a Swiss watch and the intelligence of a seasoned financial expert. Sound like a dream? Well, wake up and smell the AI-infused coffee, because that future is here, and it's ready to transform your business operations! Its called "AI Agents"


## Whats This Project About

This article takes you on a journey through the creation of an AI-Agent payment processing system. We're not just talking about a fancy calculator here - we're diving into a fully-fledged workflow that uses artificial intelligence to make decisions, generate reports, and handle payments with minimal human intervention.
Here's what we cover:
 - Setting up a workflow using LangGraph, a powerful tool for creating AI-driven processes
 - Implementing AI agents for various tasks like selecting vendors, summarizing services, and assessing payments
 - Using language models (specifically, Groq's LLMs) to generate human-like responses and make informed decisions
 - Creating a user-friendly interface with Streamlit for easy interaction with the AI system
 - Handling the nitty-gritty of sending payments securely using FastAPI

We'll walk you through each step, from the initial setup to the final implementation, showing you how these cutting-edge technologies can work together to create a robust, intelligent payment processing system.

## Why Work on It?

In today's fast-paced business world, staying ahead of the curve isn't just an advantage - it's a necessity. AI is no longer a futuristic concept; it's a present-day tool that's reshaping how businesses operate. This article shows you, through a practical example, how to harness the power of AI in your day-to-day operations.
By implementing an AI-driven payment processing system like the one described here, businesses can:
 - Reduce human error and bias in financial decisions
 - Speed up payment processes, improving relationships with vendors
 - Generate detailed, consistent reports for better financial tracking
 - Free up human resources for more strategic tasks

While our example company is fictional, the technologies and techniques discussed are very real and applicable to businesses of all sizes. Whether you're a tech-savvy startup or a traditional corporation looking to modernize, this article provides valuable insights into the practical application of AI in business processes.


## Architecture
![Design Diagram](design_docs/design.png)


# Tutorial: Let's Build Enterprise Payment Processing Department Using AI Agents, All Open Source

## Prerequisites
- Python installed on your system.
- A basic understanding of virtual environments and command-line tools.

## Steps

1. **Virtual Environment Setup:**
   - Create a dedicated virtual environment for our project:
   
     ```bash
     python -m venv How_I_Built_Supply_Chain_Optimization_Using_AI_Agent
     ```
   - Activate the environment:
   
     - Windows:
       ```bash
       How_I_Built_Supply_Chain_Optimization_Using_AI_Agent\Scripts\activate
       ```
     - Unix/macOS:
       ```bash
       source How_I_Built_Supply_Chain_Optimization_Using_AI_Agent/bin/activate
       ```
   
# Installation and Setup Guide

**Install Project Dependencies:**

Follow these steps to set up and run the ResearchAgents project:

1. Navigate to your project directory:
   ```
   cd path/to/your/project
   ```
   This ensures you're in the correct location for the subsequent steps.

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   This command installs all the necessary Python packages listed in the requirements.txt file.


## Run - Enterprise Payment Processing Department Using AI Agents, All Open Source

   ```bash 
      # Run Payment Gateway FAST API
      python  vendor_payment_gateway.py
      
      # Run Payment Gateway FAST API
      streamlit run payment_processing_workflow.py
      
   ```







