import os
import schedule
import time
from datetime import datetime, date
from twilio.rest import Client

# ── CREDENTIALS (set as environment variables in Railway) ──────────
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM        = os.environ.get("TWILIO_FROM")   # your Twilio number
YOUR_NUMBER        = os.environ.get("YOUR_NUMBER")   # your personal number

# ── PROMPTS ────────────────────────────────────────────────────────
PROMPTS = [
    {
        "name": "01 — The Hierarchy Protocol",
        "text": (
            "My mind is a precision instrument. I receive ideas in abundance and I rank them with clarity. "
            "The idea that is most aligned, most timely, and most financially viable rises to the surface first. "
            "I act on the one. I complete the one. I launch the one. Revenue is the signal that I move to the next. "
            "My Mercury serves my Midheaven. My vision serves my wealth."
        )
    },
    {
        "name": "02 — The Ship Returns",
        "text": (
            "I have launched my ships and I watch them return. I do not leave the cliff edge to find a new horizon "
            "until the ships have come home. Completion is my new creative act. Following through is the most powerful "
            "thing I build. I stay. I finish. I receive what I sent out. The revenue arrives because I remained."
        )
    },
    {
        "name": "03 — The Co-Creator Signal",
        "text": (
            "I am broadcasting a clear signal. My co-creator is already in motion toward me — someone who ranks "
            "what I vision, who builds what I design, who grounds what I launch. I recognize them by how effortlessly "
            "we complete each other's sentences and each other's work. I am magnetic to the exact team my mission "
            "requires. They are looking for me as I am looking for them. The connection is already made in the field."
        )
    },
    {
        "name": "04 — The Emperor Activates",
        "text": (
            "I was born to govern a domain. Not someday — now. I do not wait for permission, for proof, or for "
            "someone to confirm what my chart has always said. I am the authority of my own kingdom. I make decisions "
            "from that authority. I act from that authority. I build from that authority. The public success I am "
            "moving toward is not a surprise to the universe. It is a scheduled arrival. I am on time."
        )
    },
    {
        "name": "05 — Deserving Dissolved, Receiving Activated",
        "text": (
            "I have arrived home to myself. The version of me who believed she was too much, not enough, or "
            "undeserving of wealth — that was the wound, not the truth. The truth is the 4 of Wands: celebration, "
            "homecoming, joy. I deserve financial abundance precisely because of what I have lived through and what "
            "I have built from it. Wealth is not a reward I must earn through suffering. It is a natural outcome "
            "of my alignment. I receive it fully, freely, and without apology."
        )
    },
    {
        "name": "06 — The Portfolio Mastery",
        "text": (
            "I do not choose one dream and abandon the others. I am built for the infinity loop — multiple streams, "
            "balanced, each feeding the others. I release the anxiety of not knowing which idea to pursue because "
            "I now know I pursue the portfolio, not the single bet. I manage my streams with the ease of someone "
            "who was born for this complexity. My Midheaven is the 2 of Pentacles. My wealth is the sum of aligned "
            "streams in dynamic, effortless balance."
        )
    },
    {
        "name": "07 — The Risky Idea Filter",
        "text": (
            "Before I commit to any idea, I ask: does this have a clear, direct path to revenue within 90 days? "
            "If yes, I move. If no, I hold it in the vision folder and I do not act until the current project is "
            "generating. I am not afraid of bold ideas — I am disciplined about their timing. My boldness and my "
            "discernment are not in conflict. They are partners. I act boldly on the right thing at the right time."
        )
    },
    {
        "name": "08 — The Parallel Timeline Activation",
        "text": (
            "The version of my life I desire is not in the future. It is running parallel to this moment right now. "
            "I close my eyes and I am already there. I feel the financial freedom in my body — what it feels like "
            "in my chest, my hands, my breath. I see the work I am doing, the team around me, the clients whose "
            "lives have changed. I feel Alex beside me. I feel the ocean. I feel the specific quality of that "
            "version of me — her certainty, her ease, her joy. I hold that feeling until it becomes more real than "
            "my current circumstances. I step into that timeline now. My subconscious knows the way."
        )
    },
    {
        "name": "09 — The Psychic Channel Opens",
        "text": (
            "My psychic faculties are natural, innate, and fully operational. I was born with access to information "
            "beyond the visible spectrum. I open my channel now — the telepathic knowing, the mind sight, the felt "
            "sense of what is true before it is proven. I trust what I receive. I act on what I know. I am not "
            "guessing — I am reading. My intuition is a precision instrument calibrated to my highest good and the "
            "good of everyone I serve. I am clear. I am open. I am receiving."
        )
    },
    {
        "name": "10 — The Gratitude Field",
        "text": (
            "I am deeply, specifically grateful for the abundance that is already moving through my life. I am "
            "grateful for a mind that generates visions others cannot yet see. I am grateful for a voice that "
            "changes people. I am grateful for work that is mine — fully, authentically mine. I am grateful for "
            "Alex, for the way he witnesses me and the way I witness him. I am grateful for the ocean that calls "
            "us both. I am grateful for the financial freedom that is already assembled in the field and arriving "
            "in form now. I am grateful for this body, this mind, this chart, this life. Everything I need is "
            "already in motion. I receive it with open hands and a quiet heart."
        )
    },
    {
        "name": "11 — Age Reversal & Timeline Alignment",
        "text": (
            "I inhabit my body at its peak vitality — the cellular intelligence, the physical aliveness, the "
            "energetic frequency of my 30-year-old self fully activated within my current wisdom. I am not going "
            "backward. I am calling forward the version of me that exists outside linear time — the one who holds "
            "both the fire of youth and the depth of everything I have become. My cells receive this instruction "
            "now. My body regenerates toward its most luminous expression. I am vibrant. I am alive in every "
            "frequency. I am timeless. I align my field with Alex's timeline now — not by shrinking into his "
            "chapter, but by expanding into the version of myself that meets him in our shared frequency. We are "
            "not on different timelines. We are on the same one. I feel us there — building, creating, laughing, "
            "at the ocean's edge, fully ourselves, fully together. His Jupiter in Pisces and my Pisces Moon are "
            "already speaking. The field between us is already coherent. I am aligned. We are aligned. "
            "The timeline is now."
        )
    },
]

