"""
Central content for the site.

Everything that is static copy lives here so pages stay data driven and easy
to edit in one place. Dynamic data (sample courses, blog posts, quiz answers,
contact leads) lives in the database instead. See models.py and seed.py.

Writing rule for this project: no em dashes anywhere. Use commas, colons,
periods, or parentheses.
"""

SITE = {
    "name": "Paseka Seleke - Consultancy Services",
    "tagline": "eLearning, LMS, and AI-Powered Learning Solutions",
    "email": "ppseleke@outlook.com",      # replace with your real address
    "phone": "+250 78 033 6573",           # replace with your real number
    "location": "Kigali, Rwanda ",
    "linkedin": "https://www.linkedin.com/in/paseka-seleke",
    "year": 2026,
}

# Top navigation. (label, route name)
NAV = [
    ("Home", "home"),
    ("About", "about"),
    ("Services", "services"),
    ("Sample Courses", "samples"),
    ("Blog", "blog"),
    ("Contact", "contact"),
]

SERVICE_MENU = [
    ("Instructional Design", "instructional-design"),
    ("Virtual Training", "virtual-training"),
    ("LMS Training", "lms-services"),
    ("AI Learning", "ai-learning"),
    ("Learner Engagement and Increased Participations", "engagement"),
]

# The six headline value propositions on the home page.
VALUE_PROPS = [
    ("Instructional Design", "Course design, assessments, storyboarding, and learner journeys grounded in real pedagogy."),
    ("LMS Setup and Administration", "Moodle and other platforms set up, configured, and kept running smoothly."),
    ("Digital Academy Development", "Scalable, multi tenant academies that serve many groups from one ecosystem."),
    ("Virtual Training and Webinars", "End to end support for live online sessions, from setup to reporting."),
    ("AI Integration for Learning", "Practical AI for personalisation, content, translation, and learner support."),
    ("Engagement and Marketing", "Automated campaigns that lift participation and course completion."),
]

WHO_I_HELP = [
    "Training academies",
    "Universities and colleges",
    "NGOs and development organisations",
    "Government institutions",
    "Professional bodies",
    "Corporate training teams",
    "Digital transformation programmes",
]

# ---------------------------------------------------------------------------
# CV profile (based on your real background). Edit freely.
# Items marked with [Insert ...] are placeholders for you to fill in.
# ---------------------------------------------------------------------------
CV = {
    "summary": (
        "Paseka is an eLearning and digital learning specialist with experience in "
        "online learning management, Moodle administration, instructional design, "
        "webinar facilitation, LMS development, learner engagement,Project Management and digital "
        "academy implementation. He supports organisations in creating scalable, "
        "accessible, and engaging learning ecosystems that combine strong pedagogy, "
        "practical technology, and modern learner experience design."
    ),
    "experience": [
        {
            "role": "Online Learning Facilitator and Platform Operations",
            "org": "Smart Africa Digital Academy (SADA), Smart Africa",
            "period": "Current",
            "points": [
                "Manage online learning operations and the learning platform across Sub Saharan Africa, in partnership with the World Bank.",
                "Administer Moodle LMS: course setup, quiz configuration, grading, certificates, plugins, and learner support.",
                "Produce multilingual learning communications and marketing in English, French, and Portuguese.",
                "Coordinate webinars, regional workshops, and events, including setup, facilitation support, and reporting.",
                "Maintain internal documentation, readiness checklists, and platform processes.",
            ],
        },
        {
            "role": "Online Learning Manager",
            "org": "African Professionalisation Initiative",
            "period": "Previous",
            "points": [
                "Led online learning delivery and learner management for professional development programmes.",
                "Designed and quality assured courses, assessments, and learner journeys.",
                "Supported instructors and learners across the full course lifecycle.",
            ],
        },
    ],
    "skills": [
        "Instructional design (ADDIE, Bloom's, SAM, Gagne)",
        "Moodle LMS administration",
        "Course and assessment authoring",
        "Webinar and virtual event facilitation",
        "Multilingual content (English, French, Portuguese)",
        "Learner engagement and email marketing",
        "Python and FastAPI",
        "React and AI assisted development workflows",
    ],
    "lms_platforms": ["Moodle", "LearnDash", "Brightspace", "Canvas", "MOOC platforms"],
    "id_tools": ["Articulate Rise", "Articulate 365", "H5P", "Storyboarding", "Quiz and assessment design"],
    "projects": [
        "SADA self paced course catalogue and trilingual launch communications.",
        "Regional data governance and cybersecurity webinar series support.",
        "Moodle at scale: administration, optimisation, and learner support workflows.",
      #  "[Insert Paseka's CV details here: add 2 to 3 of your strongest named projects.]",
    ],
  #  "certifications": [
  #      "[Insert Paseka's CV details here: certifications and professional development.]",
  #  ],
}

