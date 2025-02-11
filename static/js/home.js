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
});