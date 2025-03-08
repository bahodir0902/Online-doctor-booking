// Add this code to a new file: doctor_dashboard.js
// Then include it in your template with: <script src="{% static 'js/doctor_dashboard.js' %}"></script>

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initTooltips();

    // Initialize sidebar toggle functionality
    initSidebarToggle();

    // Initialize notification dropdown
    initNotifications();

    // Add row hover effects
    initTableEffects();

    // Initialize charts if stats are present
    initCharts();

    // Add search functionality
    initSearch();

    // Add time-based greeting
    updateGreeting();
});

// Time-based greeting
function updateGreeting() {
    const welcomeText = document.querySelector('.welcome-text h2');
    if (!welcomeText) return;

    const hour = new Date().getHours();
    let greeting;

    if (hour < 12) {
        greeting = 'Good morning';
    } else if (hour < 18) {
        greeting = 'Good afternoon';
    } else {
        greeting = 'Good evening';
    }

    const doctorName = welcomeText.textContent.split(',')[1]?.trim() || '';
    welcomeText.textContent = `${greeting}, ${doctorName}`;
}

// Initialize tooltips
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[title]');

    tooltipElements.forEach(element => {
        const title = element.getAttribute('title');
        element.setAttribute('data-tooltip', title);
        element.removeAttribute('title');

        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');

            document.body.appendChild(tooltip);

            const rect = this.getBoundingClientRect();
            tooltip.style.top = `${rect.top - tooltip.offsetHeight - 10}px`;
            tooltip.style.left = `${rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)}px`;
            tooltip.style.opacity = '1';

            this.addEventListener('mouseleave', function() {
                document.body.removeChild(tooltip);
            }, { once: true });
        });
    });

    // Add tooltip styles
    const style = document.createElement('style');
    style.textContent = `
        .tooltip {
            position: fixed;
            background: #333;
            color: white;
            padding: 6px 10px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s;
            pointer-events: none;
        }
        
        .tooltip:after {
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #333 transparent transparent transparent;
        }
    `;
    document.head.appendChild(style);
}

