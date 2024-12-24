// Function to dynamically create the checklist in the modal
function handleOpenModal(element) {
    try {
        // Retrieve task data from the clicked element
        const title = element.getAttribute('data-title');
        const description = element.getAttribute('data-description');
        const checklistData = element.getAttribute('data-checklist') || '[]';

        // Safely parse the checklist JSON
        const checklist = JSON.parse(checklistData);

        // Populate modal content
        document.getElementById('modalTitle').textContent = title;
        document.getElementById('modalDescription').textContent = description;

        // Populate the checklist
        const checklistContainer = document.getElementById('checklistItems');
        checklistContainer.innerHTML = ''; // Clear previous checklist items

        if (checklist.length > 0) {
            checklist.forEach(item => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    <label>
                        <input type="checkbox" ${item.completed ? 'checked' : ''} 
                            onchange="toggleChecklist(${item.id}, this.checked)">
                        ${item.text}
                    </label>
                `;
                checklistContainer.appendChild(listItem);
            });
        } else {
            checklistContainer.innerHTML = '<p>No checklist items for this task.</p>';
        }

        // Display the modal
        document.getElementById('agendaModal').style.display = 'block';
    } catch (error) {
        console.error("Error parsing checklist data:", error);
        alert("Failed to open task details. Please try again.");
    }
}

// Function to toggle checklist completion status via AJAX
function toggleChecklist(itemId, isChecked) {
    fetch(`/toggle_checklist/${itemId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ completed: isChecked }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update checklist item');
        }
        return response.json();
    })
    .then(data => {
        console.log('Checklist item updated:', data);
    })
    .catch(error => {
        console.error(error);
        alert('Error updating checklist item');
    });
}

// Function to close the modal
function closeModal() {
    document.getElementById('agendaModal').style.display = 'none';
}

// Event listener to close the modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById('agendaModal');
    if (event.target === modal) {
        closeModal();
    }
};

// Function to toggle description visibility
function toggleDescription(id) {
    const desc = document.getElementById(`description-${id}`);
    desc.style.display = (desc.style.display === 'none') ? 'block' : 'none';
}

// Function to add a new checklist item
function addChecklistItem() {
    const container = document.getElementById('checklist-container');
    const inputCount = container.querySelectorAll('input').length + 1;
    const newItem = document.createElement('input');
    newItem.type = 'text';
    newItem.name = 'checklist[]';
    newItem.placeholder = `Checklist Item ${inputCount}`;
    container.appendChild(newItem);
}