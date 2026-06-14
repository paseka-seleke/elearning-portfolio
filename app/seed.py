"""
Seed the database with the sample courses, knowledge check questions, and
blog posts described in the brief.

Run automatically on app startup if the database is empty, or manually:

    python -m app.seed
"""
from sqlmodel import Session, select
from app.database import ENGINE, init_db
from app.models import SampleCourse, QuizQuestion, BlogPost


COURSE_FIELDS = (
    "slug", "title", "tool", "framework", "audience", "duration",
    "accent", "summary", "outcomes", "body",
)


SAMPLES = [
    {
        "slug": "ai-fundamentals-policy-makers",
        "title": "AI Fundamentals for Policy Makers",
        "tool": "Articulate Rise",
        "framework": "Bloom's Taxonomy",
        "audience": "Government leaders and policy professionals",
        "duration": "20 minutes",
        "accent": "teal",
        "summary": "A short interactive course that builds AI literacy from definitions up to drafting a basic adoption plan.",
        "outcomes": (
            "Define artificial intelligence in plain terms\n"
            "Explain common public sector AI use cases\n"
            "Identify risks and benefits of an AI initiative\n"
            "Distinguish between narrow AI and general AI\n"
            "Evaluate an AI procurement proposal using a basic checklist\n"
            "Outline the first steps of an AI adoption plan"
        ),
        "body": (
            "## What is Artificial Intelligence?\n\n"
            "Artificial intelligence refers to computer systems that learn from data and use that learning to make predictions, recommendations, or decisions. Unlike traditional software — which follows rules a developer writes explicitly — an AI model improves as it is exposed to more examples. Think of a spam filter that gets better the more emails it sees, or a translation tool that improves as it processes more text.\n\n"
            "There are two broad categories worth knowing. Narrow AI does one task well: recognising speech, ranking search results, or flagging unusual transactions. General AI — capable of reasoning across many domains like a person — does not yet exist outside research labs. Everything in public service today is narrow AI.\n\n"
            "**Activity:** Consider a service your department delivers. Write down one repetitive, data-heavy task in that service. Could a system that learns from past examples make that task faster or more consistent? Keep that example in mind as you work through the rest of this course.\n\n"
            "## Public Sector Use Cases\n\n"
            "Governments worldwide are piloting AI in four broad areas. Document processing uses machine learning to read, sort, and extract data from forms, applications, and reports — cutting processing times from weeks to hours. Citizen-facing assistants answer common questions around the clock using information drawn from published policies. Predictive analytics helps teams anticipate demand — for hospital beds, social services, or infrastructure maintenance — before a crisis emerges. Fraud and anomaly detection flags unusual patterns in grants, benefits, or procurement data for human review.\n\n"
            "The common thread is augmentation, not replacement. The AI handles volume and pattern-matching; the official handles judgement, exceptions, and accountability.\n\n"
            "**Scenario:** A social welfare office processes 4,000 applications a month. A vendor proposes an AI tool to pre-screen applications and flag incomplete or inconsistent submissions for staff review. The system will not approve or reject — it will prioritise the queue. Think about: what data would the system need? Who reviews its recommendations? What happens when it is wrong?\n\n"
            "## Risks and Governance\n\n"
            "AI introduces risks that differ from traditional software. Bias is the most discussed: if the training data reflects past unfair decisions, the model will reproduce them at scale. A hiring tool trained on historical CVs may disadvantage certain groups not because a developer chose that outcome, but because the data carried that pattern.\n\n"
            "Explainability matters in public services because decisions affecting citizens must be defensible. A model that produces a score without a reason is hard to challenge or audit. Procurement teams should ask vendors: can this system explain, in plain terms, why it produced a given output?\n\n"
            "Data quality is a practical risk. Garbage in, garbage out still applies. Before adopting AI, assess whether your data is complete, accurate, and representative. Pilot small, measure carefully, and keep a human in the loop for any decision with significant consequences.\n\n"
            "**Reflection:** Name one decision in your area of responsibility where an incorrect AI recommendation could harm a citizen. Now name the safeguard you would put in place before deploying any tool in that decision pathway.\n\n"
            "## Planning Your First AI Initiative\n\n"
            "A good first initiative has four characteristics: it is narrow in scope, it uses data you already have, success is measurable, and a human reviews outcomes. Start with a problem statement, not a technology. 'We want to use AI' is not a problem statement. 'Staff spend 40% of their time manually sorting applications that could be categorised by rule' is.\n\n"
            "From there, the steps are: map the data you have and check its quality; define what a correct output looks like and how you will measure it; run a small pilot with real cases; audit the results for errors and bias; only then consider scaling. Build the oversight mechanism — the human review process — before you build the tool."
        ),
        "questions": [
            {
                "prompt": "Which option best describes artificial intelligence for a non-technical audience?",
                "a": "Software that follows fixed rules written by a developer for every case",
                "b": "Systems that learn patterns from data to make predictions or decisions",
                "c": "Any computer program that connects to the internet",
                "correct": 1,
                "explanation": "AI systems learn patterns from data rather than relying only on fixed, hand-written rules. That distinction — learning vs. following explicit instructions — is the key idea.",
            },
            {
                "prompt": "A department wants to reduce time spent answering repeat citizen questions. Which is the most fitting first AI use case?",
                "a": "A chatbot trained on the department's published FAQs and policies",
                "b": "An autonomous system that approves grant applications without review",
                "c": "Replacing the entire records database overnight",
                "correct": 0,
                "explanation": "A scoped assistant grounded in known, published content is low-risk and high-value. High-stakes decisions — like grant approvals — should keep a human in the loop.",
            },
            {
                "prompt": "Which is a genuine risk to plan for before adopting AI in public services?",
                "a": "The technology is always too expensive to pilot",
                "b": "Bias in training data can lead to unfair outcomes for citizens",
                "c": "AI can never be explained to the public",
                "correct": 1,
                "explanation": "Data bias is a real and manageable risk, addressed through good data practices, testing, and oversight. Cost and explainability are negotiable — bias in decisions affecting citizens is not.",
            },
            {
                "prompt": "A vendor proposes an AI tool that scores welfare applications but cannot explain why any individual received their score. What should concern you most?",
                "a": "The tool might slow processing times compared to paper forms",
                "b": "Unexplained scores make decisions hard to challenge or audit, which is a governance problem in public services",
                "c": "Citizens will always prefer speaking to a person, making the tool pointless",
                "correct": 1,
                "explanation": "Explainability is a governance requirement, not a nice-to-have. When an AI-influenced decision affects a citizen's rights or entitlements, there must be a defensible reason that can be communicated and reviewed.",
            },
            {
                "prompt": "What should come first when planning a public sector AI initiative?",
                "a": "Selecting the AI vendor with the best marketing material",
                "b": "Writing a clear problem statement tied to a measurable outcome",
                "c": "Building a large data warehouse to prepare for any future AI need",
                "correct": 1,
                "explanation": "Start with the problem, not the technology. A precise problem statement — with a measurable definition of success — is what keeps a pilot honest and scalable.",
            },
            {
                "prompt": "Which characteristic best describes 'narrow AI' as it exists in public services today?",
                "a": "AI that can reason and learn across many domains just like a person",
                "b": "AI designed to do one well-defined task, such as classifying documents or flagging anomalies",
                "c": "AI that only works when connected to a central government mainframe",
                "correct": 1,
                "explanation": "All AI in current use is narrow — it does one thing well. General AI capable of broad human-like reasoning does not yet exist outside research. Understanding this prevents over-promising to stakeholders.",
            },
        ],
    },
    {
        "slug": "cybersecurity-awareness-staff",
        "title": "Cybersecurity Awareness for Staff",
        "tool": "H5P",
        "framework": "ADDIE",
        "audience": "General employees",
        "duration": "15 minutes",
        "accent": "indigo",
        "summary": "An interactive lesson with knowledge checks that turns everyday staff into a strong first line of defence.",
        "outcomes": (
            "Recognise the hallmarks of a phishing message\n"
            "Respond safely to a suspicious email or link\n"
            "Create and manage strong, unique passwords\n"
            "Enable and use multi-factor authentication\n"
            "Report a suspected security incident quickly and correctly"
        ),
        "body": (
            "## The Threat Landscape\n\n"
            "Most successful cyberattacks do not start with sophisticated code — they start with a person clicking a link, opening an attachment, or sharing a password. Human error accounts for the majority of data breaches across every sector. The good news is that this is the most preventable category of risk, and every member of staff can close the gap.\n\n"
            "Threats come in a few common forms. Phishing is the most common: a deceptive email or message that tricks someone into revealing credentials or installing malware. Pretexting involves an attacker constructing a convincing false identity — posing as IT support, a supplier, or a senior colleague — to request sensitive information. Malware arrives through attachments, infected USB drives, or compromised websites, and can give attackers persistent access to systems.\n\n"
            "**Activity:** Before moving on, think of the last time you received an unexpected email asking you to do something — click, verify, download, or reply. What did you do? In this course you will build a reliable habit for moments exactly like that one.\n\n"
            "## Spotting a Phishing Message\n\n"
            "Phishing messages are designed to bypass your critical thinking by triggering urgency, fear, or curiosity. The classic signals are: a sender address that looks almost right but has a small difference (support@micros0ft.com); language that creates pressure ('your account will be suspended in 10 minutes'); a link that does not match the text when you hover over it; and requests for credentials, payment details, or file downloads you were not expecting.\n\n"
            "The safest habit is to verify independently. Do not use contact details in the message. Go directly to the official website by typing the address, or call a number you already know. If the message claims to be from a colleague, phone them. Attackers count on you acting before you think.\n\n"
            "**Scenario:** You receive an email from 'IT-Support@helpdesk-org.net' telling you that your account has been compromised and you must reset your password within 30 minutes using the link provided. The email uses your organisation's logo. Consider: what are the phishing signals? What is the correct response? What would happen if you clicked the link?\n\n"
            "## Password Hygiene and Multi-Factor Authentication\n\n"
            "A weak password is an unlocked door. Password reuse is a master key for attackers — when one service is breached, every account sharing that password is at risk. The practical solution is a password manager: a secure vault that generates and stores a long, unique password for every account. You remember one strong master password; the manager handles the rest.\n\n"
            "A strong password is long and random. 'Summer2024!' is weak because it follows a predictable pattern. 'tr7#Kp!qW2mz' is strong because it is random. A passphrase — four or more unconnected words strung together — is both strong and memorable: 'correct-horse-battery-staple' is far harder to crack than a short password with special characters.\n\n"
            "Multi-factor authentication (MFA) adds a second layer: even if an attacker has your password, they cannot access your account without the second factor — a code from an app, a text message, or a hardware token. Enable MFA on every account that offers it, especially email and any work systems.\n\n"
            "## Reporting an Incident\n\n"
            "Speed matters more than certainty. If you suspect something is wrong — you clicked a link and then felt uneasy, you notice your account behaving oddly, a colleague asks for your credentials — report it immediately to your IT or security team. Do not wait until you are sure. Early reports allow the team to contain damage before it spreads.\n\n"
            "Reporting is not the same as confessing. Organisations that punish staff for honest reporting create a culture where incidents are hidden until they become crises. The right culture is: report fast, report honestly, and let the experts assess the risk. Your job is to raise the flag; their job is to act on it.\n\n"
            "**Reflection:** Where would you go right now to report a suspected security incident in your organisation? If you do not know the answer immediately, finding out is the most important action you can take after completing this course."
        ),
        "questions": [
            {
                "prompt": "An email urges you to 'verify your account in 10 minutes or lose access' with a link. What is the safest first step?",
                "a": "Click the link quickly so you do not lose access",
                "b": "Do not click — check the sender and go to the official site directly",
                "c": "Forward it to all colleagues to warn them",
                "correct": 1,
                "explanation": "Urgency plus a link is the classic phishing combination. Verify through the official channel — never through the link in the message. Forwarding spreads the risk to colleagues.",
            },
            {
                "prompt": "Which password practice is strongest?",
                "a": "One memorable password reused across all your accounts",
                "b": "A long, unique passphrase per account stored in a password manager",
                "c": "Your name and birth year so it is easy to recall",
                "correct": 1,
                "explanation": "Unique, long passwords managed by a password manager limit the blast radius when any single service is breached. Reuse turns one breach into many.",
            },
            {
                "prompt": "What is the main benefit of enabling multi-factor authentication (MFA)?",
                "a": "It makes your password shorter because you no longer need a complex one",
                "b": "An attacker who obtains your password still cannot access your account without the second factor",
                "c": "It allows you to log in without a password entirely",
                "correct": 1,
                "explanation": "MFA adds a second layer of proof. Even a stolen or guessed password alone is not enough to get in, which dramatically reduces the impact of credential theft.",
            },
            {
                "prompt": "You click a link in an email and a moment later feel uneasy — the page looked odd. What should you do?",
                "a": "Say nothing and hope nothing comes of it",
                "b": "Report it to your IT or security team immediately, even if you are not certain",
                "c": "Change your password in three days if nothing bad has happened by then",
                "correct": 1,
                "explanation": "Speed matters more than certainty. Early reports give the security team time to contain damage. Waiting turns a small incident into a big one.",
            },
            {
                "prompt": "A caller claims to be from IT support and asks for your password to fix an urgent access issue. What do you do?",
                "a": "Provide it — IT support should have access anyway",
                "b": "Decline and verify the caller's identity through the official IT service desk number",
                "c": "Give a temporary version of your password and change it afterward",
                "correct": 1,
                "explanation": "Legitimate IT staff never need your password. This is a textbook pretexting attack. Verify through a known, official channel before sharing any information.",
            },
        ],
    },
    {
        "slug": "financial-reporting-essentials",
        "title": "Financial Reporting Essentials",
        "tool": "Articulate 365",
        "framework": "SAM",
        "audience": "Non-finance managers",
        "duration": "25 minutes",
        "accent": "amber",
        "summary": "A scenario-based module, prototyped and refined with SAM, that demystifies the core financial statements and connects them to everyday management decisions.",
        "outcomes": (
            "Identify and describe the three core financial statements\n"
            "Read a basic income statement and locate the key figures\n"
            "Distinguish between profit and cash position\n"
            "Explain why a profitable business can still run out of cash\n"
            "Ask sharper, more confident questions in budget review meetings"
        ),
        "body": (
            "## Why Non-Finance Managers Need This\n\n"
            "Every manager makes decisions that have financial consequences — hiring, procurement, project scope, pricing. You do not need to be an accountant to make good decisions, but you do need to read the scoreboard. Financial statements are that scoreboard. They tell you whether the organisation is growing, whether it can pay its bills, and whether it is building or burning through its resources.\n\n"
            "This module focuses on understanding, not preparation. Your finance team prepares the statements; your job is to read them with enough confidence to ask the right questions and spot the signals that matter for your area.\n\n"
            "**Activity:** Before you start, find the most recent budget report or financial summary for your team or department. Keep it nearby. As you work through each section, try to locate the same concept in your own document.\n\n"
            "## The Three Core Statements\n\n"
            "Financial performance is reported through three documents that are designed to be read together. The income statement (also called the profit and loss, or P&L) shows revenue and expenses over a period — typically a month, quarter, or year — and arrives at either a profit or a loss. It answers the question: did we make money?\n\n"
            "The balance sheet is a snapshot at a single point in time. It lists what the organisation owns (assets), what it owes (liabilities), and the difference between the two (equity or net assets). It answers the question: what do we have and what do we owe?\n\n"
            "The cash flow statement shows the movement of actual money in and out over a period. It answers the question: do we have the cash we need to operate? These three statements tell different parts of the same story — and the most important story they can tell together is that a business can be profitable on paper while simultaneously running out of cash.\n\n"
            "## Reading the Income Statement\n\n"
            "An income statement starts at the top with revenue — money earned from providing services or selling goods. Beneath it are direct costs (also called cost of sales or cost of goods sold): the expenses directly tied to delivering that revenue. Subtract direct costs from revenue and you get gross profit.\n\n"
            "Below gross profit come operating expenses: staff costs, rent, utilities, marketing, and other overheads. Subtract those and you get operating profit (sometimes called EBIT — earnings before interest and tax). After interest and tax, you reach net profit: the bottom line.\n\n"
            "**Scenario:** Your division's income statement shows revenue up 12% year-on-year, but net profit has fallen by 8%. What would you look for to understand the gap? Work through the statement from top to bottom: did direct costs rise faster than revenue? Did a large overhead item increase? Was there a one-off expense? The structure of the statement tells you where to look.\n\n"
            "## Profit versus Cash: The Critical Distinction\n\n"
            "A business records revenue when it is earned, not necessarily when cash arrives. If you deliver a service in March and invoice the client, your income statement shows that revenue in March — but if the client pays in June, the cash does not arrive until then. Meanwhile, you still need to pay your staff and suppliers in April and May.\n\n"
            "This is why profitable businesses fail: they run out of cash while waiting for money they are owed. Cash flow management is the discipline of making sure the timing of money in matches the timing of money out. As a manager, this means understanding your payment terms, your debtors, and how long your organisation can operate on its current cash reserves.\n\n"
            "**Reflection:** Think of a project or initiative your team delivered recently. When was the revenue or funding recognised? When did the actual cash arrive? Was there a gap — and if so, how was it managed?"
        ),
        "questions": [
            {
                "prompt": "Which statement shows whether the organisation made a profit over a period?",
                "a": "The balance sheet",
                "b": "The income statement (profit and loss)",
                "c": "The asset register",
                "correct": 1,
                "explanation": "The income statement reports revenue and expenses over a period to arrive at a profit or loss figure. The balance sheet is a point-in-time snapshot of assets and liabilities.",
            },
            {
                "prompt": "Your division's revenue grew 15% this year but net profit fell. Where on the income statement would you look first to understand why?",
                "a": "The asset column of the balance sheet",
                "b": "The cost lines between revenue and net profit — direct costs and operating expenses",
                "c": "The opening cash balance on the cash flow statement",
                "correct": 1,
                "explanation": "The income statement is read from top to bottom. If revenue grew but profit fell, costs rose faster than revenue. Work down the cost lines to find where the gap opened.",
            },
            {
                "prompt": "A company reports a healthy profit this quarter but is struggling to pay its suppliers. What is the most likely explanation?",
                "a": "The accountants made an error in the income statement",
                "b": "Revenue is recognised when earned, but cash may not have been received yet — a timing difference",
                "c": "Supplier invoices are not recorded until they are paid",
                "correct": 1,
                "explanation": "Profit is an accrual concept — it records activity when it happens. Cash is when money actually moves. A profitable business can run out of cash if clients pay slowly while suppliers must be paid quickly.",
            },
            {
                "prompt": "The balance sheet shows total assets of $500,000 and total liabilities of $320,000. What is the organisation's net asset (equity) position?",
                "a": "$820,000",
                "b": "$180,000",
                "c": "$320,000",
                "correct": 1,
                "explanation": "Net assets = Assets minus Liabilities. $500,000 − $320,000 = $180,000. This is the residual value owned by the organisation after all obligations are settled.",
            },
        ],
    },
    {
        "slug": "data-analytics-accountancy",
        "title": "Data Analytics for Accountancy",
        "tool": "H5P",
        "framework": "Gagne's Nine Events",
        "audience": "Accountants and auditors",
        "duration": "20 minutes",
        "accent": "rose",
        "summary": "An interactive practice activity that uses a real audit data problem to teach a practical analytics workflow — from data import to communicating findings.",
        "outcomes": (
            "Apply a structured analytics workflow to an accounting dataset\n"
            "Identify common anomaly patterns in transaction data\n"
            "Distinguish between a red flag and evidence of wrongdoing\n"
            "Select an appropriate visualisation for financial data\n"
            "Explain findings clearly to a non-technical stakeholder"
        ),
        "body": (
            "## Why Analytics Now?\n\n"
            "Spreadsheet-era auditing sampled a fraction of transactions and accepted that most of the population would go unexamined. Modern data tools change that. A full-population analysis of a transactions file takes seconds, and patterns that would have been invisible in a 5% sample become obvious in a histogram or a scatter plot.\n\n"
            "This does not replace professional judgement — it sharpens it. Analytics tells you where to look; the accountant's expertise tells you what it means. This module walks through one realistic workflow: a messy expense dataset, a set of analytical tests, a set of findings, and the conversation you would have with a client or manager who is not a data person.\n\n"
            "**Activity:** Download or open any transaction export from your accounting system. Before applying any analytics, spend two minutes writing down what you would expect a 'normal' dataset to look like: the range of amounts, the distribution of vendors, the frequency of transactions. This baseline is your reference point for spotting anomalies.\n\n"
            "## The Analytics Workflow\n\n"
            "A practical audit analytics workflow has five steps. First, understand the data: column definitions, date ranges, record count, and any obvious quality issues — blanks, duplicates, inconsistent formatting. Second, profile the data: summary statistics (min, max, mean, median), frequency distributions, and a check for gaps or spikes in the timeline.\n\n"
            "Third, apply targeted tests: Benford's Law for first-digit distributions in large numeric datasets, duplicate detection, control threshold testing (amounts clustering just below approval limits), and vendor or payee concentration analysis. Fourth, investigate exceptions: every flag is a question, not a conclusion. Document what you found and what follow-up steps are needed. Fifth, communicate: translate the data into a clear narrative for the decision-maker, with evidence but without jargon.\n\n"
            "## Anomaly Patterns to Know\n\n"
            "Certain patterns recur across fraud and error cases. Round-number clustering: a disproportionate number of transactions at even amounts ($500, $1,000, $5,000) can indicate manual entries substituted for documented costs. Threshold avoidance: transactions that cluster just below an approval or reporting limit — for example, many expenses at $4,990 when the review threshold is $5,000 — warrant explanation. Duplicate payments: the same amount to the same vendor on dates close together, especially when invoice numbers are absent or repeated.\n\n"
            "Benford's Law is a mathematical principle that predicts the distribution of first digits in naturally occurring numeric datasets. Invoiced amounts, population figures, and stock prices all tend to follow it. A dataset that deviates significantly from Benford's distribution warrants a closer look — it does not prove fraud, but it raises the question.\n\n"
            "**Scenario:** You are reviewing an expense dataset of 3,200 transactions. Running a frequency analysis, you find 87 transactions between $4,800 and $4,999 — significantly more than any adjacent $200 band. The policy manual states that expenses over $5,000 require a second authoriser. What are your next steps? What would you need to rule out before escalating?\n\n"
            "## Communicating Findings\n\n"
            "The most rigorous analysis is worthless if it cannot be communicated. A non-technical stakeholder — a CFO, a board member, an operational manager — does not need to understand the analytics method. They need to understand what you found, why it matters, and what you are recommending.\n\n"
            "Structure findings as: observation, significance, and next step. 'We found 87 expense transactions clustering just below the $5,000 authorisation threshold. This pattern is statistically unlikely to occur by chance and warrants review of the underlying documentation. We recommend pulling the original receipts for these transactions and confirming they were approved by the correct authority level.' That is three sentences. It respects the reader's time while making the case clearly.\n\n"
            "Choose visualisations that make the point without requiring explanation. A bar chart of transaction counts by $200 band makes the threshold clustering visible immediately. A scatter plot of transaction amount against date shows temporal spikes. Avoid complex charts that require a legend and annotations to decode — if the chart needs a paragraph of explanation, simplify it."
        ),
        "questions": [
            {
                "prompt": "In an expense dataset, several transactions cluster just below the $5,000 approval threshold. What does this most likely warrant?",
                "a": "Nothing — amounts below a threshold are always within policy",
                "b": "A closer look, since clustering below a control limit can signal threshold avoidance",
                "c": "Immediate dismissal of the staff involved",
                "correct": 1,
                "explanation": "Clustering just under a control limit is a known red flag worth investigating — not proof of wrongdoing on its own. Document the pattern, pull supporting documentation, and assess intent before drawing conclusions.",
            },
            {
                "prompt": "What does Benford's Law predict about a naturally occurring numeric dataset such as a set of invoiced amounts?",
                "a": "All digits 1 through 9 should appear as the first digit with equal frequency",
                "b": "Smaller digits (1, 2, 3) should appear as the first digit more often than larger digits",
                "c": "The majority of amounts should be round numbers ending in zero",
                "correct": 1,
                "explanation": "Benford's Law predicts that in many naturally occurring datasets, digit 1 appears as the leading digit about 30% of the time, digit 2 about 18%, and so on. Significant deviation from this distribution is a flag for further review.",
            },
            {
                "prompt": "You identify a significant anomaly in the data. What is the correct next step in a professional analytics workflow?",
                "a": "Report it as confirmed fraud to management immediately",
                "b": "Document the finding as a question requiring follow-up investigation, not a conclusion",
                "c": "Delete the anomalous records and rerun the analysis on clean data",
                "correct": 1,
                "explanation": "An anomaly is a flag, not evidence. Document it precisely, identify what you would need to rule out, and investigate systematically before characterising the finding. Escalating prematurely damages credibility.",
            },
            {
                "prompt": "You need to show a CFO that expense transactions cluster unusually around the $5,000 approval threshold. Which visualisation works best?",
                "a": "A table listing every transaction above $4,500 with vendor names",
                "b": "A bar chart showing transaction count by $200 amount band, with the threshold marked",
                "c": "A pie chart of total spend by category",
                "correct": 1,
                "explanation": "A bar chart by amount band makes the threshold clustering visible at a glance — the spike in the band just below $5,000 is obvious without explanation. Tables and pie charts do not show distributional patterns clearly.",
            },
        ],
    },
]


