from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QTextEdit,
    QTableWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTableWidgetItem,
    QSpinBox,
)
from PyQt5.QtCore import Qt


def init_ui(app_instance):
    layout = QVBoxLayout()

    # 팀 수 입력
    team_input_layout = QHBoxLayout()
    team_input_layout.addWidget(QLabel("Number of Teams:"))
    app_instance.team_count_input = QSpinBox()
    app_instance.team_count_input.setMinimum(1)
    app_instance.team_count_input.setMaximum(6)
    app_instance.team_count_input.setValue(2)
    team_input_layout.addWidget(app_instance.team_count_input)
    layout.addLayout(team_input_layout)

    # 그룹 입력
    app_instance.group_inputs = []
    for i in range(3):  # 기본 3개 그룹 (최대 6개까지 확장 가능)
        group_layout = QVBoxLayout()
        label = QLabel(f"Group {i+1} Members (comma or newline separated):")
        group_input = QTextEdit()
        app_instance.group_inputs.append(group_input)
        group_layout.addWidget(label)
        group_layout.addWidget(group_input)
        layout.addLayout(group_layout)

    # 조 짜기 버튼
    button_layout = QHBoxLayout()
    app_instance.generate_button = QPushButton("Generate Teams")
    button_layout.addStretch()
    button_layout.addWidget(app_instance.generate_button)
    button_layout.addStretch()
    layout.addLayout(button_layout)

    # 결과 테이블
    layout.addWidget(QLabel("Generated Teams:"))
    app_instance.result_table = QTableWidget()
    layout.addWidget(app_instance.result_table)

    app_instance.setLayout(layout)
    app_instance.setWindowTitle("RandTeamMaker")
