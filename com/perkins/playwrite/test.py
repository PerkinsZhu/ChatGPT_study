"""
Created by PerkinsZhu on 2023/8/15 17:45
"""

from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1/login?redirect=/index")
    page.get_by_role("textbox", name="请输入租户名称").fill("芋道源码")
    page.get_by_role("textbox", name="请输入用户名").fill("admin")
    page.get_by_role("textbox", name="请输入用户名").press("Tab")
    page.get_by_role("textbox", name="请输入密码").fill("11111111")
    page.get_by_role("button", name="登录", exact=True).click()
    page.locator('img').nth(3).screenshot(path="../1.png")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