SAMPLE_EXTRAS = {
    "ai-fundamentals-policy-makers": {
        "preview": {
            "kicker": "AI readiness brief",
            "headline": "From concept to policy checklist",
            "caption": "A visual walk-through of the first four decisions leaders make before launching an AI pilot.",
            "stats": [
                {"value": "4", "label": "Decision gates"},
                {"value": "1", "label": "Human review loop"},
            ],
            "tags": ["Policy lens", "Risk aware", "FR/PT ready"],
        },
        "flip_cards": [
            {
                "front": "Where in your department is there a repetitive, high-volume task that depends on pattern recognition?",
                "back": "Start with the narrowest case. If staff can explain what a good output looks like, the use case is usually mature enough for a pilot.",
            },
            {
                "front": "Which citizen-facing decision would be risky if an AI score could not be explained?",
                "back": "List the harm first, then define the safeguard: human review, appeal path, audit logging, or a tighter scope for automation.",
            },
            {
                "front": "What would success look like after 90 days of an AI pilot?",
                "back": "Use one measurable service metric such as faster triage, fewer manual errors, or shorter response times. Avoid vague goals like 'innovation'.",
            },
        ],
        "infographic": {
            "title": "Adoption snapshot",
            "items": [
                {"value": "Scope", "label": "Start with one narrow workflow", "detail": "Keep the pilot limited enough to audit end to end."},
                {"value": "Data", "label": "Use data you already trust", "detail": "Check completeness, representativeness, and ownership early."},
                {"value": "Guardrail", "label": "Keep a human in the loop", "detail": "Review outputs before any high-impact action reaches a citizen."},
            ],
        },
        "chart": {
            "title": "Typical AI pilot effort mix",
            "caption": "Most of the work is not model building. It is governance, data preparation, and review design.",
            "bars": [
                {"label": "Problem framing", "value": 52},
                {"label": "Data readiness", "value": 78},
                {"label": "Model setup", "value": 41},
                {"label": "Oversight", "value": 68},
            ],
        },
        "translations": {
            "fr": {
                "label": "Francais",
                "title": "Fondamentaux de l'IA pour les decideurs publics",
                "summary": "Un mini-cours interactif qui explique l'IA en langage simple, montre des cas d'usage publics et aide a cadrer un premier plan d'adoption.",
                "audience": "Dirigeants publics et professionnels des politiques",
                "duration": "20 minutes",
                "outcomes": (
                    "Definir l'intelligence artificielle avec des mots simples\n"
                    "Reconnaitre des cas d'usage utiles dans le secteur public\n"
                    "Evaluer risques, benefices et garde-fous d'une initiative IA\n"
                    "Distinguer l'IA specialisee de l'IA generale\n"
                    "Poser les bonnes questions avant un achat ou un pilote"
                ),
                "body": (
                    "## Comprendre l'IA\n\n"
                    "L'intelligence artificielle designe des systemes capables d'apprendre a partir de donnees pour produire une prediction, une recommandation ou un classement. Dans les administrations, il s'agit aujourd'hui d'IA specialisee, centree sur une tache precise.\n\n"
                    "**Activity:** Notez une tache repetitive dans votre service. Si les agents utilisent toujours les memes indices pour la traiter, il existe peut-etre un point de depart pour un pilote.\n\n"
                    "## Cas d'usage publics\n\n"
                    "Les usages les plus realistes sont le tri de dossiers, l'assistance aux usagers, la detection d'anomalies et la prevision de la demande. Le principe cle reste le meme: l'outil accelere le volume, l'agent garde le jugement.\n\n"
                    "**Scenario:** Un fournisseur propose un systeme pour prioriser les demandes sociales incompletes. Quelles donnees alimentees? Qui verifie les recommandations? Comment un citoyen peut-il contester une erreur?\n\n"
                    "## Gouvernance et risques\n\n"
                    "Les risques principaux sont le biais, l'absence d'explication claire et des donnees de mauvaise qualite. Dans le secteur public, un resultat utile ne suffit pas: il doit aussi etre defendable et verifiable.\n\n"
                    "**Reflection:** Citez une decision de votre perimetre ou une recommandation erronee pourrait nuire a un citoyen. Quel garde-fou imposeriez-vous avant tout deploiement?\n\n"
                    "## Lancer un premier pilote\n\n"
                    "Commencez par un probleme concret, des donnees deja disponibles et un indicateur simple de succes. Pilotez petit, mesurez, auditez, puis decidez si l'echelle superieure est justifiee."
                ),
            },
            "pt": {
                "label": "Portugues",
                "title": "Fundamentos de IA para decisores publicos",
                "summary": "Um curso curto e interativo que desenvolve literacia em IA, mostra casos de uso no setor publico e orienta os primeiros passos de adocao.",
                "audience": "Lideres governamentais e profissionais de politicas publicas",
                "duration": "20 minutos",
                "outcomes": (
                    "Definir inteligencia artificial em linguagem simples\n"
                    "Explicar casos de uso no setor publico\n"
                    "Identificar riscos, beneficios e salvaguardas\n"
                    "Distinguir IA estreita de IA geral\n"
                    "Esbocar um primeiro plano de adocao"
                ),
                "body": (
                    "## O que e IA?\n\n"
                    "IA refere-se a sistemas que aprendem com dados para apoiar previsoes, recomendacoes e decisoes. Na administracao publica, o uso pratico atual e de IA estreita, voltada para tarefas especificas.\n\n"
                    "**Activity:** Pense em um processo do seu departamento que gere volume e repeticao. Esse processo poderia ser triado ou classificado com apoio de exemplos historicos?\n\n"
                    "## Casos de uso no setor publico\n\n"
                    "Os casos mais comuns incluem processamento documental, assistentes para cidadaos, analise preditiva de demanda e deteccao de fraude. O valor esta em acelerar volume sem retirar responsabilidade humana.\n\n"
                    "**Scenario:** Um escritorio de beneficios quer usar IA para priorizar pedidos incompletos. Que dados seriam necessarios? Quem revisa os resultados? O que acontece quando o sistema erra?\n\n"
                    "## Riscos e governanca\n\n"
                    "Bies nos dados, baixa explicabilidade e qualidade fraca de dados podem comprometer a justica e a confianca. Em servicos publicos, transparencia e revisao humana nao sao opcionais.\n\n"
                    "**Reflection:** Em qual decisao do seu contexto um erro de IA teria maior impacto para o cidadao? Qual salvaguarda deve existir antes do piloto?\n\n"
                    "## Planeando a primeira iniciativa\n\n"
                    "Comece com um problema mensuravel, dados disponiveis e um fluxo de revisao humana. Teste em pequena escala, audite resultados e so depois pense em expandir."
                ),
            },
        },
    },
    "cybersecurity-awareness-staff": {
        "preview": {
            "kicker": "Threat response lab",
            "headline": "Spot, pause, verify, report",
            "caption": "A staff-friendly walkthrough of the habits that stop phishing and credential theft before they spread.",
            "stats": [
                {"value": "30s", "label": "Pause rule"},
                {"value": "5", "label": "Core red flags"},
            ],
            "tags": ["Phishing drill", "Incident habit", "FR/PT ready"],
        },
        "flip_cards": [
            {
                "front": "What signal makes you stop fastest in an unexpected email: urgency, attachment, odd sender, or a login link?",
                "back": "Choose a single default habit: stop and verify through a trusted channel. Habits outperform memory when pressure is high.",
            },
            {
                "front": "If you clicked first and doubted later, what would stop you from reporting immediately?",
                "back": "Design the culture you need: fast reporting without blame. Delayed reporting is what turns one mistake into a larger incident.",
            },
            {
                "front": "Which account in your workday would hurt most if compromised?",
                "back": "That account should have the strongest password hygiene and MFA enforced before the end of the week.",
            },
        ],
        "infographic": {
            "title": "The safe-response pattern",
            "items": [
                {"value": "1", "label": "Inspect the sender and URL", "detail": "Small spelling changes and mismatched links are classic indicators."},
                {"value": "2", "label": "Verify outside the message", "detail": "Use the official site or a known phone number."},
                {"value": "3", "label": "Report quickly", "detail": "Speed matters more than being completely certain."},
            ],
        },
        "chart": {
            "title": "Security habits with highest payoff",
            "caption": "Simple routines prevent a disproportionate share of everyday attacks.",
            "bars": [
                {"label": "Phishing pause", "value": 84},
                {"label": "Password manager", "value": 71},
                {"label": "MFA enabled", "value": 92},
                {"label": "Fast reporting", "value": 76},
            ],
        },
        "translations": {
            "fr": {
                "label": "Francais",
                "title": "Sensibilisation a la cybersecurite pour le personnel",
                "summary": "Une lecon interactive qui transforme les gestes quotidiens du personnel en premiere ligne de defense contre le phishing et le vol d'identifiants.",
                "audience": "Employes de tous profils",
                "duration": "15 minutes",
                "outcomes": (
                    "Reconnaitre les signes d'un message d'hameconnage\n"
                    "Reagir correctement a un lien ou une piece jointe suspects\n"
                    "Utiliser des mots de passe forts et uniques\n"
                    "Comprendre l'interet de l'authentification multifacteur\n"
                    "Signaler rapidement un incident potentiel"
                ),
                "body": (
                    "## Le risque le plus courant\n\n"
                    "La plupart des incidents commencent par une action humaine simple: cliquer, telecharger, ou partager une information. Cette realite rend la vigilance du personnel essentielle.\n\n"
                    "**Activity:** Repensez au dernier message inattendu que vous avez recu. Avez-vous verifie l'expediteur, le lien et la demande avant d'agir?\n\n"
                    "## Reperer un phishing\n\n"
                    "Les signaux classiques sont l'urgence, une adresse presque correcte, un lien suspect et une demande inhabituelle de mot de passe ou de paiement. La bonne reponse consiste a verifier par un canal officiel et independant.\n\n"
                    "**Scenario:** Un mail au nom du support informatique vous demande une reinitialisation immediate du mot de passe. Quels indices doivent vous alerter? Que faites-vous a la place de cliquer?\n\n"
                    "## Mots de passe et MFA\n\n"
                    "Un mot de passe reutilise fragilise plusieurs comptes a la fois. Un gestionnaire de mots de passe et l'authentification multifacteur reduisent fortement ce risque.\n\n"
                    "## Signaler vite\n\n"
                    "Si vous avez un doute apres un clic ou un appel suspect, signalez-le tout de suite. Mieux vaut un faux positif rapide qu'un incident cache trop longtemps.\n\n"
                    "**Reflection:** Savez-vous immediatement comment joindre votre equipe informatique ou securite? Si non, c'est l'action prioritaire a prendre apres ce module."
                ),
            },
            "pt": {
                "label": "Portugues",
                "title": "Consciencializacao em ciberseguranca para colaboradores",
                "summary": "Uma aula interativa que reforca habitos simples para reconhecer phishing, proteger contas e reportar incidentes sem demora.",
                "audience": "Colaboradores em geral",
                "duration": "15 minutos",
                "outcomes": (
                    "Reconhecer sinais tipicos de phishing\n"
                    "Responder com seguranca a emails e links suspeitos\n"
                    "Criar e gerir palavras-passe fortes e unicas\n"
                    "Ativar e usar MFA\n"
                    "Reportar incidentes rapidamente"
                ),
                "body": (
                    "## O panorama da ameaca\n\n"
                    "Muitos ataques bem-sucedidos comecam por um clique apressado, uma anexo aberto ou uma credencial partilhada. Por isso, o comportamento do colaborador e uma camada critica de defesa.\n\n"
                    "**Activity:** Pense na ultima mensagem inesperada que pediu para clicar, confirmar ou descarregar algo. Qual foi a sua reacao imediata?\n\n"
                    "## Como identificar phishing\n\n"
                    "Urgencia artificial, remetente parecido com o oficial, links que nao coincidem e pedidos de credenciais sao sinais recorrentes. A melhor resposta e verificar por um canal oficial conhecido.\n\n"
                    "**Scenario:** Recebe um email a dizer que a conta sera bloqueada em 30 minutos. O que verifica primeiro? Qual e o risco de seguir o link da mensagem?\n\n"
                    "## Senhas e MFA\n\n"
                    "Reutilizar senhas amplia o dano de qualquer violacao. Um gestor de senhas e MFA reduzem drasticamente o impacto do roubo de credenciais.\n\n"
                    "## Reportar sem esperar\n\n"
                    "Se clicou e depois desconfiou, reporte logo. A equipa tecnica precisa de tempo para conter o problema antes que ele se espalhe.\n\n"
                    "**Reflection:** Se um incidente acontecesse agora, saberia exatamente para onde reportar? Essa resposta deve ser imediata."
                ),
            },
        },
    },
    "financial-reporting-essentials": {
        "preview": {
            "kicker": "Finance made readable",
            "headline": "Read the story behind the statements",
            "caption": "An executive-style visual summary that turns P&L, balance sheet, and cash flow into decisions managers can act on.",
            "stats": [
                {"value": "3", "label": "Core statements"},
                {"value": "1", "label": "Critical cash lens"},
            ],
            "tags": ["Manager ready", "Decision focused", "FR/PT ready"],
        },
        "flip_cards": [
            {
                "front": "When revenue rises but profit falls, which cost line would you inspect first in your own context?",
                "back": "Trace the story from revenue to gross profit to operating profit. The first unexpected jump usually explains where the margin is leaking.",
            },
            {
                "front": "Have you seen a project look successful on paper but still create budget stress?",
                "back": "That is usually a timing problem, not a contradiction. Profit measures performance; cash measures survivability.",
            },
            {
                "front": "What question could you ask in your next review meeting that would show stronger financial judgement?",
                "back": "Ask what changed between revenue growth and cash conversion, or which expense line moved differently from plan.",
            },
        ],
        "infographic": {
            "title": "Statement quick map",
            "items": [
                {"value": "P&L", "label": "Tracks profit over time", "detail": "Shows revenue, direct costs, operating expenses, and net result."},
                {"value": "BS", "label": "Shows what is owned and owed", "detail": "A point-in-time snapshot of assets, liabilities, and equity."},
                {"value": "CF", "label": "Explains money movement", "detail": "Reveals whether the organisation can actually fund operations."},
            ],
        },
        "chart": {
            "title": "Example monthly performance snapshot",
            "caption": "A simple comparison that shows why strong revenue does not automatically mean healthy cash.",
            "bars": [
                {"label": "Revenue", "value": 88},
                {"label": "Gross profit", "value": 63},
                {"label": "Net profit", "value": 39},
                {"label": "Cash on hand", "value": 28},
            ],
        },
        "translations": {
            "fr": {
                "label": "Francais",
                "title": "Les bases du reporting financier",
                "summary": "Un module scenarioise qui aide les managers non financiers a lire les trois etats essentiels et a poser de meilleures questions en reunion budgetaire.",
                "audience": "Managers non financiers",
                "duration": "25 minutes",
                "outcomes": (
                    "Identifier les trois etats financiers essentiels\n"
                    "Lire un compte de resultat simple\n"
                    "Distinguer profit et tresorerie\n"
                    "Comprendre pourquoi une activite rentable peut manquer de cash\n"
                    "Intervenir avec plus d'assurance dans une revue budgetaire"
                ),
                "body": (
                    "## Pourquoi cela compte\n\n"
                    "Les decisions quotidiennes des managers ont toujours un effet financier. Lire les etats ne sert pas a produire la comptabilite, mais a comprendre le score et les signaux qui exigent une question supplementaire.\n\n"
                    "**Activity:** Gardez pres de vous un rapport budgetaire recent et reperez les notions de revenu, cout, resultat et tresorerie au fil du module.\n\n"
                    "## Les trois etats cles\n\n"
                    "Le compte de resultat montre si l'organisation a genere un profit sur une periode. Le bilan montre ce qu'elle possede et ce qu'elle doit a une date donnee. Le tableau de flux de tresorerie montre les mouvements d'argent reel.\n\n"
                    "## Lire le compte de resultat\n\n"
                    "Suivez la logique du haut vers le bas: revenus, couts directs, marge brute, charges d'exploitation, resultat net. Si le revenu monte mais que le profit baisse, le probleme se trouve presque toujours entre ces lignes.\n\n"
                    "**Scenario:** Votre division augmente son chiffre d'affaires mais voit le resultat net reculer. Quels postes verifieriez-vous en premier?\n\n"
                    "## Profit contre cash\n\n"
                    "Un produit peut etre comptabilise avant l'encaissement reel. C'est pourquoi une organisation rentable peut quand meme subir une tension de tresorerie.\n\n"
                    "**Reflection:** Pensez a un projet recent: a quel moment le revenu a-t-il ete reconnu, et quand l'argent est-il effectivement arrive?"
                ),
            },
            "pt": {
                "label": "Portugues",
                "title": "Elementos essenciais do relato financeiro",
                "summary": "Um modulo orientado por cenarios que ajuda gestores nao financeiros a interpretar demonstracoes financeiras e a tomar melhores decisoes.",
                "audience": "Gestores nao financeiros",
                "duration": "25 minutos",
                "outcomes": (
                    "Identificar as tres demonstracoes financeiras principais\n"
                    "Ler uma demonstracao de resultados basica\n"
                    "Distinguir lucro de caixa\n"
                    "Explicar porque uma organizacao lucrativa pode ficar sem liquidez\n"
                    "Fazer perguntas mais fortes em reunioes de orcamento"
                ),
                "body": (
                    "## Porque isto importa\n\n"
                    "Decisoes de contratacao, compras e escopo afetam sempre o desempenho financeiro. O objetivo aqui nao e preparar contas, mas ler os sinais com confianca suficiente para agir melhor.\n\n"
                    "**Activity:** Tenha por perto um resumo financeiro recente da sua equipa e tente localizar cada conceito ao longo do modulo.\n\n"
                    "## As tres demonstracoes nucleares\n\n"
                    "A demonstracao de resultados mostra receitas, custos e lucro num periodo. O balanco mostra ativos, passivos e capital num ponto no tempo. O fluxo de caixa mostra entradas e saidas reais de dinheiro.\n\n"
                    "## Ler a demonstracao de resultados\n\n"
                    "Comece pelas receitas, depois custos diretos, margem bruta, despesas operacionais e lucro liquido. Se a receita sobe mas o lucro desce, procure onde os custos cresceram mais depressa.\n\n"
                    "**Scenario:** A sua unidade aumentou a receita em 12%, mas o lucro caiu. Que linhas investigaria primeiro para explicar a diferenca?\n\n"
                    "## Lucro versus caixa\n\n"
                    "Receita reconhecida nao significa dinheiro recebido no mesmo momento. Essa diferenca de timing explica porque negocios lucrativos ainda enfrentam stress de caixa.\n\n"
                    "**Reflection:** Num projeto recente, houve intervalo entre o reconhecimento da receita e a entrada real de caixa? Como isso foi gerido?"
                ),
            },
        },
    },
    "data-analytics-accountancy": {
        "preview": {
            "kicker": "Audit analytics studio",
            "headline": "Turn anomaly signals into clear findings",
            "caption": "A visually guided audit scenario that pairs data tests with the judgement needed to explain them credibly.",
            "stats": [
                {"value": "5", "label": "Workflow steps"},
                {"value": "87", "label": "Flagged expenses"},
            ],
            "tags": ["Audit view", "Visual evidence", "FR/PT ready"],
        },
        "flip_cards": [
            {
                "front": "What would make you trust an anomaly enough to escalate it for review?",
                "back": "You need context, documentation, and an explanation of what normal should have looked like before the spike appeared.",
            },
            {
                "front": "Which visual would help a CFO understand threshold avoidance fastest?",
                "back": "Use the simplest chart that makes the pattern obvious. Distribution charts usually beat dense tables for this conversation.",
            },
            {
                "front": "How do you stop yourself from overstating an analytics finding?",
                "back": "Phrase it as observation, significance, and next step. A red flag is a question, not a verdict.",
            },
        ],
        "infographic": {
            "title": "Analytics workflow",
            "items": [
                {"value": "Profile", "label": "Understand counts, dates, gaps", "detail": "Get record quality and baseline behaviour before testing."},
                {"value": "Test", "label": "Run focused anomaly checks", "detail": "Duplicates, thresholds, Benford patterns, and concentration."},
                {"value": "Explain", "label": "Translate the finding", "detail": "State what happened, why it matters, and what should happen next."},
            ],
        },
        "chart": {
            "title": "Expense concentration near approval threshold",
            "caption": "A simple banded view makes the cluster just below the limit immediately visible.",
            "bars": [
                {"label": "4.4k", "value": 29},
                {"label": "4.6k", "value": 37},
                {"label": "4.8k", "value": 91},
                {"label": "5.0k+", "value": 18},
            ],
        },
        "translations": {
            "fr": {
                "label": "Francais",
                "title": "Analyse de donnees pour la comptabilite",
                "summary": "Une activite pratique qui montre comment analyser un jeu de donnees comptables, interpreter des signaux d'anomalie et presenter des constats clairs.",
                "audience": "Comptables et auditeurs",
                "duration": "20 minutes",
                "outcomes": (
                    "Appliquer un flux d'analyse structure a un fichier comptable\n"
                    "Reconnaitre des motifs d'anomalie frequents\n"
                    "Distinguer un signal d'alerte d'une preuve\n"
                    "Choisir une visualisation adaptee\n"
                    "Expliquer des resultats a un decideur non technique"
                ),
                "body": (
                    "## Pourquoi l'analyse maintenant\n\n"
                    "Les outils actuels permettent d'examiner une population complete de transactions en quelques secondes. L'objectif n'est pas de remplacer le jugement professionnel, mais de concentrer l'attention la ou le risque semble plus fort.\n\n"
                    "**Activity:** Ouvrez un export de transactions et notez ce que vous considerez comme un comportement normal avant tout test.\n\n"
                    "## Le flux d'analyse\n\n"
                    "Commencez par comprendre le jeu de donnees, puis profilez-le avec des statistiques simples. Ensuite appliquez des tests cibles: doublons, concentration sous seuil, distribution des chiffres, concentration par fournisseur.\n\n"
                    "## Signaux d'anomalie\n\n"
                    "Des montants ronds repetes, des paiements proches du seuil d'approbation ou des doublons rapproches sont des motifs qui meritent verification. Ils ne prouvent rien a eux seuls.\n\n"
                    "**Scenario:** Vous observez un pic inhabituel de depenses juste sous le seuil d'autorisation. Quelles verifications documentaires devez-vous lancer avant toute escalation?\n\n"
                    "## Communiquer sans jargon\n\n"
                    "Presentez chaque constat en trois temps: observation, importance, prochaine action. Une bonne visualisation doit rendre le motif evident sans long commentaire."
                ),
            },
            "pt": {
                "label": "Portugues",
                "title": "Analitica de dados para contabilidade",
                "summary": "Uma atividade pratica que usa um problema realista de auditoria para ensinar um fluxo simples de analise, investigacao e comunicacao.",
                "audience": "Contabilistas e auditores",
                "duration": "20 minutos",
                "outcomes": (
                    "Aplicar um fluxo estruturado de analise a dados contabilisticos\n"
                    "Identificar padroes comuns de anomalia\n"
                    "Distinguir um alerta de evidencia conclusiva\n"
                    "Escolher uma visualizacao adequada\n"
                    "Explicar resultados a partes interessadas nao tecnicas"
                ),
                "body": (
                    "## Porque usar analitica agora\n\n"
                    "Ferramentas modernas permitem analisar a populacao inteira de transacoes em vez de depender apenas de amostras pequenas. Isso melhora o foco da revisao e torna certos padroes visiveis muito mais cedo.\n\n"
                    "**Activity:** Abra um ficheiro de transacoes e escreva como esperaria que um conjunto normal de dados se comportasse antes de procurar excecoes.\n\n"
                    "## O fluxo de trabalho analitico\n\n"
                    "Primeiro compreenda os campos, datas e qualidade dos registos. Depois faca perfil dos dados com contagens, medias e distribuicoes. Em seguida aplique testes direcionados como duplicados, limiares e concentracao por fornecedor.\n\n"
                    "## Padroes de anomalia\n\n"
                    "Montantes redondos em excesso, transacoes logo abaixo do limite de aprovacao e pagamentos duplicados proximos no tempo exigem explicacao adicional. Sao perguntas, nao conclusoes.\n\n"
                    "**Scenario:** Encontrou 87 despesas entre 4.800 e 4.999. Que documentos procuraria primeiro para perceber se existe evitacao de limite?\n\n"
                    "## Comunicar constatacoes\n\n"
                    "Estruture a mensagem como observacao, relevancia e proximo passo. O grafico deve tornar o padrao evidente sem precisar de muito texto auxiliar."
                ),
            },
        },
    },
}


