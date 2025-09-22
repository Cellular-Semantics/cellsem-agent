# simple_response_wrapper.py
from dataclasses import dataclass
from typing import Optional, Dict, Any
import time, httpx
from openai import OpenAI
from openai._exceptions import APIError, RateLimitError, APIStatusError

DEFAULT_MODEL = "gpt-4o-mini"  # pick any standard text model you use


@dataclass
class SingleResponseResult:
    success: bool
    status: str  # "completed", "http_timeout", "rate_limited", "api_error"
    response_id: Optional[str]
    output_text: Optional[str]
    error_type: Optional[str]
    error_message: Optional[str]
    started_at: float
    completed_at: float
    elapsed_sec: float
    raw_response: Optional[Any]


class SimpleResponder:
    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: float = 60.0,
        base_url: Optional[str] = None,
    ):
        # The official OpenAI Python SDK uses httpx under the hood and supports a per-client timeout. :contentReference[oaicite:3]{index=3}
        self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)

    def ask(
        self,
        prompt: str,
        *,
        model: str = DEFAULT_MODEL,
        instructions: Optional[str] = None,
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> SingleResponseResult:
        """
        Make a single-shot Responses API call and return a normalized result.
        """
        started = time.time()
        try:
            payload: Dict[str, Any] = dict(
                model=model,
                input=prompt,  # Responses API accepts simple strings or rich content. :contentReference[oaicite:4]{index=4}
            )
            if instructions:
                payload["instructions"] = instructions
            # if temperature is not None:
            # payload["temperature"] = temperature
            if max_output_tokens is not None:
                payload["max_output_tokens"] = max_output_tokens
            if extra:
                payload.update(extra)

            resp = self.client.responses.create(**payload)
            # GitHub README shows .output_text for convenience; you can also walk resp.output[]. :contentReference[oaicite:5]{index=5}
            out_text = getattr(resp, "output_text", None)
            status = getattr(resp, "status", "completed")
            rid = getattr(resp, "id", None)
            done = time.time()
            return SingleResponseResult(
                success=True,
                status=status,
                response_id=rid,
                output_text=out_text,
                error_type=None,
                error_message=None,
                started_at=started,
                completed_at=done,
                elapsed_sec=done - started,
                raw_response=resp,
            )

        except httpx.TimeoutException as e:
            done = time.time()
            return SingleResponseResult(
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
        except RateLimitError as e:
            done = time.time()
            return SingleResponseResult(
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
            return SingleResponseResult(
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
