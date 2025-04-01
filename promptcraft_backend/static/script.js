document.addEventListener('DOMContentLoaded', function() {
    // Initialize tag inputs
    setupTagInput('tech-stack-input', 'tech-stack-tags', 'tech-stack');
    setupTagInput('key-features-input', 'key-features-tags', 'key-features');
    setupTagInput('constraints-input', 'constraints-tags', 'constraints');

    // Handle form submission
    const form = document.getElementById('promptForm');
    form.addEventListener('submit', handleFormSubmit);

    // Initialize copy button
    const copyBtn = document.getElementById('copy-btn');
    copyBtn.addEventListener('click', function() {
        const promptText = document.getElementById('prompt-result').textContent;
        copyToClipboard(promptText);
    });

    // Check if there are query parameters to populate form
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('goal')) {
        document.getElementById('goal').value = urlParams.get('goal');
    }
});

// Function to set up tag input functionality
function setupTagInput(inputId, tagsContainerId, hiddenInputId) {
    const input = document.getElementById(inputId);
    const tagsContainer = document.getElementById(tagsContainerId);
    const hiddenInput = document.getElementById(hiddenInputId);
    const tags = [];

    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ',') {
            e.preventDefault();
            
            const text = input.value.trim();
            if (text && !tags.includes(text)) {
                addTag(text);
                input.value = '';
                updateHiddenInput();
            }
        }
    });

    // Add a blur event to also add tags when the input loses focus
    input.addEventListener('blur', function() {
        const text = input.value.trim();
        if (text && !tags.includes(text)) {
            addTag(text);
            input.value = '';
            updateHiddenInput();
        }
    });

    function addTag(text) {
        tags.push(text);
        
        const tag = document.createElement('div');
        tag.className = 'tag';
        tag.innerHTML = `
            ${escapeHtml(text)}
            <button type="button" aria-label="Remove tag">×</button>
        `;
        
        const removeButton = tag.querySelector('button');
        removeButton.addEventListener('click', function() {
            tagsContainer.removeChild(tag);
            const index = tags.indexOf(text);
            if (index !== -1) {
                tags.splice(index, 1);
                updateHiddenInput();
            }
        });
        
        tagsContainer.appendChild(tag);
    }

    function updateHiddenInput() {
        hiddenInput.value = JSON.stringify(tags);
        console.log(`Updated ${hiddenInputId} with values:`, tags);
    }
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(e.target);
    
    // Debug log the tech_stack value
    console.log('tech_stack value:', formData.get('tech_stack'));
    
    const requestData = {
        request: {
            goal: formData.get('goal'),
            tech_stack: JSON.parse(formData.get('tech_stack') || '[]'),
            coding_style: formData.get('coding_style') || null,
            key_features: JSON.parse(formData.get('key_features') || '[]'),
            target_audience: formData.get('target_audience') || null,
            constraints: JSON.parse(formData.get('constraints') || '[]'),
            output_format_request: formData.get('output_format_request'),
            ai_model_target: formData.get('ai_model_target') || 'GPT-4'
        }
    };
    
    console.log('Sending request with data:', requestData);
    
    // Show loading and result section
    const resultSection = document.getElementById('result-section');
    const loadingIndicator = document.getElementById('loading-indicator');
    const promptResult = document.getElementById('prompt-result');
    const copyBtn = document.getElementById('copy-btn');
    
    resultSection.style.display = 'block';
    loadingIndicator.style.display = 'flex';
    promptResult.style.display = 'none';
    copyBtn.style.display = 'none';
    
    // Scroll to result section
    resultSection.scrollIntoView({ behavior: 'smooth' });
    
    try {
        // Call API
        const response = await fetch('/generate-tool-prompt/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw await response.json();
        }
        
        const data = await response.json();
        
        // Show result
        promptResult.textContent = data.generated_prompt;
        promptResult.style.display = 'block';
        copyBtn.style.display = 'block';
    } catch (error) {
        // Show error
        let errorMessage = 'An unexpected error occurred.';
        
        if (error.detail) {
            errorMessage = `Error: ${error.detail}`;
        }
        
        promptResult.textContent = errorMessage;
        promptResult.style.display = 'block';
        console.error('Error:', error);
    } finally {
        loadingIndicator.style.display = 'none';
    }
}

// Helper to copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
        .then(() => {
            const copyBtn = document.getElementById('copy-btn');
            const originalText = copyBtn.textContent;
            
            copyBtn.textContent = 'Copied!';
            setTimeout(() => {
                copyBtn.textContent = originalText;
            }, 2000);
        })
        .catch(err => {
            console.error('Could not copy text: ', err);
        });
}

// Helper to escape HTML
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
