import tkinter as tk
from tkinter import scrolledtext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# FAQ DATA
# =========================

faqs = {
    "What is the admission deadline?":
        "The admission deadline is 30th September every year.",

    "How can I apply for admission?":
        "You can apply online through the university admission portal.",

    "What programs are offered?":
        "We offer BS, MS and PhD programs in multiple disciplines.",

    "Is hostel available?":
        "Yes, separate hostels are available for boys and girls.",

    "What is the fee structure?":
        "Fee structure varies according to the program.",

    
    "When does semester start?":
        "The semester starts in February and September every year.",

    "Is scholarship available?":
        "Yes, merit-based and need-based scholarships are available.",

    "What are the eligibility criteria?":
        "Generally, 12 years of education is required for BS programs.",

    "How do I check merit list?":
        "Merit lists are uploaded on the university website.",

    "What documents are required for admission?":
        "CNIC/B-Form, academic transcripts, photos and application form.",

    "Can international students apply?":
        "Yes, international students can apply.",

    "Is transport facility available?":
        "Yes, university provides transport on selected routes.",

    "How can I pay fees?":
        "Fees can be paid via bank challan or online banking.",

    "What is minimum CGPA requirement?":
        "Minimum CGPA of 2.0 is required.",

    "How many semesters are in BS program?":
        "BS program has 8 semesters.",

    "Are internships offered?":
        "Yes, internships are arranged with industry partners.",

    "Does university have library?":
        "Yes, fully equipped digital library is available.",

    "Can I change my program after admission?":
        "Yes, subject to rules and availability.",

    "How do I access student portal?":
        "Login using your student ID and password.",

    "Is Wi-Fi available on campus?":
        "Yes, free Wi-Fi is available for students.",

    "What extracurricular activities are available?":
        "Sports, societies, cultural events and seminars are offered.",

    "How do I apply for scholarship?":
        "Apply through Financial Aid Office or online portal.",

    "What are university timings?":
        "University is open from 8 AM to 5 PM on weekdays.",

    "Is cafeteria available?":
        "Yes, cafeteria is available on campus.",

    "How do I get student ID card?":
        "ID card is issued after enrollment.",

    "What is admission eligibility for BS CS?":
        "FSc Pre-Engineering or equivalent is required.",

    "Is entry test mandatory?":
        "Yes, entry test is required for most programs.",

    "What is test syllabus?":
        "It includes English, Math and General Knowledge.",

    "When are entry tests held?":
        "Entry tests are held in July and August.",

    "How can I prepare for entry test?":
        "Practice past papers and MCQs.",

    "What is class attendance policy?":
        "Minimum 75% attendance is required.",

    "Can I freeze semester?":
        "Yes, under special circumstances approval is required.",

    "What is grading system?":
        "University uses CGPA system from 0.0 to 4.0.",

    "When are exams conducted?":
        "Midterms and finals are held each semester.",

    "How is result calculated?":
        "Based on assignments, quizzes, midterms and finals.",

    "Can I reappear in exams?":
        "Yes, supplementary exams are allowed.",

    "Is hostel safe for girls?":
        "Yes, separate secure girls hostel is available.",

    "What sports facilities are available?":
        "Cricket, football, gym and indoor games are available.",

    "Is medical facility available?":
        "Yes, basic medical center is available on campus.",

    "How do I contact teachers?":
        "Through email or student portal messaging system.",

    "Can I do part-time job?":
        "Yes, with university permission.",

    "What is semester duration?":
        "Each semester is about 16–18 weeks.",

    "Is there dress code?":
        "Yes, decent dress code is required.",


    "How do I get transcript?":
        "Apply through examination office.",

    "Can I transfer from another university?":
        "Yes, transfer cases are considered.",

    "Is parking available?":
        "Yes, parking facility is available for students.",

    "What is convocation process?":
        "Graduates register for convocation ceremony online."
}
questions = list(faqs.keys())

# =========================
# NLP SETUP
# =========================

vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 3))
faq_vectors = vectorizer.fit_transform(questions)

def get_answer(query):
    query_vector = vectorizer.transform([query])
    similarity = cosine_similarity(query_vector, faq_vectors)

    best_index = similarity.argmax()
    score = similarity[0][best_index]

    if score < 0.15:
        return "Sorry, I couldn't understand your question. Please select a question from the FAQ list."

    return faqs[questions[best_index]]

# =========================
# UI FUNCTIONS
# =========================

def insert_message(sender, message, tag):
    chat_box.insert(tk.END, f"{sender}\n", tag)
    chat_box.insert(tk.END, f"{message}\n\n")
    chat_box.see(tk.END)

