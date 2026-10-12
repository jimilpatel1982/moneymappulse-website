#!/usr/bin/env python3
"""Generate static guide pages with AnnotatedScreenshot visual guides."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PLAY_STORE = "https://play.google.com/store/apps/details?id=com.jimilpatel.jpfinancelab"
FOOTER = (
    "<p>MoneyMap Pulse provides estimates and educational information only. "
    "Results depend on assumptions and should not be considered financial advice.</p>"
)


def shell(title: str, meta: str, canonical_slug: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | MoneyMap Pulse Guide</title>
  <meta name="description" content="{meta}">
  <meta property="og:title" content="{title} | MoneyMap Pulse Guide">
  <meta property="og:description" content="{meta}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://moneymappulse.co.uk/{canonical_slug}/">
  <link rel="canonical" href="https://moneymappulse.co.uk/{canonical_slug}/">
  <link rel="stylesheet" href="../css/styles.css">
  <link rel="icon" href="../assets/logo/moneymap-pulse-icon.png" type="image/png">
  <link rel="apple-touch-icon" href="../assets/logo/moneymap-pulse-icon.png">
</head>
<body class="guide-page">
  <div class="page-wrap">
    <a href="#main" class="skip-link">Skip to main content</a>
    <header class="site-header">
      <div class="container">
        <a href="../index.html" class="brand" aria-label="MoneyMap Pulse home">
          <img src="../assets/logo/moneymap-pulse-logo-transparent-trimmed.png" alt="MoneyMap Pulse" class="brand-logo" width="120" height="48">
        </a>
        <nav class="nav" aria-label="Main navigation">
          <a href="../index.html">Home</a>
          <a href="../guides.html">Guides</a>
          <a href="../features.html">Features</a>
          <a href="../faq.html">FAQ</a>
          <a href="../privacy.html">Privacy</a>
          <a href="../contact.html">Contact</a>
        </nav>
        <div class="header-cta">
          <a href="{PLAY_STORE}" class="button button-primary" rel="noopener noreferrer">Google Play</a>
        </div>
      </div>
    </header>
    <main id="main">
      <header class="page-header">
        <div class="container">
          <p class="hero-eyebrow" style="margin-bottom: 8px;">User guide</p>
          <h1>{title}</h1>
          <p class="lead">{meta}</p>
        </div>
      </header>
      {body}
    </main>
    <footer class="site-footer">
      <div class="container">
        <div class="footer-grid"><div>{FOOTER}</div></div>
        <div class="footer-bottom">
          <p>&copy; <span id="current-year">2026</span> MoneyMap Pulse. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
  <script src="../js/main.js"></script>
  <script src="../js/interactive-annotated-screenshot.js"></script>
</body>
</html>
"""


def spotlight_dims(ann: dict[str, Any]) -> tuple[float, float]:
    """Tight glow around the value/card at the marker — not a wireframe box."""
    return float(ann.get("spot_w", 20)), float(ann.get("spot_h", 5))


CIRCLED_NUMBERS = "①②③④⑤⑥⑦⑧⑨"


def render_panel_html(ann: dict[str, Any], index: int) -> str:
    badge = CIRCLED_NUMBERS[index] if index < len(CIRCLED_NUMBERS) else str(index + 1)
    source = (
        f"""<p class="interactive-tour__meta interactive-tour__meta--source">
                <span class="interactive-tour__meta-label">Source</span>
                <span class="interactive-tour__meta-value">{ann["source"]}</span>
              </p>"""
        if ann.get("source")
        else ""
    )
    example = (
        f"""<p class="interactive-tour__meta interactive-tour__meta--example">
                <span class="interactive-tour__meta-label">Example</span>
                <span class="interactive-tour__meta-value">{ann["example"]}</span>
              </p>"""
        if ann.get("example")
        else ""
    )
    tip = (
        f"""<div class="interactive-tour__tip">
                <span class="interactive-tour__meta-label">Tip</span>
                <p class="interactive-tour__tip-text">{ann["tip"]}</p>
              </div>"""
        if ann.get("tip")
        else ""
    )
    return f"""<div class="interactive-tour__panel-header">
                <span class="interactive-tour__panel-badge" aria-hidden="true">{badge}</span>
                <h3 class="interactive-tour__panel-title">{ann["title"]}</h3>
              </div>
              <p class="interactive-tour__panel-desc">{ann["body"]}</p>
              <div class="interactive-tour__panel-details">
              {source}
              {example}
              </div>
              {tip}"""


def ensure_annotation_coords(spec: dict[str, Any]) -> list[dict[str, Any]]:
    annotations = [dict(a) for a in spec["annotations"]]
    positions = spec.get("positions", [])
    total = len(annotations)
    for i, ann in enumerate(annotations):
        if "x" not in ann and i < len(positions):
            ann["x"], ann["y"] = positions[i]
        ann.setdefault("x", 50)
        ann.setdefault("y", 36 + i * 8)
        ann.setdefault("source", spec.get("annotation_source", ""))
        ann.setdefault("tip", "")
        ann.setdefault("example", "")
    return annotations


def interactive_annotated_screenshot(
    tour_id: str,
    visual_title: str,
    img_file: str,
    img_alt: str,
    annotations: list[dict[str, Any]],
) -> str:
    json_payload = []
    overlay_markers = []
    rail_markers = []
    spotlights = []
    for i, ann in enumerate(annotations):
        spot_w, spot_h = spotlight_dims(ann)
        json_payload.append(
            {
                "id": i + 1,
                "title": ann["title"],
                "description": ann["body"],
                "source": ann.get("source", ""),
                "example": ann.get("example", ""),
                "tip": ann.get("tip", ""),
                "x": ann["x"],
                "y": ann["y"],
            }
        )
        active = " is-active" if i == 0 else ""
        pressed = "true" if i == 0 else "false"
        overlay_markers.append(
            f"""<button type="button" class="annotated-shot__marker annotated-shot__marker--overlay{active}" """
            f"""style="left:{ann['x']}%;top:{ann['y']}%;" data-tour-marker="{i}" """
            f"""aria-label="{ann['title']}" aria-pressed="{pressed}">"""
            f"""<span class="annotated-shot__marker-inner">{i + 1}</span></button>"""
        )
        rail_markers.append(
            f"""<button type="button" class="interactive-tour__rail-btn{active}" """
            f"""data-tour-marker="{i}" aria-label="{ann['title']}" aria-pressed="{pressed}">"""
            f"""<span class="interactive-tour__rail-num">{i + 1}</span></button>"""
        )
        spot_active = " is-active" if i == 0 else ""
        spotlights.append(
            f"""<div class="annotated-shot__spotlight{spot_active}" data-tour-spotlight="{i}" """
            f"""style="left:{ann['x']}%;top:{ann['y']}%;--spot-w:{spot_w}%;--spot-h:{spot_h}%;"></div>"""
        )

    initial_panel = render_panel_html(annotations[0], 0)
    last_index = len(annotations) - 1
    next_disabled = " disabled" if last_index == 0 else ""

    return f"""<section class="annotated-shot interactive-tour" aria-labelledby="visual-guide-title" tabindex="0">
        <div class="container interactive-tour__container">
          <h2 class="annotated-shot__title" id="visual-guide-title">{visual_title}</h2>
          <p class="interactive-tour__hint interactive-tour__hint--mobile">Tap a number to explore each part of the screen.</p>
          <p class="interactive-tour__hint interactive-tour__hint--desktop">Click a marker on the screenshot to learn what each part does.</p>
          <div class="interactive-tour__layout">
            <div class="interactive-tour__visual">
              <div class="annotated-shot__stage">
                <img class="annotated-shot__img" src="../assets/screenshots/{img_file}" alt="{img_alt}" width="1080" height="1920" loading="lazy">
                <div class="annotated-shot__spotlights" aria-hidden="true">{"".join(spotlights)}</div>
                {"".join(overlay_markers)}
              </div>
            </div>
            <div class="interactive-tour__panel-column">
              <div class="interactive-tour__panel" role="region" aria-live="polite" aria-label="Annotation details" data-tour-swipe>
                <div class="interactive-tour__panel-inner" data-tour-panel>
                  {initial_panel}
                </div>
                <div class="interactive-tour__nav" data-tour-nav aria-label="Tour navigation">
                  <button type="button" class="interactive-tour__nav-btn" data-tour-prev disabled aria-label="Previous step">← Previous</button>
                  <button type="button" class="interactive-tour__nav-btn" data-tour-next{next_disabled} aria-label="Next step">Next →</button>
                </div>
                <p class="interactive-tour__swipe-hint" aria-hidden="true">Swipe left or right to change step</p>
              </div>
            </div>
            <div class="interactive-tour__marker-rail" role="toolbar" aria-label="Screenshot tour steps">
              {"".join(rail_markers)}
            </div>
          </div>
          <script type="application/json" class="interactive-tour__data">{json.dumps(json_payload)}</script>
        </div>
      </section>"""


def flow_diagram() -> str:
    steps = [
        ("../house-budget-calculator/", "House Budget"),
        ("../net-worth-calculator/", "Net Worth"),
        ("../portfolio-return-calculator/", "Portfolio Return"),
        ("../retirement-calculator/", "Retirement"),
        ("../financial-health-snapshot/", "Financial Health Snapshot"),
    ]
    parts = ['<div class="guide-flow" aria-label="How calculators feed your dashboard">']
    for i, (href, label) in enumerate(steps):
        parts.append(f'<a href="{href}" class="guide-flow__step">{label}</a>')
        if i < len(steps) - 1:
            parts.append('<span class="guide-flow__arrow" aria-hidden="true">↓</span>')
    parts.append("</div>")
    return "\n".join(parts)


def field_table(rows: list[tuple[str, str]]) -> str:
    trs = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in rows)
    return f'<table class="field-table">{trs}</table>'


def example_box(lines: list[str]) -> str:
    ps = "".join(f"<p>{line}</p>" for line in lines)
    return f'<div class="example-box">{ps}</div>'


def faq_block(items: list[tuple[str, str]]) -> str:
    parts = ['<div class="faq-list">']
    for q, a in items:
        parts.append(
            f"""<details class="faq-item">
              <summary>{q}</summary>
              <div class="faq-answer"><p>{a}</p></div>
            </details>"""
        )
    parts.append("</div>")
    return "\n".join(parts)


def cta() -> str:
    return f"""<section class="guide-cta-block" aria-labelledby="download-cta">
          <h2 id="download-cta">Download MoneyMap Pulse</h2>
          <p>Try this tool on Android and build your financial picture step by step.</p>
          <a href="{PLAY_STORE}" class="button button-primary" rel="noopener noreferrer">Get it on Google Play</a>
        </section>"""


def build_body(slug: str, spec: dict[str, Any]) -> str:
    shot_file, shot_alt = spec["screenshot"]
    annotations = ensure_annotation_coords(spec)
    visual = interactive_annotated_screenshot(
        slug,
        spec["visual_title"],
        shot_file,
        shot_alt,
        annotations,
    )
    extra = spec.get("after_visual", "")
    return f"""<div class="container">
        <section class="guide-section">
          <h2>What this tool does</h2>
          <p>{spec["what"]}</p>
        </section>
        {visual}
        {extra}
        <section class="guide-section">
          <h2>Understanding inputs</h2>
          {spec["inputs"]}
        </section>
        <section class="guide-section">
          <h2>Understanding results</h2>
          {spec["results"]}
        </section>
        <section class="guide-section">
          <h2>Worked example</h2>
          {spec["example"]}
        </section>
        <section class="guide-section">
          <h2>Frequently asked questions</h2>
          {faq_block(spec["faqs"])}
        </section>
        {cta()}
      </div>"""


