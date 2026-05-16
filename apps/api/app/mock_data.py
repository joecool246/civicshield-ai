from app.models import Incident, Source


OFFICIAL_SOURCES = [
    Source(
        title="Indiana Voters Portal",
        url="https://indianavoters.in.gov/",
        publisher="Indiana Secretary of State",
    ),
    Source(
        title="Vote.gov Indiana Voting Guide",
        url="https://vote.gov/register/indiana",
        publisher="U.S. General Services Administration",
    ),
]


INCIDENTS = [
    Incident(
        id="inc-001",
        title="Unverified post claims polling places changed countywide",
        incident_type="False voting information",
        location="Indiana",
        status="unconfirmed",
        risk_level="high",
        summary=(
            "A social post claims polling locations changed across an entire county. "
            "The mock review found no official confirmation in this Phase 1 dataset."
        ),
        evidence=[
            "Claim names no election office source.",
            "Users should verify polling places through official election portals.",
        ],
        sources=OFFICIAL_SOURCES,
    ),
    Incident(
        id="inc-002",
        title="AI disclosure unclear on political ad screenshot",
        incident_type="AI-generated political ad",
        location="Indiana",
        status="missing_context",
        risk_level="medium",
        summary=(
            "A circulated screenshot appears to be political advertising, but sponsor "
            "and AI disclosure details are not visible in the cropped image."
        ),
        evidence=[
            "The mock item lacks a sponsor field.",
            "No original ad library record is included in the submission.",
        ],
        sources=[
            Source(
                title="Political Advertising Disclaimers",
                url="https://www.fec.gov/help-candidates-and-committees/advertising-and-disclaimers/",
                publisher="Federal Election Commission",
            )
        ],
    ),
    Incident(
        id="inc-003",
        title="Edited candidate quote missing original context",
        incident_type="Misleading policy claim",
        location="Indiana",
        status="missing_context",
        risk_level="medium",
        summary=(
            "A shortened quote is presented as a full policy position. The mock review "
            "flags it for context rather than making a candidate judgment."
        ),
        evidence=[
            "The submitted text omits date, venue, and full transcript.",
            "A complete source would be needed before stronger verification.",
        ],
        sources=[],
    ),
]
