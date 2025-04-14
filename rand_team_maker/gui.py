from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from rand_team_maker import ui_setup, utils


class RandTeamMakerApp(QWidget):
    def __init__(self):
        super().__init__()
        ui_setup.init_ui(self)

    def log_to_console(self, message):
        ui_setup.log_to_console(self, message)

    def generate_teams(self):
        try:
            num_teams = self.team_spinbox.value()
            if num_teams <= 0:
                self.log_to_console("팀 수는 1 이상이어야 합니다.")
                return

            # 각 그룹 입력 파싱
            group_data = {}
            for idx, input_area in enumerate(self.group_inputs):
                text = input_area.toPlainText()
                group_data[idx] = utils.parse_group_text(text)

            # 전체 인원 확인
            total_members = utils.validate_groups(list(group_data.values()))
            if len(total_members) < num_teams:
                self.log_to_console("팀 수보다 구성원이 더 적습니다.")
                return

            # 팀 배정 (그룹 충돌 방지 포함)
            teams = utils.generate_team_assignments_with_group_shuffle(
                group_data, num_teams
            )

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

            self.log_to_console("팀 구성이 완료되었습니다.")

        except Exception as e:
            self.log_to_console(f"Error: {str(e)}")
