#!/usr/bin/env python3
"""Generate static guide pages for MoneyMap Pulse calculators."""

from pathlib import Path

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


def hero_img(file: str, alt: str) -> str:
    return f"""<figure class="guide-hero-media">
            <img src="../assets/screenshots/{file}" alt="{alt}" width="1080" height="1920" loading="lazy">
          </figure>"""


def cta() -> str:
    return f"""<section class="guide-cta-block" aria-labelledby="download-cta">
          <h2 id="download-cta">Download MoneyMap Pulse</h2>
          <p>Try this tool on Android and build your financial picture step by step.</p>
          <a href="{PLAY_STORE}" class="button button-primary" rel="noopener noreferrer">Get it on Google Play</a>
        </section>"""


def faq_block(items: list[tuple[str, str]]) -> str:
    parts = ['<div class="faq-list">']
    for q, a in items:
        parts.append(f"""<details class="faq-item">
              <summary>{q}</summary>
              <div class="faq-answer"><p>{a}</p></div>
            </details>""")
    parts.append("</div>")
    return "\n".join(parts)


GUIDES: dict[str, dict] = {}


def register(slug: str, **kwargs):
    GUIDES[slug] = kwargs


register(
    "financial-health-snapshot",
    title="Financial Health Snapshot",
    meta="Learn how the Financial Health Snapshot dashboard brings together savings, net worth, risk profile and retirement readiness.",
    screenshot=("MoneyMapPulse_Screenshot_FinancialSnapshot_1080x1920.png", "Financial Health Snapshot in MoneyMap Pulse"),
    content="""
      <div class="container">
        <section class="guide-section">
          <h2>What this tool does</h2>
          <p>The Financial Health Snapshot is your personal dashboard in MoneyMap Pulse. It summarises key numbers from your calculators so you can see how you are doing without opening every tool separately.</p>
        </section>
        <section class="guide-section">
          <h2>Why it is useful</h2>
          <p>Budgeting, net worth, investments and retirement can feel disconnected. The snapshot connects them in one view so you can spot gaps, confirm progress and decide what to work on next.</p>
        </section>
        <section class="guide-section">
          <h2>How to complete the calculator</h2>
          <p>You do not enter data directly on the snapshot screen. Complete the calculators below, save your results, then open your profile or home dashboard to refresh the snapshot.</p>
          <ol>
            <li>Run the House Budget Calculator and save your budget.</li>
            <li>Complete the Net Worth Calculator with assets and liabilities.</li>
            <li>Use the Portfolio Return Calculator to choose a risk profile.</li>
            <li>Run the Retirement Calculator and save your projection.</li>
            <li>Return to the Financial Health Snapshot to review summary cards.</li>
          </ol>
        </section>
        <section class="guide-section">
          <h2>What each summary card means</h2>
          <table class="field-table">
            <tr><th>Monthly savings</th><td>Leftover income after expenses for the month. Pulled from your saved House Budget.</td></tr>
            <tr><th>Net worth</th><td>Total assets minus total liabilities. Pulled from your saved Net Worth calculation.</td></tr>
            <tr><th>Risk profile</th><td>Your selected planning profile (for example Balanced). Pulled from the Portfolio Return Calculator.</td></tr>
            <tr><th>Retirement status</th><td>Whether your projected fund meets your required fund. Pulled from the Retirement Calculator.</td></tr>
          </table>
        </section>
        <section class="guide-section">
          <h2>Where dashboard data comes from</h2>
          <ul class="source-list">
            <li><strong>Monthly savings</strong> — House Budget Calculator</li>
            <li><strong>Net worth</strong> — Net Worth Calculator</li>
            <li><strong>Risk profile</strong> — Portfolio Return Calculator</li>
            <li><strong>Retirement</strong> — Retirement Calculator</li>
          </ul>
        </section>
        <section class="guide-section">
          <h2>Understanding your results</h2>
          <p><strong>On track</strong> means your projected retirement fund meets or exceeds the fund you need based on your assumptions. <strong>Shortfall</strong> means the projection falls below what is required — you may want to adjust savings, retirement age or spending assumptions in the Retirement Calculator.</p>
          <p>Tap any summary card to open the related detail view (budget breakdown, net worth list, risk profile notes or retirement projection).</p>
        </section>
        <section class="guide-section">
          <h2>Frequently asked questions</h2>
          """ + faq_block([
        ("Why is a card empty?", "The snapshot shows saved calculator results. Open the linked calculator, enter your figures and save."),
        ("Do I need an account?", "No. Data stays on your device. Saving within the app links calculators to your snapshot."),
        ("How often should I update?", "Update whenever your income, expenses, assets or retirement assumptions change."),
    ]) + """
        </section>
        """ + cta() + """
      </div>
    """,
)