GUIDES: dict[str, dict[str, Any]] = {
    "financial-health-snapshot": {
        "title": "Financial Health Snapshot",
        "meta": "Learn how the Financial Health Snapshot dashboard brings together savings, net worth, risk profile and retirement readiness.",
        "screenshot": (
            "MoneyMapPulse_Screenshot_FinancialSnapshot_1080x1920.png",
            "Financial Health Snapshot in MoneyMap Pulse",
        ),
        "what": "The Financial Health Snapshot is your personal dashboard. It pulls saved results from other calculators into one view so you can see savings, wealth, risk and retirement readiness at a glance.",
        "visual_title": "Understanding your dashboard",
        "annotations": [
            {
                "title": "Monthly savings",
                "body": "Shows how much money remains after expenses are deducted from monthly income — your household cash surplus each month.",
                "source": "House Budget Calculator",
                "example": "£1,479 per month",
                "tip": "Higher monthly savings can improve retirement readiness and long-term wealth building.",
                "x": 27,
                "y": 45.5,
                "spot_w": 30,
                "spot_h": 4.5,
            },
            {
                "title": "Net worth",
                "body": "Your total assets minus liabilities — a snapshot of overall financial position at a point in time.",
                "source": "Net Worth Calculator",
                "example": "£300,000",
                "tip": "Update property and pension values periodically so your dashboard reflects reality.",
                "x": 73,
                "y": 45.5,
                "spot_w": 30,
                "spot_h": 4.5,
            },
            {
                "title": "Risk profile",
                "body": "Summarises the growth and volatility assumptions you chose for long-term planning.",
                "source": "Portfolio Return Calculator",
                "example": "Balanced",
                "tip": "Pick a profile you could stick with in a downturn — it shapes retirement projections.",
                "x": 27,
                "y": 57,
                "spot_w": 30,
                "spot_h": 4.5,
            },
            {
                "title": "Retirement status",
                "body": "Indicates whether projected savings at retirement are likely to meet your spending goal.",
                "source": "Retirement Calculator",
                "example": "On track",
                "tip": "If you see a shortfall, try small increases to monthly saving before changing retirement age.",
                "x": 73,
                "y": 57,
                "spot_w": 22,
                "spot_h": 3.5,
            },
        ],
        "after_visual": (
            '<section class="guide-section">'
            "<h2>Where this data comes from</h2>"
            "<p>Complete calculators in this order to populate your dashboard.</p>"
            f"{flow_diagram()}</section>"
        ),
        "inputs": "<p>You do not type into the snapshot directly. Complete and save the House Budget, Net Worth, Portfolio Return and Retirement calculators first.</p>",
        "results": "<p><strong>On track</strong> means your projected retirement fund meets or exceeds what you need. <strong>Shortfall</strong> means you may need to adjust savings, retirement age or spending assumptions. Tap a card to open its detail view.</p>",
        "example": example_box(
            [
                "<strong>Monthly savings:</strong> £1,479 (from budget)",
                "<strong>Net worth:</strong> £300,000",
                "<strong>Risk profile:</strong> Balanced",
                "<strong>Retirement:</strong> On track",
            ]
        ),
        "faqs": [
            ("Why is a dashboard card empty?", "Save results in the linked calculator first. The snapshot only shows saved data."),
            ("How often should I update my information?", "Review monthly or after any major change to income, spending, assets or retirement plans."),
            ("Can I use estimated values?", "Yes for planning. Replace estimates with actual figures when you have them."),
            ("Do I need an account?", "No. Data stays on your device."),
            ("What should count as retirement income?", "Include pensions, investments and other income you expect in retirement — only if you entered them in the Retirement Calculator."),
        ],
    },
    "house-budget-calculator": {
        "title": "House Budget Calculator",
        "meta": "Track household income, expenses and monthly savings with the House Budget Calculator.",
        "screenshot": ("MoneyMapPulse_Screenshot_Budget_1080x1920.png", "House Budget Calculator in MoneyMap Pulse"),
        "what": "The House Budget Calculator records household income and spending by category, then shows monthly savings and your savings rate.",
        "visual_title": "Understanding your budget summary",
        "annotation_source": "House Budget Calculator",
        "annotations": [
            {
                "title": "Monthly income",
                "body": "Total household income received each month before you allocate it to spending or saving.",
                "source": "House Budget Calculator",
                "example": "£5,000",
                "tip": "Use after-tax income if that is what you actually spend from each month.",
                "x": 50,
                "y": 33.5,
                "spot_w": 36,
                "spot_h": 4,
            },
            {
                "title": "Monthly expenses",
                "body": "Everything you spend in a typical month across categories such as housing, food and bills.",
                "source": "House Budget Calculator",
                "example": "£1,980",
                "tip": "Include annual costs spread monthly (insurance, subscriptions) for a fair picture.",
            },
            {
                "title": "Monthly balance",
                "body": "Income minus expenses — the amount left over to save, invest or pay down debt.",
                "source": "House Budget Calculator",
                "example": "£3,020",
                "tip": "This figure feeds Monthly savings on your Financial Health Snapshot.",
            },
            {
                "title": "Savings rate",
                "body": "The share of income you keep each month, expressed as a percentage.",
                "source": "House Budget Calculator",
                "example": "60.4%",
                "tip": "Many households aim for 10–20% as a starting goal; yours depends on goals and costs.",
            },
            {
                "title": "Expense breakdown",
                "body": "Category totals that show where money goes and where you might trim spending.",
                "source": "House Budget Calculator",
                "example": "Housing, food, transport",
                "tip": "Sort by largest categories first when looking for quick wins.",
            },
        ],
        "positions": [(50, 34), (50, 44), (50, 52), (50, 60), (50, 70)],
        "inputs": field_table(
            [
                ("Income", "Salary, benefits and other money received each month."),
                ("Expense categories", "Housing, food, transport, bills and discretionary spending."),
                ("Savings", "Automatically calculated as income minus expenses."),
            ]
        ),
        "results": "<p>Your summary feeds <strong>Monthly savings</strong> on the Financial Health Snapshot. Category totals help you spot areas to adjust.</p>",
        "example": example_box(
            [
                "<strong>Income:</strong> £5,000",
                "<strong>Expenses:</strong> £1,980",
                "<strong>Monthly balance:</strong> £3,020",
                "<strong>Savings rate:</strong> 60.4%",
            ]
        ),
        "faqs": [
            ("What is a good savings rate?", "Many planners suggest 10–20% as a starting goal, but your target depends on your goals and costs."),
            ("Should I use net or gross income?", "Use the amount you actually receive if that is how you manage cash flow."),
            ("Can I use estimated values?", "Yes. Refine categories when you have exact figures."),
            ("How often should I update my budget?", "Monthly is ideal; at minimum after income or major expense changes."),
            ("What if my expenses exceed income?", "The calculator will show a negative balance — a signal to review spending or income."),
        ],
    },
    "mortgage-calculator": {
        "title": "Mortgage Calculator",
        "meta": "Estimate mortgage payments, interest and loan-to-value with the Mortgage Calculator.",
        "screenshot": ("MoneyMapPulse_Screenshot_Mortgage_1080x1920.png", "Mortgage Calculator in MoneyMap Pulse"),
        "what": "Estimates repayment and interest-only payments plus loan-to-value (LTV) from property value, deposit, rate and term.",
        "visual_title": "Understanding your mortgage results",
        "annotation_source": "Mortgage Calculator",
        "annotations": [
            {
                "title": "Property value",
                "body": "The purchase price or current market value used to size your loan.",
                "source": "Mortgage Calculator",
                "example": "£350,000",
                "tip": "Use a realistic valuation — overstating it can underestimate your deposit need.",
                "x": 50,
                "y": 32,
            },
            {
                "title": "Deposit",
                "body": "Cash you contribute upfront; it reduces the amount you need to borrow.",
                "source": "Mortgage Calculator",
                "example": "£70,000",
                "tip": "A larger deposit often improves loan-to-value and illustrative rate scenarios.",
                "x": 50,
                "y": 42,
            },
            {
                "title": "Mortgage amount",
                "body": "Property value minus deposit — the principal you would repay over the term.",
                "source": "Mortgage Calculator",
                "example": "£280,000",
                "tip": "Compare this with your Net Worth liabilities for a full debt picture.",
                "x": 50,
                "y": 50,
            },
            {
                "title": "Monthly payment",
                "body": "Illustrative repayment based on rate, term and amount borrowed.",
                "source": "Mortgage Calculator",
                "example": "See app estimate",
                "tip": "Check the payment fits your House Budget before treating it as affordable.",
                "x": 50,
                "y": 59,
                "spot_w": 40,
                "spot_h": 4.5,
            },
            {
                "title": "LTV ratio",
                "body": "Loan as a percentage of property value — a common shorthand for equity and risk.",
                "source": "Mortgage Calculator",
                "example": "80% LTV",
                "tip": "Below 80% LTV is a common planning benchmark; real products vary.",
                "x": 50,
                "y": 70,
            },
        ],
        "inputs": field_table(
            [
                ("Property value", "Purchase price or current value."),
                ("Deposit", "Cash you contribute upfront."),
                ("Interest rate", "Annual rate for illustration."),
                ("Mortgage term", "Loan length in years."),
            ]
        ),
        "results": "<p>Compare the monthly payment with your House Budget. LTV helps you understand equity — lower LTV often attracts better rates in real lending, but this tool only estimates.</p>",
        "example": example_box(
            [
                "<strong>Property value:</strong> £350,000",
                "<strong>Deposit:</strong> £70,000",
                "<strong>Mortgage amount:</strong> £280,000",
                "<strong>Monthly payment:</strong> See app estimate",
                "<strong>LTV:</strong> 80%",
            ]
        ),
        "faqs": [
            ("Is this a mortgage offer?", "No. Figures are for planning only, not lending advice."),
            ("Does it include fees?", "Add stamp duty, legal fees and insurance separately."),
            ("Can I use estimated property values?", "Yes for early planning."),
            ("What is a good LTV?", "Below 80% is common for better rates, but products vary."),
            ("How often should I recalculate?", "When rates, property value or deposit plans change."),
        ],
    },
    "investment-calculator": {
        "title": "Investment Calculator",
        "meta": "Project future investment value from lump sums and monthly contributions.",
        "screenshot": ("MoneyMapPulse_Screenshot_Investment_1080x1920.png", "Investment Calculator in MoneyMap Pulse"),
        "what": "Projects how an investment might grow using a starting amount, monthly contributions, expected return and time horizon.",
        "visual_title": "Understanding your investment projection",
        "annotation_source": "Investment Calculator",
        "annotations": [
            {
                "title": "Initial investment",
                "body": "The lump sum you start with today before any future contributions.",
                "source": "Investment Calculator",
                "example": "£10,000",
                "tip": "Include pensions or ISAs only if they match how you model this scenario.",
            },
            {
                "title": "Monthly contributions",
                "body": "Regular amounts added each month — often the biggest driver of long-term growth.",
                "source": "Investment Calculator",
                "example": "£500",
                "tip": "Align this with your House Budget monthly balance where possible.",
            },
            {
                "title": "Future value",
                "body": "Projected total at the end of your time horizon using your return assumption.",
                "source": "Investment Calculator",
                "example": "£583,242",
                "tip": "Run a lower return scenario to stress-test optimistic assumptions.",
            },
            {
                "title": "Investment growth",
                "body": "Return above what you paid in — illustrates compounding, not a guarantee.",
                "source": "Investment Calculator",
                "example": "Growth vs contributions",
                "tip": "Markets fluctuate; use this for planning ranges, not predictions.",
            },
        ],
        "positions": [(50, 35), (50, 45), (50, 55), (50, 65)],
        "inputs": field_table(
            [
                ("Initial investment", "Lump sum at the start."),
                ("Monthly contributions", "Regular additions."),
                ("Expected return", "Annual growth assumption."),
                ("Time horizon", "Years you stay invested."),
            ]
        ),
        "results": "<p><strong>Future value</strong> is the projected total. <strong>Investment growth</strong> is future value minus what you contributed. Milestone years help you see progress over time.</p>",
        "example": example_box(
            [
                "<strong>Initial:</strong> £10,000",
                "<strong>Monthly:</strong> £500",
                "<strong>Return:</strong> 6% per year",
                "<strong>Horizon:</strong> 16 years",
                "<strong>Future value:</strong> £583,242 (illustrative)",
            ]
        ),
        "faqs": [
            ("Will I achieve this return?", "No projection is guaranteed. Markets go up and down."),
            ("Can I use estimated values?", "Yes — try conservative and optimistic scenarios."),
            ("Does this include tax?", "Treat results as simplified unless you model tax separately."),
            ("What return should I assume?", "Many beginners use a modest long-term figure; the Portfolio Return Calculator can help."),
            ("How often should I update?", "Yearly or when your contribution plan changes."),
        ],
    },
    "portfolio-return-calculator": {
        "title": "Portfolio Return Calculator",
        "meta": "Estimate inflation-adjusted returns and choose a risk profile for planning.",
        "screenshot": (
            "MoneyMapPulse_Screenshot_PortfolioReturn_1080x1920.png",
            "Portfolio Return Calculator in MoneyMap Pulse",
        ),
        "what": "Explores expected returns and risk levels so retirement and investment assumptions feel realistic.",
        "visual_title": "Understanding portfolio assumptions",
        "annotation_source": "Portfolio Return Calculator",
        "annotations": [
            {
                "title": "Risk profile",
                "body": "A planning label for how much short-term volatility you are willing to accept.",
                "source": "Portfolio Return Calculator",
                "example": "Balanced",
                "tip": "This profile appears on your Financial Health Snapshot once saved.",
            },
            {
                "title": "Expected return",
                "body": "Illustrative annual growth before inflation — tied to your chosen profile.",
                "source": "Portfolio Return Calculator",
                "example": "6% per year",
                "tip": "Use conservative figures when testing retirement shortfalls.",
            },
            {
                "title": "Inflation",
                "body": "Assumed rise in living costs — erodes what future pounds can buy.",
                "source": "Portfolio Return Calculator",
                "example": "2.5%",
                "tip": "Even modest inflation matters over 20–30 year horizons.",
            },
            {
                "title": "Real return",
                "body": "Expected return after inflation — better reflects purchasing power over time.",
                "source": "Portfolio Return Calculator",
                "example": "~3.5% real",
                "tip": "Retirement projections are more meaningful when built on real returns.",
            },
        ],
        "positions": [(50, 36), (50, 46), (50, 56), (50, 66)],
        "inputs": field_table(
            [
                ("Risk profile", "Summary of how much volatility you accept on paper."),
                ("Asset mix", "Split across cash, bonds and shares where shown."),
                ("Inflation", "Reduces purchasing power over time."),
            ]
        ),
        "results": "<p>Your selected <strong>risk profile</strong> appears on the Financial Health Snapshot. Use <strong>real return</strong> when judging whether retirement projections are ambitious or cautious.</p>",
        "example": example_box(
            [
                "<strong>Profile:</strong> Balanced",
                "<strong>Expected return:</strong> 6%",
                "<strong>Inflation:</strong> 2.5%",
                "<strong>Real return:</strong> ~3.5% (illustrative)",
            ]
        ),
        "faqs": [
            ("Is this investment advice?", "No. It is an educational planning aid."),
            ("Which risk profile should I pick?", "Choose one that matches how much short-term fluctuation you could tolerate."),
            ("Can I change profile later?", "Yes. Update and refresh your snapshot."),
            ("Why adjust for inflation?", "Retirement spending in 20 years will not buy the same as today."),
            ("How often should I review?", "When your goals or comfort with risk changes."),
        ],
    },
    "retirement-calculator": {
        "title": "Retirement Calculator",
        "meta": "Review retirement projections, journey checkpoints and whether you are on track.",
        "screenshot": ("MoneyMapPulse_Screenshot_Retirement_1080x1920.png", "Retirement projection in MoneyMap Pulse"),
        "what": "Projects your retirement fund, what you will need, journey checkpoints and whether you are on track or facing a shortfall.",
        "visual_title": "Understanding your retirement journey",
        "annotation_source": "Retirement Calculator",
        "annotations": [
            {
                "title": "What you'll have",
                "body": "Estimated pot at your chosen retirement age from savings, contributions and growth assumptions.",
                "source": "Retirement Calculator",
                "example": "£1,092,666",
                "tip": "Refresh when pension statements arrive or your contribution rate changes.",
                "x": 50,
                "y": 27,
                "spot_w": 44,
                "spot_h": 4.5,
            },
            {
                "title": "What you'll need",
                "body": "Target fund implied by how much monthly income you want in retirement and for how long.",
                "source": "Retirement Calculator",
                "example": "£1,085,649",
                "tip": "Small changes to spending assumptions can shift this number significantly.",
                "x": 50,
                "y": 37,
                "spot_w": 44,
                "spot_h": 4.5,
            },
            {
                "title": "Retirement journey",
                "body": "A timeline from today through retirement and later life — connects habits now with outcomes later.",
                "source": "Retirement Calculator",
                "example": "Today → Retirement → Age 100",
                "tip": "Use milestones to see whether steady saving closes any gap over time.",
                "x": 50,
                "y": 50,
                "spot_w": 48,
                "spot_h": 7,
            },
            {
                "title": "Today",
                "body": "Your current age, savings and monthly contributions — the starting point for every projection.",
                "source": "Retirement Calculator",
                "example": "Age 43",
                "tip": "Accurate starting balances make the journey view more trustworthy.",
                "x": 50,
                "y": 61,
                "spot_w": 36,
                "spot_h": 4,
            },
            {
                "title": "Retirement",
                "body": "Checkpoint at retirement age: projected fund, income need and on-track or shortfall status.",
                "source": "Retirement Calculator",
                "example": "Age 65",
                "tip": "Feeds Retirement status on your Financial Health Snapshot when saved.",
                "x": 50,
                "y": 71,
                "spot_w": 36,
                "spot_h": 4,
            },
        ],
        "inputs": field_table(
            [
                ("Current savings", "Pensions and investments today."),
                ("Monthly saving", "Contributions until retirement."),
                ("Retirement age", "When you plan to retire."),
                ("Retirement spending", "Monthly income needed in retirement."),
                ("Return assumption", "Growth rate used in projections."),
            ]
        ),
        "results": "<p><strong>On track</strong> means projected assets meet required fund. <strong>Shortfall</strong> suggests reviewing savings, retirement age or spending. The journey view links today’s habits to retirement and later years.</p>",
        "example": example_box(
            [
                "<strong>What you'll have:</strong> £1,092,666",
                "<strong>What you'll need:</strong> £1,085,649",
                "<strong>Status:</strong> On track",
                "<strong>Ahead by:</strong> £7,017",
            ]
        ),
        "faqs": [
            ("What should count as retirement income?", "Include workplace pensions, private pensions, investments and other sources you expect."),
            ("Does this include State Pension?", "Only if you add it in your inputs."),
            ("Can I use estimated values?", "Yes — refine as you get pension statements."),
            ("What if I have a shortfall?", "Try higher savings, later retirement or lower spending assumptions in the calculator."),
            ("How often should I update?", "At least yearly, or after a pay rise, bonus or major life change."),
        ],
    },
    "net-worth-calculator": {
        "title": "Net Worth Calculator",
        "meta": "Calculate assets, liabilities and track your net worth over time.",
        "screenshot": ("MoneyMapPulse_Screenshot_NetWorth_1080x1920.png", "Net Worth Calculator in MoneyMap Pulse"),
        "what": "Adds up what you own and what you owe, then calculates net worth and optional context such as wealth percentile.",
        "visual_title": "Understanding your net worth",
        "annotation_source": "Net Worth Calculator",
        "annotations": [
            {
                "title": "Assets",
                "body": "Everything you own with material value — property, cash, investments and pensions.",
                "source": "Net Worth Calculator",
                "example": "£550,000",
                "tip": "Use realistic valuations; estimates are fine until you have formal figures.",
                "x": 50,
                "y": 38,
            },
            {
                "title": "Liabilities",
                "body": "Debts you owe, including mortgages, loans and credit balances.",
                "source": "Net Worth Calculator",
                "example": "£250,000",
                "tip": "Include all major debts so net worth is not overstated.",
                "x": 50,
                "y": 48,
            },
            {
                "title": "Net worth",
                "body": "Assets minus liabilities — your headline wealth number at a point in time.",
                "source": "Net Worth Calculator",
                "example": "£300,000",
                "tip": "This value powers the Net worth tile on your Financial Health Snapshot.",
                "x": 50,
                "y": 57.5,
                "spot_w": 38,
                "spot_h": 4.5,
            },
            {
                "title": "Wealth percentile",
                "body": "Illustrative context for how your net worth compares to UK households — not a goal to chase.",
                "source": "Net Worth Calculator",
                "example": "Context band",
                "tip": "Focus on your own trend over time rather than the percentile alone.",
                "x": 50,
                "y": 68,
            },
        ],
        "inputs": field_table(
            [
                ("Assets", "Property, savings, investments, pensions, vehicles, etc."),
                ("Liabilities", "Mortgages, loans and credit balances."),
                ("Valuations", "Use realistic current values, even if estimated."),
            ]
        ),
        "results": "<p>Net worth feeds your Financial Health Snapshot. Track liquid vs illiquid assets where shown to see what is accessible quickly.</p>",
        "example": example_box(
            [
                "<strong>Assets:</strong> £550,000",
                "<strong>Liabilities:</strong> £250,000",
                "<strong>Net worth:</strong> £300,000",
            ]
        ),
        "faqs": [
            ("What should I include as assets?", "Include major items: home equity, savings, investments and pensions. Skip small household goods unless material."),
            ("Should I include my home?", "Include it for a full picture, or track a version without property if you prefer."),
            ("Can I use estimated values?", "Yes. Update when you have formal valuations."),
            ("How often should I update?", "Every few months or after buying property, paying off debt or large investments."),
            ("What is wealth percentile?", "A rough comparison for context — not a ranking you need to optimise."),
        ],
    },
    "buy-to-let-calculator": {
        "title": "Buy To Let Calculator",
        "meta": "Evaluate rental property using cash flow, ROI and yield estimates.",
        "screenshot": ("MoneyMapPulse_Screenshot_BuyToLet_1080x1920.png", "Buy To Let summary in MoneyMap Pulse"),
        "what": "Estimates rent, costs, mortgage, net income, yield and ROI for a rental property scenario.",
        "visual_title": "Understanding your property investment",
        "annotation_source": "Buy To Let Calculator",
        "annotations": [
            {
                "title": "Property value",
                "body": "Purchase price used to size rent, yield and how much capital the deal ties up.",
                "source": "Buy To Let Calculator",
                "example": "£250,000",
                "tip": "Stress-test with conservative valuations if the market is uncertain.",
                "x": 50,
                "y": 30,
            },
            {
                "title": "Rent",
                "body": "Expected monthly rental income before costs and tax.",
                "source": "Buy To Let Calculator",
                "example": "£1,250 per month",
                "tip": "Use local letting research and allow for void periods.",
                "x": 50,
                "y": 40,
            },
            {
                "title": "Expenses",
                "body": "Running costs such as maintenance, insurance, agents and mortgage interest.",
                "source": "Buy To Let Calculator",
                "example": "Monthly cost total",
                "tip": "Under-estimating maintenance is a common reason projections look too rosy.",
                "x": 50,
                "y": 48,
            },
            {
                "title": "Monthly net income",
                "body": "Cash left each month after expenses — your day-to-day cash-flow result.",
                "source": "Buy To Let Calculator",
                "example": "£362.50",
                "tip": "Compare with other uses of the same deposit in your wider plan.",
                "x": 50,
                "y": 57.5,
                "spot_w": 40,
                "spot_h": 4.5,
            },
            {
                "title": "Yield",
                "body": "Rental income relative to property price — useful for comparing listings.",
                "source": "Buy To Let Calculator",
                "example": "6.00% gross",
                "tip": "Gross yield ignores costs; pair it with net income for decisions.",
                "x": 50,
                "y": 66,
            },
            {
                "title": "ROI",
                "body": "Return on the cash you put in, accounting for income and equity deployed.",
                "source": "Buy To Let Calculator",
                "example": "4.44%",
                "tip": "ROI answers whether the deal rewards your deposit — not just the property price.",
                "x": 50,
                "y": 74,
            },
        ],
        "inputs": field_table(
            [
                ("Property value", "Price you pay or expect to pay."),
                ("Deposit / cash invested", "Your equity in the deal."),
                ("Rent and expenses", "Income and running costs."),
                ("Mortgage", "Monthly payment if financed."),
            ]
        ),
        "results": "<p>Focus on <strong>monthly net income</strong> for cash flow, <strong>yield</strong> for rent vs price, and <strong>ROI</strong> for return on cash invested. Compare with other uses of the same capital.</p>",
        "example": example_box(
            [
                "<strong>Monthly net income:</strong> £362.50",
                "<strong>Annual net income:</strong> £4,350",
                "<strong>ROI:</strong> 4.44%",
                "<strong>Gross yield:</strong> 6.00%",
            ]
        ),
        "faqs": [
            ("Does this include tax?", "Rental tax is not advice here — plan separately with a qualified professional."),
            ("Can I use estimated rent?", "Yes. Use local letting agent guides or conservative figures."),
            ("What expenses should I include?", "Insurance, maintenance, void periods, agent fees and mortgage interest."),
            ("Is yield or ROI more important?", "Use both: yield compares rent to price; ROI compares profit to cash you put in."),
            ("How often should I update?", "When purchase price, rent or mortgage assumptions change."),
        ],
    },
}


def main() -> None:
    for slug, spec in GUIDES.items():
        body = build_body(slug, spec)
        html = shell(spec["title"], spec["meta"], slug, body)
        out_dir = ROOT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        print("wrote", out_dir / "index.html")


if __name__ == "__main__":
    main()
