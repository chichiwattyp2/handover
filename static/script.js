// WhatsApp Chat Analyzer - Frontend JavaScript

// DOM Elements
const uploadForm = document.getElementById('uploadForm');
const chatFileInput = document.getElementById('chatFile');
const fileLabel = document.getElementById('fileLabel');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');

// File input change handler
chatFileInput.addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name;
    if (fileName) {
        fileLabel.classList.add('file-selected');
        fileLabel.querySelector('.file-label-text').textContent = fileName;
    } else {
        fileLabel.classList.remove('file-selected');
        fileLabel.querySelector('.file-label-text').textContent = 'Choose File';
    }
});

// Form submit handler
uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault();

    // Hide previous results/errors
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';

    // Get file
    const file = chatFileInput.files[0];
    if (!file) {
        showError('Please select a file');
        return;
    }

    // Validate file type
    if (!file.name.toLowerCase().endsWith('.txt')) {
        showError('Please upload a .txt file');
        return;
    }

    // Show loading state
    setLoading(true);

    // Create FormData
    const formData = new FormData();
    formData.append('chat_file', file);

    try {
        // Send request
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'Analysis failed');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please check your connection and try again.');
    } finally {
        setLoading(false);
    }
});

// Set loading state
function setLoading(isLoading) {
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoader = analyzeBtn.querySelector('.btn-loader');

    if (isLoading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-flex';
        analyzeBtn.disabled = true;
    } else {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        analyzeBtn.disabled = false;
    }
}