register(
    "house-budget-calculator",
    title="House Budget Calculator",
    meta="Track household income, expenses and monthly savings with the House Budget Calculator.",
    screenshot=("MoneyMapPulse_Screenshot_Budget_1080x1920.png", "House Budget Calculator in MoneyMap Pulse"),
    content="""
      <div class="container">
        <section class="guide-section"><h2>What this tool does</h2>
          <p>The House Budget Calculator helps you record income and spending by category, then shows how much you save each month and your savings rate.</p></section>
        <section class="guide-section"><h2>Why it is useful</h2>
          <p>Knowing your monthly savings is the foundation for retirement planning, investments and your Financial Health Snapshot. It turns everyday spending into a clear cash-flow picture.</p></section>
        <section class="guide-section"><h2>How to complete the calculator</h2>
          <ol><li>Open Financial Calculators and choose House Budget.</li>
          <li>Enter all income sources for the household.</li>
          <li>Enter expenses in each category that applies to you.</li>
          <li>Review totals and save your budget.</li></ol></section>
        <section class="guide-section"><h2>Input fields explained</h2>
          <table class="field-table">
            <tr><th>Income</th><td>Money coming in each month (salary, self-employment, benefits, rent received, etc.).</td></tr>
            <tr><th>Expenses</th><td>Money going out, grouped into categories such as housing, transport, food and leisure.</td></tr>
            <tr><th>Savings</th><td>Income minus expenses — what is left at the end of the month.</td></tr>
            <tr><th>Savings rate</th><td>Savings divided by income, shown as a percentage.</td></tr>
          </table></section>
        <section class="guide-section"><h2>Worked example</h2>
          <div class="example-box">
            <p><strong>Income:</strong> £4,700</p>
            <p><strong>Expenses:</strong> £3,221</p>
            <p><strong>Savings:</strong> £1,479</p>
            <p><strong>Savings rate:</strong> 31.5%</p>
          </div></section>
        <section class="guide-section"><h2>Understanding your results</h2>
          <p>The summary shows whether your plan is sustainable and feeds <strong>Monthly savings</strong> on your Financial Health Snapshot. Use category totals to see where you might adjust spending.</p></section>
        <section class="guide-section"><h2>Frequently asked questions</h2>
          """ + faq_block([
        ("Should I use net or gross income?", "Use the amount that actually lands in your account if that is how you plan day to day."),
        ("Can I budget monthly if I am paid weekly?", "Yes. Enter typical monthly totals or average your weekly figures across a month."),
    ]) + """</section>""" + cta() + """</div>""",
)

