from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import pandas as pd
from urllib.parse import unquote


app = Flask(__name__)

app.secret_key = "smartcourse123"


# =========================================================
# LOAD COURSES
# =========================================================

def load_courses():

    return pd.read_csv("dataset/courses.csv")


# =========================================================
# CAREER → INTEREST
# =========================================================

def get_career_interest(career):

    career_map = {

        "Data Scientist": "Data Science",

        "Web Developer": "Web Development",

        "Business Analyst": "Data Science",

        "Software Developer": "Software Development",

        "Artificial Intelligence Engineer":
            "Artificial Intelligence",

        "Cyber Security Analyst":
            "Cyber Security",

        "Cloud Engineer":
            "Cloud Computing"

    }

    return career_map.get(career)


# =========================================================
# FIND ONE COURSE
# =========================================================

def get_course_by_name(course_name):

    data = load_courses()

    course_name = unquote(
        course_name
    ).strip()

    result = data[
        data["Course"]
        .astype(str)
        .str.strip()
        .str.lower()
        ==
        course_name.lower()
    ]

    if result.empty:

        return None

    return result.iloc[0].to_dict()


# =========================================================
# COURSE LESSONS
# =========================================================

def get_course_lessons(course_name):

    lesson_map = {

        # -------------------------------------------------
        # DATA SCIENCE
        # -------------------------------------------------

        "Python for Data Science": [

            "Python Basics",
            "Variables and Data Types",
            "Functions and Modules",
            "NumPy Basics",
            "Pandas DataFrames",
            "Data Cleaning",
            "Data Analysis with Python",
            "Python Data Science Project"

        ],

        "Data Analytics": [

            "Introduction to Data Analytics",
            "Excel for Data Analysis",
            "Python for Data Analysis",
            "SQL for Data Analysis",
            "Data Cleaning",
            "Exploratory Data Analysis",
            "Business Data Analysis",
            "Data Analytics Project"

        ],

        "Data Visualization": [

            "Introduction to Data Visualization",
            "Matplotlib Basics",
            "Charts and Graphs",
            "Power BI Basics",
            "Tableau Basics",
            "Dashboard Design",
            "Interactive Dashboards",
            "Data Visualization Project"

        ],

        "Statistics for Data Science": [

            "Introduction to Statistics",
            "Descriptive Statistics",
            "Probability Basics",
            "Probability Distributions",
            "Mean Median and Mode",
            "Correlation and Regression",
            "Hypothesis Testing",
            "Statistics Project"

        ],

        "SQL for Data Science": [

            "SQL Basics",
            "Database and Tables",
            "SELECT Queries",
            "Filtering and Sorting",
            "Aggregate Functions",
            "Joins",
            "Subqueries",
            "SQL Data Analysis Project"

        ],

        "Big Data Analytics": [

            "Introduction to Big Data",
            "Hadoop Basics",
            "HDFS",
            "MapReduce",
            "Apache Hive",
            "Apache Pig",
            "Apache Spark",
            "Big Data Analytics Project"

        ],

        "Power BI": [

            "Introduction to Power BI",
            "Importing Data",
            "Data Cleaning",
            "Power Query",
            "Data Modeling",
            "DAX Basics",
            "Creating Dashboards",
            "Power BI Project"

        ],

        "Tableau": [

            "Introduction to Tableau",
            "Connecting Data",
            "Tableau Worksheets",
            "Charts and Graphs",
            "Filters and Parameters",
            "Dashboards",
            "Interactive Visualizations",
            "Tableau Project"

        ],


        # -------------------------------------------------
        # ARTIFICIAL INTELLIGENCE
        # -------------------------------------------------

        "Artificial Intelligence Fundamentals": [

            "Introduction to Artificial Intelligence",
            "AI Problem Solving",
            "Search Algorithms",
            "Knowledge Representation",
            "Machine Learning Basics",
            "Neural Networks Introduction",
            "AI Applications",
            "AI Project"

        ],

        "Machine Learning": [

            "Introduction to Machine Learning",
            "Python for Machine Learning",
            "Data Preprocessing",
            "Regression",
            "Classification",
            "Clustering",
            "Model Evaluation",
            "Machine Learning Project"

        ],

        "Deep Learning": [

            "Introduction to Deep Learning",
            "Neural Networks",
            "Activation Functions",
            "Backpropagation",
            "TensorFlow Basics",
            "Keras Basics",
            "Convolutional Neural Networks",
            "Deep Learning Project"

        ],

        "Natural Language Processing": [

            "Introduction to NLP",
            "Text Processing",
            "Tokenization",
            "Stop Words",
            "Stemming and Lemmatization",
            "Text Classification",
            "Chatbots",
            "NLP Project"

        ],

        "Computer Vision": [

            "Introduction to Computer Vision",
            "Image Processing",
            "OpenCV Basics",
            "Image Classification",
            "Object Detection",
            "Feature Detection",
            "Computer Vision Models",
            "Computer Vision Project"

        ],

        "Generative AI": [

            "Introduction to Generative AI",
            "Large Language Models",
            "Generative AI Applications",
            "ChatGPT Basics",
            "AI Content Generation",
            "AI Tools",
            "Responsible AI",
            "Generative AI Project"

        ],

        "Prompt Engineering": [

            "Introduction to Prompt Engineering",
            "Prompt Basics",
            "Prompt Structure",
            "Zero Shot Prompting",
            "Few Shot Prompting",
            "Role Based Prompts",
            "Advanced Prompting",
            "Prompt Engineering Project"

        ],

        "AI Projects": [

            "AI Project Planning",
            "Data Collection",
            "Data Preparation",
            "Model Development",
            "Model Testing",
            "Model Improvement",
            "AI Application Development",
            "Final AI Project"

        ],


        # -------------------------------------------------
        # CYBER SECURITY
        # -------------------------------------------------

        "Ethical Hacking": [

            "Cyber Security Fundamentals",
            "Networking Basics",
            "Linux Basics",
            "Kali Linux",
            "Reconnaissance",
            "Vulnerability Assessment",
            "Penetration Testing",
            "Ethical Hacking Project"

        ],

        "Network Security": [

            "Networking Fundamentals",
            "Network Threats",
            "Firewalls",
            "Network Monitoring",
            "Intrusion Detection",
            "Secure Network Design",
            "Network Security Tools",
            "Network Security Project"

        ],

        "Kali Linux": [

            "Introduction to Kali Linux",
            "Kali Linux Installation",
            "Linux Commands",
            "Network Tools",
            "Security Testing Tools",
            "Scanning Tools",
            "Password Security",
            "Kali Linux Security Project"

        ],

        "Cryptography": [

            "Introduction to Cryptography",
            "Encryption Basics",
            "Symmetric Encryption",
            "Asymmetric Encryption",
            "Hash Functions",
            "Digital Signatures",
            "Cryptographic Protocols",
            "Cryptography Project"

        ],

        "Penetration Testing": [

            "Introduction to Penetration Testing",
            "Reconnaissance",
            "Scanning",
            "Vulnerability Analysis",
            "Exploitation",
            "Post Exploitation",
            "Reporting",
            "Penetration Testing Project"

        ],


        # -------------------------------------------------
        # CLOUD
        # -------------------------------------------------

        "AWS Cloud Computing": [

            "Introduction to Cloud Computing",
            "AWS Fundamentals",
            "AWS EC2",
            "AWS S3",
            "AWS IAM",
            "AWS RDS",
            "AWS Networking",
            "AWS Cloud Project"

        ],

        "Microsoft Azure": [

            "Introduction to Microsoft Azure",
            "Azure Fundamentals",
            "Azure Virtual Machines",
            "Azure Storage",
            "Azure Networking",
            "Azure Databases",
            "Azure Security",
            "Azure Project"

        ],

        "Google Cloud Platform": [

            "Introduction to Google Cloud",
            "Google Cloud Fundamentals",
            "Compute Engine",
            "Cloud Storage",
            "Cloud SQL",
            "Cloud Networking",
            "Cloud Security",
            "Google Cloud Project"

        ],

        "Docker & Kubernetes": [

            "Introduction to Containers",
            "Docker Basics",
            "Docker Images",
            "Docker Containers",
            "Docker Compose",
            "Kubernetes Basics",
            "Kubernetes Deployments",
            "Container Project"

        ],

        "DevOps Fundamentals": [

            "Introduction to DevOps",
            "Git and GitHub",
            "CI/CD",
            "Jenkins",
            "Docker",
            "Testing Automation",
            "Deployment",
            "DevOps Project"

        ],


        # -------------------------------------------------
        # SOFTWARE DEVELOPMENT
        # -------------------------------------------------

        "Python Programming": [

            "Python Basics",
            "Variables and Data Types",
            "Operators",
            "Conditional Statements",
            "Loops",
            "Functions",
            "Lists and Dictionaries",
            "Python Project"

        ],

        "Java Programming": [

            "Java Basics",
            "Variables and Data Types",
            "Operators",
            "Control Statements",
            "Classes and Objects",
            "Inheritance",
            "Polymorphism",
            "Java Project"

        ],

        "C Programming": [

            "C Programming Basics",
            "Variables and Data Types",
            "Operators",
            "Conditional Statements",
            "Loops",
            "Functions",
            "Arrays and Pointers",
            "C Programming Project"

        ],

        "Data Structures": [

            "Introduction to Data Structures",
            "Arrays",
            "Linked Lists",
            "Stacks",
            "Queues",
            "Trees",
            "Graphs",
            "Data Structures Project"

        ],

        "Software Engineering": [

            "Introduction to Software Engineering",
            "Software Development Life Cycle",
            "Requirements Analysis",
            "Software Design",
            "Software Testing",
            "Agile Development",
            "Project Management",
            "Software Engineering Project"

        ],

        "Git & GitHub": [

            "Introduction to Git",
            "Git Installation",
            "Git Commands",
            "Repositories",
            "Branches",
            "Merging",
            "GitHub Collaboration",
            "GitHub Project"

        ],

        "Object Oriented Programming": [

            "OOP Fundamentals",
            "Classes and Objects",
            "Constructors",
            "Inheritance",
            "Polymorphism",
            "Encapsulation",
            "Abstraction",
            "OOP Project"

        ],

        "Database Management Systems": [

            "Introduction to Databases",
            "Relational Databases",
            "Tables and Records",
            "SQL Basics",
            "Keys and Constraints",
            "Normalization",
            "Joins",
            "Database Project"

        ],


        # -------------------------------------------------
        # WEB DEVELOPMENT
        # -------------------------------------------------

        "Full Stack Web Development": [

            "HTML Basics",
            "CSS Basics",
            "JavaScript Basics",
            "Bootstrap",
            "React JS",
            "Node.js",
            "MongoDB",
            "Full Stack Web Project"

        ],

        "Frontend Development": [

            "HTML",
            "CSS",
            "Responsive Design",
            "Bootstrap",
            "JavaScript",
            "DOM Manipulation",
            "React JS",
            "Frontend Project"

        ],

        "Backend Development": [

            "Backend Fundamentals",
            "Python",
            "Flask",
            "Django",
            "Node.js",
            "REST APIs",
            "SQL",
            "Backend Project"

        ],

        "React JS": [

            "React Introduction",
            "Components",
            "JSX",
            "Props",
            "State",
            "Hooks",
            "React Router",
            "React Project"

        ],

        "Angular Development": [

            "Angular Introduction",
            "TypeScript Basics",
            "Angular Components",
            "Templates",
            "Services",
            "Routing",
            "Forms",
            "Angular Project"

        ],

        "PHP & MySQL": [

            "PHP Basics",
            "Variables",
            "Functions",
            "Forms",
            "PHP and MySQL",
            "Database Queries",
            "Sessions",
            "PHP Project"

        ],

        "Django Web Development": [

            "Django Introduction",
            "Project Setup",
            "URLs and Views",
            "Templates",
            "Models",
            "Forms",
            "Authentication",
            "Django Project"

        ],

        "Node.js Development": [

            "Node.js Introduction",
            "Node.js Installation",
            "Modules",
            "NPM",
            "Express.js",
            "REST APIs",
            "Database Connection",
            "Node.js Project"

        ]

    }


    return lesson_map.get(

        course_name,

        [
            "Introduction",
            "Fundamentals",
            "Core Concepts",
            "Practical Skills",
            "Advanced Concepts",
            "Practice",
            "Project",
            "Final Assessment"
        ]

    )


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]

        email = request.form["email"]

        password = request.form["password"]


        try:

            with sqlite3.connect(
                "users.db",
                timeout=10
            ) as conn:

                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO users
                    (fullname, email, password)
                    VALUES (?, ?, ?)
                    """,
                    (
                        fullname,
                        email,
                        password
                    )
                )

                conn.commit()


            return redirect("/login")


        except sqlite3.IntegrityError:

            return "Email already exists!"


        except sqlite3.OperationalError as e:

            return f"Database Error: {e}"


    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]


        conn = sqlite3.connect(
            "users.db"
        )

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT fullname
            FROM users
            WHERE email=? AND password=?
            """,
            (
                email,
                password
            )
        )


        user = cursor.fetchone()

        conn.close()


        if user:

            session["user"] = user

            return redirect(
                "/dashboard"
            )


        return "Invalid Email or Password"


    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect("/login")


    return render_template(
        "dashboard.html",
        name=session["user"][0]
    )


