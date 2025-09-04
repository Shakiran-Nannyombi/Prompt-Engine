#!/usr/bin/env python3
"""
Generate Mermaid PNG using Playwright - works offline!
Run: python generate_graph_png.py
"""
import asyncio
from playwright.async_api import async_playwright
from agents.refiner_agent import refiner_graph

async def generate_mermaid_png():
    # Get the mermaid text
    graph = refiner_graph.get_graph(xray=True)
    mermaid_text = graph.draw_mermaid()
    
    print("✅ Generated Mermaid text")
    
    # Create HTML with Mermaid
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
        <style>
            body {{ margin: 0; padding: 20px; background: white; }}
            .mermaid {{ font-family: Arial, sans-serif; }}
        </style>
    </head>
    <body>
        <div class="mermaid">
{mermaid_text}
        </div>
        <script>
            mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        </script>
    </body>
    </html>
    """
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Set content and wait for Mermaid to render
        await page.set_content(html_content)
        await page.wait_for_timeout(2000)  # Wait for rendering
        
        # Find the mermaid element and screenshot it
        mermaid_element = page.locator(".mermaid")
        await mermaid_element.screenshot(path="refiner_agent_mermaid.png")
        
        await browser.close()
        print("✅ Successfully generated 'refiner_agent_mermaid.png'!")

if __name__ == "__main__":
    asyncio.run(generate_mermaid_png())
