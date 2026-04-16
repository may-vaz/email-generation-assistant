# scenarios.py
"""
Test scenarios: 10 unique (intent, facts, tone) inputs + human reference emails.
Human reference emails serve as the gold standard for evaluation.

Coverage across:
- Emotional range: apologetic, urgent, warm, formal, celebratory
- Contexts: B2B, academic, internal comms, job search, customer support
- Fact complexity: 4–5 facts per scenario (varied specificity)
"""

SCENARIOS = [
    {
        "id": 1,
        "intent": "Follow up after a job interview",
        "facts": [
            "Interview was for a Senior Product Manager role",
            "Interviewed with Sarah Chen (VP of Product) on April 10th",
            "Discussed roadmap prioritization and OKR alignment",
            "Still very interested in the role",
        ],
        "tone": "grateful and professional",
        "reference": """Subject: Thank You — Senior PM Interview on April 10th

Hi Sarah,

Thank you for taking the time to speak with me on Thursday. I genuinely enjoyed our conversation about roadmap prioritization and how the team approaches OKR alignment — it gave me a much clearer picture of the challenges and opportunities in the role.

The discussion reinforced my enthusiasm for the Senior Product Manager position. I left the conversation even more confident that my background in cross-functional prioritization would translate well to what your team is building.

Please don't hesitate to reach out if you need anything further from me. I look forward to hearing about next steps.

Best regards,
[Your Name]""",
    },
    {
        "id": 2,
        "intent": "Request a meeting with a potential investor",
        "facts": [
            "Startup is in the B2B SaaS space, focused on HR automation",
            "Recently closed $500K pre-seed from angel investors",
            "Seeking a 30-minute intro call",
            "Have a pitch deck ready to share",
        ],
        "tone": "concise and confident",
        "reference": """Subject: Intro Call — HR Automation Startup (Post Pre-Seed)

Hi [Investor Name],

I'm the founder of [Company], a B2B SaaS platform automating repetitive HR workflows for mid-size companies. We recently closed a $500K pre-seed round and are now in conversations with our first institutional investors.

I'd love to schedule a 30-minute call to share our traction and roadmap. I have a pitch deck ready whenever you'd like a preview.

Would any time this week or next work for you?

Best,
[Your Name]""",
    },
    {
        "id": 3,
        "intent": "Apologize for a delayed project delivery",
        "facts": [
            "Deadline was March 31st",
            "Delivery will now happen April 18th",
            "Delay caused by unexpected API migration issues",
            "No additional cost to the client",
            "Daily progress updates will be shared",
        ],
        "tone": "apologetic and accountable",
        "reference": """Subject: Project Delay Update — New Delivery Date: April 18th

Hi [Client Name],

I want to reach out directly to apologize for missing the March 31st delivery deadline on your project.

During the final phase of development, we ran into unforeseen complications with an API migration that required us to rebuild a core component from scratch. This was entirely on our end, and I take full responsibility for not catching it earlier.

The revised delivery date is April 18th. There will be no additional cost to you as a result of this delay. Starting today, I'll be sending you daily progress updates so you always have a clear picture of where things stand.

I understand this is frustrating, and I'm committed to making sure the final delivery meets and exceeds what we originally scoped.

Thank you for your patience.

Sincerely,
[Your Name]""",
    },
    {
        "id": 4,
        "intent": "Announce a new company policy to the team",
        "facts": [
            "New policy: flexible Fridays starting May 1st",
            "Employees can work from anywhere on Fridays",
            "Core hours still apply: 10am–3pm in their local timezone",
            "Policy is permanent, not a trial",
        ],
        "tone": "upbeat and clear",
        "reference": """Subject: Introducing Flexible Fridays — Starting May 1st 🎉

Hi team,

We have some news we're excited to share: starting May 1st, every Friday is a Flexible Friday.

That means you can work from anywhere on Fridays — whether that's home, a café, or wherever you do your best thinking. The only thing that stays consistent is our core hours window: 10am–3pm in your local timezone, so we can still collaborate across time zones when needed.

This isn't a pilot. It's a permanent change, and it's our way of investing in the flexibility that helps everyone do great work.

More details will follow in our team meeting next week, but feel free to reply with any questions in the meantime.

Excited for this one,
[Your Name]""",
    },
    {
        "id": 5,
        "intent": "Send a cold outreach email to a potential partner",
        "facts": [
            "Company makes project management software",
            "Partner prospect runs a popular developer productivity newsletter (50k subscribers)",
            "Proposing a co-marketing campaign",
            "Offering a revenue share on referral signups",
        ],
        "tone": "direct and value-focused",
        "reference": """Subject: Co-Marketing Idea for Your Newsletter Audience

Hi [Name],

I'll keep this short: I think your newsletter audience and our product are a natural fit, and I'd love to explore a co-marketing partnership.

We make [Product Name], a project management tool built specifically for developer teams. Your 50,000 subscribers are exactly the people who deal with the workflow pain points we solve.

What I'm proposing is a sponsored feature or dedicated mention, backed by a revenue-share arrangement on any referral signups — so there's a real upside for you, not just a flat fee.

If this sounds like something worth a quick conversation, I'd be glad to share more details and some sample creative.

Best,
[Your Name]""",
    },
    {
        "id": 6,
        "intent": "Request a deadline extension on a university assignment",
        "facts": [
            "Assignment is due April 17th",
            "Requesting 3 extra days (new due date: April 20th)",
            "Reason: sudden illness, was bedridden for 5 days",
            "Medical certificate is available upon request",
            "All other coursework is up to date",
        ],
        "tone": "respectful and honest",
        "reference": """Subject: Extension Request — [Assignment Name] (Due April 17th)

Dear Professor [Name],

I am writing to respectfully request a short extension on the [assignment name] that is due on April 17th. I am asking for three additional days, making the revised submission date April 20th.

Over the past week, I was unexpectedly ill and bedridden for five days, which significantly disrupted my ability to complete the work. I have a medical certificate documenting this and am happy to share it upon request. All of my other coursework and participation are up to date.

I understand this may not always be possible, and I am grateful for any flexibility you are able to offer. I am committed to submitting a complete and quality piece of work by April 20th.

Thank you for your understanding.

Sincerely,
[Your Name]""",
    },
    {
        "id": 7,
        "intent": "Notify a client that a subscription is about to expire",
        "facts": [
            "Subscription expires April 30th",
            "Renewal is one click away in the dashboard",
            "Price is unchanged from last year: $299/year",
            "Offer: 10% discount if renewed before April 25th",
        ],
        "tone": "friendly and helpful",
        "reference": """Subject: Your Subscription Renews April 30th — Save 10% if You Act Early

Hi [Name],

Just a quick heads-up: your subscription is set to expire on April 30th, and we'd love to keep you on board.

The good news is renewing takes about 10 seconds — just head to your dashboard and hit "Renew." The price stays the same as last year: $299/year.

Even better: if you renew before April 25th, you'll get 10% off — bringing it down to $269. No code needed; the discount applies automatically in your dashboard.

As always, let us know if you have any questions or if there's anything we can do to make the platform more useful for you.

Thanks for being a customer,
[Your Name]""",
    },
    {
        "id": 8,
        "intent": "Recommend a colleague for a job opening",
        "facts": [
            "Colleague's name: Priya Nair",
            "Role being recommended for: UX Design Lead",
            "Priya and I worked together for 3 years at Designify",
            "She led the redesign of the core product that increased retention by 22%",
            "She is a strong communicator and natural collaborator",
        ],
        "tone": "warm and endorsing",
        "reference": """Subject: Recommendation for Priya Nair — UX Design Lead Role

Hi [Hiring Manager's Name],

I wanted to take a moment to personally recommend Priya Nair for the UX Design Lead opening at your company.

Priya and I worked closely together for three years at Designify, where she led the redesign of our core product. That project directly contributed to a 22% improvement in user retention — a result driven largely by her ability to balance user research with pragmatic design decisions under tight timelines.

What makes Priya exceptional isn't just her craft. She's one of the clearest communicators I've worked with, and she has a rare ability to bring stakeholders along on the design process without losing momentum.

I'd recommend her without hesitation. Feel free to reach out if you'd like to chat further.

Best,
[Your Name]""",
    },
    {
        "id": 9,
        "intent": "Escalate an unresolved customer support issue",
        "facts": [
            "Ticket #48291 was opened 12 days ago",
            "Issue: payments not processing since the March 14th update",
            "Three follow-up messages sent with no resolution",
            "Business has lost approximately $4,000 in failed transactions",
            "Requesting urgent escalation to a senior engineer",
        ],
        "tone": "firm and urgent",
        "reference": """Subject: Escalation Required — Ticket #48291 (Payment Processing Issue, 12 Days Unresolved)

Hi [Support Manager's Name],

I am writing to formally escalate Ticket #48291, which has been open for 12 days without resolution.

Since your March 14th platform update, our payment processing has been broken. I have sent three follow-up messages to the support team and have received no actionable response. In the meantime, we have experienced approximately $4,000 in failed transactions — a direct and ongoing business impact.

This needs to be escalated to a senior engineer immediately. We cannot continue operating with a broken payment system, and a general support queue is not the appropriate channel for an issue of this severity and duration.

I am requesting a direct line of communication with whoever is responsible for resolving this. Please respond by end of business today.

[Your Name]""",
    },
    {
        "id": 10,
        "intent": "Send a thank-you note after receiving mentorship",
        "facts": [
            "Mentor's name: Dr. Amara Osei",
            "She spent 6 months guiding the writer through a career transition into data science",
            "Writer just accepted their first data science role at a fintech company",
            "The mentor's advice on building a project portfolio was especially impactful",
        ],
        "tone": "sincere and heartfelt",
        "reference": """Subject: I Got the Job — Thank You, Dr. Osei

Dear Dr. Osei,

I have some news I've been waiting to share: I just accepted my first data science role, at a fintech company, and I genuinely could not have done it without you.

Over the past six months, your guidance reshaped how I thought about the entire transition. But what made the biggest difference was your advice on building a portfolio of real, scoped projects rather than trying to cover every possible topic. That shift in approach is what ultimately made my applications stand out.

I know how much time and energy you invest in the people you mentor, and I want you to know it meant everything to me. I hope to pay it forward someday.

With deep gratitude,
[Your Name]""",
    },
]