register(
    "mortgage-calculator",
    title="Mortgage Calculator",
    meta="Estimate mortgage payments, interest and loan-to-value with the Mortgage Calculator.",
    screenshot=("MoneyMapPulse_Screenshot_Mortgage_1080x1920.png", "Mortgage Calculator in MoneyMap Pulse"),
    content="""
      <div class="container">
        <section class="guide-section"><h2>What this tool does</h2>
          <p>Estimates monthly mortgage payments, interest-only payments and loan-to-value (LTV) based on property value, deposit, rate and term.</p></section>
        <section class="guide-section"><h2>Why it is useful</h2>
          <p>Before you buy or remortgage, you can test whether a payment fits your household budget and how deposit size affects borrowing.</p></section>
        <section class="guide-section"><h2>How to complete the calculator</h2>
          <ol><li>Open the Mortgage Calculator from the hub.</li>
          <li>Enter property value and deposit.</li>
          <li>Enter interest rate and mortgage term in years.</li>
          <li>Review repayment and interest-only results.</li></ol></section>
        <section class="guide-section"><h2>Input fields explained</h2>
          <table class="field-table">
            <tr><th>Property value</th><td>Price of the home you are buying or current value for remortgage planning.</td></tr>
            <tr><th>Deposit</th><td>Cash you put down. Mortgage amount is usually value minus deposit.</td></tr>
            <tr><th>Mortgage amount</th><td>Amount borrowed (often calculated automatically).</td></tr>
            <tr><th>Interest rate</th><td>Annual rate for illustration — use a rate you expect, not a guaranteed offer.</td></tr>
            <tr><th>Mortgage term</th><td>Length of the loan in years (for example 25 or 30).</td></tr>
          </table></section>
        <section class="guide-section"><h2>Worked example</h2>
          <div class="example-box">
            <p><strong>Property value:</strong> £350,000</p>
            <p><strong>Deposit:</strong> £70,000</p>
            <p><strong>Mortgage amount:</strong> £280,000</p>
            <p><strong>Interest rate:</strong> 4.5%</p>
            <p><strong>Term:</strong> 25 years</p>
            <p><strong>Monthly payment (repayment):</strong> illustrative figure shown in app</p>
            <p><strong>LTV:</strong> 80%</p>
          </div></section>
        <section class="guide-section"><h2>Understanding your results</h2>
          <p><strong>Monthly payment</strong> is your estimated repayment mortgage cost. <strong>Interest only</strong> shows payments if you paid interest alone (not suitable for all products). <strong>LTV ratio</strong> helps you see how much equity you have — lower LTV often means better rates in real lending, but this app only estimates.</p></section>
        <section class="guide-section"><h2>Frequently asked questions</h2>
          """ + faq_block([
        ("Is this a mortgage offer?", "No. Figures are estimates for planning, not lending advice."),
        ("Does it include fees or insurance?", "Only what you enter. Add stamp duty, fees and insurance separately in your budget."),
    ]) + """</section>""" + cta() + """</div>""",
)

register(
    "investment-calculator",
    title="Investment Calculator",
    meta="Project future investment value from lump sums and monthly contributions.",
    screenshot=("MoneyMapPulse_Screenshot_Investment_1080x1920.png", "Investment projection in MoneyMap Pulse"),
    content="""
      <div class="container">
        <section class="guide-section"><h2>What this tool does</h2>
          <p>Projects how savings might grow over time using an initial amount, regular contributions, expected return and time horizon.</p></section>
        <section class="guide-section"><h2>Why it is useful</h2>
          <p>Helps you set realistic expectations for long-term goals and compare different contribution levels — without promising actual market performance.</p></section>
        <section class="guide-section"><h2>How to complete the calculator</h2>
          <ol><li>Open Investment Calculator.</li>
          <li>Enter initial investment and monthly contribution.</li>
          <li>Set expected annual return and investment period.</li>
          <li>Choose contribution timing if shown (start or end of month).</li>
          <li>Review future value and milestone projections.</li></ol></section>
        <section class="guide-section"><h2>Input fields explained</h2>
          <table class="field-table">
            <tr><th>Initial investment</th><td>Lump sum already invested or starting balance.</td></tr>
            <tr><th>Monthly contributions</th><td>Amount you plan to add each month.</td></tr>
            <tr><th>Expected return</th><td>Annual growth rate assumption — not a guarantee.</td></tr>
            <tr><th>Time horizon</th><td>Number of years you plan to stay invested.</td></tr>
          </table></section>
        <section class="guide-section"><h2>Worked example</h2>
          <div class="example-box">
            <p><strong>Initial investment:</strong> £10,000</p>
            <p><strong>Monthly contributions:</strong> £500</p>
            <p><strong>Expected return:</strong> 6% per year</p>
            <p><strong>Time horizon:</strong> 20 years</p>
            <p><strong>Future value:</strong> shown in app (illustrative)</p>
            <p><strong>Total contributions:</strong> £130,000</p>
            <p><strong>Investment growth:</strong> future value minus contributions</p>
          </div></section>
        <section class="guide-section"><h2>Understanding your results</h2>
          <p><strong>Future value</strong> is the projected balance at the end of the period. <strong>Total contributions</strong> is what you paid in. <strong>Investment growth</strong> is the projected gain. Reference milestones (5, 10, 15 years) help you see progress along the way.</p></section>
        <section class="guide-section"><h2>Frequently asked questions</h2>
          """ + faq_block([
        ("Will I really get this return?", "No projection is guaranteed. Markets vary; use conservative assumptions."),
        ("Does this include tax?", "Unless you add tax assumptions elsewhere, treat results as before-tax illustrations."),
    ]) + """</section>""" + cta() + """</div>""",
)