# ---------------------------------------------------------------------------
# Instructional design frameworks (with mock course examples).
# ---------------------------------------------------------------------------
FRAMEWORKS = [
    {
        "code": "ADDIE",
        "name": "ADDIE",
        "desc": "A structured model covering Analysis, Design, Development, Implementation, and Evaluation.",
        "course": "Introduction to Cybersecurity for Public Sector Professionals",
        "steps": [
            "Needs analysis quiz",
            "Course map",
            "Interactive lesson",
            "Knowledge check",
            "Final assessment",
            "Evaluation survey",
        ],
    },
    {
        "code": "BLOOM",
        "name": "Bloom's Taxonomy",
        "desc": "A framework for designing outcomes and assessments across levels of thinking, from remembering to creating.",
        "course": "AI Fundamentals for Policy Makers",
        "steps": [
            "Remember: define artificial intelligence",
            "Understand: explain common AI use cases",
            "Apply: identify AI opportunities in public services",
            "Analyse: compare risks and benefits",
            "Evaluate: review an AI governance scenario",
            "Create: draft a basic AI adoption plan",
        ],
    },
    {
        "code": "SAM",
        "name": "Successive Approximation Model (SAM)",
        "desc": "An agile model focused on rapid prototyping, testing, feedback, and iteration.",
        "course": "Financial Reporting Basics for Non Finance Managers",
        "steps": [
            "Rapid prototype lesson",
            "Client feedback checkpoint",
            "Interactive financial statement activity",
            "Improved course version",
            "Learner testing summary",
        ],
    },
    {
        "code": "GAGNE",
        "name": "Gagne's Nine Events of Instruction",
        "desc": "A structured approach that gains attention, guides learning, supports practice, and assesses performance.",
        "course": "Using Data Analytics in Accountancy",
        "steps": [
            "Gain attention with a real world audit data problem",
            "State learning objectives",
            "Activate prior knowledge",
            "Present content",
            "Provide guided examples",
            "Let learners practice",
            "Give feedback",
            "Assess performance",
            "Support retention and transfer",
        ],
    },
]