LOCALIZED_INTERACTIVE_CONTENT = {
    "ai-fundamentals-policy-makers": {
        "fr": {
            "preview": {
                "kicker": "Brief de preparation IA",
                "headline": "Du concept au premier cadre de decision",
                "caption": "Un apercu visuel des decisions essentielles a prendre avant de lancer un pilote IA dans le service public.",
                "stats": [{"value": "4", "label": "Etapes de decision"}, {"value": "1", "label": "Boucle de revue humaine"}],
                "tags": ["Vision politique", "Risque maitrise", "Bilingue"],
            },
            "flip_cards": [
                {"front": "Dans quel service avez-vous une tache repetitive, volumineuse et basee sur des motifs reconnaissables ?", "back": "Commencez par le cas le plus etroit. Si les agents peuvent decrire clairement un bon resultat, le cas se prete souvent a un pilote."},
                {"front": "Quelle decision touchant le citoyen serait trop risquee si un score IA ne pouvait pas etre explique ?", "back": "Nommez d'abord le prejudice possible, puis choisissez le garde-fou adapte : revue humaine, voie de recours, journal d'audit ou limitation du perimetre."},
                {"front": "A quoi ressemblerait un succes credible au bout de 90 jours de pilote ?", "back": "Choisissez un indicateur mesurable : tri plus rapide, moins d'erreurs manuelles ou meilleur delai de reponse. Evitez les objectifs vagues."},
            ],
            "infographic": {
                "title": "Apercu de l'adoption",
                "items": [
                    {"value": "Perimetre", "label": "Commencer par un seul flux de travail", "detail": "Le pilote doit rester assez etroit pour etre observe et audite de bout en bout."},
                    {"value": "Donnees", "label": "S'appuyer sur des donnees deja fiables", "detail": "Verifiez tot la qualite, la representativite et la responsabilite sur les donnees."},
                    {"value": "Garde-fou", "label": "Maintenir une revue humaine", "detail": "Aucun resultat sensible ne devrait atteindre un citoyen sans verification."},
                ],
            },
            "chart": {
                "title": "Repartition type d'un pilote IA",
                "caption": "La majeure partie du travail concerne la gouvernance, les donnees et l'organisation de la revue, pas seulement le modele.",
                "bars": [{"label": "Cadrage", "value": 52}, {"label": "Preparation des donnees", "value": 78}, {"label": "Mise en place du modele", "value": 41}, {"label": "Supervision", "value": 68}],
            },
            "questions": [
                {"prompt": "Quelle option decrit le mieux l'intelligence artificielle pour un public non technique ?", "a": "Un logiciel qui applique uniquement des regles fixes ecrites a l'avance", "b": "Des systemes qui apprennent a partir des donnees pour faire des predictions ou des decisions", "c": "Tout programme informatique connecte a internet", "explanation": "La difference essentielle est l'apprentissage a partir des donnees plutot que l'execution exclusive de regles explicites."},
                {"prompt": "Un ministere veut reduire le temps passe a repondre aux questions repetitives des citoyens. Quel premier cas d'usage IA est le plus adapte ?", "a": "Un agent conversationnel entraine sur les FAQ et politiques publiees", "b": "Un systeme autonome qui approuve des subventions sans controle", "c": "Le remplacement complet de la base documentaire en une nuit", "explanation": "Un assistant limite a un contenu public connu est un premier usage prudent et utile. Les decisions sensibles doivent garder une revue humaine."},
                {"prompt": "Quel risque doit etre planifie avant d'adopter l'IA dans les services publics ?", "a": "La technologie est toujours trop couteuse pour etre testee", "b": "Un biais dans les donnees d'entrainement peut produire des resultats injustes", "c": "L'IA ne peut jamais etre expliquee au public", "explanation": "Le biais des donnees est un risque reel qui doit etre gere par des tests, de bonnes donnees et une supervision adaptee."},
                {"prompt": "Un fournisseur propose un outil qui note des demandes sociales sans pouvoir expliquer chaque score. Quelle est la principale inquietude ?", "a": "L'outil pourrait etre plus lent que les formulaires papier", "b": "Des scores inexpliques rendent les decisions difficiles a contester ou a auditer", "c": "Les citoyens prefereront toujours parler a une personne", "explanation": "L'explicabilite est une exigence de gouvernance. Une decision publique influencee par l'IA doit pouvoir etre expliquee et revue."},
                {"prompt": "Quelle etape doit venir en premier lors de la planification d'une initiative IA publique ?", "a": "Choisir le fournisseur au meilleur marketing", "b": "Rediger un probleme clair relie a un resultat mesurable", "c": "Construire un vaste entrepot de donnees pour tout usage futur", "explanation": "Il faut commencer par le probleme et la mesure de succes, pas par la technologie ni par l'infrastructure generique."},
                {"prompt": "Quelle caracteristique decrit le mieux l'IA specialisee utilisee aujourd'hui dans les services publics ?", "a": "Une IA capable de raisonner dans tous les domaines comme une personne", "b": "Une IA concue pour accomplir une tache bien definie", "c": "Une IA qui ne fonctionne qu'avec un grand systeme central", "explanation": "L'IA actuelle est specialisee : elle execute une tache precise. L'IA generale reste du domaine de la recherche."},
            ],
        },
        "pt": {
            "preview": {
                "kicker": "Resumo de prontidao em IA",
                "headline": "Do conceito ao primeiro quadro de decisao",
                "caption": "Uma leitura visual das decisoes essenciais antes de lancar um piloto de IA no setor publico.",
                "stats": [{"value": "4", "label": "Etapas de decisao"}, {"value": "1", "label": "Ciclo de revisao humana"}],
                "tags": ["Visao politica", "Risco controlado", "Bilingue"],
            },
            "flip_cards": [
                {"front": "Em que area existe uma tarefa repetitiva, de alto volume e dependente de padroes reconheciveis?", "back": "Comece pelo caso mais estreito. Se a equipa consegue descrever um bom resultado, o caso costuma estar maduro para um piloto."},
                {"front": "Que decisao com impacto no cidadao seria demasiado arriscada se um resultado de IA nao pudesse ser explicado?", "back": "Nomeie primeiro o dano potencial e depois escolha a salvaguarda adequada: revisao humana, recurso, registo de auditoria ou escopo mais limitado."},
                {"front": "Como seria um sucesso credivel apos 90 dias de piloto?", "back": "Use um indicador mensuravel como triagem mais rapida, menos erros manuais ou melhor tempo de resposta. Evite metas vagas."},
            ],
            "infographic": {
                "title": "Panorama da adocao",
                "items": [
                    {"value": "Escopo", "label": "Comecar por um fluxo de trabalho estreito", "detail": "O piloto deve ser pequeno o suficiente para ser observado e auditado de ponta a ponta."},
                    {"value": "Dados", "label": "Usar dados ja confiaveis", "detail": "Verifique cedo qualidade, representatividade e responsabilidade sobre os dados."},
                    {"value": "Salvaguarda", "label": "Manter revisao humana", "detail": "Nenhum resultado sensivel deve chegar ao cidadao sem verificacao."},
                ],
            },
            "chart": {
                "title": "Distribuicao tipica do esforco num piloto de IA",
                "caption": "Grande parte do trabalho esta na governanca, nos dados e no desenho da revisao, nao apenas no modelo.",
                "bars": [{"label": "Definicao do problema", "value": 52}, {"label": "Preparacao dos dados", "value": 78}, {"label": "Configuracao do modelo", "value": 41}, {"label": "Supervisao", "value": 68}],
            },
            "questions": [
                {"prompt": "Qual opcao descreve melhor a inteligencia artificial para um publico nao tecnico?", "a": "Software que segue apenas regras fixas escritas antecipadamente", "b": "Sistemas que aprendem com dados para fazer previsoes ou decisoes", "c": "Qualquer programa ligado a internet", "explanation": "A diferenca central esta em aprender com dados, e nao apenas executar regras explicitas."},
                {"prompt": "Um departamento quer reduzir o tempo gasto a responder a perguntas repetidas dos cidadaos. Qual e o primeiro caso de uso mais adequado?", "a": "Um chatbot treinado com FAQs e politicas publicadas", "b": "Um sistema autonomo que aprova subvencoes sem revisao", "c": "Substituir toda a base documental de um dia para o outro", "explanation": "Um assistente limitado a conteudo publico conhecido e um bom primeiro uso. Decisoes sensiveis devem manter revisao humana."},
                {"prompt": "Qual risco precisa de ser planeado antes de adotar IA nos servicos publicos?", "a": "A tecnologia e sempre demasiado cara para testar", "b": "Vies nos dados de treino pode gerar resultados injustos", "c": "A IA nunca pode ser explicada ao publico", "explanation": "O vies dos dados e um risco real e gerivel com testes, boa qualidade de dados e supervisao apropriada."},
                {"prompt": "Um fornecedor propoe uma ferramenta que atribui pontuacoes a pedidos sociais, mas nao consegue explicar cada pontuacao. Qual e a principal preocupacao?", "a": "A ferramenta pode ser mais lenta do que formularios em papel", "b": "Pontuacoes sem explicacao dificultam contestacao e auditoria", "c": "Os cidadaos preferirao sempre falar com uma pessoa", "explanation": "Explicabilidade e um requisito de governanca. Uma decisao publica influenciada por IA precisa de poder ser explicada e revista."},
                {"prompt": "O que deve vir primeiro ao planear uma iniciativa publica de IA?", "a": "Escolher o fornecedor com melhor marketing", "b": "Escrever um problema claro ligado a um resultado mensuravel", "c": "Construir um grande armazem de dados para qualquer uso futuro", "explanation": "Comeca-se pelo problema e pela definicao de sucesso, nao pela tecnologia ou por uma infraestrutura generica."},
                {"prompt": "Que caracteristica descreve melhor a IA estreita usada atualmente nos servicos publicos?", "a": "Uma IA que raciocina em muitos dominios como uma pessoa", "b": "Uma IA desenhada para uma tarefa bem definida", "c": "Uma IA que so funciona ligada a um sistema central", "explanation": "A IA atual e estreita: faz uma tarefa especifica. A IA geral continua fora do uso pratico."},
            ],
        },
    },
    "cybersecurity-awareness-staff": {
        "fr": {
            "preview": {"kicker": "Atelier de reaction aux menaces", "headline": "Voir, stopper, verifier, signaler", "caption": "Un parcours visuel sur les reflexes qui bloquent le phishing et le vol d'identifiants avant qu'ils ne se propagent.", "stats": [{"value": "30s", "label": "Regle de pause"}, {"value": "5", "label": "Signaux d'alerte"}], "tags": ["Phishing", "Reflexe d'alerte", "Bilingue"]},
            "flip_cards": [
                {"front": "Quel signal vous ferait vous arreter en premier dans un message inattendu : urgence, piece jointe, expediteur ou lien de connexion ?", "back": "Choisissez un reflexe par defaut : s'arreter puis verifier par un canal fiable. Un bon reflexe est plus solide qu'un simple souvenir."},
                {"front": "Si vous avez clique puis doute apres coup, qu'est-ce qui pourrait vous empecher de signaler tout de suite ?", "back": "La bonne culture est une culture sans blame pour les signalements rapides. Le vrai danger vient du silence apres l'erreur."},
                {"front": "Quel compte de votre quotidien professionnel serait le plus critique s'il etait compromis ?", "back": "C'est ce compte qui doit avoir les mots de passe les plus robustes et l'authentification multifacteur activee en priorite."},
            ],
            "infographic": {"title": "Schema de reaction sure", "items": [{"value": "1", "label": "Verifier expediteur et lien", "detail": "Les petites fautes et les URL incoherentes sont des signaux frequents."}, {"value": "2", "label": "Verifier hors du message", "detail": "Passez par le site officiel ou un numero connu."}, {"value": "3", "label": "Signaler rapidement", "detail": "La rapidite compte plus que la certitude complete."}]},
            "chart": {"title": "Habitudes de securite a plus fort impact", "caption": "Quelques routines simples empechent une grande part des attaques quotidiennes.", "bars": [{"label": "Pause phishing", "value": 84}, {"label": "Gestionnaire MDP", "value": 71}, {"label": "MFA active", "value": 92}, {"label": "Signalement rapide", "value": 76}]},
            "questions": [
                {"prompt": "Un email vous dit de verifier votre compte en 10 minutes sinon vous perdrez l'acces. Quelle est la premiere action la plus sure ?", "a": "Cliquer vite pour ne pas perdre l'acces", "b": "Ne pas cliquer et verifier l'expediteur puis aller directement au site officiel", "c": "Le transferer a tous les collegues", "explanation": "Urgence plus lien correspond au schema classique du phishing. Il faut verifier par le canal officiel, pas par le lien du message."},
                {"prompt": "Quelle pratique de mot de passe est la plus solide ?", "a": "Un mot de passe memorisable reutilise partout", "b": "Une phrase de passe longue et unique par compte, stockee dans un gestionnaire", "c": "Votre nom et votre annee de naissance", "explanation": "Des mots de passe uniques et longs limitent l'impact d'une fuite sur un service unique. La reutilisation etend le dommage a tous les comptes."},
                {"prompt": "Quel est le principal avantage de l'authentification multifacteur ?", "a": "Elle permet d'avoir un mot de passe plus court", "b": "Un attaquant avec le mot de passe ne peut toujours pas entrer sans second facteur", "c": "Elle remplace totalement le mot de passe", "explanation": "Le second facteur bloque la plupart des acces frauduleux memes en cas de mot de passe vole."},
                {"prompt": "Vous cliquez sur un lien puis la page vous semble etrange. Que faire ?", "a": "Ne rien dire et attendre", "b": "Signaler immediatement a l'equipe IT ou securite meme sans certitude", "c": "Changer le mot de passe dans quelques jours", "explanation": "La rapidite compte plus que la certitude. Signaler tot permet de contenir l'incident avant qu'il ne s'aggrave."},
                {"prompt": "Un appelant dit appartenir au support IT et vous demande votre mot de passe pour regler un probleme urgent. Que faites-vous ?", "a": "Le donner car le support doit y avoir acces", "b": "Refuser et verifier l'identite via le numero officiel du service", "c": "Donner un mot de passe temporaire", "explanation": "Le support legitime n'a pas besoin de votre mot de passe. Il faut verifier par le canal officiel connu."},
            ],
        },
        "pt": {
            "preview": {"kicker": "Laboratorio de resposta a ameacas", "headline": "Ver, parar, verificar, reportar", "caption": "Um percurso visual sobre os habitos que travam phishing e roubo de credenciais antes de se espalharem.", "stats": [{"value": "30s", "label": "Regra de pausa"}, {"value": "5", "label": "Sinais de alerta"}], "tags": ["Phishing", "Habito de reporte", "Bilingue"]},
            "flip_cards": [
                {"front": "Que sinal o faria parar primeiro numa mensagem inesperada: urgencia, anexo, remetente estranho ou link de login?", "back": "Escolha um habito padrao: parar e verificar por um canal confiavel. Um bom habito vale mais do que a memoria sob pressao."},
                {"front": "Se clicou primeiro e duvidou depois, o que poderia impedi-lo de reportar logo?", "back": "A cultura certa nao pune o reporte rapido e honesto. O maior risco aparece quando a duvida fica em silencio."},
                {"front": "Que conta de trabalho teria maior impacto se fosse comprometida?", "back": "Essa conta deve ter as melhores praticas de senha e MFA ativado antes de qualquer outra."},
            ],
            "infographic": {"title": "Padrao de resposta segura", "items": [{"value": "1", "label": "Inspecionar remetente e URL", "detail": "Pequenas alteracoes na escrita e links incoerentes sao sinais frequentes."}, {"value": "2", "label": "Verificar fora da mensagem", "detail": "Use o site oficial ou um numero conhecido."}, {"value": "3", "label": "Reportar rapidamente", "detail": "A rapidez importa mais do que ter certeza absoluta."}]},
            "chart": {"title": "Habitos de seguranca com maior retorno", "caption": "Rotinas simples evitam uma grande parte dos ataques do dia a dia.", "bars": [{"label": "Pausa anti-phishing", "value": 84}, {"label": "Gestor de senhas", "value": 71}, {"label": "MFA ativo", "value": 92}, {"label": "Reporte rapido", "value": 76}]},
            "questions": [
                {"prompt": "Um email pede para verificar a conta em 10 minutos ou perdera o acesso. Qual e a primeira acao mais segura?", "a": "Clicar depressa para nao perder o acesso", "b": "Nao clicar, verificar o remetente e ir diretamente ao site oficial", "c": "Reencaminhar para todos os colegas", "explanation": "Urgencia com link e o padrao classico de phishing. A verificacao deve ser feita pelo canal oficial, nao pelo link da mensagem."},
                {"prompt": "Qual pratica de palavra-passe e mais forte?", "a": "Uma palavra-passe memoravel reutilizada em todas as contas", "b": "Uma frase-passe longa e unica por conta guardada num gestor de senhas", "c": "O seu nome e ano de nascimento", "explanation": "Senhas unicas e longas reduzem o impacto de uma violacao num unico servico. A reutilizacao multiplica o dano."},
                {"prompt": "Qual e o principal beneficio de ativar MFA?", "a": "Permite usar uma senha mais curta", "b": "Mesmo com a senha, o atacante continua sem acesso sem o segundo fator", "c": "Elimina totalmente a necessidade de senha", "explanation": "O segundo fator reduz drasticamente o impacto do roubo de credenciais."},
                {"prompt": "Clicou num link e depois a pagina pareceu suspeita. O que deve fazer?", "a": "Ficar em silencio e esperar", "b": "Reportar imediatamente a equipa de IT ou seguranca, mesmo sem certeza total", "c": "Mudar a senha em alguns dias", "explanation": "Rapidez vale mais do que certeza. Um reporte precoce permite conter o incidente antes de se alargar."},
                {"prompt": "Uma pessoa diz ser do suporte IT e pede a sua senha para resolver um problema urgente. O que faz?", "a": "Fornece, porque o suporte deve ter acesso", "b": "Recusa e confirma a identidade pelo numero oficial do servico", "c": "Da uma senha temporaria", "explanation": "Suporte legitimo nao precisa da sua senha. E preciso verificar por um canal oficial conhecido."},
            ],
        },
    },
    "financial-reporting-essentials": {
        "fr": {
            "preview": {"kicker": "La finance rendue lisible", "headline": "Lire l'histoire derriere les etats", "caption": "Un resume visuel qui transforme compte de resultat, bilan et tresorerie en decisions praticables pour les managers.", "stats": [{"value": "3", "label": "Etats cles"}, {"value": "1", "label": "Lecture cash critique"}], "tags": ["Managers", "Decision", "Bilingue"]},
            "flip_cards": [
                {"front": "Si le chiffre d'affaires monte mais que le profit baisse, quelle ligne de cout examineriez-vous d'abord ?", "back": "Suivez l'histoire du revenu a la marge brute puis au resultat d'exploitation. Le premier ecart inhabituel indique souvent la fuite de marge."},
                {"front": "Avez-vous deja vu un projet paraitre solide sur le papier tout en creant une tension budgetaire ?", "back": "C'est generalement une question de timing. Le profit mesure la performance, la tresorerie mesure la capacite a tenir."},
                {"front": "Quelle question pourriez-vous poser a votre prochaine revue budgetaire pour montrer un meilleur jugement financier ?", "back": "Demandez ce qui a change entre la croissance du revenu et la conversion en cash, ou quelle ligne de depense s'est ecartee du plan."},
            ],
            "infographic": {"title": "Carte rapide des etats", "items": [{"value": "P&L", "label": "Suit le profit dans le temps", "detail": "Montre revenus, couts directs, charges d'exploitation et resultat net."}, {"value": "Bilan", "label": "Montre ce qui est possede et du", "detail": "Photo a une date donnee des actifs, passifs et capitaux."}, {"value": "Cash", "label": "Explique les mouvements d'argent", "detail": "Montre si l'organisation peut reellement financer son activite."}]},
            "chart": {"title": "Exemple de performance mensuelle", "caption": "Une comparaison simple montre pourquoi un bon revenu ne garantit pas une tresorerie saine.", "bars": [{"label": "Revenus", "value": 88}, {"label": "Marge brute", "value": 63}, {"label": "Resultat net", "value": 39}, {"label": "Cash disponible", "value": 28}]},
            "questions": [
                {"prompt": "Quel etat montre si l'organisation a realise un profit sur une periode ?", "a": "Le bilan", "b": "Le compte de resultat", "c": "Le registre des actifs", "explanation": "Le compte de resultat presente revenus et charges sur une periode pour aboutir a un profit ou a une perte."},
                {"prompt": "Le revenu de votre division a augmente de 15 % mais le resultat net a baisse. Ou regarder d'abord ?", "a": "Dans la colonne des actifs du bilan", "b": "Dans les lignes de cout entre le revenu et le resultat net", "c": "Dans le solde de tresorerie d'ouverture", "explanation": "Si le revenu augmente alors que le profit baisse, les couts ont evolue plus vite. Il faut suivre les lignes de cout du haut vers le bas."},
                {"prompt": "Une entreprise affiche un bon profit ce trimestre mais peine a payer ses fournisseurs. Quelle explication est la plus probable ?", "a": "Les comptables ont commis une erreur", "b": "Le revenu est comptabilise quand il est gagne, mais le cash n'est peut-etre pas encore encaisse", "c": "Les factures fournisseurs ne sont enregistrees qu'au paiement", "explanation": "Le profit repose sur l'activite comptabilisee, alors que la tresorerie depend du mouvement reel d'argent. L'ecart de timing explique la tension."},
                {"prompt": "Le bilan montre 500 000 $ d'actifs et 320 000 $ de passifs. Quelle est la position nette ?", "a": "820 000 $", "b": "180 000 $", "c": "320 000 $", "explanation": "Les actifs nets correspondent aux actifs moins les passifs : 500 000 moins 320 000 egalent 180 000."},
            ],
        },
        "pt": {
            "preview": {"kicker": "Financas em linguagem clara", "headline": "Ler a historia por tras das demonstracoes", "caption": "Um resumo visual que transforma demonstracao de resultados, balanco e caixa em decisoes acionaveis para gestores.", "stats": [{"value": "3", "label": "Demonstracoes-chave"}, {"value": "1", "label": "Lente critica de caixa"}], "tags": ["Gestao", "Decisao", "Bilingue"]},
            "flip_cards": [
                {"front": "Se a receita sobe mas o lucro cai, que linha de custo examinaria primeiro no seu contexto?", "back": "Siga a historia da receita ate a margem bruta e depois ao lucro operacional. O primeiro desvio inesperado costuma revelar onde a margem esta a escapar."},
                {"front": "Ja viu um projeto parecer bem-sucedido no papel e mesmo assim gerar pressao orcamental?", "back": "Isso normalmente e um problema de timing. Lucro mede desempenho; caixa mede sobrevivencia operacional."},
                {"front": "Que pergunta poderia fazer na proxima reuniao de revisao para mostrar melhor julgamento financeiro?", "back": "Pergunte o que mudou entre o crescimento da receita e a conversao em caixa, ou qual linha de despesa se afastou do plano."},
            ],
            "infographic": {"title": "Mapa rapido das demonstracoes", "items": [{"value": "DR", "label": "Acompanha o lucro no tempo", "detail": "Mostra receitas, custos diretos, despesas operacionais e resultado liquido."}, {"value": "Balanco", "label": "Mostra o que se possui e se deve", "detail": "Retrato num ponto no tempo de ativos, passivos e capital proprio."}, {"value": "Caixa", "label": "Explica o movimento do dinheiro", "detail": "Revela se a organizacao consegue financiar as operacoes."}]},
            "chart": {"title": "Exemplo de desempenho mensal", "caption": "Uma comparacao simples mostra porque receita forte nao significa caixa saudavel.", "bars": [{"label": "Receita", "value": 88}, {"label": "Margem bruta", "value": 63}, {"label": "Lucro liquido", "value": 39}, {"label": "Caixa disponivel", "value": 28}]},
            "questions": [
                {"prompt": "Que demonstracao mostra se a organizacao obteve lucro num periodo?", "a": "O balanco", "b": "A demonstracao de resultados", "c": "O registo de ativos", "explanation": "A demonstracao de resultados apresenta receitas e gastos de um periodo para chegar ao lucro ou prejuizo."},
                {"prompt": "A receita da sua divisao cresceu 15%, mas o lucro liquido caiu. Onde olhar primeiro para perceber por que motivo?", "a": "Na coluna de ativos do balanco", "b": "Nas linhas de custo entre a receita e o lucro liquido", "c": "No saldo inicial do fluxo de caixa", "explanation": "Se a receita sobe e o lucro cai, os custos cresceram mais rapidamente. E preciso seguir as linhas de custo na demonstracao."},
                {"prompt": "Uma empresa apresenta bom lucro no trimestre, mas tem dificuldade em pagar fornecedores. Qual e a explicacao mais provavel?", "a": "Os contabilistas cometeram um erro", "b": "A receita e reconhecida quando e obtida, mas o dinheiro pode ainda nao ter entrado", "c": "As faturas de fornecedores so sao registadas quando pagas", "explanation": "Lucro segue o principio do acrescimo; caixa depende do movimento real de dinheiro. O diferimento entre ambos explica a tensao."},
                {"prompt": "O balanco mostra ativos totais de 500 000 $ e passivos totais de 320 000 $. Qual e a posicao liquida?", "a": "820 000 $", "b": "180 000 $", "c": "320 000 $", "explanation": "Posicao liquida = ativos menos passivos. 500 000 menos 320 000 resulta em 180 000."},
            ],
        },
    },
    "data-analytics-accountancy": {
        "fr": {
            "preview": {"kicker": "Studio d'analyse d'audit", "headline": "Transformer des signaux en constats clairs", "caption": "Un scenario visuel qui relie tests de donnees et jugement professionnel pour expliquer une anomalie avec credibilite.", "stats": [{"value": "5", "label": "Etapes du flux"}, {"value": "87", "label": "Depenses signalees"}], "tags": ["Audit", "Preuve visuelle", "Bilingue"]},
            "flip_cards": [
                {"front": "Qu'est-ce qui vous ferait suffisamment confiance a une anomalie pour l'escalader ?", "back": "Il faut du contexte, des pieces justificatives et une idee claire de ce que le comportement normal aurait du etre."},
                {"front": "Quel visuel aiderait le plus vite un CFO a comprendre un evitement de seuil ?", "back": "Utilisez le graphique le plus simple qui rend le motif evident. Les distributions parlent souvent mieux que les tableaux."},
                {"front": "Comment eviter de sur-interpreter un resultat analytique ?", "back": "Formulez-le comme observation, importance et prochaine action. Un signal d'alerte n'est pas un verdict."},
            ],
            "infographic": {"title": "Flux d'analyse", "items": [{"value": "Profiler", "label": "Comprendre comptes, dates et ecarts", "detail": "Etablissez le comportement de base avant d'appliquer des tests."}, {"value": "Tester", "label": "Lancer des verifications ciblees", "detail": "Doublons, seuils, Benford et concentration par fournisseur."}, {"value": "Expliquer", "label": "Traduire le constat", "detail": "Dire ce qui apparait, pourquoi cela compte et quelle suite proposer."}]},
            "chart": {"title": "Concentration des depenses pres du seuil", "caption": "Une vue par tranches rend le pic juste sous la limite immediatement visible.", "bars": [{"label": "4,4k", "value": 29}, {"label": "4,6k", "value": 37}, {"label": "4,8k", "value": 91}, {"label": "5,0k+", "value": 18}]},
            "questions": [
                {"prompt": "Dans un jeu de depenses, plusieurs transactions se concentrent juste sous le seuil d'approbation de 5 000 $. Que faut-il en conclure d'abord ?", "a": "Rien, car tout montant sous le seuil est forcement conforme", "b": "Cela merite une revue plus precise car ce motif peut signaler un evitement de seuil", "c": "Il faut licencier immediatement les agents concernes", "explanation": "Une concentration juste sous un seuil de controle est un signal d'alerte a investiguer, pas une preuve a elle seule."},
                {"prompt": "Que predit la loi de Benford pour un ensemble naturel de montants factures ?", "a": "Les chiffres 1 a 9 doivent apparaitre aussi souvent en premiere position", "b": "Les petits chiffres comme 1, 2 ou 3 apparaissent plus souvent en premiere position", "c": "La majorite des montants doivent finir par zero", "explanation": "La loi de Benford predit une frequence plus elevee des petits chiffres en tete. Un ecart important justifie une analyse plus poussee."},
                {"prompt": "Vous detectez une anomalie importante dans les donnees. Quelle est la bonne etape suivante ?", "a": "La declarer immediatement comme fraude confirmee", "b": "La documenter comme point a investiguer, pas comme conclusion", "c": "Supprimer les lignes anormales et relancer l'analyse", "explanation": "Une anomalie est une question a traiter. Elle doit etre documentee et verifiee avant toute conclusion."},
                {"prompt": "Vous devez montrer a un CFO que des depenses se concentrent anormalement autour du seuil de 5 000 $. Quelle visualisation convient le mieux ?", "a": "Un tableau de toutes les transactions superieures a 4 500 $", "b": "Un diagramme en barres par tranche de 200 $ avec le seuil indique", "c": "Un camembert des depenses par categorie", "explanation": "Le diagramme en barres par tranche montre immediatement le pic juste sous le seuil, sans longue explication."},
            ],
        },
        "pt": {
            "preview": {"kicker": "Estudio de analitica de auditoria", "headline": "Transformar sinais em conclusoes claras", "caption": "Um cenario visual que liga testes de dados ao julgamento profissional necessario para explicar uma anomalia com credibilidade.", "stats": [{"value": "5", "label": "Etapas do fluxo"}, {"value": "87", "label": "Despesas sinalizadas"}], "tags": ["Auditoria", "Evidencia visual", "Bilingue"]},
            "flip_cards": [
                {"front": "O que o faria confiar numa anomalia ao ponto de a escalar para revisao?", "back": "Precisa de contexto, documentacao e uma ideia clara de como o comportamento normal deveria ser antes de avaliar o pico."},
                {"front": "Que visual ajudaria mais rapidamente um CFO a perceber evitacao de limite?", "back": "Use o grafico mais simples que torne o padrao obvio. Distribuicoes costumam funcionar melhor do que tabelas densas."},
                {"front": "Como evita exagerar uma constatacao analitica?", "back": "Descreva-a como observacao, relevancia e proximo passo. Um alerta nao e um veredito."},
            ],
            "infographic": {"title": "Fluxo analitico", "items": [{"value": "Perfil", "label": "Compreender contagens, datas e lacunas", "detail": "Defina o comportamento base antes de aplicar testes."}, {"value": "Testar", "label": "Executar verificacoes direcionadas", "detail": "Duplicados, limites, Benford e concentracao por fornecedor."}, {"value": "Explicar", "label": "Traduzir a constatacao", "detail": "Dizer o que apareceu, porque importa e qual deve ser o passo seguinte."}]},
            "chart": {"title": "Concentracao de despesas perto do limite", "caption": "Uma visao por faixas torna o agrupamento logo abaixo do limite imediatamente visivel.", "bars": [{"label": "4,4k", "value": 29}, {"label": "4,6k", "value": 37}, {"label": "4,8k", "value": 91}, {"label": "5,0k+", "value": 18}]},
            "questions": [
                {"prompt": "Num conjunto de despesas, varias transacoes concentram-se logo abaixo do limite de aprovacao de 5 000 $. O que isso justifica mais provavelmente?", "a": "Nada, porque valores abaixo do limite sao sempre conformes", "b": "Uma revisao mais atenta, porque o padrao pode indicar evitacao de limite", "c": "Demissao imediata das pessoas envolvidas", "explanation": "Concentracao logo abaixo de um limite de controlo e um sinal de alerta a investigar, nao prova conclusiva."},
                {"prompt": "O que preve a Lei de Benford para um conjunto natural de montantes faturados?", "a": "Os digitos de 1 a 9 devem surgir com a mesma frequencia inicial", "b": "Digitos menores como 1, 2 e 3 aparecem mais vezes como primeiro digito", "c": "A maioria dos montantes deve terminar em zero", "explanation": "A Lei de Benford indica maior frequencia de digitos pequenos na primeira posicao. Um desvio relevante justifica analise adicional."},
                {"prompt": "Identificou uma anomalia significativa nos dados. Qual e o passo seguinte correto?", "a": "Reporta-la imediatamente como fraude confirmada", "b": "Documenta-la como uma questao a investigar, nao como conclusao final", "c": "Apagar os registos anormais e repetir a analise", "explanation": "Uma anomalia e um ponto de investigacao. Deve ser documentada e verificada antes de qualquer conclusao."},
                {"prompt": "Precisa de mostrar a um CFO que as despesas se concentram de forma anormal perto do limite de 5 000 $. Que visualizacao funciona melhor?", "a": "Uma tabela com todas as transacoes acima de 4 500 $", "b": "Um grafico de barras por faixas de 200 $ com o limite assinalado", "c": "Um grafico circular do gasto por categoria", "explanation": "O grafico de barras por faixas torna o pico imediatamente evidente sem exigir uma explicacao longa."},
            ],
        },
    },
}


