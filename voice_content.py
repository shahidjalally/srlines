"""Commercial copy for the voice platform and its deployment scenarios."""
AGENT = "/ai-calling-agent-pakistan.html"
RECEPTION = "/ai-receptionist-pakistan.html"
PRICING = "/ai-pbx-pricing-pakistan.html"
RESTAURANT = "/industries/restaurant-ai-calling.html"
HOSPITAL = "/industries/hospital-ai-calling.html"
SCHOOL = "/industries/school-ai-calling.html"
VIDEO = "https://youtu.be/8TfKMlWI9Qs"
VIDEO_EMBED = "https://www.youtube-nocookie.com/embed/8TfKMlWI9Qs"
VIDEO_IMAGE = "https://i.ytimg.com/vi/8TfKMlWI9Qs/hqdefault.jpg"
VIDEO_TITLE = "SRLINES AI Calling Agent and PBX demonstration"
# Use the original public publication date from the uploader, in ISO 8601.
VIDEO_UPLOAD_DATE = "2026-11-13"
CONSULT = "/contact.html?service=srlines-pbx&intent=consultation#contact-form"
QUOTE = "/contact.html?service=srlines-pbx&intent=quotation#contact-form"

LANDINGS = {
    AGENT: (
        "AI Calling Agent Pakistan",
        "Explore conversational AI voice agents for Pakistani business calls, including Urdu and English conversations, lead qualification, follow-up and human handover.",
        "AI Calling Agents for Business in Pakistan",
        "An AI calling agent listens to spoken requests and responds using business instructions. SRLINES supports inbound and outbound calls in Urdu and English, transfers to human staff, and integrates with wCRM through its AI-enabled PBX.",
        [
            ("Inbound enquiries and lead qualification", "Start with enquiries that have reliable answers. For a distributor, the agent could ask about the caller’s city and product category, give approved information and route a wholesale enquiry to sales."),
            ("Outbound calls with a defined purpose", "SRLINES supports outbound calling for flows such as requested callbacks, confirmations or follow-ups. Agree who may be contacted, caller identification, opt-out handling, retry limits and transfer behaviour before enabling the workflow."),
            ("Urdu, English and mixed-language trials", "Bring examples of real phrasing, product names, addresses and numbers to the demo. Test Urdu, English and code-switching with your callers’ accents and agree when a call should go directly to staff."),
        ],
        [
            ("How does the agent handle an unfamiliar request?", "Agree a fallback such as a human transfer, a callback request or a message for staff when the answer falls outside its instructions."),
            ("Can I trial it with a Pakistani business number?", "SRLINES assesses the number, SIP handoff and carrier terms during discovery. Test calls and routing before moving your live number."),
        ],
    ),
    RECEPTION: (
        "AI Receptionist Pakistan",
        "Plan an AI telephone receptionist for business hours, appointment enquiries, after-hours answering and transfer to Pakistani business teams.",
        "AI Receptionist for Pakistani Businesses",
        "Give callers a spoken way to reach the right team. An AI receptionist can be scoped around approved answers, opening hours and transfer rules.",
        [
            ("Map the receptionist’s first questions", "Define how the greeting identifies the business and how the agent separates appointment requests, billing questions and support calls. Keep instructions short enough to test with real caller phrasing."),
            ("Plan appointments and after-hours calls", "Without an approved calendar connection, treat a booking as a request for staff to confirm. Keep separate rules for holidays, closed departments and callers who need a callback."),
            ("Build a human route into every workflow", "Choose an extension, queue or callback route for exceptions. Test busy and unanswered transfers as well as the option to ask for a person early in the call."),
        ],
        [
            ("Can callers speak instead of pressing a key?", "Conversational AI accepts spoken requests. A keypad menu can still serve as a fallback or route callers to a fixed destination."),
            ("Can I update the receptionist’s instructions?", "Define who owns opening hours, approved answers and routing rules. Agree the update process and rerun the affected test calls after a change."),
        ],
    ),
    RESTAURANT: (
        "Restaurant AI Calling Agent Pakistan",
        "Explore AI telephone answering for Pakistani restaurants, including menu enquiries, reservations, takeaway, delivery and peak-hour transfers.",
        "AI Calling Agent for Restaurants",
        "Handle common restaurant enquiries over the phone and route calls to the right branch or staff member during busy service.",
        [
            ("Answer branch and menu questions", "A multi-branch restaurant can ask which location the caller means before sharing opening hours, pickup instructions or approved menu information. Route allergy and ingredient questions to staff when the answer is uncertain."),
            ("Handle order enquiries and reservation requests", "Capture whether the caller needs delivery, takeaway or a table, plus a time and party size when relevant. Staff confirm availability, bookings or orders unless a separately tested integration can do so."),
            ("Plan for peak hours and customer feedback", "Test Friday-evening routing and unavailable staff. Agree a callback workflow for missed calls and use outbound feedback calls only for eligible customers with a clear opt-out."),
        ],
        [
            ("Will it place orders directly in the POS?", "Direct ordering requires a separately verified POS integration. Start with order enquiries and staff handover."),
            ("Can it confirm table availability?", "A reservation can be confirmed only using a verified availability workflow or by restaurant staff."),
        ],
    ),
    HOSPITAL: (
        "Hospital and Clinic AI Receptionist Pakistan",
        "Plan an administrative AI phone receptionist for clinic information, appointment enquiries, reminders and transfer to hospital staff.",
        "AI Calling Agent for Hospitals and Clinics",
        "Give patients a telephone route to administrative help with appointments, departments and clinic information. Keep clinical judgement with qualified staff.",
        [
            ("Route appointment enquiries", "Use approved department hours, doctor schedules and branch details. With no verified scheduling link, send an appointment request to staff for confirmation before promising a slot."),
            ("Minimize patient information", "Collect only what the administrative workflow requires. Agree callback identity checks, access to recordings and transcripts, retention, notice and permissions before processing patient information."),
            ("Escalate urgent and clinical calls", "The AI receptionist does not diagnose illnesses, prescribe medication or replace medical professionals. For a medical emergency, contact local emergency services immediately or go to the nearest emergency department. Do not wait for an automated callback."),
        ],
        [
            ("Can it send appointment reminders?", "Confirm the approved reminder channel, patient preferences and disclosure rules. Keep reminder wording limited to the information needed to attend or reschedule."),
            ("Can it give treatment advice?", "Treatment and medication questions belong with qualified clinicians. Configure a route to staff for clinical questions."),
        ],
    ),
    SCHOOL: (
        "School and College AI Calling Agent Pakistan",
        "Plan an AI school receptionist for admissions, campus information, parent enquiries and transfer to school or college staff.",
        "AI Calling Agent for Schools and Colleges",
        "Give families a clear telephone route to admissions information and staff, especially when application deadlines and campus visits generate extra calls.",
        [
            ("Give families campus-specific answers", "Ask which campus, grade or programme the family is interested in. Use approved information about dates, fee schedules, documents and office hours. Send scholarship and exception enquiries to the admissions team."),
            ("Plan for peak admissions weeks", "Route new applicants, existing parents and fee enquiries to different destinations. Agree callback ownership when lines are busy and publish separate rules for campus visits and school holidays."),
            ("Keep applicant follow-up scoped", "Use approved contacts for admission follow-ups and collect only the information staff need to respond. Route student records, safeguarding concerns and individual decisions directly to authorized staff."),
        ],
        [
            ("Can the agent confirm an admission decision?", "Admissions decisions stay with authorized school staff. The calling agent can provide published information and route the enquiry."),
            ("Can parents ask about fees?", "The workflow can use an approved, dated fee schedule for the relevant campus and programme. Staff handle account-specific balances and exceptions."),
        ],
    ),
}

# Plan, inbound AI minutes, OpenAI (PKR), and SRLINES (PKR/min).
PBX_PLANS = (
    ("Starter", 200, 860, 6),
    ("Essential", 400, 1_720, 5),
    ("Growth", 750, 3_225, 4),
    ("Business", 1_400, 6_020, 3),
    ("Scale", 2_500, 10_750, 2),
)
PBX_ZONG_MINUTES = 1_100
PBX_ZONG_RATE_PKR = 3.15
PBX_ZONG_PKR = 3_465
PBX_OPENAI_RATE_USD = 0.0154
PBX_OPENAI_RATE_PKR = 4.30
PBX_SETUP_PKR = 12_000
PBX_EXTRA_MINUTE_USD = 0.05

PBX_PACKAGE_FEATURES = [
    ("AI telephone receptionist", "Answers routine questions, captures enquiries and takes booking, appointment or order requests. Configured rules can route exceptions to your team."),
    ("Business calling identity", "A DID is the number customers dial. A CLI is the authorised caller ID shown on outbound calls. Licensed telecom operators control allocation and use, subject to verification, approval and availability. A specific number or permanent ownership is not guaranteed."),
    ("Self-service web portal", "Manage AI prompts, business knowledge and automation workflows. See allocated and remaining minutes, plan expiry and available activity reports."),
    ("Shared call capacity", "Plans use a shared pool of simultaneous SIP call sessions. Fair use, network availability and shared capacity apply. Dedicated simultaneous lines are outside the package."),
]

PBX_PRICING_FAQS = [
    ("How are inbound AI minutes counted?", "Each connected AI session uses the plan’s inbound AI allowance and is rounded up to the next full minute per call."),
    ("Do unused minutes roll over?", "Unused minutes expire at the end of each prepaid 30-day cycle without rollover or refund. Service may pause when the allowance or prepaid credit runs out."),
    ("Are outbound calls included?", "Outbound calls are billed separately unless included by written agreement. Charges cover AI processing, applicable operator airtime, taxes and destination-based charges. SRLINES confirms the rates before activation."),
    ("Can I activate any number or outbound caller ID?", "Activation requires operator approval, customer verification (KYC), a lawful business purpose and availability. Confirm number allocation and outbound caller-ID use before publishing a number."),
]

PBX_PACKAGE_TERMS = [
    ("Billing and renewals", "Pay for each 30-day cycle in advance. Package totals are shown in PKR. Applicable taxes and any additional third-party charges are extra. The setup fee is non-refundable once implementation starts. Material changes and custom work require separate written approval."),
    ("Pricing changes", "Prices, included minutes, extra-minute charges and service conditions may change because of exchange rates, inflation, taxes, operator tariffs or AI-provider pricing. SRLINES communicates changes before the next renewal. Existing prepaid periods remain subject to applicable law and agreed terms."),
    ("Consent and acceptable use", "Customers are responsible for lawful calling lists, consent, marketing restrictions, notices and recording permissions. Spoofing, spam, fraud, harassment and unlawful automated dialling are prohibited. SRLINES may suspend misuse or act on regulator or operator instructions."),
    ("AI and data handling", "AI can give inaccurate answers. Review prompts, business information and high-impact workflows. Minimise sensitive personal or medical information and manage authorised portal users. The infrastructure and AI providers needed to deliver the service process data under applicable policies."),
    ("Availability and liability", "Shared telecom capacity, networks, operators and AI services can experience interruptions. Call-answer rates, uptime, sales outcomes and suitability for emergency services are not guaranteed. As permitted by law, liability is limited to fees paid for the affected service in the preceding 30 days, and indirect losses are excluded."),
]

