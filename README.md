# Nugget Inference Script

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/JBU_Tyson_Capstone.git
   cd your-repo
   ```

2. Create and activate a virtual environment:

   - **On macOS/Linux:**

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - **On Windows:**

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the MariaDB database

   - **On macOS/Linux/WSL:**
     ```bash
     bash scripts/setup_db.sh
     ```
   - **On Windows:**

     ```bash
     scripts\setup_db.bat
     ```

     🛑 Make sure you have MariaDB installed and that the mysql command is available in your terminal. This will create the robertodb database and load the schema and sample data from db/robertodb.sql.

     💡 Need MariaDB?
     Install from: https://mariadb.org/download

5. Extract the Ignition project .zip file
   ```bash
    python scripts/download_ignition_project.py
   ```
   This will unzip the Ignition project archive located at ignition/NuggetInference.zip into a folder named NuggetInference in your current directory. You can then import the project into Ignition using the Gateway web interface.

## Running the Program

6. Run the script:

   ```bash
   python main.py
   ```

   Make sure your camera is connected and any necessary hardware (like the scale or external devices) is properly set up before running the script.
