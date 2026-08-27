# llm-integration

Practice project for integrating an LLM into a backend service. The current
implementation exposes a FastAPI API that classifies the sentiment of a piece
of text.

Per `JOB-CARD.md`, the service accepts text and returns a sentiment
classification. The real Gemini-backed classifier (`GeminiLlmService`) is not
yet implemented — `GeminiLlmService.process` currently raises
`NotImplementedError`. A `StubLlmService` is provided for local development and
testing; it returns a fixed response and is selected via the `LLM_STUB`
environment variable.

## Requirements

- Python 3.12
- [`uv`](https://docs.astral.sh/uv/) for dependency and environment management
- A Google Gemini API key (only required when running with the real LLM, not
  for stub mode)

## Setup

1. Install dependencies (this also creates/uses the local virtual environment):

   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root. Copy the example and fill in your
   values:

   ```bash
   cp .env.example .env
   ```

   The service reads the following variables via `pydantic-settings`:

   | Variable          | Required | Description                                                          |
   | ----------------- | -------- | -------------------------------------------------------------------- |
   | `GEMINI_API_KEY`  | yes      | Google Gemini API key. A placeholder is fine in stub mode.           |
   | `LLM_STUB`        | yes      | Set to `1` to use `StubLlmService`. Any other value uses the real LLM (currently unimplemented). |

   For local development with the stub, your `.env` should contain:

   ```dotenv
   GEMINI_API_KEY=your-key-here
   LLM_STUB=1
   ```

## Running

Start the server with:

```bash
uv run fastapi run -e src.llm_integration.main:app
```

The server listens on `http://127.0.0.1:8000` (default FastAPI port `8000`).

Interactive API docs are available at `http://127.0.0.1:8000/docs`.

## Endpoints

### `GET /`

Returns a health-check string.

- Response: `200 OK` with body `"Hello World!"`

### `POST /sentiment-classifier`

Classifies the sentiment of the provided text.

- Request body (`ClfReq`):

  ```json
  { "text": "string, 1-10,000 characters, non-empty" }
  ```

  The `text` field must be non-empty (whitespace-only strings are rejected).

- Response body (`ClfResp`), `200 OK`:

  | Field          | Type                                      | Constraints                              |
  | -------------- | ----------------------------------------- | ---------------------------------------- |
  | `sentiment`    | `positive \| negative \| neutral \| unsure` | The predicted class                    |
  | `confidence`   | `number`                                  | Between `0.0` and `1.0`                  |
  | `second_best`  | `positive \| negative \| neutral \| unsure` | Must differ from `sentiment`          |
  | `reason`       | `string`                                  | Short explanation, max `64` characters   |

## Example requests

### Correct request (stub mode)

With `LLM_STUB=1` set in `.env`, the service returns the deterministic stub
response:

```bash
curl -X POST http://127.0.0.1:8000/sentiment-classifier \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

Expected response (`200 OK`):

```json
{
  "sentiment": "neutral",
  "confidence": 0.6,
  "second_best": "unsure",
  "reason": "No clear context."
}
```

### Deliberately broken request

Sending an empty/whitespace-only `text` fails the request validation:

```bash
curl -X POST http://127.0.0.1:8000/sentiment-classifier \
  -H "Content-Type: application/json" \
  -d '{"text": ""}'
```

Expected response: `422 Unprocessable Entity`, with a validation error such as:

```json
{
  "detail": [
    {
      "type": "value_error",
      "msg": "Value error, Request cannot have be an empty string!",
      "loc": ["body", "text"]
    }
  ]
}
```

## Project layout

```
src/llm_integration/
├── main.py        # FastAPI app entry point
├── routes.py      # API routes (e.g. /sentiment-classifier)
├── schemas.py     # Request/response Pydantic models + validators
├── llm.py         # LlmService protocol, stub + (unimplemented) Gemini service
├── utils.py       # Dependency wiring for the LLM client/service
└── config.py      # Settings loaded from .env
```
