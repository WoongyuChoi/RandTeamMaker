# RandTeamMaker

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=fff&labelColor=grey&color=yellowgreen)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/WoongyuChoi/RandTeamMaker/blob/main/LICENSE)
![Platform](https://img.shields.io/badge/platform-desktop-blue)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/WoongyuChoi/RandTeamMaker)

<figure align="center">
  <img src="https://github.com/user-attachments/assets/212a87da-1cfd-4d44-a634-0166035b979e" width="80%" />
</figure>

## Overview
**RandTeamMaker** is a Python-based GUI application designed to randomly generate team assignments based on multiple user-defined groups. Built with PyQt5, the tool supports fair mixing between groups, avoiding assigning identical groups to the same team.

## Features

- **Group-Based Input**: Input up to 5 different member groups.
- **Team Count Selection**: Set the number of teams (up to 6) to generate.
- **Smart Shuffling**: Ensures members from the same group are not re-grouped into the same team when possible.
- **Conflict Avoidance**: Prevents repeated identical team compositions by re-shuffling when necessary.
- **Console Feedback**: Logs assignment success or error messages for traceability.
- **CSV Export**: Save the final team assignments to a CSV file.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/WoongyuChoi/RandTeamMaker.git
   cd RandTeamMaker
   ```

2. Install dependencies:
   Make sure Python 3.7+ is installed. Then install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

4. Or generate an executable:
   ```bash
   pyinstaller --onefile --icon=.\favicon.ico main.py
   ```

## Usage

1. **Enter Groups**: Fill each group box with a list of names (one per line).
2. **Set Team Count**: Choose the desired number of teams from the dropdown.
3. **Generate**: Click **Generate Teams** to auto-assign members.
4. **View Assignment**: The result table will show all teams and their members.
5. **Export**: Click the export button to save the team assignment as a CSV.

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.
