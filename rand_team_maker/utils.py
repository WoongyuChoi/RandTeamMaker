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


def generate_team_assignments_with_group_shuffle(group_data: dict, num_teams: int) -> dict:
    """
    그룹별 멤버를 무작위로 섞고, 팀 내에 기존 그룹과 동일한 멤버 구성이 들어가지 않도록 팀을 나눕니다.
    또한, 전체 멤버 중 중복되는 이름은 한 번만 배정되도록 보장합니다.
    """

    # 중복 제거된 전체 멤버 수집
    seen = set()
    all_members = []
    for group in group_data.values():
        for member in group:
            name = member.strip()
            if name and name not in seen:
                all_members.append(name)
                seen.add(name)

    # 필터링되지 않은 모든 그룹을 집합으로 저장 (2명 이상)
    original_groups = [set([m.strip() for m in group if m.strip()])
                       for group in group_data.values() if len(group) > 1]

    for _ in range(100):  # 최대 100번 재시도
        random.shuffle(all_members)
        teams = {i + 1: [] for i in range(num_teams)}

        for idx, member in enumerate(all_members):
            team_id = (idx % num_teams) + 1
            teams[team_id].append(member)

        # 팀과 기존 그룹이 완전히 일치하는 경우가 있는지 검사
        team_sets = [set(team) for team in teams.values()]
        has_conflict = any(team_set in original_groups for team_set in team_sets)

        if not has_conflict:
            return teams

    raise ValueError("적절한 팀 구성을 찾을 수 없습니다. 그룹 구성이 너무 고정되어 있거나 팀 수가 부족합니다.")