// Display results
function displayResults(data) {
    const { metadata, analysis } = data;

    // Display metadata
    displayMetadata(metadata);

    // Display summary
    displaySummary(analysis.summary);

    // Display sentiment
    displaySentiment(analysis.overall_sentiment, analysis.participant_sentiments);

    // Display topics
    displayTopics(analysis.key_topics);

    // Display actionables
    displayActionables(analysis.actionables);

    // Display insights
    displayInsights(analysis.conversation_insights);

    // Show results section
    resultsSection.style.display = 'block';

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Display metadata
function displayMetadata(metadata) {
    const participantsEl = document.getElementById('participants');
    const messageCountEl = document.getElementById('messageCount');
    const dateRangeEl = document.getElementById('dateRange');

    participantsEl.textContent = metadata.participants.join(', ');
    messageCountEl.textContent = metadata.message_count.toLocaleString();

    if (metadata.date_range.start && metadata.date_range.end) {
        const startDate = new Date(metadata.date_range.start).toLocaleDateString();
        const endDate = new Date(metadata.date_range.end).toLocaleDateString();
        dateRangeEl.textContent = `${startDate} - ${endDate}`;
    } else {
        dateRangeEl.textContent = 'N/A';
    }
}

// Display summary
function displaySummary(summary) {
    const summaryEl = document.getElementById('summary');
    summaryEl.textContent = summary;
}

// Display sentiment
function displaySentiment(overallSentiment, participantSentiments) {
    // Overall sentiment
    const sentimentBadge = document.getElementById('sentimentBadge');
    const sentimentIcon = document.getElementById('sentimentIcon');
    const sentimentLabel = document.getElementById('sentimentLabel');
    const sentimentExplanation = document.getElementById('sentimentExplanation');
    const confidenceFill = document.getElementById('confidenceFill');
    const confidenceValue = document.getElementById('confidenceValue');

    const sentiment = overallSentiment.sentiment.toLowerCase();

    // Set icon
    const icons = {
        'positive': '😊',
        'negative': '😞',
        'neutral': '😐',
        'mixed': '🤔'
    };
    sentimentIcon.textContent = icons[sentiment] || '😐';
    sentimentLabel.textContent = sentiment.charAt(0).toUpperCase() + sentiment.slice(1);

    // Set badge class
    sentimentBadge.className = `sentiment-badge ${sentiment}`;

    // Set confidence
    const confidencePercent = Math.round(overallSentiment.confidence * 100);
    confidenceFill.style.width = `${confidencePercent}%`;
    confidenceValue.textContent = `${confidencePercent}%`;

    // Set explanation
    sentimentExplanation.textContent = overallSentiment.explanation;

    // Participant sentiments
    const participantSentimentsEl = document.getElementById('participantSentiments');
    participantSentimentsEl.innerHTML = '';

    if (participantSentiments && participantSentiments.length > 0) {
        participantSentiments.forEach(ps => {
            const psDiv = document.createElement('div');
            psDiv.className = 'participant-sentiment';

            const psSentiment = ps.sentiment.toLowerCase();
            const psIcon = icons[psSentiment] || '😐';

            psDiv.innerHTML = `
                <span class="participant-name">${escapeHtml(ps.participant)}</span>
                <div>
                    <span class="participant-sentiment-badge ${psSentiment}">
                        <span>${psIcon}</span>
                        <span>${ps.sentiment}</span>
                    </span>
                </div>
            `;

            participantSentimentsEl.appendChild(psDiv);
        });
    }
}

// Display topics
function displayTopics(topics) {
    const topicsEl = document.getElementById('keyTopics');
    topicsEl.innerHTML = '';

    if (topics && topics.length > 0) {
        topics.forEach(topic => {
            const topicTag = document.createElement('span');
            topicTag.className = 'topic-tag';
            topicTag.textContent = topic;
            topicsEl.appendChild(topicTag);
        });
    } else {
        topicsEl.innerHTML = '<p class="no-actionables">No specific topics identified</p>';
    }
}

// Display actionables
function displayActionables(actionables) {
    const actionablesEl = document.getElementById('actionables');
    actionablesEl.innerHTML = '';

    if (actionables && actionables.length > 0) {
        actionables.forEach(actionable => {
            const actionDiv = document.createElement('div');
            const priority = actionable.priority?.toLowerCase() || 'not specified';
            actionDiv.className = `actionable-item priority-${priority.replace(' ', '-')}`;

            actionDiv.innerHTML = `
                <div class="actionable-action">${escapeHtml(actionable.action)}</div>
                <div class="actionable-details">
                    <div class="actionable-detail">
                        <strong>👤 Assignee:</strong> ${escapeHtml(actionable.assignee || 'Not specified')}
                    </div>
                    <div class="actionable-detail">
                        <strong>📅 Deadline:</strong> ${escapeHtml(actionable.deadline || 'Not specified')}
                    </div>
                    <div class="actionable-detail">
                        <strong>🎯 Priority:</strong> ${escapeHtml(priority)}
                    </div>
                </div>
                ${actionable.context ? `<div class="actionable-context">"${escapeHtml(actionable.context)}"</div>` : ''}
            `;

            actionablesEl.appendChild(actionDiv);
        });
    } else {
        actionablesEl.innerHTML = '<div class="no-actionables">✨ No action items found in this conversation</div>';
    }
}

// Display insights
function displayInsights(insights) {
    const insightsEl = document.getElementById('insights');
    insightsEl.innerHTML = '';

    if (insights) {
        // Tone
        if (insights.tone) {
            const toneDiv = document.createElement('div');
            toneDiv.className = 'insight-item';
            toneDiv.innerHTML = `
                <div class="insight-label">Conversation Tone</div>
                <div class="insight-value">${escapeHtml(insights.tone)}</div>
            `;
            insightsEl.appendChild(toneDiv);
        }

        // Engagement Level
        if (insights.engagement_level) {
            const engagementDiv = document.createElement('div');
            engagementDiv.className = 'insight-item';
            engagementDiv.innerHTML = `
                <div class="insight-label">Engagement Level</div>
                <div class="insight-value">${escapeHtml(insights.engagement_level)}</div>
            `;
            insightsEl.appendChild(engagementDiv);
        }

        // Key Points
        if (insights.key_points && insights.key_points.length > 0) {
            const keyPointsDiv = document.createElement('div');
            keyPointsDiv.className = 'insight-item';
            keyPointsDiv.style.gridColumn = '1 / -1'; // Span all columns

            let keyPointsHtml = '<div class="insight-label">Key Points</div><ul class="insight-list">';
            insights.key_points.forEach(point => {
                keyPointsHtml += `<li>${escapeHtml(point)}</li>`;
            });
            keyPointsHtml += '</ul>';

            keyPointsDiv.innerHTML = keyPointsHtml;
            insightsEl.appendChild(keyPointsDiv);
        }
    }
}

// Show error
function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
