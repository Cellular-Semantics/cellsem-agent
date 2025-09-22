# deepresearch_wrapper.py
from dataclasses import dataclass
from typing import Optional, Dict, Any
import time
import httpx
from openai import OpenAI
from openai._exceptions import APIError, RateLimitError, APIStatusError

DEEP_RESEARCH_MODEL = "o4-mini-deep-research-2025-06-26"  # or o3-deep-research-2025-06-26

@dataclass
class DeepResearchResult:
    success: bool
    status: str
    response_id: Optional[str]
    output_text: Optional[str]
    error_type: Optional[str]
    error_message: Optional[str]
    started_at: float
    completed_at: float
    elapsed_sec: float
    raw_response: Optional[Any]

class DeepResearchClient:
    def __init__(self, api_key: Optional[str] = None, timeout: float = 600.0, base_url: Optional[str] = None):
        """
        timeout: total request timeout (Deep Research can take minutes).
        base_url: override for OpenAI-compatible endpoints if needed.
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)

    def run(
        self,
        user_query: str,
        system_message: str = "You are a meticulous research analyst. Produce a structured, citation-backed report.",
        model: str = DEEP_RESEARCH_MODEL,
        tools: Optional[list] = None,
        reasoning: Optional[Dict[str, Any]] = None,
        background: bool = True,
        poll_interval: float = 5.0,
        max_wait_sec: float = 1800.0,
    ) -> DeepResearchResult:
        """
        background=True lets the API do long work server-side; we then poll by id.
        """
        started = time.time()
        if tools is None:
            tools = [{"type": "web_search_preview"}]
        if reasoning is None:
            reasoning = {"summary": "auto"}

        try:
            # Kick off the task
            resp = self.client.responses.create(
                model=model,
                input=[
                    {"role": "developer", "content": [{"type": "input_text", "text": system_message}]},
                    {"role": "user", "content": [{"type": "input_text", "text": user_query}]},
                ],
                reasoning=reasoning,
                tools=tools,
                # Background mode is supported by the Deep Research models via Responses API
                background=background,
            )
            resp_id = getattr(resp, "id", None)
            status = getattr(resp, "status", "in_progress")

            # If not background, many servers will return the finished object directly
            if not background and status in ("completed", "failed", "cancelled"):
                output_text = _extract_output_text(resp)
                done = time.time()
                return DeepResearchResult(
                    success=(status == "completed"),
                    status=status,
                    response_id=resp_id,
                    output_text=output_text,
                    error_type=None if status == "completed" else "DeepResearchFailed",
                    error_message=None if status == "completed" else "Deep Research did not complete.",
                    started_at=started,
                    completed_at=done,
                    elapsed_sec=done - started,
                    raw_response=resp,
                )

            # Poll for completion
            deadline = started + max_wait_sec
            while time.time() < deadline:
                cur = self.client.responses.retrieve(resp_id)
                status = getattr(cur, "status", "in_progress")
                if status in ("completed", "failed", "cancelled"):
                    output_text = _extract_output_text(cur)
                    done = time.time()
                    return DeepResearchResult(
                        success=(status == "completed"),
                        status=status,
                        response_id=resp_id,
                        output_text=output_text,
                        error_type=None if status == "completed" else "DeepResearchFailed",
                        error_message=None if status == "completed" else "Deep Research did not complete.",
                        started_at=started,
                        completed_at=done,
                        elapsed_sec=done - started,
                        raw_response=cur,
                    )
                time.sleep(poll_interval)

            # timed out locally
            done = time.time()
            return DeepResearchResult(
                success=False,
                status="client_timeout",
                response_id=resp_id,
                output_text=None,
                error_type="TimeoutError",
                error_message=f"Polling exceeded {max_wait_sec:.0f}s without completion.",
                started_at=started,
                completed_at=done,
                elapsed_sec=done - started,
                raw_response=None,
            )

        except (httpx.TimeoutException,) as e:
            done = time.time()
            return DeepResearchResult(
                success=False,
                status="http_timeout",
                response_id=None,
                output_text=None,
                error_type="httpx.TimeoutException",
                error_message=str(e),
                started_at=started,
                completed_at=done,
                elapsed_sec=done - started,
                raw_response=None,
            )
        except (RateLimitError,) as e:
            done = time.time()
            return DeepResearchResult(
                success=False,
                status="rate_limited",
                response_id=None,
                output_text=None,
                error_type="RateLimitError",
                error_message=str(e),
                started_at=started,
                completed_at=done,
                elapsed_sec=done - started,
                raw_response=getattr(e, "response", None),
            )
        except (APIStatusError, APIError) as e:
            done = time.time()
            return DeepResearchResult(
                success=False,
                status="api_error",
                response_id=None,
                output_text=None,
                error_type=e.__class__.__name__,
                error_message=str(e),
                started_at=started,
                completed_at=done,
                elapsed_sec=done - started,
                raw_response=getattr(e, "response", None),
            )

def _extract_output_text(resp) -> Optional[str]:
    try:
        # Deep Research returns the final report at the end of response.output
        return resp.output[-1].content[0].text
    except Exception:
        return None
