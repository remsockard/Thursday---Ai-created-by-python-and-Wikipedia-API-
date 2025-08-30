🧠 AI Learning Assistant

This project is a personal AI assistant that can learn, remember, and adapt over time through interaction with the user. It combines memory storage, natural interaction, math solving, voice/chat support, and emotional responses into one system.

🔑 Key Features

📚 Self-Learning Memory

Remembers facts told by the user (e.g., “my birthday is 2 May”).

Can recall, forget, and list memories (memory.py, memory.json).

Stores facts permanently in memory_store.json.

🌐 Knowledge Expansion

If it doesn’t know something, it asks the user whether to teach it or to search online.

Uses WolframAlpha API + Wikipedia fallback for learning new facts.

➗ Built-in Math Engine

Detects math-related queries.

Solves expressions using a custom math module (works like a calculator).

🗣 Voice & Text Interaction

Two modes:

Chat mode (type text in terminal/UI).

Voice mode (speech recognition + speech synthesis).

Can dynamically switch between modes with commands.

😊 Emotional Mascot UI

Includes two Tkinter-based interfaces:

ui.py: Chat-style assistant with attach-file option.

moscot_ui.py: Floating mascot character that changes emotions (happy, sad, confused, excited, etc.) based on interactions.

Emotion images are stored in assets/emotions/.

🔤 Smart Input Handling

Built-in spellchecker with a whitelist for technical terms.

Normalizes user queries (e.g., “I’m Pradeep” → identity: Pradeep).

📝 Context-Aware Conversation

Can adapt its responses depending on memory, current mode, and user queries.

Special system to track pending lookups and learning sessions.

📂 Project Structure

main.py → Core AI logic (chat, memory, math, web search, emotion updates).

memory.py → Functions for remembering, recalling, forgetting, listing facts.

memory.json / memory_store.json → Storage files for learned knowledge.

ui.py → Full-featured Tkinter-based assistant interface.

moscot_ui.py → Cute floating mascot with emotions and draggable UI.

assets/emotions/ → Images representing emotional states.

⚠️ Current Status

The project is still under development and contains some bugs.

Features like Wikipedia API integration, better NLP understanding, and bug fixes are planned.
