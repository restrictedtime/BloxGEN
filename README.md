BloxGEN - Roblox Username Sniper Tool

========================
Requirements
========================
- Python 3.10+ installed
- pip (Python package manager)
- Internet connection
- Git (optional if cloning from GitHub)

Python packages needed:
- requests
- colorama

Install packages with:
pip install requests colorama

========================
Windows Instructions
========================
1. Download Python 3.10+ from https://www.python.org/downloads/windows/
2. Install Python and make sure "Add Python to PATH" is checked
3. Download or clone the BloxGEN repository
   - To clone: git clone https://github.com/restrictedtime/BloxGEN.git
4. Open Command Prompt (cmd) in the BloxGEN folder
5. Install requirements:
   pip install requests colorama
6. Create a file named usernames.txt with usernames you want to check
7. Run the script:
   python main.py
8. Follow on-screen options:
   1) Choose layout → Generate usernames with custom pattern
   2) Choose from file → Check usernames in usernames.txt
   3) Quit → Exit
9. Valid usernames are saved in valid.txt
   Invalid/taken usernames are saved in invalid.txt

========================
Mac Instructions
========================
1. Install Python 3.10+ (via https://www.python.org/downloads/macos/)
2. Open Terminal
3. Navigate to the BloxGEN folder
   cd /path/to/BloxGEN
4. Install requirements:
   pip3 install requests colorama
5. Create a file named usernames.txt with usernames you want to check
6. Run the script:
   python3 main.py
7. Follow the same on-screen options as Windows
8. Output files:
   - valid.txt → valid usernames
   - invalid.txt → invalid/taken usernames

========================
Notes
========================
- Make sure to replace the webhook URL in main.py if you want notifications
- Use a reasonable number of threads (default 20)
- Press Ctrl+C to stop continuous generation if using layout option
