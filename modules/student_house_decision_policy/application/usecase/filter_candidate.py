from __future__ import annotations

from modules.finder_request.application.port.finder_request_repository_port import (
    FinderRequestRepositoryPort,
)
from modules.student_house_decision_policy.application.dto.candidate_filter_dto import (
    FilterCandidateCommand,
    FilterCandidateCriteria,
    FilterCandidateResult,
    ObservationPriceFeatures,
)
from modules.student_house_decision_policy.application.port_in.filter_candidate_port import (
    FilterCandidatePort,
)
from modules.student_house_decision_policy.application.port_out.house_platform_candidate_port import (
    HousePlatformCandidateReadPort,
)
from modules.student_house_decision_policy.domain.value_object.budget_filter_policy import (
    BudgetFilterPolicy,
)


class FilterCandidateService(FilterCandidatePort):
    """finder_request 조건으로 후보 매물을 선별한다.

    여유율 변경은 BudgetFilterPolicy 주입으로 조정한다.
    """

    def __init__(
        self,
        finder_request_repo: FinderRequestRepositoryPort,
        house_platform_repo: HousePlatformCandidateReadPort,
        observation_repo,
        policy: BudgetFilterPolicy | None = None,
    ):
        self.finder_request_repo = finder_request_repo
        self.house_platform_repo = house_platform_repo
        self.observation_repo = observation_repo
        self.policy = policy or BudgetFilterPolicy()

    def execute(self, command: FilterCandidateCommand) -> FilterCandidateResult:
        """finder_request 기준으로 후보를 조회한다."""
        request = self.finder_request_repo.find_by_id(
            command.finder_request_id
        )
        if not request:
            criteria = FilterCandidateCriteria(
                max_deposit_limit=None,
                max_rent_limit=None,
                budget_margin_ratio=self.policy.budget_margin_ratio,
            )
            return FilterCandidateResult(
                finder_request_id=command.finder_request_id,
                criteria=criteria,
                candidates=[],
                message="finder_request가 존재하지 않습니다.",
            )

        max_deposit_limit = self.policy.clamp_budget(request.max_deposit)
        max_rent_limit = self.policy.clamp_budget(request.max_rent)
        criteria = FilterCandidateCriteria(
            max_deposit_limit=max_deposit_limit,
            max_rent_limit=max_rent_limit,
            budget_margin_ratio=self.policy.budget_margin_ratio,
            price_type=request.price_type,
            preferred_region=request.preferred_region,
            house_type=request.house_type,
            additional_condition=request.additional_condition,
        )
        # TODO: finder_request에 필수 옵션/이동 제한/리스크 허용 컬럼이 준비되면 criteria로 확장한다.

        if max_deposit_limit is None and max_rent_limit is None:
            return FilterCandidateResult(
                finder_request_id=command.finder_request_id,
                criteria=criteria,
                candidates=[],
                message="예산 조건이 없어 후보를 선별할 수 없습니다.",
            )

        candidates = self._fetch_candidates(criteria)
        candidates = self._filter_by_observation(criteria, candidates)
        # TODO: 필수 옵션 조건이 준비되면 후보를 추가 필터링한다.
        # TODO: 이동 제한(거리) 조건이 준비되면 후보를 추가 필터링한다.
        # TODO: 리스크 허용 조건이 준비되면 후보를 추가 필터링한다.

        # TODO: additional_condition 파싱 규칙이 확정되면 필터 조건에 반영한다.
        return FilterCandidateResult(
            finder_request_id=command.finder_request_id,
            criteria=criteria,
            candidates=candidates,
            message=None,
        )

    def _fetch_candidates(
        self,
        criteria: FilterCandidateCriteria,
    ) -> list:
        """finder_request 기본 조건으로 후보를 조회한다."""
        if criteria.max_deposit_limit is None and criteria.max_rent_limit is None:
            return []
        return list(self.house_platform_repo.fetch_candidates(criteria))

    def _filter_by_observation(
        self,
        criteria: FilterCandidateCriteria,
        candidates: list,
    ) -> list:
        """관측된 가격 지표(입주비/월비용)로 후보를 필터링한다."""
        filtered = []
        for candidate in candidates:
            observation = self._fetch_observation_price(candidate)
            if not observation:
                # TODO: 관측값 미존재 시 허용/제외 정책을 확정한다.
                continue

            if (
                criteria.max_deposit_limit is not None
                and observation.estimated_move_in_cost
                > criteria.max_deposit_limit
            ):
                continue
            if (
                criteria.max_rent_limit is not None
                and observation.monthly_cost_est > criteria.max_rent_limit
            ):
                continue
            filtered.append(candidate)
        return filtered

    def _fetch_observation_price(self, candidate):
        """관측 저장소에서 가격 지표를 조회한다."""
        if not candidate.snapshot_id:
            # TODO: 관측값이 없는 매물에 대한 처리 정책을 확정한다.
            return None
        observation = None
        if hasattr(self.observation_repo, "find_latest_by_house_id"):
            observation = self.observation_repo.find_latest_by_house_id(
                candidate.house_platform_id
            )
        elif hasattr(self.observation_repo, "find_latest_by_platform_id"):
            observation = self.observation_repo.find_latest_by_platform_id(
                candidate.house_platform_id
            )
        elif hasattr(self.observation_repo, "fetch_price_features"):
            observation = self.observation_repo.fetch_price_features(
                candidate.house_platform_id,
                candidate.snapshot_id,
            )

        if not observation:
            return None

        if hasattr(observation, "snapshot_id") and (
            observation.snapshot_id != candidate.snapshot_id
        ):
            return None

        if hasattr(observation, "가격_관측치"):
            가격_관측치 = observation.가격_관측치
            return ObservationPriceFeatures(
                house_platform_id=candidate.house_platform_id,
                snapshot_id=observation.snapshot_id,
                estimated_move_in_cost=가격_관측치.예상_입주비용,
                monthly_cost_est=가격_관측치.월_비용_추정,
                price_percentile=가격_관측치.가격_백분위,
                price_zscore=가격_관측치.가격_z점수,
                price_burden_nonlinear=가격_관측치.가격_부담_비선형,
            )

        if hasattr(observation, "estimated_move_in_cost"):
            return observation

        # TODO: 관측 저장소 응답 타입이 확정되면 분기 처리를 단순화한다.
        return None
