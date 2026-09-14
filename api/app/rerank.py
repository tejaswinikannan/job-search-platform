from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)


class RelevantJobs(BaseModel):
    job_ids: list[int] = Field(
        description="IDs of the candidate jobs that are a genuinely good match for the search query, "
                    "ordered from most to least relevant. Exclude any candidate that is not a real match, "
                    "even if it shares some vocabulary with the query."
    )


_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
_structured_llm = _llm.with_structured_output(RelevantJobs)


def rerank_jobs(query: str, candidates: list[tuple[int, str, str]]) -> list[int]:
    listing = "\n".join(f"id={job_id}: {title} — {description}" for job_id, title, description in candidates)
    prompt = (
        f"Search query: {query!r}\n\n"
        f"Candidate jobs:\n{listing}\n\n"
        "Which of these candidates are a genuinely good match for the search query?"
    )
    result = _structured_llm.invoke(prompt)
    return result.job_ids