def bot_reply(user_msg):
    answer = get_answer(user_msg)
    insert_message("🤖 University Bot", answer, "bot")
    status_var.set("Ready")

def send_message(event=None):
    user_msg = entry.get().strip()

    if not user_msg:
        return

    insert_message("👨 You", user_msg, "user")

    entry.delete(0, tk.END)

    status_var.set("Bot is typing...")

    root.after(500, lambda: bot_reply(user_msg))

def clear_chat():
    chat_box.delete(1.0, tk.END)
    insert_message(
        "🎓 University FAQ Bot",
        "Welcome to University FAQ! Ask me anything about admissions, scholarships, hostel, fees, or programs.",
        "welcome"
    )

def faq_selected(event):
    if faq_listbox.curselection():
        selected = faq_listbox.get(faq_listbox.curselection()[0])
        entry.delete(0, tk.END)
        entry.insert(0, selected)

# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("🎓 Welcome to University FAQ")
root.geometry("1100x700")
root.configure(bg="#0f172a")

# =========================
# HEADER
# =========================

header = tk.Label(
    root,
    text="🎓 Welcome to University FAQ",
    font=("Segoe UI", 22, "bold"),
    bg="#2563eb",
    fg="white",
    pady=15
)
header.pack(fill="x")

# =========================
# MAIN FRAME
# =========================

main_frame = tk.Frame(root, bg="#0f172a")
main_frame.pack(fill="both", expand=True)

# =========================
# SIDEBAR
# =========================

sidebar = tk.Frame(
    main_frame,
    width=350,
    bg="#1e293b"
)
sidebar.pack(side="left", fill="y")

sidebar_title = tk.Label(
    sidebar,
    width=50,
    text="📚 FAQ Questions",
    font=("Segoe UI", 12, "bold"),
    bg="#1e293b",
    fg="white"
)
sidebar_title.pack(pady=10)

faq_listbox = tk.Listbox(
    sidebar,
    bg="#334155",
    fg="white",
    font=("Segoe UI", 11),
    selectbackground="#3b82f6",
    selectforeground="white",
    bd=0
)

faq_listbox.pack(fill="both", expand=True, padx=10, pady=10)

for q in questions:
    faq_listbox.insert(tk.END, q)

faq_listbox.bind("<<ListboxSelect>>", faq_selected)

# =========================
# CHAT AREA
# =========================

chat_frame = tk.Frame(main_frame, bg="#0f172a")
chat_frame.pack(side="right", fill="both", expand=True)

chat_box = scrolledtext.ScrolledText(
    chat_frame,
    wrap=tk.WORD,
    font=("Segoe UI", 11),
    bg="#f8fafc",
    fg="black",
    padx=15,
    pady=15
)

chat_box.pack(fill="both", expand=True, padx=10, pady=10)

# Message Styles
chat_box.tag_config(
    "user",
    foreground="#2563eb",
    font=("Segoe UI", 11, "bold")
)

chat_box.tag_config(
    "bot",
    foreground="#16a34a",
    font=("Segoe UI", 11, "bold")
)

chat_box.tag_config(
    "welcome",
    foreground="#f97316",
    font=("Segoe UI", 12, "bold")
)

# Welcome Message
insert_message(
    "🎓 University FAQ Bot",
    "Welcome to University FAQ! Ask me anything about admissions, scholarships, hostel, fees, or programs.",
    "welcome"
)

# =========================
# INPUT AREA
# =========================

input_frame = tk.Frame(chat_frame, bg="#0f172a")
input_frame.pack(fill="x", pady=10)

entry = tk.Entry(
    input_frame,
    font=("Segoe UI", 12),
    bd=2,
    relief="groove"
)

entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=10,
    ipady=8
)

send_btn = tk.Button(
    input_frame,
    text="📤 Send",
    bg="#2563eb",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=send_message,
    cursor="hand2"
)
send_btn.pack(side="left", padx=5)

clear_btn = tk.Button(
    input_frame,
    text="🗑 Clear",
    bg="#f59e0b",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=clear_chat,
    cursor="hand2"
)
clear_btn.pack(side="left", padx=5)

exit_btn = tk.Button(
    input_frame,
    text="❌ Exit",
    bg="#dc2626",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=root.destroy,
    cursor="hand2"
)
exit_btn.pack(side="left", padx=5)

# =========================
# STATUS BAR
# =========================

status_var = tk.StringVar()
status_var.set("Ready")

status_bar = tk.Label(
    root,
    textvariable=status_var,
    bg="#1e293b",
    fg="white",
    anchor="w",
    padx=10
)
status_bar.pack(fill="x")

# Enter Key Support
entry.bind("<Return>", send_message)

# =========================
# RUN APP
# =========================

root.mainloop()