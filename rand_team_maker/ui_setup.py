from PyQt5.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QSpinBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QGroupBox,
)
from PyQt5.QtCore import Qt


def init_ui(app_instance):
    layout = QVBoxLayout()

    # 팀 수 설정
    team_count_layout = QHBoxLayout()
    team_count_layout.addWidget(QLabel("Number of Teams:"))
    app_instance.team_spinbox = QSpinBox()
    app_instance.team_spinbox.setMinimum(1)
    app_instance.team_spinbox.setMaximum(6)
    team_count_layout.addWidget(app_instance.team_spinbox)
    layout.addLayout(team_count_layout)

    # 그룹 입력
    app_instance.group_inputs = []
    for i in range(3):  # 최대 그룹 3개로 시작 (필요시 확장 가능)
        group_box = QGroupBox(f"Group {i + 1}")
        group_layout = QVBoxLayout()
        group_text = QTextEdit()
        app_instance.group_inputs.append(group_text)
        group_layout.addWidget(group_text)
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

    # 팀 배정 버튼
    app_instance.generate_button = QPushButton("Generate Teams")
    app_instance.generate_button.clicked.connect(app_instance.generate_teams)
    layout.addWidget(app_instance.generate_button)

    # 콘솔 출력 영역
    app_instance.console_output = QTextEdit()
    app_instance.console_output.setReadOnly(True)
    app_instance.console_output.setMaximumHeight(100)
    layout.addWidget(QLabel("Console Output:"))
    layout.addWidget(app_instance.console_output)

    # 결과 출력 테이블
    app_instance.result_table = QTableWidget()
    layout.addWidget(QLabel("Team Assignments:"))
    layout.addWidget(app_instance.result_table)

    app_instance.setLayout(layout)
    app_instance.setWindowTitle("RandTeamMaker")
