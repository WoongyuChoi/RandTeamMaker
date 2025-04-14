import random


def shuffle_and_divide(members: list[str], num_teams: int) -> list[list[str]]:
    """
    주어진 멤버 리스트를 무작위로 섞고, 지정된 수의 팀으로 나눕니다.
    """
    if num_teams <= 0:
        raise ValueError("Number of teams must be greater than 0")

    shuffled = members[:]
    random.shuffle(shuffled)
    teams = [[] for _ in range(num_teams)]

    for idx, member in enumerate(shuffled):
        teams[idx % num_teams].append(member)

    return teams


def validate_groups(groups: list[list[str]]) -> list[str]:
    """
    그룹 리스트를 하나의 멤버 리스트로 통합하며 공백이나 빈 항목 제거
    """
    all_members = []
    for group in groups:
        all_members.extend([member.strip() for member in group if member.strip()])
    return all_members


def parse_group_text(group_text: str) -> list[str]:
    """
    QTextEdit에 입력된 그룹 텍스트를 줄바꿈 기준으로 분리하여 리스트로 반환합니다.
    """
    return [line.strip() for line in group_text.strip().splitlines() if line.strip()]


def generate_team_assignments(group_data: dict, num_teams: int) -> dict:
    """그룹별 데이터를 받아 전체 인원을 랜덤하게 팀으로 분배합니다."""
    all_members = []

    for members in group_data.values():
        all_members.extend([m.strip() for m in members if m.strip()])

    if num_teams <= 0:
        raise ValueError("Number of teams must be greater than 0")

    random.shuffle(all_members)

    teams = {i + 1: [] for i in range(num_teams)}
    for idx, member in enumerate(all_members):
        team_number = (idx % num_teams) + 1
        teams[team_number].append(member)

    return teams


def generate_team_assignments_with_group_shuffle(
    group_data: dict, num_teams: int
) -> dict:
    """
    그룹별 데이터를 받아 전체 인원을 랜덤하게 팀으로 분배하되,
    동일 그룹 멤버들이 가능한 서로 다른 팀에 배정되도록 하고,
    중복된 멤버는 한 번만 배정되도록 처리합니다.
    """
    teams = {i + 1: [] for i in range(num_teams)}
    assigned_members = set()
    unique_members = []

    # 중복 없는 멤버 수집
    for members in group_data.values():
        for member in members:
            name = member.strip()
            if name and name not in assigned_members:
                unique_members.append(name)
                assigned_members.add(name)

    random.shuffle(unique_members)

    for idx, member in enumerate(unique_members):
        team_id = (idx % num_teams) + 1
        teams[team_id].append(member)

    return teams
