 // Modal Handling
 const addModal = document.getElementById('addModal');
 const removeModal = document.getElementById('removeModal');
 const openAddModal = document.getElementById('openAddModal');
 const openRemoveModal = document.getElementById('openRemoveModal');
 const closeAddModal = document.getElementById('closeAddModal');
 const closeRemoveModal = document.getElementById('closeRemoveModal');

 openAddModal.addEventListener('click', () => {
     addModal.classList.add('active');
 });

 closeAddModal.addEventListener('click', () => {
     addModal.classList.remove('active');
 });

 openRemoveModal.addEventListener('click', () => {
     removeModal.classList.add('active');
 });

 closeRemoveModal.addEventListener('click', () => {
     removeModal.classList.remove('active');
 });

 // Close modals when clicking outside
 window.addEventListener('click', (event) => {
     if (event.target === addModal) {
         addModal.classList.remove('active');
     }
     if (event.target === removeModal) {
         removeModal.classList.remove('active');
     }
 });
