import asyncio
import json
from playwright.async_api import async_playwright

async def generate_image():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = context.pages[0] if context.pages else await context.new_page()
        
        print("正在打开 Gemini...")
        await page.goto("https://gemini.google.com", wait_until="networkidle")
        await asyncio.sleep(3)
        
        print("输入描述词...")
        # 尝试找到输入框
        try:
            # 新版 Gemini 界面
            input_box = await page.wait_for_selector('textarea[placeholder*="Ask"], [contenteditable="true"], textarea', timeout=5000)
            await input_box.fill("生成一张图片：春日樱花，粉色浪漫")
            await asyncio.sleep(1)
            
            # 发送
            await input_box.press("Enter")
            print("已发送请求，等待生成...")
            await asyncio.sleep(15)
            
            print("请检查浏览器中的 Gemini 页面")
            
        except Exception as e:
            print(f"操作失败: {e}")
        
        await browser.close()

asyncio.run(generate_image())
