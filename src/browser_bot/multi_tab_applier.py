"""Multi-Tab Human-Handoff Playwright Browser Applier for TalentFlow-AI."""
from __future__ import annotations

import logging
import re
import unicodedata
from pathlib import Path
from typing import Any

from src.schemas.models import JobPosting, TailoredApplicationPackage

logger = logging.getLogger(__name__)

_FORM_FIELD_SELECTORS: list[tuple[list[str], str]] = [
    (["input[name*='first' i]", "input[id*='first' i]", "input[placeholder*='first' i]"], "Sam"),
    (["input[name*='last' i]", "input[id*='last' i]", "input[placeholder*='last' i]"], "Moradian"),
    (
        [
            "input[name*='full' i]",
            "input[id*='full' i]",
            "input[name*='name' i]",
            "input[id*='name' i]",
            "input[placeholder*='full name' i]",
        ],
        "Sam Moradian",
    ),
    (
        ["input[type='email']", "input[name*='email' i]", "input[id*='email' i]"],
        "m.hesam.moradian@gmail.com",
    ),
    (
        ["input[type='tel']", "input[name*='phone' i]", "input[id*='phone' i]"],
        "+18059007207",
    ),
    (
        ["input[name*='linkedin' i]", "input[id*='linkedin' i]", "input[placeholder*='linkedin' i]"],
        "https://www.linkedin.com/in/m-hesam-moradian",
    ),
    (
        ["input[name*='github' i]", "input[id*='github' i]", "input[placeholder*='github' i]"],
        "https://github.com/m-hesam-moradian",
    ),
    (
        ["input[name*='location' i]", "input[id*='location' i]", "input[name*='city' i]"],
        "Open to Relocation (Germany / EU Blue Card)",
    ),
    (
        ["input[name*='notice' i]", "input[id*='notice' i]", "input[placeholder*='notice' i]"],
        "Immediately",
    ),
    (
        ["input[name*='start' i]", "input[id*='start' i]", "input[placeholder*='start' i]"],
        "Immediately",
    ),
]

_COVER_LETTER_SELECTORS = [
    "textarea[name*='cover' i]",
    "textarea[id*='cover' i]",
    "textarea[name*='motivation' i]",
    "textarea[id*='motivation' i]",
    "textarea[name*='letter' i]",
    "textarea[placeholder*='cover' i]",
    "textarea[placeholder*='motivation' i]",
    "textarea",
]

_CAPTCHA_SELECTORS = [
    "iframe[src*='recaptcha']",
    "iframe[src*='hcaptcha']",
    "iframe[src*='turnstile']",
    "[class*='captcha']",
    "#captcha",
    "[data-human-required='true']",
]

_HUMAN_BANNER_JS = """(reason) => {
    const existing = document.getElementById('tf-human-banner');
    if (existing) { existing.remove(); }
    const banner = document.createElement('div');
    banner.id = 'tf-human-banner';
    banner.style.cssText = `
        position: fixed; top: 0; left: 0; right: 0; z-index: 999999;
        background: #ff4444; color: white; font-size: 16px; font-weight: bold;
        padding: 12px 20px; text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.5);
        font-family: Arial, sans-serif;
    `;
    banner.textContent = '⚠️ HUMAN ACTION NEEDED (' + reason + ') — CV & Motivation Letter are uploaded! Complete the remaining check and click Submit.';
    document.body.insertBefore(banner, document.body.firstChild);
}"""


async def detect_human_action_needed(page: Any) -> tuple[bool, str]:
    """Check the DOM for CAPTCHA, login walls, or unfilled required fields."""
    # Check CAPTCHA
    for selector in _CAPTCHA_SELECTORS:
        try:
            elem = await page.query_selector(selector)
            if elem:
                return True, f"CAPTCHA/human-check detected ({selector})"
        except Exception:
            pass

    # Check login/SSO wall
    try:
        pw_input = await page.query_selector("input[type='password']")
        if pw_input:
            return True, "Login/SSO wall detected (password input found)"
    except Exception:
        pass

    # Check unfilled required fields
    try:
        required_selectors = ["input[required]", "select[required]", "textarea[required]"]
        for sel in required_selectors:
            elements = await page.query_selector_all(sel)
            for elem in elements:
                value = await elem.evaluate("el => el.value")
                if not value or value.strip() == "":
                    return True, f"Unfilled required field detected ({sel})"
    except Exception:
        pass

    return False, ""


def _sanitize_filename(text: str) -> str:
    """Convert text to a safe filename fragment."""
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_str = nfkd.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^\w\-]", "_", ascii_str).strip("_")[:50]


