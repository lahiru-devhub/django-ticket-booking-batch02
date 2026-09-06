from huggingface_hub import InferenceClient

from django.conf import settings

from .models import Event


_client: InferenceClient | None = None

_SYSTEM_PROMPT = (
    "You are a friendly event-ticketing support assistant. Start with a short greeting. "
    "Answer only with facts from the provided event catalog. "
    "If the catalog does not contain enough information, say that clearly and ask one short follow-up question. "
    "Do not mention outside knowledge, links, policies, or internal notes."
)


def _build_catalog_context(limit: int = 80) -> str:
    events = list(
        Event.objects.filter(is_published=True)
        .select_related("venue")
        .order_by("event_date", "event_time")[:limit]
    )

    if not events:
        return "No published events found in the catalog."

    return "\n".join(
        (
            f"- id={event.id}; title={event.title}; venue={event.venue.name}; "
            f"city={event.venue.city}; date={event.event_date}; time={event.event_time}; "
            f"price={event.price}; available_tickets={event.available_tickets}; "
            f"description={(event.description or '').strip()}"
        )
        for event in events
    )


def get_chat_client() -> InferenceClient:
    global _client

    if _client is None:
        if not settings.HF_API_TOKEN:
            raise RuntimeError("Hugging Face chat is not configured.")

        _client = InferenceClient(
            token=settings.HF_API_TOKEN,
            base_url=settings.HF_CHAT_URL,
        )

    return _client


def generate_chat_reply(customer_message: str) -> str:
    catalog_context = _build_catalog_context()

    if catalog_context == "No published events found in the catalog.":
        return "Hello! There are no published events in the catalog right now."

    completion = get_chat_client().chat.completions.create(
        model=settings.HF_CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": f"{_SYSTEM_PROMPT}\n\nEvent catalog:\n{catalog_context}",
            },
            {"role": "user", "content": f"Customer question: {customer_message}"},
        ],
        temperature=0.3,
        max_tokens=256,
    )
    reply = completion.choices[0].message.content if completion.choices else ""
    return (reply or "").strip() or "Hello! I could not generate a response. Please try again."