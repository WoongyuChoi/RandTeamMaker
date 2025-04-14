from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QCheckBox,
)
from PyQt5.QtCore import Qt


def init_ui(app_instance):
    layout = QVBoxLayout()

    # 그룹 입력 라벨
    layout.addWidget(QLabel("Enter Groups (one per line, comma-separated):"))
    app_instance.group_input = QTextEdit()
    layout.addWidget(app_instance.group_input)

    # 조 수 선택
    team_layout = QHBoxLayout()
    team_layout.addWidget(QLabel("Number of Teams:"))
    app_instance.team_count_spinbox = QSpinBox()
    app_instance.team_count_spinbox.setMinimum(1)
    app_instance.team_count_spinbox.setMaximum(6)
    team_layout.addWidget(app_instance.team_count_spinbox)
    layout.addLayout(team_layout)

    # 중복 체크
    app_instance.shuffle_checkbox = QCheckBox("Ensure group members are mixed")
    app_instance.shuffle_checkbox.setChecked(True)
    layout.addWidget(app_instance.shuffle_checkbox)

    # 버튼
    app_instance.generate_button = QPushButton("Generate Teams")
    app_instance.generate_button.clicked.connect(app_instance.generate_teams)
    layout.addWidget(app_instance.generate_button)

    # 결과 테이블
    app_instance.result_table = QTableWidget()
    layout.addWidget(app_instance.result_table)

    # 설정
    app_instance.setLayout(layout)
    app_instance.setWindowTitle("RandTeamMaker")