register(
    "portfolio-return-calculator",
    title="Portfolio Return Calculator",
    meta="Estimate inflation-adjusted returns and choose a risk profile for planning.",
    screenshot=("MoneyMapPulse_Screenshot_PortfolioReturn_1080x1920.png", "Portfolio Return Calculator in MoneyMap Pulse"),
    content="""
      <div class="container">
        <section class="guide-section"><h2>What this tool does</h2>
          <p>Helps you explore expected portfolio returns based on asset mix or risk level, often with inflation in mind, so planning assumptions are more realistic.</p></section>
        <section class="guide-section"><h2>Why it is useful</h2>
          <p>Retirement and investment calculators need a return assumption. This tool supports choosing a profile that matches how much risk you are comfortable taking on paper.</p></section>
        <section class="guide-section"><h2>How to complete the calculator</h2>
          <ol><li>Open Portfolio Return Calculator.</li>
          <li>Review asset categories or risk profiles available in the app.</li>
          <li>Enter allocations or select a profile (for example Cautious, Balanced, Growth).</li>
          <li>Save results to feed your Financial Health Snapshot risk profile.</li></ol></section>
        <section class="guide-section"><h2>Input fields explained</h2>
          <table class="field-table">
            <tr><th>Asset allocation</th><td>How your money is split across types such as cash, bonds and shares.</td></tr>
            <tr><th>Expected return</th><td>Illustrative long-term return for each asset class or combined portfolio.</td></tr>
            <tr><th>Inflation</th><td>Optional adjustment so you see real (inflation-adjusted) returns.</td></tr>
            <tr><th>Risk profile</th><td>Label summarising your mix (feeds the dashboard card).</td></tr>
          </table></section>
        <section class="guide-section"><h2>Worked example</h2>
          <div class="example-box">
            <p><strong>Profile:</strong> Balanced</p>
            <p><strong>Illustrative return:</strong> 5–6% before inflation</p>
            <p><strong>After inflation:</strong> lower real return shown in app</p>
            <p>Use these figures as planning inputs in retirement or investment tools — not as forecasts.</p>
          </div></section>
        <section class="guide-section"><h2>Understanding your results</h2>
          <p>The summary explains expected volatility in plain terms. Your selected <strong>risk profile</strong> appears on the Financial Health Snapshot so you can align retirement assumptions with how you invest on paper.</p></section>
        <section class="guide-section"><h2>Frequently asked questions</h2>
          """ + faq_block([
        ("Is this personal investment advice?", "No. It is an educational planning aid."),
        ("Can I change profile later?", "Yes. Update anytime and refresh your snapshot."),
    ]) + """</section>""" + cta() + """</div>""",
)