# =========================================================
# ALL COURSES
# =========================================================

@app.route("/recommendation")
def all_courses():

    if "user" not in session:

        return redirect("/login")


    data = load_courses()

    courses = data.to_dict(
        "records"
    )


    return render_template(
        "recommendation.html",
        courses=courses,
        career="All Courses"
    )


# =========================================================
# CAREER RECOMMENDATION
# =========================================================

@app.route(
    "/recommendation/<career>"
)
def recommendation(career):

    if "user" not in session:

        return redirect("/login")


    data = load_courses()

    interest = get_career_interest(
        career
    )


    if interest:

        result = data[

            data["Interest"]
            .astype(str)
            .str.strip()
            .str.lower()
            ==
            interest.strip().lower()

        ]

        courses = result.to_dict(
            "records"
        )


    else:

        courses = []


    session["career"] = career


    return render_template(
        "recommendation.html",
        courses=courses,
        career=career
    )


# =========================================================
# AI ASSESSMENT
# =========================================================

@app.route("/ai_assessment")
def ai_assessment():

    if "user" not in session:

        return redirect("/login")


    return render_template(
        "ai_assessment.html"
    )


# =========================================================
# AI RESULT
# =========================================================

@app.route(
    "/ai_result",
    methods=["POST"]
)
def ai_result():

    programming = int(
        request.form["programming"]
    )

    maths = int(
        request.form["maths"]
    )

    problem = int(
        request.form["problem"]
    )

    communication = int(
        request.form["communication"]
    )

    creativity = int(
        request.form["creativity"]
    )


    if programming >= 85 and maths >= 85:

        career = "Data Scientist"

        match = 95


    elif programming >= 85 and creativity >= 80:

        career = "Web Developer"

        match = 92


    elif programming >= 80 and problem >= 85:

        career = "Artificial Intelligence Engineer"

        match = 94


    elif problem >= 85 and programming >= 75:

        career = "Cyber Security Analyst"

        match = 90


    elif communication >= 85:

        career = "Business Analyst"

        match = 89


    elif creativity >= 85:

        career = "Cloud Engineer"

        match = 88


    else:

        career = "Software Developer"

        match = 80


    session["career"] = career

    session["match"] = match

    session["course_progress"] = {}


    return render_template(

        "ai_result.html",

        programming=programming,

        maths=maths,

        problem=problem,

        communication=communication,

        creativity=creativity,

        career=career,

        match=match

    )


