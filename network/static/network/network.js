document.addEventListener("DOMContentLoaded", function () {
	const modal = document.getElementById("myModal");
	const openBtn = document.getElementById("openModalBtn");
	const closeBtn = document.querySelector(".close");
	const modalBody = document.getElementById("modal-body-content");

	if (openBtn) {
		openBtn.onclick = async function () {
			const url = openBtn.getAttribute("data-url");
			try {
				const response = await fetch(url);
				const htmlContent = await response.text();
				modalBody.innerHTML = htmlContent;
				modal.style.display = "block";

				// Attach form submission handler after modal content loads
				attachFormHandler();
			} catch (error) {
				console.error("Error fetching modal content:", error);
			}
		};
	}

	// Close modal when close button is clicked
	if (closeBtn) {
		closeBtn.onclick = function () {
			modal.style.display = "none";
		};
	}

	// Close modal when clicking outside of it
	window.onclick = function (event) {
		if (event.target == modal) {
			modal.style.display = "none";
		}
	};

	function attachFormHandler() {
		const form = document.querySelector("#modal-body-content form");
		if (!form) return;

		form.onsubmit = async function (e) {
			e.preventDefault();

			const formData = new FormData(form);

			try {
				const response = await fetch(form.action, {
					method: "POST",
					body: formData,
					headers: {
						"X-CSRFToken": formData.get("csrfmiddlewaretoken"),
					},
				});

				const data = await response.json();

				if (data.success) {
					// Close modal and reload page
					modal.style.display = "none";
					window.location.reload();
				} else {
					// Display error message in modal
					showError(data.error);
				}
			} catch (error) {
				console.error("Error submitting form:", error);
				showError("An error occurred. Please try again.");
			}
		};
	}

	function showError(message) {
		// Remove existing error if present
		const existingError = modalBody.querySelector(".alert-danger");
		if (existingError) {
			existingError.remove();
		}

		// Create and insert error message
		const errorDiv = document.createElement("div");
		errorDiv.className = "alert alert-danger";
		errorDiv.textContent = message;

		const form = modalBody.querySelector("form");
		form.insertBefore(errorDiv, form.firstChild);
	}
});
