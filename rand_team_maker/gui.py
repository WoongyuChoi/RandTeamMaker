import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
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

            # 그래프 출력
            self._draw_distribution_chart(teams, group_data)

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
        """모든 입력·출력 위젯을 초기 상태로 되돌립니다."""
        try:
            # 1) 그룹 입력 칸 비우기
            for input_area in self.group_inputs:
                input_area.clear()

            # 2) 결과 테이블 초기화
            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(0)
            self.result_table.clear()

            # 3) 그래프 초기화
            self.figure.clear()
            self.canvas.draw_idle()

            # 4) 팀 수 스핀박스 기본값
            self.team_spinbox.setValue(1)

            # 5) 콘솔 로그 클리어
            self.console_output.clear()
        except Exception as e:
            self.log_to_console(f"초기화 오류: {str(e)}")
    
    def _draw_distribution_chart(self, teams: dict, group_data: dict) -> None:
        """팀별 그룹 비율을 수평 스택 막대 그래프로 표시."""
        try:
            fig = self.figure
            fig.clear()
            ax = fig.add_subplot(111)

            # 1) 이름 → 그룹명 매핑
            name_to_group = {
                name.strip(): f"Group {idx+1}"
                for idx, members in group_data.items()
                for name in members
            }

            team_ids = sorted(teams.keys())
            groups = sorted({name_to_group[n] for lst in teams.values() for n in lst})

            # 2) 색상 팔레트 지정
            cmap = plt.get_cmap("tab10")
            color_map = {g: cmap(i) for i, g in enumerate(groups)}
            
            # 3) 백분율 계산
            widths = {g: [0] * len(team_ids) for g in groups}
            for col, tid in enumerate(team_ids):
                cnt = Counter(name_to_group[n] for n in teams[tid])
                total = len(teams[tid])
                for g in groups:
                    widths[g][col] = round((cnt[g] / total) * 100, 1)  # 소수점 1자리
            
           # 4) 스택 막대 + 내부 라벨
            left = [0] * len(team_ids)
            for g in groups:
                w = widths[g]
                bars = ax.barh(team_ids, w, left=left, color=color_map[g])
                # 새로 추가된 내부 백분율 텍스트
                for bar, pct in zip(bars, w):
                    if pct > 0:
                        ax.text(
                            bar.get_x() + bar.get_width() / 2,
                            bar.get_y() + bar.get_height() / 2,
                            f"{g} {pct:.0f}%",
                            ha="center", va="center",
                            fontsize=8, color="white"
                        )
                left = [l + dw for l, dw in zip(left, w)]
            # 5) 불필요한 축·제목 제거
            # ax.set_xlabel("Percentage (%)")
            # ax.set_ylabel("Team")
            ax.set_yticks(team_ids)
            ax.set_yticklabels([f"Team {tid}" for tid in team_ids], fontsize=8)
            ax.invert_yaxis()
            
            # 0~100 % 고정
            ax.set_xlim(0, 100)
            # x축은 숨기고 y축만 살림
            for spine in ("top", "right", "bottom"):
                ax.spines[spine].set_visible(False)
            ax.tick_params(axis="x", length=0, labelbottom=False)

            # ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=len(groups))
            # ax.set_title("Group Composition per Team")
            # 축/눈금/프레임 한꺼번에 숨김
            # ax.axis("off")
            # 여백 최소화
            fig.tight_layout(pad=0.3)

            self.canvas.draw_idle()
        except Exception as e:
            self.log_to_console(f"그래프 생성 오류: {str(e)}")