register(
    "retirement-calculator",
    title="Retirement Calculator",
    meta="Review retirement projections, journey checkpoints and whether you are on track.",
    screenshot=("MoneyMapPulse_Screenshot_Retirement_1080x1920.png", "Retirement projection in MoneyMap Pulse"),
    content="""
      <div class="container">
        <section class="guide-section"><h2>What this tool does</h2>
          <p>Projects retirement fund growth, required fund at retirement, monthly income needs and journey checkpoints from today through retirement age.</p></section>
        <section class="guide-section"><h2>Why it is useful</h2>
          <p>Shows whether current savings habits might support your target lifestyle and highlights shortfalls early enough to adjust contributions or retirement age on paper.</p></section>
        <section class="guide-section"><h2>How to complete the calculator</h2>
          <ol><li>Open Retirement Calculator.</li>
          <li>Enter current age, retirement age and life expectancy if asked.</li>
          <li>Add current savings, monthly contributions and return assumptions.</li>
          <li>Enter expected retirement spending.</li>
          <li>Save and review journey and funding breakdown.</li></ol></section>
        <section class="guide-section"><h2>Input fields explained</h2>
          <table class="field-table">
            <tr><th>Current savings</th><td>Pensions and investments counted toward retirement.</td></tr>
            <tr><th>Monthly saving</th><td>Regular contributions until retirement.</td></tr>
            <tr><th>Retirement age</th><td>Age you plan to stop full-time work.</td></tr>
            <tr><th>Retirement spending</th><td>Monthly income you want in retirement (today's money or as labelled in app).</td></tr>
            <tr><th>Return assumption</th><td>Growth rate applied to projections.</td></tr>
          </table></section>
        <section class="guide-section"><h2>Worked example</h2>
          <div class="example-box">
            <p><strong>Projected pension fund:</strong> £1,092,666</p>
            <p><strong>Required fund:</strong> £1,085,649</p>
            <p><strong>Status:</strong> On track</p>
            <p><strong>Ahead by:</strong> £7,017 (illustrative)</p>
          </div></section>
        <section class="guide-section"><h2>Understanding your results</h2>
          <p><strong>On track</strong> means projected assets meet required fund. <strong>Shortfall</strong> means you may need higher savings, later retirement or lower spending assumptions. The <strong>retirement journey</strong> timeline shows checkpoints at today, retirement and later ages with funding breakdowns.</p></section>
        <section class="guide-section"><h2>Frequently asked questions</h2>
          """ + faq_block([
        ("Does this include State Pension?", "Only if you enter it. Add state and workplace pensions explicitly."),
        ("Are tax rules modelled?", "The app provides estimates; tax treatment may be simplified."),
    ]) + """</section>""" + cta() + """</div>""",
)

register(
    "net-worth-calculator",
    title="Net Worth Calculator",
    meta="Calculate assets, liabilities and track your net worth over time.",
    screenshot=("MoneyMapPulse_Screenshot_NetWorth_1080x1920.png", "Net Worth Calculator in MoneyMap Pulse"),
    content="""
      <div class="container">
        <section class="guide-section"><h2>What this tool does</h2>
          <p>Lists what you own (assets) and what you owe (liabilities), then calculates net worth.</p></section>
        <section class="guide-section"><h2>Why it is useful</h2>
          <p>Net worth is a single number for your overall position — useful for goals, retirement planning and the Financial Health Snapshot.</p></section>
        <section class="guide-section"><h2>How to complete the calculator</h2>
          <ol><li>Open Net Worth Calculator.</li>
          <li>Add assets (property, savings, investments, pensions, etc.).</li>
          <li>Add liabilities (mortgages, loans, credit cards).</li>
          <li>Review totals and save.</li></ol></section>
        <section class="guide-section"><h2>Input fields explained</h2>
          <table class="field-table">
            <tr><th>Assets</th><td>Items with positive value you own.</td></tr>
            <tr><th>Liabilities</th><td>Debts you still owe.</td></tr>
            <tr><th>Net worth</th><td>Assets minus liabilities.</td></tr>
            <tr><th>Liquid vs illiquid</th><td>Where shown, separates easy-to-access cash from property and long-term holdings.</td></tr>
          </table></section>
        <section class="guide-section"><h2>Worked example</h2>
          <div class="example-box">
            <p><strong>Assets:</strong> £550,000</p>
            <p><strong>Liabilities:</strong> £250,000</p>
            <p><strong>Net worth:</strong> £300,000</p>
          </div></section>
        <section class="guide-section"><h2>Understanding your results</h2>
          <p>Totals feed the <strong>Net worth</strong> card on your snapshot. Update when you buy property, pay down debt or build savings.</p></section>
        <section class="guide-section"><h2>Frequently asked questions</h2>
          """ + faq_block([
        ("Should I include my home?", "Include property if you want a full picture; some people track with and without home equity separately."),
        ("How often should I update?", "Every few months or after major life changes."),
    ]) + """</section>""" + cta() + """</div>""",
)

