from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from rand_team_maker import ui_setup, utils


class RandTeamMakerApp(QWidget):
    def __init__(self):
        super().__init__()
        ui_setup.init_ui(self)
        self.generate_button.clicked.connect(self.generate_teams)

    def generate_teams(self):
        try:
            num_teams = self.team_spinbox.value()
            if num_teams <= 0:
                self.console_output.append("Team count must be greater than 0.")
                return

            # 각 그룹 입력 파싱
            group_data = {}
            for idx, input_area in enumerate(self.group_inputs):
                text = input_area.toPlainText()
                group_data[idx] = utils.parse_group_text(text)

            # 전체 인원 확인
            total_members = utils.validate_groups(list(group_data.values()))
            if len(total_members) < num_teams:
                self.console_output.append(
                    "Members are fewer than the number of teams."
                )
                return

            # 팀 배정
            teams = utils.generate_team_assignments(group_data, num_teams)

            # 테이블 출력
            max_team_size = max(len(team) for team in teams.values())
            self.result_table.setRowCount(max_team_size)
            self.result_table.setColumnCount(num_teams)
            self.result_table.setHorizontalHeaderLabels(
                [f"Team {i}" for i in teams.keys()]
            )

            for col, team in teams.items():
                for row, member in enumerate(team):
                    item = QTableWidgetItem(member)
                    self.result_table.setItem(row, col - 1, item)

            self.console_output.append("Team generation complete.")

        except Exception as e:
            self.console_output.append(f"Error: {str(e)}")
