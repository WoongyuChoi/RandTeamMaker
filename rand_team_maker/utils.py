import math
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

def generate_team_assignments_balanced(group_data: dict, num_teams: int, max_retries: int = 500) -> dict:
        """
        Return balanced random teams with per‑group dispersion.
        """
        if num_teams <= 0:
            raise ValueError("num_teams must be positive")

        # 1. Deduplicate & sanitise names per group
        clean_groups = []
        seen_global = set()
        for members in group_data.values():
            cleaned = []
            for m in members:
                m = m.strip()
                if not m or m in seen_global:
                    continue
                cleaned.append(m)
                seen_global.add(m)
            if cleaned:
                clean_groups.append(cleaned)

        total_members = sum(len(g) for g in clean_groups)
        if total_members < num_teams:
            raise ValueError("팀 수가 구성원 수보다 많습니다.")

        # 2. Target team sizes so that |size_i − size_j| ≤ 1
        base, extra = divmod(total_members, num_teams)
        target_sizes = [base + (1 if i < extra else 0) for i in range(num_teams)]

        # 3. Per‑group per‑team cap: ceil(group_size / num_teams)
        group_caps = [math.ceil(len(g) / num_teams) for g in clean_groups]

        def _greedy_allocate() -> dict | None:
            """Greedy round‑robin allocation respecting caps; return None on failure."""
            teams = {i + 1: [] for i in range(num_teams)}
            slots_remaining = target_sizes.copy()  # mutable copy

            # Largest groups first → 더 어려운 걸 먼저 배치
            groups_idx = sorted(range(len(clean_groups)), key=lambda i: len(clean_groups[i]), reverse=True)
            
            # 같은 크기 그룹도 랜덤하게 시도
            random.shuffle(groups_idx)

            for gi in groups_idx:
                members = clean_groups[gi][:]
                random.shuffle(members)
                cap = group_caps[gi]
                team_pointer = 0  # 시작 팀 인덱스(0‑based)

                for mem in members:
                    placed = False
                    for offset in range(num_teams):
                        ti = (team_pointer + offset) % num_teams  # 0‑based 팀 인덱스
                        if slots_remaining[ti] == 0:
                            continue
                        # 같은 그룹원 수 검사
                        same_count = sum(1 for m in teams[ti + 1] if m in clean_groups[gi])
                        if same_count < cap:
                            teams[ti + 1].append(mem)
                            slots_remaining[ti] -= 1
                            team_pointer = (ti + 1) % num_teams
                            placed = True
                            break
                    if not placed:
                        # 캡을 모두 초과. 가장 여유 있는 팀에 강제 배치
                        ti = max(range(num_teams), key=lambda t: slots_remaining[t])
                        if slots_remaining[ti] == 0:
                            return None  # 실패
                        teams[ti + 1].append(mem)
                        slots_remaining[ti] -= 1

            if any(len(teams[i + 1]) != target_sizes[i] for i in range(num_teams)):
                return None
            return teams

        # 4. 시도: Greedy → 실패 시 섞어서 랜덤 재시도(필요 시 시도 횟수 조절)
        for _ in range(20):
            result = _greedy_allocate()
            if result is not None:
                return result
        
        # fallback
        members_all = list(seen_global)
        for _ in range(max_retries):
            random.shuffle(members_all)
            candidate = {i + 1: members_all[i::num_teams] for i in range(num_teams)}

            # 검사 ① 팀 크기 균형
            if any(len(candidate[i + 1]) != target_sizes[i] for i in range(num_teams)):
                continue
            # 검사 ② 그룹 분산(캡)
            ok = True
            for gi, grp in enumerate(clean_groups):
                cap = group_caps[gi]
                grp_set = set(grp)
                for team in candidate.values():
                    if len(grp_set.intersection(team)) > cap:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                return candidate

        raise ValueError("적절한 팀 구성을 찾을 수 없습니다. 제약 조건이 과도하거나 팀 수가 부족합니다.")