// Sidebar toggle functionality for mobile
function initSidebarToggle() {
    // Create toggle button for mobile
    const mainContent = document.querySelector('.main-content');
    const sidebar = document.querySelector('.sidebar');

    if (!mainContent || !sidebar) return;

    const toggleButton = document.createElement('button');
    toggleButton.className = 'sidebar-toggle';
    toggleButton.innerHTML = '<i class="fas fa-bars"></i>';

    const topBar = document.querySelector('.top-bar');
    if (topBar) {
        topBar.prepend(toggleButton);
    }

    // Add toggle functionality
    toggleButton.addEventListener('click', function() {
        sidebar.classList.toggle('sidebar-open');
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(event) {
        const isMobile = window.innerWidth <= 768;
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnToggleButton = toggleButton.contains(event.target);

        if (isMobile && !isClickInsideSidebar && !isClickOnToggleButton && sidebar.classList.contains('sidebar-open')) {
            sidebar.classList.remove('sidebar-open');
        }
    });

    // Add necessary styles
    const style = document.createElement('style');
    style.textContent = `
        @media (max-width: 768px) {
            .sidebar {
                position: fixed;
                left: -260px;
                transition: left 0.3s ease;
                z-index: 1000;
            }
            
            .sidebar-open {
                left: 0;
            }
            
            .sidebar-toggle {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 40px;
                height: 40px;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                cursor: pointer;
                margin-right: 15px;
            }
        }
        
        @media (min-width: 769px) {
            .sidebar-toggle {
                display: none;
            }
        }
    `;
    document.head.appendChild(style);
}

// Initialize notification dropdown
function initNotifications() {
    const notificationButton = document.querySelector('.btn-icon');
    if (!notificationButton) return;

    // Create dropdown
    const dropdown = document.createElement('div');
    dropdown.className = 'notification-dropdown';
    dropdown.innerHTML = `
        <div class="notification-header">
            <h3>Notifications</h3>
            <a href="#" class="mark-all-read">Mark all as read</a>
        </div>
        <div class="notification-list">
            <div class="notification-item unread">
                <div class="notification-icon message">
                    <i class="fas fa-comment-medical"></i>
                </div>
                <div class="notification-content">
                    <p>New message from <strong>John Doe</strong></p>
                    <span class="notification-time">5 minutes ago</span>
                </div>
            </div>
            <div class="notification-item unread">
                <div class="notification-icon appointment">
                    <i class="fas fa-calendar-plus"></i>
                </div>
                <div class="notification-content">
                    <p>New appointment request from <strong>Jane Smith</strong></p>
                    <span class="notification-time">30 minutes ago</span>
                </div>
            </div>
            <div class="notification-item">
                <div class="notification-icon system">
                    <i class="fas fa-bell"></i>
                </div>
                <div class="notification-content">
                    <p>System update completed successfully</p>
                    <span class="notification-time">2 hours ago</span>
                </div>
            </div>
        </div>
        <div class="notification-footer">
            <a href="#">View all notifications</a>
        </div>
    `;

    document.body.appendChild(dropdown);

    // Toggle dropdown
    let isDropdownOpen = false;

    notificationButton.addEventListener('click', function(event) {
        event.stopPropagation();
        isDropdownOpen = !isDropdownOpen;

        if (isDropdownOpen) {
            const rect = notificationButton.getBoundingClientRect();
            dropdown.style.top = `${rect.bottom + 10}px`;
            dropdown.style.right = `${window.innerWidth - rect.right}px`;
            dropdown.classList.add('show-dropdown');
        } else {
            dropdown.classList.remove('show-dropdown');
        }
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function() {
        if (isDropdownOpen) {
            dropdown.classList.remove('show-dropdown');
            isDropdownOpen = false;
        }
    });

    // Prevent closing when clicking inside dropdown
    dropdown.addEventListener('click', function(event) {
        event.stopPropagation();
    });

    // Handle "Mark all as read"
    const markAllReadButton = dropdown.querySelector('.mark-all-read');
    if (markAllReadButton) {
        markAllReadButton.addEventListener('click', function(e) {
            e.preventDefault();

            const unreadItems = dropdown.querySelectorAll('.notification-item.unread');
            unreadItems.forEach(item => {
                item.classList.remove('unread');
            });

            // Update badge count
            const badge = document.querySelector('.badge-small');
            if (badge) {
                badge.style.display = 'none';
            }
        });
    }

    // Add dropdown styles
    const style = document.createElement('style');
    style.textContent = `
        .notification-dropdown {
            position: fixed;
            width: 320px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border: 1px solid #e2e8f0;
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.3s ease;
        }
        
        .show-dropdown {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }
        
        .notification-header {
            padding: 15px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .notification-header h3 {
            font-size: 16px;
            font-weight: 600;
            color: #1e293b;
            margin: 0;
        }
        
        .mark-all-read {
            font-size: 12px;
            color: #0080ff;
            text-decoration: none;
        }
        
        .notification-list {
            max-height: 320px;
            overflow-y: auto;
        }
        
        .notification-item {
            padding: 15px;
            border-bottom: 1px solid #f1f5f9;
            display: flex;
            gap: 15px;
            transition: background-color 0.2s ease;
        }
        
        .notification-item:hover {
            background-color: #f8fafc;
        }
        
        .notification-item.unread {
            background-color: #f0f9ff;
        }
        
        .notification-item.unread:hover {
            background-color: #e0f2fe;
        }
        
        .notification-icon {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            flex-shrink: 0;
        }
        
        .notification-icon.message {
            background: linear-gradient(135deg, #0080ff, #00bfff);
        }
        
        .notification-icon.appointment {
            background: linear-gradient(135deg, #10b981, #34d399);
        }
        
        .notification-icon.system {
            background: linear-gradient(135deg, #f59e0b, #fbbf24);
        }
        
        .notification-content {
            flex: 1;
        }
        
        .notification-content p {
            margin: 0 0 5px 0;
            font-size: 14px;
            color: #1e293b;
        }
        
        .notification-time {
            font-size: 12px;
            color: #64748b;
        }
        
        .notification-footer {
            padding: 12px;
            text-align: center;
            border-top: 1px solid #e2e8f0;
        }
        
        .notification-footer a {
            font-size: 14px;
            color: #0080ff;
            text-decoration: none;
        }
    `;
    document.head.appendChild(style);
}

// Add table row effects
function initTableEffects() {
    const tableRows = document.querySelectorAll('.appointments-table tbody tr:not(.empty-row)');

    tableRows.forEach(row => {
        // Add hover class
        row.addEventListener('mouseenter', function() {
            this.classList.add('row-hover');
        });

        row.addEventListener('mouseleave', function() {
            this.classList.remove('row-hover');
        });

        // Add click effect for the whole row
        row.addEventListener('click', function(event) {
            // Prevent triggering if clicking on action buttons
            if (!event.target.closest('.action-buttons')) {
                this.classList.add('row-active');
                setTimeout(() => {
                    this.classList.remove('row-active');
                }, 200);
            }
        });
    });

    // Add necessary styles
    const style = document.createElement('style');
    style.textContent = `
        .row-hover {
            background-color: #f8fafc;
        }
        
        .row-active {
            background-color: #e0f2fe;
            transition: background-color 0.2s ease;
        }
    `;
    document.head.appendChild(style);
}

// Initialize mini charts for stats cards
function initCharts() {
    // Check if we have the stats cards and if chart.js is available
    const statsCards = document.querySelectorAll('.stat-card');
    if (!statsCards.length) return;

    // Create mini chart containers
    statsCards.forEach((card, index) => {
        const statDetails = card.querySelector('.stat-details');
        if (!statDetails) return;

        const miniChart = document.createElement('div');
        miniChart.className = 'mini-chart';
        miniChart.id = `miniChart${index}`;
        card.appendChild(miniChart);

        // Generate sample data based on card type
        let data;
        if (card.querySelector('.patients-icon')) {
            data = [65, 70, 68, 72, 75, 78, 82];
        } else if (card.querySelector('.appointments-icon')) {
            data = [22, 18, 26, 20, 24, 28, 25];
        } else {
            data = [8, 12, 5, 10, 7, 9, 11];
        }

        // Render a simple sparkline
        renderSparkline(miniChart.id, data);
    });

    // Add styles for charts
    const style = document.createElement('style');
    style.textContent = `
        .stat-card {
            position: relative;
            overflow: hidden;
            padding-bottom: 40px;
        }
        
        .mini-chart {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 40px;
            padding: 0 20px 5px;
        }
        
        .sparkline {
            width: 100%;
            height: 100%;
            stroke-width: 2;
            fill: none;
        }
        
        .patients-sparkline {
            stroke: #60a5fa;
        }
        
        .appointments-sparkline {
            stroke: #34d399;
        }
        
        .messages-sparkline {
            stroke: #fb7185;
        }
        
        .sparkline-fill {
            opacity: 0.2;
        }
        
        .patients-fill {
            fill: #60a5fa;
        }
        
        .appointments-fill {
            fill: #34d399;
        }
        
        .messages-fill {
            fill: #fb7185;
        }
    `;
    document.head.appendChild(style);
}

// Render a simple sparkline chart
function renderSparkline(containerId, data) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Determine chart type based on container ID
    let chartClass;
    if (containerId.includes('0')) {
        chartClass = 'patients';
    } else if (containerId.includes('1')) {
        chartClass = 'appointments';
    } else {
        chartClass = 'messages';
    }

    // Calculate points for the sparkline
    const width = container.clientWidth;
    const height = container.clientHeight;
    const max = Math.max(...data);
    const min = Math.min(...data);
    const range = max - min;

    // Create path for the line
    const pointGap = width / (data.length - 1);
    let path = `M 0,${height - ((data[0] - min) / range) * height}`;

    for (let i = 1; i < data.length; i++) {
        const x = i * pointGap;
        const y = height - ((data[i] - min) / range) * height;
        path += ` L ${x},${y}`;
    }

    // Create path for the fill
    const fillPath = `${path} L ${width},${height} L 0,${height} Z`;

    // Create SVG
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '100%');
    svg.setAttribute('height', '100%');
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.setAttribute('preserveAspectRatio', 'none');

    // Create the line path
    const linePath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    linePath.setAttribute('d', path);
    linePath.setAttribute('class', `sparkline ${chartClass}-sparkline`);

    // Create the fill path
    const fillPathEl = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    fillPathEl.setAttribute('d', fillPath);
    fillPathEl.setAttribute('class', `sparkline-fill ${chartClass}-fill`);

    // Add paths to SVG
    svg.appendChild(fillPathEl);
    svg.appendChild(linePath);

    // Add SVG to container
    container.appendChild(svg);
}

