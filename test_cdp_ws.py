import json
import urllib.request
import websocket # websocket-client package

# Get list of targets from Chrome CDP
req = urllib.request.urlopen("http://localhost:9222/json")
targets = json.loads(req.read().decode())
print(f"Found {len(targets)} targets in Chrome:")
page_target = None
for t in targets:
    print(f" - [{t.get('type')}] {t.get('title')} ({t.get('url')})")
    if t.get('type') == 'page':
        page_target = t
        break

if page_target:
    ws_url = page_target['webSocketDebuggerUrl']
    print(f"\nConnecting to page WebSocket: {ws_url}")
    ws = websocket.create_connection(ws_url)
    
    # Send Page.navigate
    nav_cmd = {"id": 1, "method": "Page.navigate", "params": {"url": "https://www.etoro.com/markets/aapl/research"}}
    ws.send(json.dumps(nav_cmd))
    res = ws.recv()
    print("Navigate result:", res)
    ws.close()
