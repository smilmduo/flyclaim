from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # 1. Home Page
    print("Navigating to Home...")
    page.goto("http://localhost:5173")
    expect(page.get_by_text("Claim Your Flight Compensation Easily")).to_be_visible()
    page.screenshot(path="verification/1_home.png")
    print("Home page verified.")

    # 2. Signup
    print("Navigating to Signup...")
    page.get_by_role("link", name="Sign Up").click()
    expect(page.get_by_role("heading", name="Create an account")).to_be_visible()
    page.screenshot(path="verification/2_signup_page.png")

    # Fill form
    print("Filling Signup form...")
    page.get_by_label("Full Name").fill("Test User")
    page.get_by_label("Email Address").fill("testuser@example.com")
    # Use a random phone to avoid conflict
    import random
    phone = f"+91{random.randint(1000000000, 9999999999)}"
    print(f"Using phone: {phone}")
    page.get_by_label("Phone Number").fill(phone)
    page.get_by_label("Password").fill("password123")

    page.get_by_role("button", name="Create Account").click()

    # 3. Dashboard
    print("Waiting for Dashboard...")
    expect(page).to_have_url("http://localhost:5173/dashboard")
    expect(page.get_by_text("My Dashboard")).to_be_visible()
    expect(page.get_by_text("Test User")).to_be_visible()
    page.screenshot(path="verification/3_dashboard.png")
    print("Dashboard verified.")

    # 4. File a Claim
    print("Navigating to File Claim...")
    page.get_by_role("link", name="New Claim").click()
    expect(page.get_by_text("File a New Claim")).to_be_visible()

    page.get_by_placeholder("e.g. 6E-234").fill("6E-555")
    page.fill('input[type="date"]', "2025-10-28")
    page.get_by_placeholder("e.g. IndiGo").fill("IndiGo")

    page.get_by_role("button", name="Submit Claim").click()

    # 5. Track Claim
    print("Waiting for Tracking Page...")
    expect(page.get_by_text("Track Your Claim")).to_be_visible()
    expect(page.get_by_text("6E-555", exact=True)).to_be_visible()
    page.screenshot(path="verification/4_track_claim.png")
    print("Claim tracking verified.")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
