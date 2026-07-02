"""FastAPI application for OPINE."""

from fastapi import FastAPI
from pydantic import BaseModel

from kraken.intelligence import OpportunityIntelligence
from kraken.match_explainer import MatchExplainer
from kraken.matcher import OpportunityMatcher
from kraken.profile.user_profile import UserProfile
from kraken.resume import ResumeAnalyzer
from kraken.resume_matcher import ResumeMatcher
from kraken.schemas.jobs import JobResponse
from kraken.schemas.resume import ResumeAnalysisResponse, ResumeMatch
from kraken.services.database_service import DatabaseService

app = FastAPI(
    title="OPINE API",
    version="0.9.1",
    description="Opportunity Intelligence Engine API",
)

service = DatabaseService()
intelligence = OpportunityIntelligence()
matcher = OpportunityMatcher()
explainer = MatchExplainer()
resume_analyzer = ResumeAnalyzer()
resume_matcher = ResumeMatcher()


class ResumeRequest(BaseModel):
    """Resume analysis request."""

    resume: str


profile = UserProfile(
    name="Default User",
    skills=["Python", "FastAPI", "Docker"],
    desired_roles=["Backend Engineer", "Python Developer"],
    preferred_locations=["Remote"],
    remote_only=True,
    minimum_salary="$120000",
)


@app.get("/")
def root() -> dict[str, str]:
    """Health endpoint."""
    return {
        "name": "OPINE API",
        "status": "running",
        "engine": "Kraken",
    }


@app.post("/refresh")
def refresh_jobs() -> dict[str, int | str]:
    """Refresh the local opportunity database."""

    count = service.refresh_and_cache()

    return {
        "status": "success",
        "jobs_collected": count,
    }


@app.post("/resume/analyze", response_model=ResumeAnalysisResponse)
def analyze_resume(request: ResumeRequest) -> ResumeAnalysisResponse:
    """Analyze a resume and rank opportunities."""

    skills = resume_analyzer.extract_skills(request.resume)

    opportunities = service.get_cached()

    matches = [
        ResumeMatch(
            title=opportunity.title,
            organization=opportunity.organization,
            resume_match=resume_matcher.match(
                request.resume,
                opportunity,
            ),
        )
        for opportunity in opportunities
    ]

    matches.sort(
        key=lambda item: item.resume_match,
        reverse=True,
    )

    return ResumeAnalysisResponse(
        skills=skills,
        top_matches=matches,
    )


@app.get("/jobs", response_model=list[JobResponse])
def get_jobs(
    q: str | None = None,
    location: str | None = None,
    company: str | None = None,
    min_score: int | None = None,
) -> list[JobResponse]:
    """Return cached ranked opportunities."""

    opportunities = service.get_cached()

    if q:
        query = q.lower()
        opportunities = [
            opportunity
            for opportunity in opportunities
            if query in opportunity.title.lower()
            or query in opportunity.description.lower()
            or query in opportunity.organization.lower()
        ]

    if location:
        opportunities = [
            opportunity
            for opportunity in opportunities
            if location.lower() in opportunity.location.lower()
        ]

    if company:
        opportunities = [
            opportunity
            for opportunity in opportunities
            if company.lower() in opportunity.organization.lower()
        ]

    if min_score is not None:
        opportunities = [
            opportunity
            for opportunity in opportunities
            if opportunity.score >= min_score
        ]

    return [
        JobResponse(
            id=opportunity.id,
            title=opportunity.title,
            organization=opportunity.organization,
            location=opportunity.location,
            salary=opportunity.salary,
            opportunity_score=opportunity.score,
            personal_match=matcher.match(profile, opportunity),
            source=opportunity.source,
            insights=intelligence.analyze(opportunity),
            why_this_matches=explainer.explain(profile, opportunity),
        )
        for opportunity in opportunities
    ]