def merge_dict(base: dict, override: dict) -> dict:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_dict(merged[key], value)
        else:
            merged[key] = value
    return merged


def get_sample_extras(slug: str) -> dict:
    extras = SAMPLE_EXTRAS.get(slug, {})
    localized = LOCALIZED_INTERACTIVE_CONTENT.get(slug)
    if not localized:
        return extras

    merged = merge_dict({}, extras)
    merged.setdefault("translations", {})
    for locale, locale_extra in localized.items():
        existing = merged["translations"].get(locale, {})
        merged["translations"][locale] = merge_dict(existing, locale_extra)
    return merged


BLOG_POSTS = [
    {
        "slug": "digital-academies-engagement",
        "title": "Why Digital Academies Need Strong Learner Engagement Strategies",
        "category": "Digital Academy Strategy",
        "excerpt": "A great platform is not enough. Completion comes from deliberate engagement design, not hope.",
        "body": "Many organisations launch a digital academy, fill it with good courses, and then wonder why completion stays low.\n\nThe platform is only the stage. Engagement is the script. A learner who enrols and hears nothing for two weeks has effectively left. Welcome messages, timely nudges, and re engagement campaigns are not extras, they are the difference between a library and a learning programme.\n\nThe practical move is to map the learner journey and attach a communication to each moment that matters: enrolment, first inactivity, mid course, and completion.",
    },
    {
        "slug": "ai-tutors-online-learners",
        "title": "How AI Tutors Can Support Online Learners",
        "category": "AI in Learning",
        "excerpt": "Used well, an AI copilot extends support to every learner at any hour, without replacing the human.",
        "body": "An AI tutor is most useful as a patient first responder. It answers the small questions that would otherwise stall a learner at 9pm when no facilitator is online.\n\nThe key is scope. Ground the assistant in your own course content, set clear limits, and route anything high stakes back to a human. Done this way, AI raises the floor of support without pretending to be the ceiling.",
    },
    {
        "slug": "moodle-at-scale-lessons",
        "title": "Lessons Learned from Managing Moodle at Scale",
        "category": "Moodle Tips",
        "excerpt": "Running Moodle for thousands of learners across languages teaches you to design for maintenance, not just launch.",
        "body": "At scale, the work is rarely the launch. It is the second year: plugin updates, course archiving, role hygiene, and support that does not fall over.\n\nThree habits pay off: keep a clean role and permission structure, document your configuration so it survives staff changes, and build learner support workflows before you need them.",
    },
    {
        "slug": "instructional-design-professional-training",
        "title": "The Role of Instructional Design in Professional Training",
        "category": "Instructional Design",
        "excerpt": "Good content is not a good course. Design is what turns information into capability.",
        "body": "Subject matter experts know the content. Instructional design decides how that content becomes something a busy professional can actually learn and apply.\n\nOutcomes first, then assessment, then the lesson. When you design in that order, every activity has a job, and nothing is in the course just because it was easy to add.",
    },
    {
        "slug": "lms-analytics-completion",
        "title": "Using LMS Analytics to Improve Course Completion",
        "category": "LMS Lessons Learned",
        "excerpt": "Your LMS already knows who is about to drop off. The question is whether anyone is looking.",
        "body": "Completion rarely fails at the end. It fails quietly in the first week. Analytics let you see the drop off curve and act before learners disappear.\n\nStart simple: a weekly view of progress and last activity, a flag for learners who stalled, and one re engagement message. Measure, then refine.",
    },
]


