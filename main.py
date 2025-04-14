import sys
import os
from PyQt5.QtWidgets import QApplication
from rand_team_maker.gui import RandTeamMakerApp

# 현재 디렉터리를 Python 모듈 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    app = QApplication(sys.argv)
    window = RandTeamMakerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