register(
    "buy-to-let-calculator",
    title="Buy To Let Calculator",
    meta="Evaluate rental property using cash flow, ROI and yield estimates.",
    screenshot=("MoneyMapPulse_Screenshot_BuyToLet_1080x1920.png", "Buy To Let summary in MoneyMap Pulse"),
    content="""
      <div class="container">
        <section class="guide-section"><h2>What this tool does</h2>
          <p>Estimates rental income, costs, mortgage payments, net cash flow, ROI and gross yield for a buy-to-let property scenario.</p></section>
        <section class="guide-section"><h2>Why it is useful</h2>
          <p>Compare property against other uses of your cash and see whether rent covers costs after mortgage and expenses.</p></section>
        <section class="guide-section"><h2>How to complete the calculator</h2>
          <ol><li>Open Buy To Let Calculator.</li>
          <li>Enter purchase price, deposit and mortgage details.</li>
          <li>Enter expected rent and running costs.</li>
          <li>Review summary and save if you want to compare later.</li></ol></section>
        <section class="guide-section"><h2>Input fields explained</h2>
          <table class="field-table">
            <tr><th>Purchase price</th><td>Property purchase amount.</td></tr>
            <tr><th>Deposit / cash invested</th><td>Your equity in the deal.</td></tr>
            <tr><th>Rental income</th><td>Expected monthly rent.</td></tr>
            <tr><th>Expenses</th><td>Management, maintenance, insurance, voids allowance, etc.</td></tr>
            <tr><th>Mortgage payment</th><td>Monthly cost if financed.</td></tr>
          </table></section>
        <section class="guide-section"><h2>Worked example</h2>
          <div class="example-box">
            <p><strong>Monthly net income:</strong> £362.50</p>
            <p><strong>Annual net income:</strong> £4,350</p>
            <p><strong>ROI:</strong> 4.44%</p>
            <p><strong>Gross yield:</strong> 6.00%</p>
          </div></section>
        <section class="guide-section"><h2>Understanding your results</h2>
          <p><strong>Monthly net income</strong> is rent minus mortgage and expenses. <strong>ROI</strong> relates return to cash invested. <strong>Gross yield</strong> compares annual rent to property price before costs. Use all three together — not in isolation.</p></section>
        <section class="guide-section"><h2>Frequently asked questions</h2>
          """ + faq_block([
        ("Does this include tax?", "Tax on rental income is not personal advice here; speak to a qualified professional for tax."),
        ("Is void period included?", "Include voids in expenses if the app provides a field or add a conservative allowance."),
    ]) + """</section>""" + cta() + """</div>""",
)


def main():
    for slug, data in GUIDES.items():
        shot_file, shot_alt = data["screenshot"]
        hero = hero_img(shot_file, shot_alt)
        inner = data["content"]
        body = f'<div class="container guide-hero-wrap">{hero}</div>\n{inner}'
        html = shell(data["title"], data["meta"], slug, body)
        out_dir = ROOT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        print("wrote", out_dir / "index.html")


if __name__ == "__main__":
    main()
