import pandas as pd
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QFileDialog
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
            
            # 기존 출력 테이블 초기화
            self.result_table.clear()

            # 팀 배정
            teams = utils.generate_team_assignments_balanced(group_data, num_teams)

            # 테이블 출력
            max_team_size = max(len(team) for team in teams.values())
            self.result_table.setRowCount(max_team_size)
            self.result_table.setColumnCount(num_teams)
            self.result_table.setHorizontalHeaderLabels([f"Team {i}" for i in teams.keys()])

            for col, team in teams.items():
                for row, member in enumerate(team):
                    item = QTableWidgetItem(member)
                    self.result_table.setItem(row, col - 1, item)

            self.log_to_console("팀 구성이 완료되었습니다.")
        except Exception as e:
            self.log_to_console(f"Error: {str(e)}")
    
    def export_csv(self):
        try:
            row_count = self.result_table.rowCount()
            col_count = self.result_table.columnCount()

            if row_count == 0 or col_count == 0:
                self.log_to_console("내보낼 데이터가 없습니다.")
                return

            # QTableWidget → DataFrame 변환
            data = []
            for row in range(row_count):
                row_data = []
                for col in range(col_count):
                    item = self.result_table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)

            headers = [self.result_table.horizontalHeaderItem(i).text() for i in range(col_count)]
            df = pd.DataFrame(data, columns=headers)

            # 파일 저장
            file_name, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv);;All Files (*)")
            if file_name:
                df.to_csv(file_name, index=False)
                self.log_to_console(f"CSV 파일로 내보내기 완료: {file_name}")
        except Exception as e:
            self.log_to_console(f"CSV 내보내기 오류: {str(e)}")
    
    def reset_ui(self) -> None:
        try:
            """모든 입력·출력 위젯을 초기 상태로 되돌립니다."""
            # 1) 그룹 입력 칸 비우기
            for input_area in self.group_inputs:
                input_area.clear()

            # 2) 결과 테이블 초기화
            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(0)
            self.result_table.clear()

            # 3) 팀 수 스핀박스 기본값
            self.team_spinbox.setValue(1)  # 필요 없으면 삭제

            # 4) 콘솔 로그 클리어
            self.console_output.clear()
        except Exception as e:
            self.log_to_console(f"초기화 오류: {str(e)}")