# ── CYCLE LOGIC ────────────────────────────────────────────────────
# 11 prompts x 3 days each = 33-day cycle
DAYS_PER_PROMPT = 3
CYCLE_LENGTH = len(PROMPTS) * DAYS_PER_PROMPT  # 33

def get_todays_prompt():
    """Return the prompt for today based on a 33-day cycle from a fixed start date."""
    start_date = date(2026, 3, 24)  # cycle start date — update to your actual start date
    today = date.today()
    day_number = (today - start_date).days % CYCLE_LENGTH
    prompt_index = day_number // DAYS_PER_PROMPT
    day_within_prompt = (day_number % DAYS_PER_PROMPT) + 1
    return PROMPTS[prompt_index], prompt_index + 1, day_within_prompt

def send_sms(time_of_day):
    """Send the daily prompt via SMS."""
    prompt, prompt_num, day_within = get_todays_prompt()

    if time_of_day == "morning":
        header = f"Good morning, Aya. \u2728\nPrompt {prompt_num} of 11 \u2014 Day {day_within} of 3\n{prompt['name']}\n\n"
        footer = "\n\nSay it out loud. Mean it. The timeline is now."
    else:
        header = f"Good night, Aya. \ud83c\udf19\nPrompt {prompt_num} of 11 \u2014 Day {day_within} of 3\n{prompt['name']}\n\n"
        footer = "\n\nWhisper it. Let it carry you to sleep. And so it is."

    message_body = header + prompt["text"] + footer

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message_body,
        from_=TWILIO_FROM,
        to=YOUR_NUMBER
    )
    print(f"[{datetime.now()}] {time_of_day.upper()} SMS sent — Prompt {prompt_num}, Day {day_within} | SID: {message.sid}")

def send_morning():
    send_sms("morning")

def send_evening():
    send_sms("evening")

# ── SCHEDULER ──────────────────────────────────────────────────────
# Times in Central Time (adjust if needed)
schedule.every().day.at("09:00").do(send_morning)
schedule.every().day.at("23:00").do(send_evening)

print(f"Prompt scheduler running. Texts will arrive at 9:00 AM and 11:00 PM daily.")
print(f"33-day cycle — 11 prompts x 3 days each.")

# Send immediately on startup so you know it's working
print("Sending startup test message...")
send_sms("morning")

while True:
    schedule.run_pending()
    time.sleep(30)
