from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate-career", methods=["POST"])
def generate_career():
    data = request.get_json()

    education = data.get("education", "")
    skills = data.get("skills", "")
    interests = data.get("interests", "")
    career_goal = data.get("career_goal", "")

    if not education or not skills or not interests or not career_goal:
        return jsonify({
            "success": False,
            "message": "Please fill all required fields."
        }), 400

    # Basic career guidance logic
    skills_lower = skills.lower()
    interests_lower = interests.lower()
    goal_lower = career_goal.lower()

    suggestions = []

    if any(word in skills_lower for word in ["python", "programming", "coding", "java"]):
        suggestions.append("Software Developer")

    if any(word in skills_lower for word in ["html", "css", "javascript", "web"]):
        suggestions.append("Web Developer")

    if any(word in skills_lower for word in ["sql", "database"]):
        suggestions.append("Database / Backend Developer")

    if any(word in skills_lower for word in ["machine learning", "ml", "ai", "artificial intelligence"]):
        suggestions.append("AI / Machine Learning Engineer")

    if "data" in skills_lower or "data" in interests_lower:
        suggestions.append("Data Analyst")

    if "design" in interests_lower or "creative" in interests_lower:
        suggestions.append("UI/UX Designer")

    if not suggestions:
        suggestions = [
            "Software Developer",
            "Data Analyst",
            "Digital Marketing Specialist"
        ]

    # Remove duplicate suggestions
    suggestions = list(dict.fromkeys(suggestions))

    roadmap = [
        "Build strong fundamentals related to your selected career.",
        "Complete practical projects and create a portfolio.",
        "Improve your resume and LinkedIn/GitHub profile.",
        "Practice interview and communication skills.",
        "Apply for internships and entry-level jobs."
    ]

    return jsonify({
        "success": True,
        "career_suggestions": suggestions,
        "skill_recommendations": [
            "Problem solving",
            "Communication",
            "Technical skills related to your target career",
            "Project development",
            "Interview preparation"
        ],
        "roadmap": roadmap,
        "message": f"Career guidance generated for your goal: {career_goal}"
    })


@app.route("/generate-resume", methods=["POST"])
def generate_resume():
    data = request.get_json()

    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    education = data.get("education", "")
    skills = data.get("skills", "")
    interests = data.get("interests", "")
    career_goal = data.get("career_goal", "")

    if not name or not email or not education or not skills:
        return jsonify({
            "success": False,
            "message": "Please fill the required resume details."
        }), 400

    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    story = []

    story.append(Paragraph(name, title_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        f"<b>Email:</b> {email}<br/>"
        f"<b>Phone:</b> {phone}",
        styles["Normal"]
    ))

    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Career Objective</b>", styles["Heading2"]))
    story.append(Paragraph(
        f"Seeking opportunities in {career_goal} where I can apply my skills, "
        f"learn new technologies and contribute to organizational growth.",
        styles["Normal"]
    ))

    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Education</b>", styles["Heading2"]))
    story.append(Paragraph(education, styles["Normal"]))

    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Skills</b>", styles["Heading2"]))
    story.append(Paragraph(skills, styles["Normal"]))

    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Interests</b>", styles["Heading2"]))
    story.append(Paragraph(interests, styles["Normal"]))

    doc.build(story)

    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="AI_Generated_Resume.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)