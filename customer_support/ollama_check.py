#!/usr/bin/env python3
# ollama_quick.py — simple inspector for local Ollama endpoints
# Usage examples:
#   API_BASE="http://localhost:11434" python ollama_quick.py chat "Say hi in one sentence"
#   API_BASE="http://localhost:11434" python ollama_quick.py embed "hello world"

import os
import sys
import json
import requests

API_BASE = os.getenv("API_BASE", "http://localhost:11434")

def pretty(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))

def call_chat(model, message, max_tokens=200, timeout=60):
    url = API_BASE.rstrip("/") + "/v1/chat/completions"
    payload = {"model": model, "messages": [{"role": "user", "content": message}], "max_tokens": max_tokens}
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json()

def call_embed(model, text, timeout=60):
    url = API_BASE.rstrip("/") + "/v1/embeddings"
    payload = {"model": model, "input": [text]}
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json()

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  ollama_quick.py chat  \"Your message\"  [model]")
        print("  ollama_quick.py embed \"Text to embed\" [model]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    text = sys.argv[2]
    if cmd == "chat":
        model = sys.argv[3] if len(sys.argv) > 3 else os.getenv("MODEL", "gpt-oss:20b")
        try:
            resp = call_chat(model, text)
            print("\n=== raw JSON response ===")
            pretty(resp)
            # show assistant text if available
            choices = resp.get("choices") or []
            if choices:
                first = choices[0]
                msg = first.get("message") or first.get("text")
                if isinstance(msg, dict):
                    content = msg.get("content") or msg.get("text")
                else:
                    content = msg
                print("\n=== assistant text (first choice) ===")
                print(content or "<no text>")
        except requests.HTTPError as e:
            print("HTTP error:", e, file=sys.stderr)
            try:
                print("response body:", e.response.text, file=sys.stderr)
            except Exception:
                pass
            sys.exit(2)
    elif cmd == "embed":
        model = sys.argv[3] if len(sys.argv) > 3 else os.getenv("EMBEDDER_MODEL", "nomic-embed-text:latest")
        try:
            resp = call_embed(model, text)
            print("\n=== raw JSON response ===")
            pretty(resp)
            # print embedding length if present
            data = resp.get("data") or []
            if data and isinstance(data, list) and len(data) > 0:
                emb = data[0].get("embedding")
                if emb is None:
                    print("\nembedding field missing or empty")
                else:
                    print("\nembedding length:", len(emb))
        except requests.HTTPError as e:
            print("HTTP error:", e, file=sys.stderr)
            try:
                print("response body:", e.response.text, file=sys.stderr)
            except Exception:
                pass
            sys.exit(2)
    else:
        print("Unknown command:", cmd)
        sys.exit(1)

if __name__ == "__main__":
    main()