# =========================================================
# SINGLE COURSE LEARNING ROADMAP
# =========================================================

@app.route(
    "/learning_roadmap/<path:course_name>"
)
def learning_roadmap(course_name):

    if "user" not in session:

        return redirect("/login")


    # Find ONLY the selected course

    course = get_course_by_name(
        course_name
    )


    if course is None:

        return "Course not found."


    # Get ONLY the lessons for this course

    lessons = get_course_lessons(
        course["Course"]
    )


    # Get progress

    course_progress = session.get(
        "course_progress",
        {}
    )


    completed = course_progress.get(

        course["Course"],

        []

    )


    return render_template(

        "learning_roadmap.html",

        course=course,

        lessons=lessons,

        completed=completed

    )


# =========================================================
# COURSE COMPLETION
# =========================================================

@app.route("/course_completed/<path:course_name>")
def course_completed(course_name):

    if "user" not in session:
        return redirect("/login")

    course = get_course_by_name(course_name)

    if course is None:
        return redirect("/recommendation")

    actual_course_name = course["Course"]
    lessons = get_course_lessons(actual_course_name)

    course_progress = session.get("course_progress", {})
    completed = course_progress.get(actual_course_name, [])

    if len(completed) < len(lessons):
        return redirect(url_for("learning_roadmap", course_name=actual_course_name))

    return render_template("course_completed.html", course=course)


