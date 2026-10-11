document.addEventListener("DOMContentLoaded", function () {

    // ==============================
    // Resume Form
    // ==============================

    const resumeForm = document.getElementById("resumeForm");

    resumeForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const phone = document.getElementById("phone").value.trim();
        const education = document.getElementById("education").value.trim();
        const skills = document.getElementById("skills").value.trim();
        const interests = document.getElementById("interests").value.trim();
        const careerGoal = document.getElementById("career_goal").value.trim();

        if (!name || !email || !education || !skills || !careerGoal) {
            alert("Please fill all required fields.");
            return;
        }

        try {
            const response = await fetch("/generate-resume", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    phone: phone,
                    education: education,
                    skills: skills,
                    interests: interests,
                    career_goal: careerGoal
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert(errorData.message || "Something went wrong.");
                return;
            }

            const blob = await response.blob();

            const url = window.URL.createObjectURL(blob);

            const link = document.createElement("a");
            link.href = url;
            link.download = "AI_Generated_Resume.pdf";

            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            window.URL.revokeObjectURL(url);

            alert("Resume generated successfully!");

        } catch (error) {
            console.error("Resume Error:", error);
            alert("Unable to generate resume. Please check the Flask server.");
        }
    });


    // ==============================
    // Career Guidance
    // ==============================

    const careerBtn = document.getElementById("careerBtn");

    careerBtn.addEventListener("click", async function () {

        const education = document.getElementById("education").value.trim();
        const skills = document.getElementById("skills").value.trim();
        const interests = document.getElementById("interests").value.trim();
        const careerGoal = document.getElementById("career_goal").value.trim();

        if (!education || !skills || !interests || !careerGoal) {
            alert("Please fill Education, Skills, Interests and Career Goal first.");
            return;
        }

        careerBtn.disabled = true;
        careerBtn.textContent = "Generating...";

        try {
            const response = await fetch("/generate-career", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    education: education,
                    skills: skills,
                    interests: interests,
                    career_goal: careerGoal
                })
            });

            const result = await response.json();

            if (!response.ok || !result.success) {
                alert(result.message || "Unable to generate career guidance.");
                return;
            }

            // ==============================
            // Career Suggestions
            // ==============================

            const careerSuggestions =document.getElementById("careerSuggestions");

            careerSuggestions.innerHTML = "";

            result.career_suggestions.forEach(function (career) {

                const li = document.createElement("li");
                li.textContent = career;

                careerSuggestions.appendChild(li);
            });


            // ==============================
            // Skill Recommendations
            // ==============================

            const skillRecommendations =
                document.getElementById("skillRecommendations");

            skillRecommendations.innerHTML = "";

            result.skill_recommendations.forEach(function (skill) {

                const li = document.createElement("li");
                li.textContent = skill;

                skillRecommendations.appendChild(li);
            });


            // ==============================
            // Career Roadmap
            // ==============================

            const careerRoadmap =
                document.getElementById("careerRoadmap");

            careerRoadmap.innerHTML = "";

            result.roadmap.forEach(function (step) {

                const li = document.createElement("li");
                li.textContent = step;

                careerRoadmap.appendChild(li);
            });


            // ==============================
            // Show Result
            // ==============================

            const careerResult =
                document.getElementById("careerResult");

            careerResult.classList.remove("hidden");

            careerResult.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        } catch (error) {

            console.error("Career Guidance Error:", error);

            alert(
                "Unable to connect with the server. " +
                "Please make sure Flask is running."
            );

        } finally {

            careerBtn.disabled = false;
            careerBtn.textContent = "Get Career Guidance";
        }
    });
});    