// Initialize search functionality
function initSearch() {
    const topBar = document.querySelector('.quick-actions');
    if (!topBar) return;

    // Create search input
    const searchContainer = document.createElement('div');
    searchContainer.className = 'search-container';

    searchContainer.innerHTML = `
        <div class="search-input">
            <i class="fas fa-search search-icon"></i>
            <input type="text" placeholder="Search patients or appointments...">
            <button class="search-clear"><i class="fas fa-times"></i></button>
        </div>
    `;

    topBar.prepend(searchContainer);

    // Add functionality
    const searchInput = searchContainer.querySelector('input');
    const clearButton = searchContainer.querySelector('.search-clear');

    searchInput.addEventListener('input', function() {
        if (this.value) {
            clearButton.style.display = 'flex';
            filterTable(this.value);
        } else {
            clearButton.style.display = 'none';
            filterTable('');
        }
    });

    clearButton.addEventListener('click', function() {
        searchInput.value = '';
        clearButton.style.display = 'none';
        filterTable('');
        searchInput.focus();
    });

    // Initially hide clear button
    clearButton.style.display = 'none';

    // Add search styles
    const style = document.createElement('style');
    style.textContent = `
        .search-container {
            margin-right: auto;
        }
        
        .search-input {
            position: relative;
            width: 250px;
        }
        
        .search-input input {
            width: 100%;
            padding: 10px 15px 10px 35px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            font-size: 14px;
            outline: none;
            transition: all 0.2s ease;
        }
        
        .search-input input:focus {
            border-color: #0080ff;
            box-shadow: 0 0 0 3px rgba(0, 128, 255, 0.1);
        }
        
        .search-icon {
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: #94a3b8;
        }
        
        .search-clear {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #f1f5f9;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            color: #64748b;
        }
        
        .search-clear:hover {
            background: #e2e8f0;
        }
        
        @media (max-width: 768px) {
            .search-container {
                width: 100%;
                margin-bottom: 10px;
                order: -1;
            }
            
            .search-input {
                width: 100%;
            }
        }
    `;
    document.head.appendChild(style);
}

