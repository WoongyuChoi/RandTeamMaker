from PyQt5.QtWidgets import (
    QGridLayout,
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

    # 그룹 입력을 가로로 배치 (최대 5개까지 확장 가능)
    app_instance.group_inputs = []
    group_input_layout = QGridLayout()

    for i in range(5):
        group_box = QGroupBox(f"Group {i + 1}")
        group_layout = QVBoxLayout()
        group_text = QTextEdit()
        app_instance.group_inputs.append(group_text)
        group_layout.addWidget(group_text)
        group_box.setLayout(group_layout)
        group_input_layout.addWidget(group_box, 0, i)  # 가로로 배치

    layout.addLayout(group_input_layout)

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
    app_instance.result_table.setMinimumHeight(200)
    layout.addWidget(app_instance.result_table)

    app_instance.setLayout(layout)
    app_instance.setWindowTitle("RandTeamMaker")

    # 화면 해상도에 따른 윈도우 크기 조정
    adjust_window_size(app_instance)
    center(app_instance)


def adjust_window_size(app_instance):
    """해상도에 따라 윈도우 크기를 조정하는 함수"""
    screen_geometry = app_instance.screen().availableGeometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()

    # 기본 비율 설정 (화면 크기의 50%)
    width_ratio = 0.5
    height_ratio = 0.5

    # 전체 화면 크기의 비율로 윈도우 크기 설정
    window_width = int(screen_width * width_ratio)
    window_height = int(screen_height * height_ratio)

    # 최소 크기 설정
    min_width = 800
    min_height = 600

    # 최소 크기보다 작은 경우, 최소 크기로 설정
    window_width = max(window_width, min_width)
    window_height = max(window_height, min_height)

    app_instance.resize(window_width, window_height)


def center(app_instance):
    """화면 중앙에 윈도우를 배치하는 함수"""
    qr = app_instance.frameGeometry()
    cp = app_instance.screen().availableGeometry().center()
    qr.moveCenter(cp)
    app_instance.move(qr.topLeft())


def log_to_console(app_instance, message):
    """콘솔 창에 로그 메시지를 출력하는 함수"""
    app_instance.console_output.append(message)
