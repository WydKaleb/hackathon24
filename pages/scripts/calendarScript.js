// Get the selected date input field and display elements
const selectedDate = document.getElementById("datePicked");
const slideshowLink = document.getElementById("slideshowLink").querySelector("span");
const homeworkForm = document.getElementById("homeworkForm").querySelector("span");

// Function to fetch and display assignment details
async function getAssignments() {
    if (!selectedDate.value) {
        alert("Please select a date.");
        return;
    }

    // Backend API URL
    const url = `http://127.0.0.1:8000/${selectedDate.value}`;

    try {
        // API call
        const response = await fetch(url);
        const data = await response.json();

        // Check for errors in the response
        if (data.error) {
            slideshowLink.textContent = "Error: " + data.error;
            homeworkForm.textContent = "";
        } else {
            // Update the assignment details in the DOM
            slideshowLink.innerHTML = data.slideshow_link
                ? `<a href="${data.slideshow_link}" target="_blank">View Slideshow</a>`
                : "No slideshow link available.";
            homeworkForm.innerHTML = data.homework_form_link
                ? `<a href="${data.homework_form_link}" target="_blank">View Homework Form</a>`
                : `<p> No homework form available.</p>`;
        }
    } catch (error) {
        console.error("Error fetching assignments:", error);
        slideshowLink.textContent = "Error fetching data.";
        homeworkForm.textContent = "";
    }
}
