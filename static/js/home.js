document.getElementById('department').addEventListener('change', function () {
    const selectedDept = this.value;
    const doctorOptions = document.querySelectorAll('#doctor option');

    doctorOptions.forEach(option => {
        const doctorDept = option.getAttribute('data-department');
        if (!doctorDept) {
            // Always show the default option "Select Doctor"
            option.style.display = '';
        } else if (doctorDept === selectedDept) {
            option.style.display = '';
        } else {
            option.style.display = 'none';
        }
    });
    // Reset doctor selection
    document.getElementById('doctor').value = '';


    document.getElementById("department").addEventListener("change", function () {
        var departmentId = this.value;
        var doctorSelect = document.getElementById("doctor");
        console.log("Selected department:", departmentId); // Should log a valid id

        // Clear current doctor options
        doctorSelect.innerHTML = '<option value="">Select Doctor</option>';

        if (departmentId) {
            // Make an AJAX GET request to fetch doctors
            fetch(`/get-doctors/?department_id=${departmentId}`)
                .then(response => response.json())
                .then(data => {
                    // Populate the doctor select with the returned data
                    data.forEach(function (doctor) {
                        var option = document.createElement("option");
                        option.value = doctor.id;
                        option.text = doctor.name;
                        doctorSelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Error fetching doctors:', error));
        }
    });
});