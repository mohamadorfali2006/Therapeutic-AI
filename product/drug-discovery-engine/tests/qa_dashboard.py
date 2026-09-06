"""Playwright visual QA + clickability audit for the DDE dashboard."""

import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright

BASE = "http://127.0.0.1:8011"
SHOT_DIR = Path(__file__).parent / "qa-screenshots"
SHOT_DIR.mkdir(exist_ok=True)

RESULTS = []


def log(name, passed, detail=""):
    RESULTS.append({"name": name, "passed": passed, "detail": detail})
    print(f"[{'PASS' if passed else 'FAIL'}] {name} {detail}")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})

        # 1. Load dashboard
        await page.goto(BASE, wait_until="networkidle")
        title = await page.title()
        log("title", "Drug Discovery Engine" in title, f"title={title!r}")
        await page.screenshot(path=str(SHOT_DIR / "01-dark-load.png"), full_page=False)

        # 2. Health indicator
        await page.wait_for_timeout(1500)
        health_text = await page.locator("body").inner_text()
        ok = ("ok" in health_text.lower()) or ("healthy" in health_text.lower())
        log("health indicator", ok)

        # 3. Models table populated
        models_text = await page.locator("body").inner_text()
        log("models table", "baseline" in models_text, "baseline row present")

        # 4. Predict form
        await page.fill("input#smiles, input[placeholder*='SMILES'], input[type='text']", "c1ccccc1")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(SHOT_DIR / "02-before-predict.png"))
        # click the primary predict button
        buttons = page.locator("button")
        clicked = False
        for i in range(await buttons.count()):
            txt = (await buttons.nth(i).inner_text()).strip().lower()
            if "predict" in txt or "run" in txt:
                await buttons.nth(i).click()
                clicked = True
                break
        log("predict button clickable", clicked)
        await page.wait_for_timeout(2500)
        await page.wait_for_selector("text=/trace-|Trace ID|trace_id/i", timeout=5000)
        body = await page.locator("body").inner_text()
        value_ok = "value" in body.lower() or float(
            next((word for word in body.split() if word.replace('.', '', 1).isdigit() and '.' in word), "0")
        )
        log("prediction result rendered", value_ok)
        await page.screenshot(path=str(SHOT_DIR / "03-prediction-result.png"))

        # Capture displayed prediction value if any
        m = [w for w in body.split() if w.replace('.', '', 1).replace('-', '', 1).isdigit() and '.' in w]
        log("prediction value present", len(m) > 0, f"numbers={m[:5]}")

        # 5. Theme toggle
        toggled = False
        theme_before = await page.evaluate("document.documentElement.dataset.theme")
        btn = None
        for i in range(await buttons.count()):
            txt = (await buttons.nth(i).inner_text()).strip().lower()
            if "theme" in txt or "light" in txt or "dark" in txt:
                btn = buttons.nth(i)
                break
        if btn is not None:
            await btn.click()
            toggled = True
        log("theme toggle button", toggled)
        await page.wait_for_timeout(600)
        theme_after = await page.evaluate("document.documentElement.dataset.theme")
        html_bg = await page.evaluate("getComputedStyle(document.documentElement).backgroundColor")
        await page.screenshot(path=str(SHOT_DIR / "04-theme-toggle.png"))
        log("theme switch changed data-theme", theme_after != theme_before,
            f"before={theme_before!r} after={theme_after!r} html-bg={html_bg}")
        # light theme must use a light canvas
        light_bg_ok = False
        if theme_after == "light":
            r, g, b, *_ = [int(v) for v in html_bg.strip("rgba()").split(",")][:3]
            light_bg_ok = (r > 200 and g > 200 and b > 200)
        log("light canvas is light", light_bg_ok, f"bg={html_bg}")

        # 6. Trace fetch flow
        trace_input = page.locator("input")  # second input for trace
        if await trace_input.count() > 1:
            trace_input = page.locator("input").nth(1)
        await trace_input.fill("demo-0001")
        trace_btn = None
        for i in range(await buttons.count()):
            txt = (await buttons.nth(i).inner_text()).strip().lower()
            if "fetch" in txt or "trace" in txt:
                trace_btn = buttons.nth(i)
                break
        if trace_btn is not None:
            await trace_btn.click()
            await page.wait_for_timeout(2000)
        log("trace fetch button", trace_btn is not None)

        # 7. Invalid SMILES error handling
        await page.fill("input#smiles, input[placeholder*='SMILES'], input[type='text']", "")
        # use API directly for invalid-smiles check
        resp = await page.request.post(f"{BASE}/api/v1/predict", data=json.dumps({"smiles": "=="}))
        err_status = resp.status
        log("invalid SMILES -> 422", err_status == 422, f"status={err_status}")

        # 8. Full-page screenshots both themes
        theme_cls = await page.evaluate("document.documentElement.className")
        await page.screenshot(path=str(SHOT_DIR / "05-full-current-theme.png"), full_page=True)

        # API direct checks as fallback evidence
        h = await page.request.get(f"{BASE}/health")
        log("health endpoint", h.status == 200)

        await browser.close()

    passed = sum(1 for r in RESULTS if r["passed"])
    print(f"\n=== SUMMARY: {passed}/{len(RESULTS)} passed ===")
    for r in RESULTS:
        if not r["passed"]:
            print(f"FAIL: {r['name']} — {r['detail']}")
    raise SystemExit(0 if passed == len(RESULTS) else 1)


if __name__ == "__main__":
    asyncio.run(main())