def run() -> None:
    init_db()
    with Session(ENGINE) as s:
        for data in SAMPLES:
            course_data = {field: data[field] for field in COURSE_FIELDS}
            questions = data["questions"]
            course = s.exec(
                select(SampleCourse).where(SampleCourse.slug == data["slug"])
            ).first()
            if course:
                for key, value in course_data.items():
                    setattr(course, key, value)
            else:
                course = SampleCourse(**course_data)
                s.add(course)
            s.commit()
            s.refresh(course)

            existing_questions = s.exec(
                select(QuizQuestion).where(QuizQuestion.course_id == course.id)
            ).all()
            for q in existing_questions:
                s.delete(q)
            s.commit()

            for i, q in enumerate(questions):
                s.add(QuizQuestion(
                    course_id=course.id, order=i, prompt=q["prompt"],
                    option_a=q["a"], option_b=q["b"], option_c=q["c"],
                    correct=q["correct"], explanation=q["explanation"],
                ))
            s.commit()

        for p in BLOG_POSTS:
            post = s.exec(select(BlogPost).where(BlogPost.slug == p["slug"])).first()
            if post:
                for key, value in p.items():
                    setattr(post, key, value)
            else:
                s.add(BlogPost(**p))
        s.commit()
        print("Seeded or updated sample courses and blog posts.")


if __name__ == "__main__":
    run()
