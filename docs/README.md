##### **ChronoOS - A Proactive Energy Strategist (Windows Prototype)**
Welcome to the complete documentation for the ChronoOS project. This document covers our unique approach, technical architecture, implementation details, and a full guide to setting up and running the simulation.

#### Table of Contents
1. Our Unique Approach
2. Salient Features
3. Design Link (Figma)
4. Technical Architecture
5. Technical Stack
6. Installation & User Guide
7. Implementation Details

#### Our Unique Approach
The innovation of ChronoOS lies in shifting from reactive, application-level power saving to proactive, session-level energy planning.
While traditional battery savers ask, "How do I save power on Instagram right now?", ChronoOS asks a more intelligent question:
"The user is on their 45-minute train commute. They'll likely use Spotify, Maps, and a news app. How do I allocate a total energy budget across this entire sequence to guarantee the phone is ready for the work day ahead?"
This fusion of a predictive sequence model (The Seer) with a real-time resource allocation engine (The Planner & Governor) is what makes ChronoOS truly agentic and unique. We aren't just optimizing; we're creating a goal-oriented energy strategist that plans for the future.

#### Salient Features
1. End-to-End Simulation: The project provides a complete, four-layer simulation of the agent's logic, running on a Windows machine.
2. Live Data Integration: The simulation is driven by live data, including the user's actual app usage history (via a background logger) and the device's real-time battery level.
3. Machine Learning Core: At its heart is a TensorFlow Lite LSTM model trained to predict user behavior, showcasing a practical application of on-device AI.
4. Modular and Scalable: The code is cleanly separated into its architectural layers, making it easy to understand, maintain, and eventually port to Android.
5. One-Click Execution: A master script (start_simulation.py) handles all setup, including launching the background data logger, providing a seamless demo experience.

#### 🎨 Design Link
[Link to our Figma Design Prototype] (<- Add your Figma link here)

#### 🏛️ Technical Architecture
The ChronoOS agent is designed with a layered, modular architecture. Each layer has a distinct responsibility, making the system clean, robust, and scalable.
**Layer 1: Perception Service (The Collector)**
Function: Gathers contextual data about the user's activity.
Prototype: data_logger.py runs in the background to log app switches, and data_collector.py reads this log to provide the most recent app history.

**Layer 2: Prediction Engine (The Seer)**
Function: Predicts the user's next sequence of apps based on their recent history.
Prototype: A pre-trained TensorFlow Lite LSTM model (chrono_os_seer.tflite) and a vocabulary file (app_vocab.json) are loaded and managed by the seer_engine.py class.

**Layer 3: Reasoning Engine (The Planner)**
Function: The "brain" of the agent. It takes the Seer's prediction, checks the battery, and creates a dynamic energy budget.
Prototype: reasoning_engine.py uses a knowledge base in data_store.py to assign power scores to apps based on their category (e.g., "web_browser", "gaming") and allocates the session budget proportionally.

**Layer 4: Actuation Kernel (The Governor)**
Function: Executes the Planner's energy plan by controlling hardware states.
Prototype: actuation_kernel.py is a simulation module that receives directives, logs the actions it would take (e.g., "throttling"), and calculates the simulated battery drain.

#### 🛠️ Technical Stack
This project leverages a range of powerful, open-source libraries.
1. TensorFlow: The primary machine learning framework used to design and train the LSTM neural network.
2. Keras: A high-level API within TensorFlow used to define the model architecture.
3. NumPy: The fundamental package for numerical computation in Python.
4. Pandas: Used for data analysis and manipulation of the app usage logs.
5. psutil: A cross-platform library used to get the foreground application and real-time battery level.
5. pywin32: Provides access to Windows APIs to identify the foreground window.

#### 🚀 Installation & User Guide
This guide provides step-by-step instructions to set up and run the simulation.
1. Installation
First, set up the Python virtual environment and install dependencies.
<img width="976" height="279" alt="image" src="https://github.com/user-attachments/assets/e4c02891-f2c7-4735-9e12-2679d6462d9d" />

2. User Guide
The entire simulation is launched from a single script.
<img width="978" height="121" alt="image" src="https://github.com/user-attachments/assets/85649fae-feb8-40d7-a89e-32c4137299c1" />

This command starts the background data logger and then runs the main simulation, showing you the live output from all four layers.

3. Stopping the Background Logger (IMPORTANT)
The data logger will continue running silently even after the simulation is complete. You must stop it manually.
a) Press Ctrl+Shift+Esc to open the Task Manager.
b) Navigate to the "Details" tab.
c) Scroll down, find the process named pythonw.exe, and click "End task".

#### ⚙️ Implementation Details
**The Seer: Machine Learning Pipeline**
Data Collection (data_logger.py): A background script logs app switches to app_usage_log.csv.
Preprocessing (preprocess_data.py): The raw log is transformed into trainable data by grouping app switches into "sessions" (based on inactivity) and using a sliding window to create input-output sequence pairs.
Training (train_model.py): A Keras Sequential model (Embedding -> LSTM -> Dense) is trained on the sequences. EarlyStopping is used to prevent overfitting.
Conversion (convert_to_tflite.py): The final Keras model is converted to the TensorFlow Lite format and quantized, which significantly reduces its size and makes it highly efficient for on-device inference.

**The Planner: Rule-Based Logic**
Knowledge Base (data_store.py): The Planner uses a two-level dictionary system to determine an app's power consumption. It maps an executable name (e.g., chrome.exe) to a category (web_browser), and then finds the power score for that category. This makes the system highly scalable.
Budget Allocation (reasoning_engine.py): The Planner calculates the total "power need" for a predicted session by summing the scores of all apps. It then allocates the session's total energy budget proportionally. For example, an app with a score of 4 will receive twice the budget of an app with a score of 2.

