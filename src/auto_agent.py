"""Unified CLI entry point for TalentFlow-AI."""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("auto_agent")

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "output"


def load_or_init_profile(force_rebuild: bool = False):
    """Load existing profile or build a fresh one."""
    from src.profiler.profile_ingestor import build_dynamic_profile

    ultimate_path = DATA_DIR / "ultimate_profile.json"
    profile_path = DATA_DIR / "dynamic_profile.json"

    target_path = ultimate_path if ultimate_path.exists() else profile_path

    if target_path.exists() and not force_rebuild:
        from src.schemas.models import DynamicCandidateProfile

        data = json.loads(target_path.read_text(encoding="utf-8"))
        return DynamicCandidateProfile.model_validate(data)
    return build_dynamic_profile(output_path=profile_path)


def run_init_profile() -> None:
    """Run the --init-profile command."""
    logger.info("Building dynamic profile from GitHub + seed data...")
    profile = load_or_init_profile(force_rebuild=True)
    logger.info(
        "Profile built: %s | Skills: %d | Projects: %d",
        profile.static_identity.full_name,
        len(profile.dynamic_template.skill_bank),
        len(profile.dynamic_template.project_bank),
    )


def run_jobs_pipeline(
    jobs_file: Path,
    headless: bool = True,
    auto_submit: bool = False,
    strict_visa_remote: bool = False,
    limit: int | None = None,
) -> None:
    """Run the full jobs pipeline: filter → tailor → PDF → browser."""
    from src.ingestion.visa_filter import evaluate_visa_and_role_eligibility
    from src.schemas.models import JobPosting
    from src.tailor.document_tailor import compile_application_pdfs, tailor_application_for_job

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load jobs
    raw_jobs = json.loads(jobs_file.read_text(encoding="utf-8"))
    all_jobs = [JobPosting.model_validate(j) for j in raw_jobs]
    logger.info("Loaded %d jobs from %s", len(all_jobs), jobs_file)

    # Load / build profile
    profile = load_or_init_profile()

    # Filter jobs
    eligible_jobs = []
    rejected_count = 0
    for job in all_jobs:
        is_eligible, reason, boost = evaluate_visa_and_role_eligibility(
            job, strict_visa_or_remote=strict_visa_remote
        )
        if is_eligible:
            eligible_jobs.append((job, boost, reason))
            logger.info("✅ ELIGIBLE [+%d]: %s @ %s — %s", boost, job.title, job.company, reason)
        else:
            rejected_count += 1
            logger.info("❌ REJECTED: %s @ %s — %s", job.title, job.company, reason)

    logger.info("Filtering complete: %d Eligible, %d Rejected", len(eligible_jobs), rejected_count)

    if not eligible_jobs:
        logger.warning("No eligible jobs found. Exiting.")
        return

    # Sort by boost descending (Visa Sponsorship & Remote first)
    eligible_jobs.sort(key=lambda x: x[1], reverse=True)

    if limit and limit > 0:
        logger.info("Limiting application batch to top %d jobs", limit)
        eligible_jobs = eligible_jobs[:limit]

    # Tailor and compile PDFs
    jobs_and_packages = []
    for job, boost, reason in eligible_jobs:
        logger.info("Tailoring application for %s @ %s (Boost: +%d)...", job.title, job.company, boost)
        package = tailor_application_for_job(job, profile)
        pdf_paths = compile_application_pdfs(package, profile, OUTPUT_DIR)
        logger.info(
            "PDFs compiled: CV=%s, ML=%s",
            pdf_paths.get("cv_pdf"),
            pdf_paths.get("motivation_pdf"),
        )
        jobs_and_packages.append(
            (job, package, pdf_paths.get("cv_pdf"), pdf_paths.get("motivation_pdf"))
        )

    # Run browser applier
    from src.browser_bot.multi_tab_applier import MultiTabBrowserApplier

    applier = MultiTabBrowserApplier(
        output_dir=OUTPUT_DIR,
        headless=headless,
        auto_submit=auto_submit,
        keep_open_on_blocker=True,
    )

    results = asyncio.run(applier.apply_batch(jobs_and_packages))

    clean_results = []
    for r in results:
        clean_r = {
            k: str(v) if not isinstance(v, (str, int, float, bool, type(None))) else v
            for k, v in r.items()
            if k != "page"
        }
        clean_results.append(clean_r)

    summary = {
        "total_jobs": len(all_jobs),
        "eligible_jobs": len(eligible_jobs),
        "rejected_jobs": rejected_count,
        "results": clean_results,
    }
    summary_path = OUTPUT_DIR / "run_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logger.info("Run summary written to %s", summary_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="TalentFlow-AI — Autonomous Job Application CLI")
    parser.add_argument("--init-profile", action="store_true", help="Build dynamic profile from GitHub + seed data")
    parser.add_argument("--jobs-file", type=Path, help="Path to jobs JSON file")
    parser.add_argument("--headless", action="store_true", default=True, help="Run browser in headless mode")
    parser.add_argument("--auto-submit", action="store_true", default=False, help="Auto-submit forms if no human action needed")
    parser.add_argument("--strict-visa-remote", action="store_true", default=False, help="Strictly require visa sponsorship or remote work option")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of jobs to process")

    args = parser.parse_args()

    if args.init_profile:
        run_init_profile()
    elif args.jobs_file:
        run_jobs_pipeline(
            jobs_file=args.jobs_file,
            headless=args.headless,
            auto_submit=args.auto_submit,
            strict_visa_remote=args.strict_visa_remote,
            limit=args.limit,
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
