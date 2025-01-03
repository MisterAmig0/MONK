document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal');
    const openModal = document.getElementById('openModal');
    const closeModal = document.getElementById('closeModal');
    const modalForm = document.getElementById('modalForm');
    const modalTitle = document.getElementById('modalTitle');
    const editIdField = document.getElementById('editId');

    const question1Field = document.getElementById('question1');
    const question2Field = document.getElementById('question2');
    const question3Field = document.getElementById('question3');
    const question4Field = document.getElementById('question4');

    const editButtons = document.querySelectorAll('.edit-post');
    const editIcons = document.querySelectorAll('.edit-icon'); // New edit icons next to date

    // Open modal for creating a new post
    openModal.addEventListener('click', () => {
        modalTitle.textContent = 'Journaling';
        modalForm.reset();
        editIdField.value = ''; // Ensure no edit ID is set for creating a new post
        modal.style.display = 'block';
    });

    // Open modal for editing a post via the Edit button
    editButtons.forEach(button => {
        button.addEventListener('click', () => {
            const id = button.getAttribute('data-id');
            const question1 = button.getAttribute('data-question1');
            const question2 = button.getAttribute('data-question2');
            const question3 = button.getAttribute('data-question3');
            const question4 = button.getAttribute('data-question4');

            modalTitle.textContent = 'Edit Your Journal Entry';
            editIdField.value = id;
            question1Field.value = question1;
            question2Field.value = question2;
            question3Field.value = question3;
            question4Field.value = question4;

            modal.style.display = 'block';
        });
    });

    // Open modal for editing a post via the new Edit icon next to date
    editIcons.forEach(icon => {
        icon.addEventListener('click', () => {
            const id = icon.getAttribute('data-id');
            const question1 = icon.getAttribute('data-question1');
            const question2 = icon.getAttribute('data-question2');
            const question3 = icon.getAttribute('data-question3');
            const question4 = icon.getAttribute('data-question4');

            modalTitle.textContent = 'Edit Your Journal Entry';
            editIdField.value = id;
            question1Field.value = question1;
            question2Field.value = question2;
            question3Field.value = question3;
            question4Field.value = question4;

            modal.style.display = 'block';
        });
    });

    // Close modal
    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Close modal when clicking outside it
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});
