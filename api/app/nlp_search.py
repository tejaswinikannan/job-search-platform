from typing import Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv(override=True)


class JobSearchFilters(BaseModel):
    title_keywords: list[str] = Field(
        default_factory=list,
        description="Words describing the role, domain, or seniority mentioned in the query "
                     "(e.g. 'database', 'senior', 'frontend') — matched against the job title and description",
    )
    location: Optional[str] = Field(
        default=None,
        description="City, state, or region mentioned in the query, e.g. 'New York', 'Boston'",
    )
    job_type: Optional[str] = Field(
        default=None,
        description="Employment type if explicitly mentioned: Full-Time, Part-Time, Remote, or Internship",
    )
    company_keywords: list[str] = Field(
        default_factory=list,
        description="Words describing company culture, values, or work environment mentioned in the query "
                     "(e.g. 'collaborative', 'innovative', 'remote-friendly') — matched against the company description",
    )


_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
_structured_llm = _llm.with_structured_output(JobSearchFilters)


def parse_query(query: str) -> JobSearchFilters:
    return _structured_llm.invoke(query)
