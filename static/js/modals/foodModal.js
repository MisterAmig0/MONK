    const addModal = document.getElementById('foodModal');
    const editModal = document.getElementById('editModal');
    const addFoodBtn = document.getElementById('addFoodBtn');
    const closeButtons = document.querySelectorAll('.close');
    const editButtons = document.querySelectorAll('.edit-btn');
    const overlay = document.querySelector('.modal');

    // Open "Add Food" Modal
    addFoodBtn.addEventListener('click', () => {
        addModal.style.display = 'block';
    });

    // Open "Edit Food" Modal
    editButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            document.getElementById('edit-id').value = btn.dataset.id;
            document.getElementById('edit-title').value = btn.dataset.title;
            document.getElementById('edit-description').value = btn.dataset.description;
            document.getElementById('edit-category').value = btn.dataset.category;
            document.getElementById('edit-kcal').value = btn.dataset.kcal;

            editModal.style.display = 'block';
        });
    });

    // Close Modals
    closeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            addModal.style.display = 'none';
            editModal.style.display = 'none';
        });
    });

    // Close Modals When Clicking Outside
    window.addEventListener('click', event => {
        if (event.target == addModal) {
            addModal.style.display = 'none';
        }
        if (event.target == editModal) {
            editModal.style.display = 'none';
        }
    });
