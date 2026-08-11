import pytest
from playwright.sync_api import Page, expect

def test_e2e_profile_page_elements(page: Page):
    page.goto("http://localhost:8000/static/profile.html")
    expect(page.locator("h1")).to_contain_text("Account Settings")
    expect(page.locator("#username")).to_be_visible()
    expect(page.locator("#email")).to_be_visible()
    expect(page.locator("#current_password")).to_be_visible()
    expect(page.locator("#new_password")).to_be_visible()