PBX_SECTIONS = [
    ("Conversational AI and business telephony", "SRLINES AI Calling Agent and AI-Enabled PBX is a wCRM-integrated business communication platform for Pakistani businesses. Conversational AI listens to a caller’s request and responds using business instructions. Traditional interactive voice response (IVR) plays prompts and routes by menu choice, including DTMF keypad input. A deployment can combine the two."),
    ("Inbound calls, outbound workflows and human handover", "The agent handles inbound and outbound calls in Urdu and English, transfers callers to staff and integrates with wCRM. Scope individual workflows for receptionist enquiries, lead qualification, order questions, appointment requests and follow-ups. Agree approved answers and escalation rules, then test conversational context and any booking or CRM actions."),
    ("PBX routing, recording and reporting", "SRLINES PBX supports layered IVR, team extensions, routing, managed SIP connectivity, call recording and reporting. Review queue behaviour, call history visibility, softphones, agent access and peak simultaneous calls during discovery. Configure the route when a destination is busy or unavailable."),
    ("How the pieces connect", "In a common deployment pattern, a local business number reaches an Asterisk-based PBX through a supported SIP trunk. A real-time speech service, such as the OpenAI Realtime API, can provide the conversational layer where configured. The PBX routes calls to an IVR, an AI voice workflow or a human extension. A conversational voice service handles speech in real time. Work with SRLINES to confirm the deployment architecture, tenant boundaries, access and what call activity is passed to wCRM."),
    ("Pakistani UAN, SIP and carrier terms", "Discuss whether your existing business UAN or a new number can be connected. Number availability, inbound and outbound routes, concurrent sessions and charges depend on carrier terms and the selected package. Confirm compatibility before porting or publishing a number."),
    ("Deployment and onboarding", "Map call intent, hours, escalation, consent and staff ownership first. Then test SIP connectivity, a small set of AI scenarios, fallbacks, peak load and the wCRM handoff before routing live traffic. Agree a rollback route for launch."),
    ("Recording, consent and data handling", "Agree which calls are recorded, how callers are informed, who can access call data, how long it is kept and when staff should take over. Use authorized outbound lists and a documented opt-out process. Review privacy and applicable requirements before going live."),
    ("Plans and custom quotations", "Compare published 30-day inbound AI plans and one-time setup on the pricing page. Request a quote for outbound usage, integrations or custom workflows. The signed quote defines the commercial terms."),
]

PBX_FAQS = [
    ("What is an AI Calling Agent?", "An AI calling agent is a voice assistant that responds to spoken requests using business instructions and can route an enquiry to staff under agreed rules."),
    ("What is an AI-enabled PBX?", "It is a business phone system that connects extensions, routing and other PBX functions with conversational AI voice workflows."),
    ("How does conversational AI differ from IVR?", "Conversational AI uses spoken requests. Traditional IVR routes callers using prerecorded prompts and a fixed menu, often through keypad input."),
    ("Can the AI answer Pakistani telephone calls?", "Pakistani inbound calls can be considered where the chosen carrier and number provide a supported SIP route to the PBX."),
    ("Can it make outbound calls?", "Yes. SRLINES supports outbound AI calls. Availability for your number depends on the carrier, caller ID setup, applicable permissions and calling purpose."),
    ("Does it support Urdu?", "Yes. SRLINES supports Urdu and English. Use your business phrases, accents and product names to test call quality before launch."),
    ("Can it transfer callers to human staff?", "Yes. SRLINES supports transfer to human staff. Choose the destination and test overflow and callbacks before launch."),
    ("Can it connect with a business UAN?", "SRLINES reviews UAN connectivity with your carrier. Feasibility and migration depend on number and package terms."),
    ("Can it work with WhatsApp CRM?", "Yes. SRLINES AI Calling Agent and PBX integrates with wCRM. Confirm which call records, contact matches and follow-up steps are part of your deployment."),
    ("Can it record calls?", "SRLINES PBX supports call recording. Agree when recordings are enabled, how callers are informed and who can access them."),
    ("How are concurrent calls managed?", "The carrier and platform capacity determine how many calls can run at once. Test overflow and how transfers count before going live."),
    ("How is AI calling usage charged?", "Ask for a quote separating AI billing units and overage from SIP or outbound rates, subscriptions, setup and taxes."),
    ("Can businesses customize the AI instructions?", "Define approved business information, destinations and escalation rules during discovery and test them with realistic calls."),
    ("Can restaurants, hospitals and schools use the platform?", "These organizations can scope administrative call workflows such as enquiries and routing, with staff handling exceptions and sensitive decisions."),
    ("How do I request a demonstration?", "Watch the product walkthrough on this page and use the consultation form to arrange a demo for your workflow."),
]