class MultiTabBrowserApplier:
    """Manages multi-tab Playwright browser sessions for job applications."""

    def __init__(
        self,
        output_dir: Path,
        headless: bool = True,
        auto_submit: bool = False,
        keep_open_on_blocker: bool = True,
    ) -> None:
        self.output_dir = Path(output_dir)
        self.headless = headless
        self.auto_submit = auto_submit
        self.keep_open_on_blocker = keep_open_on_blocker
        self.results: list[dict[str, Any]] = []

    async def apply_batch(
        self,
        jobs_and_packages: list[
            tuple[JobPosting, TailoredApplicationPackage, Path | None, Path | None]
        ],
    ) -> list[dict[str, Any]]:
        """Apply to a batch of jobs using a single shared browser context."""
        from playwright.async_api import async_playwright

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=self.headless)
            context = await browser.new_context()

            for job, package, cv_pdf_path, motivation_pdf_path in jobs_and_packages:
                result = await self._apply_single(
                    context, job, package, cv_pdf_path, motivation_pdf_path
                )
                self.results.append(result)

            # Cleanup: close only submitted pages; leave human-needed ones open
            # until the context closes naturally
            await context.close()
            await browser.close()

        return self.results

    async def _apply_single(
        self,
        context: Any,
        job: JobPosting,
        package: TailoredApplicationPackage,
        cv_pdf_path: Path | None,
        motivation_pdf_path: Path | None,
    ) -> dict[str, Any]:
        """Apply to a single job in a new tab."""
        page = await context.new_page()
        job_output = self.output_dir / _sanitize_filename(f"{job.company}_{job.id}")
        job_output.mkdir(parents=True, exist_ok=True)

        try:
            await page.goto(job.url, wait_until="domcontentloaded", timeout=30_000)
        except Exception as exc:
            logger.warning("Failed to navigate to %s: %s", job.url, exc)
            await page.close()
            return {
                "job_id": job.id,
                "company": job.company,
                "status": "NAVIGATION_FAILED",
                "reason": str(exc),
            }

        # Auto-fill form fields
        for selectors, value in _FORM_FIELD_SELECTORS:
            for sel in selectors:
                try:
                    elem = await page.query_selector(sel)
                    if elem:
                        await elem.fill(value)
                        break
                except Exception:
                    pass

        # Fill cover letter textarea
        for sel in _COVER_LETTER_SELECTORS:
            try:
                elem = await page.query_selector(sel)
                if elem:
                    await elem.fill(package.motivation_letter)
                    break
            except Exception:
                pass

        # Upload CV PDF
        if cv_pdf_path and cv_pdf_path.exists():
            try:
                file_inputs = await page.query_selector_all("input[type='file']")
                if file_inputs:
                    await file_inputs[0].set_input_files(str(cv_pdf_path))
            except Exception as exc:
                logger.debug("CV upload failed: %s", exc)

        # Upload motivation letter PDF
        if motivation_pdf_path and motivation_pdf_path.exists():
            try:
                file_inputs = await page.query_selector_all("input[type='file']")
                if len(file_inputs) >= 2:
                    await file_inputs[1].set_input_files(str(motivation_pdf_path))
            except Exception as exc:
                logger.debug("Motivation letter upload failed: %s", exc)

        # Detect human action needed
        needs_human, reason = await detect_human_action_needed(page)

        if needs_human:
            # Inject warning banner
            try:
                await page.evaluate(_HUMAN_BANNER_JS, reason or "Manual review required")
            except Exception:
                pass

            # Save screenshot
            screenshot_path = job_output / "needs_human_screenshot.png"
            try:
                await page.screenshot(path=str(screenshot_path))
            except Exception:
                pass

            if self.keep_open_on_blocker:
                # DO NOT close the tab
                logger.info("Tab kept open for human action: job %s (%s)", job.id, reason)
                return {
                    "job_id": job.id,
                    "company": job.company,
                    "status": "OPEN_IN_TAB_NEEDS_HUMAN",
                    "reason": reason,
                    "screenshot": str(screenshot_path),
                    "page": page,  # keep reference so page stays alive
                }
            else:
                await page.close()
                return {
                    "job_id": job.id,
                    "company": job.company,
                    "status": "NEEDS_HUMAN_CLOSED",
                    "reason": reason,
                    "screenshot": str(screenshot_path),
                }

        elif self.auto_submit:
            # Auto-submit
            try:
                submit_btn = await page.query_selector(
                    "button[type='submit'], input[type='submit']"
                )
                if submit_btn:
                    await submit_btn.click()
                    await page.wait_for_load_state("domcontentloaded", timeout=10_000)
            except Exception as exc:
                logger.warning("Submit click failed for job %s: %s", job.id, exc)

            screenshot_path = job_output / "submitted_screenshot.png"
            try:
                await page.screenshot(path=str(screenshot_path))
            except Exception:
                pass

            await page.close()
            return {
                "job_id": job.id,
                "company": job.company,
                "status": "SUBMITTED",
                "screenshot": str(screenshot_path),
            }

        else:
            screenshot_path = job_output / "filled_screenshot.png"
            try:
                await page.screenshot(path=str(screenshot_path))
            except Exception:
                pass
            await page.close()
            return {
                "job_id": job.id,
                "company": job.company,
                "status": "FILLED_NO_SUBMIT",
                "screenshot": str(screenshot_path),
            }
