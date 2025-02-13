// document.addEventListener("DOMContentLoaded", function() {
//     // Listen for department changes to load doctors
//     document.getElementById("department").addEventListener("change", function () {
//         var departmentId = this.value;
//         var doctorSelect = document.getElementById("doctor");
//         // Reset doctor, date, and time dropdowns
//         doctorSelect.innerHTML = '<option value="">Select Doctor</option>';
//         document.getElementById("appointment-date").innerHTML = '<option value="">Select Date</option>';
//         document.getElementById("appointment-time").innerHTML = '<option value="">Select Time</option>';
//
//         if (departmentId) {
//             fetch(`/get-doctors/?department_id=${departmentId}`)
//                 .then(response => response.json())
//                 .then(data => {
//                     data.forEach(function (doctor) {
//                         var option = document.createElement("option");
//                         option.value = doctor.id;
//                         option.text = doctor.name;
//                         doctorSelect.appendChild(option);
//                     });
//                 })
//                 .catch(error => console.error('Error fetching doctors:', error));
//         }
//     });
//
//     // Listen for doctor selection to fetch available dates
//     document.getElementById("doctor").addEventListener("change", function() {
//         var doctorId = this.value;
//         var appointmentDateSelect = document.getElementById("appointment-date");
//         // Reset the appointment date and time dropdowns
//         appointmentDateSelect.innerHTML = '<option value="">Select Date</option>';
//         document.getElementById("appointment-time").innerHTML = '<option value="">Select Time</option>';
//
//         if (doctorId) {
//             // Fetch available dates for the selected doctor
//             fetch(`/get-available-dates/?doctor_id=${doctorId}`)
//                 .then(response => response.json())
//                 .then(data => {
//                     // Expecting JSON response like: [{ "date": "2025-02-14", "display": "14-02-2025, Monday" }, ...]
//                     data.forEach(function(item) {
//                         var option = document.createElement("option");
//                         option.value = item.date;   // Raw date for backend queries
//                         option.text = item.display; // Formatted display
//                         appointmentDateSelect.appendChild(option);
//                     });
//                 })
//                 .catch(error => console.error('Error fetching available dates:', error));
//         }
//     });
//
//     // Listen for appointment date changes to update available times
//     document.getElementById("appointment-date").addEventListener("change", updateAvailableTimes);
//
//     function updateAvailableTimes() {
//         var doctorId = document.getElementById("doctor").value;
//         var selectedDate = document.getElementById("appointment-date").value;
//         var appointmentTimeSelect = document.getElementById("appointment-time");
//
//         // Clear existing time slots
//         appointmentTimeSelect.innerHTML = '<option value="">Select Time</option>';
//
//         // Only make the AJAX call if both doctor and date are selected
//         if (doctorId && selectedDate) {
//             fetch(`/get-available-datetime/?doctor_id=${doctorId}&date=${selectedDate}`)
//                 .then(response => response.json())
//                 .then(data => {
//                     // Data should be an array of time slot strings (e.g., ["09:00", "10:30", ...])
//                     data.forEach(function(slot) {
//                         var option = document.createElement("option");
//                         option.value = slot;
//                         option.text = slot;
//                         appointmentTimeSelect.appendChild(option);
//                     });
//                 })
//                 .catch(error => console.error('Error fetching available times:', error));
//         }
//     }
// });
document.addEventListener("DOMContentLoaded", function() {
    // Listen for department changes to load doctors
    document.getElementById("department").addEventListener("change", function () {
        var departmentId = this.value;
        var doctorSelect = document.getElementById("doctor");
        // Reset doctor, date, and time dropdowns
        doctorSelect.innerHTML = '<option value="">Select Doctor</option>';
        document.getElementById("appointment-date").innerHTML = '<option value="">Select Date</option>';
        document.getElementById("appointment-time").innerHTML = '<option value="">Select Time</option>';

        if (departmentId) {
            fetch(`/get-doctors/?department_id=${departmentId}`)
                .then(response => response.json())
                .then(data => {
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

    // Listen for doctor selection to fetch available dates
    document.getElementById("doctor").addEventListener("change", function() {
        var doctorId = this.value;
        var appointmentDateSelect = document.getElementById("appointment-date");
        // Reset the appointment date and time dropdowns
        appointmentDateSelect.innerHTML = '<option value="">Select Date</option>';
        document.getElementById("appointment-time").innerHTML = '<option value="">Select Time</option>';

        if (doctorId) {
            // Fetch available dates for the selected doctor
            fetch(`/get-available-dates/?doctor_id=${doctorId}`)
                .then(response => response.json())
                .then(data => {
                    // Expecting JSON response like: [{ "date": "2025-02-14", "display": "14-02-2025, Monday" }, ...]
                    data.forEach(function(item) {
                        var option = document.createElement("option");
                        option.value = item.date;   // Raw date for backend queries
                        option.text = item.display; // Formatted display
                        appointmentDateSelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Error fetching available dates:', error));
        }
    });

    // Listen for appointment date changes to update available times
    document.getElementById("appointment-date").addEventListener("change", updateAvailableTimes);

    function updateAvailableTimes() {
        var doctorId = document.getElementById("doctor").value;
        var selectedDate = document.getElementById("appointment-date").value;
        var appointmentTimeSelect = document.getElementById("appointment-time");

        // Clear existing time slots
        appointmentTimeSelect.innerHTML = '<option value="">Select Time</option>';

        // Only make the AJAX call if both doctor and date are selected
        if (doctorId && selectedDate) {
            fetch(`/get-available-datetime/?doctor_id=${doctorId}&date=${selectedDate}`)
                .then(response => response.json())
                .then(data => {
                    // Data should be an array of time slot strings (e.g., ["09:00", "10:30", ...])
                    data.forEach(function(slot) {
                        var option = document.createElement("option");
                        option.value = slot;
                        option.text = slot;
                        appointmentTimeSelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Error fetching available times:', error));
        }
    }
});