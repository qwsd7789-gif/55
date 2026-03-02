import asyncio
import json
import websockets

async def generate_image():
    uri = "ws://127.0.0.1:9222/devtools/browser"
    
    async with websockets.connect(uri) as ws:
        # Get targets
        await ws.send(json.dumps({"id": 1, "method": "Target.getTargets"}))
        response = await ws.recv()
        data = json.loads(response)
        
        target_id = None
        for target in data["result"]["targetInfos"]:
            if target["type"] == "page":
                target_id = target["targetId"]
                break
        
        if not target_id:
            print("No page target found")
            return
        
        # Attach to target
        await ws.send(json.dumps({
            "id": 2,
            "method": "Target.attachToTarget",
            "params": {"targetId": target_id, "flatten": True}
        }))
        response = await ws.recv()
        
        # Navigate to Gemini
        session_id = json.loads(response)["result"]["sessionId"]
        await ws.send(json.dumps({
            "id": 3,
            "sessionId": session_id,
            "method": "Page.navigate",
            "params": {"url": "https://gemini.google.com"}
        }))
        
        print("Navigating to Gemini...")
        await asyncio.sleep(5)
        
        # Find and click the input field
        await ws.send(json.dumps({
            "id": 4,
            "sessionId": session_id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": """
                    const input = document.querySelector('textarea[placeholder*="Ask"]') || 
                                  document.querySelector('[contenteditable="true"]') ||
                                  document.querySelector('textarea');
                    if (input) {
                        input.focus();
                        input.value = '生成一张图片：春日樱花，粉色浪漫';
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        "found";
                    } else "not found";
                """
            }
        }))
        
        response = await ws.recv()
        print(f"Input field: {response}")
        
        # Click send button
        await asyncio.sleep(1)
        await ws.send(json.dumps({
            "id": 5,
            "sessionId": session_id,
            "method": "Input.dispatchKeyEvent",
            "params": {"type": "keyDown", "key": "Return"}
        }))
        
        print("Prompt sent!")
        await asyncio.sleep(10)
        
        print("Image generation started. Please check the browser.")

asyncio.run(generate_image())