// Filter table by search term
function filterTable(searchTerm) {
    const tableRows = document.querySelectorAll('.appointments-table tbody tr:not(.empty-row)');
    const emptyRow = document.querySelector('.empty-row');
    const searchLower = searchTerm.toLowerCase();

    let hasVisibleRows = false;

    tableRows.forEach(row => {
        const text = row.textContent.toLowerCase();

        if (text.includes(searchLower) || searchTerm === '') {
            row.style.display = '';
            hasVisibleRows = true;
        } else {
            row.style.display = 'none';
        }
    });

    // Handle empty state
    if (emptyRow) {
        if (hasVisibleRows || searchTerm === '') {
            emptyRow.style.display = 'none';
        } else {
            emptyRow.style.display = '';
            const emptyMessage = emptyRow.querySelector('.empty-state p');
            if (emptyMessage) {
                emptyMessage.textContent = `No results found for "${searchTerm}"`;
            }
        }
    }
}

// Animate stats numbers on page load
setTimeout(function() {
    const statNumbers = document.querySelectorAll('.stat-number');

    statNumbers.forEach(statNumber => {
        const finalValue = parseInt(statNumber.textContent, 10);

        if (!isNaN(finalValue)) {
            let startValue = 0;
            const duration = 1500;
            const startTime = Date.now();

            function updateNumber() {
                const currentTime = Date.now();
                const elapsed = currentTime - startTime;

                if (elapsed < duration) {
                    const progress = elapsed / duration;
                    const easeOutProgress = 1 - Math.pow(1 - progress, 3); // Cubic ease-out
                    const currentValue = Math.floor(easeOutProgress * finalValue);

                    statNumber.textContent = currentValue;
                    requestAnimationFrame(updateNumber);
                } else {
                    statNumber.textContent = finalValue;
                }
            }

            updateNumber();
        }
    });
}, 300);