# ---------------------------------------------------------------------------
# Service pages. Each is rendered by one shared template (service_page.html).
# Keyed by slug used in the URL: /services/<slug>
# ---------------------------------------------------------------------------
SERVICE_PAGES = {
    "instructional-design": {
        "nav_label": "Instructional Design",
        "title": "Instructional Design Services",
        "intro": "Courses that are clear, engaging, and built on real pedagogy, from a single module to a full curriculum.",
        "groups": [
            {
                "heading": "What I design",
                "items": [
                    "Course design and curriculum mapping",
                    "Learning outcomes development",
                    "Assessment design",
                    "Storyboarding",
                    "Learner journey design",
                    "Interactive learning activities",
                    "Scenario based learning",
                    "Microlearning design",
                    "eLearning quality assurance",
                    "Multilingual and localised learning design",
                ],
            },
        ],
        "show_frameworks": True,
        "cta": ("See sample learning experiences", "samples"),
    },
    "virtual-training": {
        "nav_label": "Virtual Training",
        "title": "Online and Virtual Training Services",
        "intro": "End to end support for live online learning, so your sessions run smoothly and your learners stay engaged.",
        "groups": [
            {
                "heading": "Services",
                "items": [
                    "Virtual training coordination",
                    "Online workshop support",
                    "Webinar facilitation",
                    "Speaker and participant support",
                    "Zoom and Webex administration",
                    "Live session moderation",
                    "Breakout room management",
                    "Attendance tracking",
                    "Polls, Q and A, and engagement support",
                    "Post webinar reporting",
                    "Certificate and completion support",
                ],
            },
        ],
        "process": {
            "heading": "End to end webinar and virtual event support",
            "steps": [
                "Planning",
                "Platform setup",
                "Registration configuration",
                "Speaker preparation",
                "Live facilitation",
                "Engagement and support",
                "Reporting and follow up",
            ],
        },
        "cta": ("Request a proposal", "contact"),
    },
    "lms-services": {
        "nav_label": "LMS Services",
        "title": "LMS Setup, Administration, and Development",
        "intro": "Set up, configure, and run your learning platform, with deep Moodle expertise and support across major systems.",
        "platforms": [
            ("Moodle", "Setup, administration, course management, quiz configuration, grading, certificates, plugins, reporting, learner support, and optimisation."),
            ("LearnDash", "WordPress based LMS setup for flexible course sales, learner management, certificates, and training portals."),
            ("MOOC platforms", "Scalable open online courses, learner pathways, assessments, and digital academy models."),
            ("Brightspace", "Course structuring, learner experience design, platform administration, and institutional delivery."),
            ("Canvas", "Course setup, learning pathways, assessment management, and digital learning implementation."),
        ],
        "groups": [
            {
                "heading": "Services per platform",
                "items": [
                    "LMS setup", "Course configuration", "User management",
                    "Roles and permissions", "Gradebook setup", "Assessment configuration",
                    "Certificates and badges", "Reporting and analytics", "Theme customisation",
                    "Plugin configuration", "Learner support workflows", "Maintenance and troubleshooting",
                ],
            },
        ],
        "cta": ("Book a consultation", "contact"),
    },
    "ai-learning": {
        "nav_label": "AI Learning",
        "title": "Other eLearning Development Services",
        "intro": "Digital academies, AI enhanced learning, and analytics that turn platform data into decisions.",
        "groups": [
            {
                "heading": "Digital academies and multi tenancy LMS",
                "items": [
                    "Digital academy planning", "Multi tenant LMS structure",
                    "Branded learning portals", "Country or department based workspaces",
                    "Role based access", "Course catalogues",
                    "Reporting dashboards", "Scalable learner onboarding",
                ],
            },
            {
                "heading": "AI integration to enhance learning",
                "items": [
                    "AI driven personalisation", "Generative AI copilots and tutors",
                    "AI powered translations", "Localised learning",
                    "AI assisted content development", "AI powered learner support",
                    "LMS analytics", "Learning risk identification", "Automated recommendations",
                ],
            },
            {
                "heading": "LMS analytics",
                "items": [
                    "Course completion dashboards", "Learner progress reports",
                    "Assessment performance reports", "Engagement tracking",
                    "Drop off analysis", "At risk learner identification",
                    "Executive reporting dashboards",
                ],
            },
        ],
        "cta": ("Explore a pilot", "contact"),
    },
    "engagement": {
        "nav_label": "Engagement",
        "title": "eLearning Communication, Engagement, and Marketing",
        "intro": "Automated communication that lifts participation and course completion across every channel.",
        "groups": [
            {
                "heading": "Services",
                "items": [
                    "Automated learner notifications", "Email campaigns", "LMS announcements",
                    "WhatsApp communication workflows", "SMS reminders", "Social media campaigns",
                    "Digital outlet campaigns", "Learner onboarding campaigns", "Course launch campaigns",
                    "Re engagement campaigns", "Completion reminders", "Certificate announcement campaigns",
                ],
            },
        ],
        "process": {
            "heading": "Engagement automation workflow",
            "steps": [
                "Learner enrols",
                "Welcome message is sent",
                "Course reminder is triggered",
                "Inactive learner alert is sent",
                "Assessment reminder is sent",
                "Completion message is sent",
                "Certificate notification is sent",
                "Feedback survey is sent",
            ],
        },
        "cta": ("Plan a campaign", "contact"),
    },
}

# Maps the simple NAV labels to service slugs so the navbar can link correctly.
NAV_SLUGS = {
    "Instructional Design": "instructional-design",
    "Virtual Training": "virtual-training",
    "LMS Services": "lms-services",
    "AI Learning": "ai-learning",
    "Engagement": "engagement",
}
