#!/usr/bin/env python3
"""Generate static guide pages with AnnotatedScreenshot visual guides."""

from __future__ import annotations

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
</body>
</html>
"""


def annotated_screenshot(
    visual_title: str,
    img_file: str,
    img_alt: str,
    annotations: list[dict[str, str]],
    positions: list[tuple[float, float]],
    single_col_callouts: bool = False,
) -> str:
    markers = []
    for i, (left, top) in enumerate(positions, start=1):
        markers.append(
            f'<span class="annotated-shot__marker" style="left:{left}%;top:{top}%;" '
            f'aria-hidden="true"><span class="annotated-shot__marker-inner">{i}</span></span>'
        )
    callouts = []
    for i, ann in enumerate(annotations, start=1):
        example = ann.get("example")
        ex_html = (
            f'<p class="annotated-callout__example"><strong>Example:</strong> {example}</p>'
            if example
            else ""
        )
        callouts.append(
            f"""<article class="annotated-callout" id="annotation-{i}">
              <span class="annotated-callout__num" aria-hidden="true">{i}</span>
              <div>
                <h3>{ann["title"]}</h3>
                <p>{ann["body"]}</p>
                {ex_html}
              </div>
            </article>"""
        )
    col_class = " annotated-callouts--single-col" if single_col_callouts else ""
    return f"""<section class="annotated-shot" aria-labelledby="visual-guide-title">
        <div class="container">
          <h2 class="annotated-shot__title" id="visual-guide-title">{visual_title}</h2>
          <div class="annotated-shot__stage">
            <img class="annotated-shot__img" src="../assets/screenshots/{img_file}" alt="{img_alt}" width="1080" height="1920" loading="lazy">
            {"".join(markers)}
          </div>
          <div class="annotated-callouts{col_class}">
            {"".join(callouts)}
          </div>
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


def build_body(spec: dict[str, Any]) -> str:
    shot_file, shot_alt = spec["screenshot"]
    visual = annotated_screenshot(
        spec["visual_title"],
        shot_file,
        shot_alt,
        spec["annotations"],
        spec["positions"],
        spec.get("single_col_callouts", False),
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
                "body": "From the House Budget Calculator. Income minus expenses.",
                "example": "£1,479 per month",
            },
            {
                "title": "Net worth",
                "body": "From the Net Worth Calculator. Assets minus liabilities.",
                "example": "£300,000",
            },
            {
                "title": "Risk profile",
                "body": "From the Portfolio Return Calculator. Conservative, Balanced or Aggressive.",
                "example": "Balanced",
            },
            {
                "title": "Retirement status",
                "body": "From the Retirement Calculator. Displays On track or Shortfall.",
                "example": "On track",
            },
        ],
        "positions": [(48, 42), (48, 52), (48, 62), (48, 72)],
        "after_visual": (
            '<section class="guide-section">'
            "<h2>How calculators connect</h2>"
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
        "annotations": [
            {"title": "Monthly income", "body": "Total monthly household income.", "example": "£5,000"},
            {"title": "Monthly expenses", "body": "Total monthly spending.", "example": "£1,980"},
            {"title": "Monthly balance", "body": "Remaining monthly amount after expenses.", "example": "£3,020"},
            {"title": "Savings rate", "body": "Percentage of income saved each month.", "example": "60.4%"},
            {
                "title": "Expense breakdown",
                "body": "Shows where spending occurs. Helps identify improvement opportunities.",
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
        "annotations": [
            {"title": "Mortgage amount", "body": "Property value minus deposit."},
            {"title": "Monthly payment", "body": "Estimated repayment mortgage payment."},
            {"title": "Interest only", "body": "Monthly interest cost only (not suitable for all products)."},
            {
                "title": "Loan to value",
                "body": "Mortgage amount divided by property value. Higher LTV generally means higher borrowing risk.",
                "example": "80% LTV",
            },
        ],
        "positions": [(50, 36), (50, 46), (50, 56), (50, 66)],
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
        "annotations": [
            {"title": "Initial investment", "body": "Amount invested today.", "example": "£10,000"},
            {"title": "Monthly contributions", "body": "Regular monthly investing.", "example": "£500"},
            {"title": "Future value", "body": "Estimated portfolio value at the end of the period.", "example": "£583,242"},
            {"title": "Investment growth", "body": "Growth generated by investment returns (not guaranteed)."},
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
        "annotations": [
            {"title": "Risk profile", "body": "Conservative, Balanced or Aggressive.", "example": "Balanced"},
            {"title": "Expected return", "body": "Projected annual investment return before inflation."},
            {"title": "Inflation", "body": "Expected long-term inflation."},
            {
                "title": "Real return",
                "body": "Expected return minus inflation. Real return feeds long-term retirement planning.",
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
        "annotations": [
            {"title": "What you'll have", "body": "Projected retirement fund at your target age.", "example": "£1,092,666"},
            {"title": "What you'll need", "body": "Required retirement amount based on your assumptions.", "example": "£1,085,649"},
            {"title": "Retirement journey", "body": "Timeline from today through retirement and later ages."},
            {"title": "Retirement status", "body": "Shows On track or Shortfall."},
            {"title": "Checkpoints", "body": "Progress milestones throughout your retirement planning journey."},
        ],
        "positions": [(50, 30), (50, 40), (50, 50), (50, 60), (50, 70)],
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
        "annotations": [
            {"title": "Total assets", "body": "Everything you own.", "example": "£550,000"},
            {"title": "Total liabilities", "body": "Everything you owe.", "example": "£250,000"},
            {"title": "Net worth", "body": "Assets minus liabilities.", "example": "£300,000"},
            {
                "title": "Wealth percentile",
                "body": "Estimated position relative to UK households (illustrative context only).",
            },
        ],
        "positions": [(50, 38), (50, 48), (50, 58), (50, 68)],
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
        "annotations": [
            {"title": "Property value", "body": "Purchase price of the property."},
            {"title": "Monthly rent", "body": "Expected rental income each month."},
            {"title": "Monthly expenses", "body": "Running costs including maintenance and management."},
            {"title": "Monthly net income", "body": "Monthly profit after costs.", "example": "£362.50"},
            {"title": "Yield", "body": "Rental return relative to property value.", "example": "6.00% gross"},
            {"title": "ROI", "body": "Return on invested capital.", "example": "4.44%"},
        ],
        "positions": [(50, 32), (50, 42), (50, 50), (50, 58), (50, 66), (50, 74)],
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
        body = build_body(spec)
        html = shell(spec["title"], spec["meta"], slug, body)
        out_dir = ROOT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        print("wrote", out_dir / "index.html")


if __name__ == "__main__":
    main()
