import random
from PyQt5.QtWidgets import (
    QWidget,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
)
from rand_team_maker import ui_setup


class RandTeamMakerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.group_inputs = []
        self.num_teams_input = None
        self.generate_button = None
        self.team_table = None

        ui_setup.init_ui(self)

    def generate_teams(self):
        all_members = []
        group_data = []

        # 각 그룹별 멤버 수집
        for input_widget in self.group_inputs:
            members = [
                m.strip() for m in input_widget.toPlainText().splitlines() if m.strip()
            ]
            if members:
                group_data.append(members)
                all_members.extend(members)

        try:
            num_teams = int(self.num_teams_input.toPlainText().strip())
            if num_teams <= 0:
                raise ValueError
        except ValueError:
            self.display_result([["Please enter a valid number of teams."]])
            return

        if not all_members or num_teams > len(all_members):
            self.display_result([["Not enough members to form teams."]])
            return

        # 섞되 그룹 간 멤버들이 나뉘도록 처리
        assigned = [[] for _ in range(num_teams)]

        for group in group_data:
            shuffled = group.copy()
            random.shuffle(shuffled)
            for idx, member in enumerate(shuffled):
                assigned[idx % num_teams].append(member)

        self.display_result(assigned)

    def display_result(self, team_data):
        self.team_table.clear()
        self.team_table.setRowCount(max(len(t) for t in team_data))
        self.team_table.setColumnCount(len(team_data))

        for col, team in enumerate(team_data):
            self.team_table.setHorizontalHeaderItem(
                col, QTableWidgetItem(f"Team {col + 1}")
            )
            for row, member in enumerate(team):
                self.team_table.setItem(row, col, QTableWidgetItem(member))
