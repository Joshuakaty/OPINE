"""FastAPI application for OPINE."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from kraken.dashboard import Dashboard
from kraken.intelligence import OpportunityIntelligence
from kraken.match_explainer import MatchExplainer
from kraken.matcher import OpportunityMatcher
from kraken.profile.user_profile import UserProfile
from kraken.resume import ResumeAnalyzer
from kraken.resume_matcher import ResumeMatcher
from kraken.resume_profile import ResumeProfile
from kraken.schemas.jobs import JobResponse
from kraken.schemas.resume import ResumeAnalysisResponse, ResumeMatch
from kraken.services.database_service import DatabaseService
from kraken.users.service import UserService

app = FastAPI(
    title="OPINE API",
    version="1.1.0",
    description="Opportunity Intelligence Engine API",
)

# ---------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------

service = DatabaseService()
dashboard = Dashboard()

intelligence = OpportunityIntelligence()
matcher = OpportunityMatcher()
explainer = MatchExplainer()

resume_analyzer = ResumeAnalyzer()
resume_matcher = ResumeMatcher()

user_service = UserService()

# ---------------------------------------------------------------------
# Demo User
# ---------------------------------------------------------------------

demo_user = user_service.create_user(
    user_id="1",
    name="Joshua",
    email="joshua@example.com",
)

demo_user.update_resume(
    """
    Python
    FastAPI
    Docker
    PostgreSQL
    """
)

profile = UserProfile(
    name="Joshua",
    skills=["Python", "FastAPI", "Docker"],
    desired_roles=[
        "Backend Engineer",
        "Python Developer",
    ],
    preferred_locations=["Remote"],
    remote_only=True,
    minimum_salary="$120000",
)


class ResumeRequest(BaseModel):
    """Resume analysis request."""

    resume: str


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "OPINE API",
        "status": "running",
        "engine": "Kraken",
    }


@app.post("/refresh")
def refresh_jobs() -> dict[str, int | str]:
    count = service.refresh_and_cache()

    return {
        "status": "success",
        "jobs_collected": count,
    }


@app.post("/resume/analyze", response_model=ResumeAnalysisResponse)
def analyze_resume(request: ResumeRequest) -> ResumeAnalysisResponse:
    skills = resume_analyzer.extract_skills(request.resume)

    opportunities = service.get_cached()

    matches = [
        ResumeMatch(
            title=o.title,
            organization=o.organization,
            resume_match=resume_matcher.match(
                request.resume,
                o,
            ),
        )
        for o in opportunities
    ]

    matches.sort(
        key=lambda m: m.resume_match,
        reverse=True,
    )

    return ResumeAnalysisResponse(
        skills=skills,
        top_matches=matches,
    )


@app.get("/dashboard")
def get_dashboard() -> dict:
    opportunities = service.get_cached()

    return dashboard.build(
        demo_user.resume_profile,
        opportunities,
    )


@app.get("/users/{user_id}/dashboard")
def get_user_dashboard(user_id: str) -> dict:
    """Return a dashboard for a specific user."""

    user = user_service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    opportunities = service.get_cached()

    return dashboard.build(
        user.resume_profile,
        opportunities,
    )


@app.get("/jobs", response_model=list[JobResponse])
def get_jobs(
    q: str | None = None,
    location: str | None = None,
    company: str | None = None,
    min_score: int | None = None,
) -> list[JobResponse]:

    opportunities = service.get_cached()

    if q:
        query = q.lower()

        opportunities = [
            o
            for o in opportunities
            if query in o.title.lower()
            or query in o.description.lower()
            or query in o.organization.lower()
        ]

    if location:
        opportunities = [
            o
            for o in opportunities
            if location.lower() in o.location.lower()
        ]

    if company:
        opportunities = [
            o
            for o in opportunities
            if company.lower() in o.organization.lower()
        ]

    if min_score is not None:
        opportunities = [
            o
            for o in opportunities
            if o.score >= min_score
        ]

    return [
        JobResponse(
            id=o.id,
            title=o.title,
            organization=o.organization,
            location=o.location,
            salary=o.salary,
            opportunity_score=o.score,
            personal_match=matcher.match(
                profile,
                o,
            ),
            source=o.source,
            insights=intelligence.analyze(o),
            why_this_matches=explainer.explain(
                profile,
                o,
            ),
        )
        for o in opportunities
    ]