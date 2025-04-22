// Site-wide time tracking implementation
// Add this to a common JavaScript file that's included on all pages of your website

// Global variables for time tracking
let startTime = new Date();
let totalSeconds = 0;
const WEBSITE_TIMER_KEY = 'websiteTrackerData';

// Initialize timer when page loads
function initializeTimer() {
    // Check if we already have saved time for today
    const today = new Date().toLocaleDateString();
    let savedData = JSON.parse(localStorage.getItem(WEBSITE_TIMER_KEY) || '{}');
    
    // If we have saved data for today, use it
    if (savedData.date === today) {
        totalSeconds = savedData.timeSpent || 0;
    } else {
        // Reset for a new day
        savedData = {
            date: today,
            timeSpent: 0,
            // Keep any other site-wide data you need
        };
        localStorage.setItem(WEBSITE_TIMER_KEY, JSON.stringify(savedData));
    }
    
    // Set the start time to now
    startTime = new Date();
    
    // Initial display update
    updateTimerDisplay();
    
    // Start regular updates
    setInterval(updateTimer, 1000);
}

// Update timer and save to localStorage
function updateTimer() {
    const now = new Date();
    const diffSeconds = Math.floor((now - startTime) / 1000);
    totalSeconds += diffSeconds;
    startTime = now;
    
    // Save updated time
    const today = new Date().toLocaleDateString();
    const savedData = JSON.parse(localStorage.getItem(WEBSITE_TIMER_KEY) || '{}');
    savedData.date = today;
    savedData.timeSpent = totalSeconds;
    localStorage.setItem(WEBSITE_TIMER_KEY, JSON.stringify(savedData));
    
    // Update display
    updateTimerDisplay();
}

// Update the time display on page
function updateTimerDisplay() {
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    
    const formattedTime = `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    // Update any timer display elements on the current page
    const timerElements = document.querySelectorAll('.website-time-display');
    timerElements.forEach(element => {
        element.textContent = formattedTime;
    });
}

// Handle page visibility changes (when tab is switched or minimized)
function handleVisibilityChange() {
    if (document.visibilityState === 'hidden') {
        // Save the current time before leaving
        updateTimer();
    } else {
        // Reset the start time when returning
        startTime = new Date();
    }
}

// Save time when user leaves the page
function handleBeforeUnload() {
    updateTimer();
}

// Set up event listeners
function setupTimerEventListeners() {
    document.addEventListener('visibilitychange', handleVisibilityChange);
    window.addEventListener('beforeunload', handleBeforeUnload);
}

// Initialize everything
function initializeSiteWideTimer() {
    initializeTimer();
    setupTimerEventListeners();
}

// Call when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeSiteWideTimer);