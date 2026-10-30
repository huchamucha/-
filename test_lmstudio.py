import os

from lmstudio_client import LMStudioClient


def main() -> None:
    client = LMStudioClient(
        base_url=os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("LMSTUDIO_API_KEY", "lm-studio"),
        model=os.getenv("LMSTUDIO_MODEL", "local-model"),
    )

    prompt = "Напиши одно слово: ok"
    try:
        answer = client.ask(prompt)
        print("LM Studio response:")
        print(answer)
    except Exception as exc:  # pragma: no cover - local smoke test only
        print(f"LM Studio test failed: {exc}")
        raise


if __name__ == "__main__":
    main()