# =========================================================
# COURSE LEARNING
# =========================================================

@app.route(
    "/course_learning/<path:course_name>"
)
def course_learning(course_name):

    if "user" not in session:

        return redirect("/login")


    course = get_course_by_name(
        course_name
    )


    if course is None:

        return "Course not found."


    lessons = get_course_lessons(
        course["Course"]
    )


    course_progress = session.get(
        "course_progress",
        {}
    )


    completed = course_progress.get(

        course["Course"],

        []

    )


    return render_template(

        "course_learning.html",

        course=course,

        lessons=lessons,

        completed=completed

    )


# =========================================================
# COMPLETE LESSON
# =========================================================

@app.route(
    "/complete_lesson/<path:course_name>/<int:lesson_index>",
    methods=["POST"]
)
def complete_lesson(
    course_name,
    lesson_index
):

    if "user" not in session:

        return redirect("/login")


    course = get_course_by_name(
        course_name
    )


    if course is None:

        return "Course not found."


    actual_course_name = course[
        "Course"
    ]


    lessons = get_course_lessons(
        actual_course_name
    )


    if (
        lesson_index < 0
        or
        lesson_index >= len(lessons)
    ):

        return redirect(
            url_for(
                "learning_roadmap",
                course_name=actual_course_name
            )
        )


    course_progress = session.get(
        "course_progress",
        {}
    )


    completed = course_progress.get(

        actual_course_name,

        []

    )


    if lesson_index not in completed:

        completed.append(
            lesson_index
        )


    completed = sorted(
        set(completed)
    )


    course_progress[
        actual_course_name
    ] = completed


    session["course_progress"] = (
        course_progress
    )

    session.modified = True


    completed_all = len(completed) >= len(lessons)

    return {
        "success": True,
        "completed_all": completed_all,
        "course_name": actual_course_name,
        "redirect_url": (
            url_for("course_completed", course_name=actual_course_name)
            if completed_all else ""
        )
    }


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )