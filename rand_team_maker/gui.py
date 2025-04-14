import random
import pandas as pd
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from rand_team_maker import ui_setup


class RandTeamMakerApp(QWidget):
    def __init__(self):
        super().__init__()
        ui_setup.init_ui(self)
        self.generate_button.clicked.connect(self.generate_teams)

    def generate_teams(self):
        try:
            num_teams = int(self.team_count_input.text())
            if num_teams <= 0:
                self.console_output.append("Team count must be greater than 0.")
                return

            # 그룹별 입력 수집
            all_members = []
            for input_area in self.group_inputs:
                text = input_area.toPlainText()
                members = [line.strip() for line in text.splitlines() if line.strip()]
                all_members.append(members)

            # 전체 구성원 통합 및 중복 제거 없이 유지
            flat_members = [member for group in all_members for member in group]
            if len(flat_members) < num_teams:
                self.console_output.append(
                    "Members are fewer than the number of teams."
                )
                return

            # 그룹 간 멤버가 동일하면 섞기 방지용으로 그룹 정보를 유지하면서 분리
            group_indices = [i for i, group in enumerate(all_members) for _ in group]
            combined = list(zip(flat_members, group_indices))

            random.shuffle(combined)

            # 그룹이 섞이도록 팀에 분배
            teams = [[] for _ in range(num_teams)]
            team_indices = list(range(num_teams))
            group_map = {}
            for member, group_idx in combined:
                random.shuffle(team_indices)
                for idx in team_indices:
                    if idx not in group_map.get(group_idx, set()):
                        teams[idx].append(member)
                        group_map.setdefault(group_idx, set()).add(idx)
                        break
                else:
                    # fallback: 아무 데나 넣기
                    teams[random.choice(team_indices)].append(member)

            # 출력 테이블 세팅
            max_team_size = max(len(team) for team in teams)
            self.result_table.setRowCount(max_team_size)
            self.result_table.setColumnCount(num_teams)
            self.result_table.setHorizontalHeaderLabels(
                [f"Team {i+1}" for i in range(num_teams)]
            )

            for col, team in enumerate(teams):
                for row, member in enumerate(team):
                    item = QTableWidgetItem(member)
                    self.result_table.setItem(row, col, item)

            self.console_output.append("Team generation complete.")
        except Exception as e:
            self.console_output.append(f"Error: {str(e)}")
