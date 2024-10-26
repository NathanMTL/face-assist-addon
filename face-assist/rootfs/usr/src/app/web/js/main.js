// Main application JavaScript
document.addEventListener('DOMContentLoaded', () => {
    // Navigation handling
    const navButtons = document.querySelectorAll('.nav-btn');
    const sections = document.querySelectorAll('.section');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.dataset.target;
            
            // Update active states
            navButtons.forEach(b => b.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(target).classList.add('active');
        });
    });

    // Toast notification system
    const showToast = (message, type = 'success') => {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast show ${type}`;
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    };

    // File upload handling
    const handleDragOver = (e) => {
        e.preventDefault();
        e.currentTarget.classList.add('dragover');
    };

    const handleDragLeave = (e) => {
        e.currentTarget.classList.remove('dragover');
    };

    // Model Management
    const modelDropZone = document.getElementById('modelDropZone');
    const modelInput = document.getElementById('modelInput');
    const modelsList = document.getElementById('modelsList');

    const uploadModel = async (file) => {
        const formData = new FormData();
        formData.append('model', file);

        try {
            const response = await fetch('/api/models/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (response.ok) {
                showToast('Model uploaded successfully');
                loadModels();
            } else {
                showToast(data.error, 'error');
            }
        } catch (error) {
            showToast('Error uploading model', 'error');
        }
    };

    const loadModels = async () => {
        try {
            const response = await fetch('/api/models');
            const models = await response.json();
            
            modelsList.innerHTML = models.map(model => `
                <div class="list-item">
                    <span>${model.name}</span>
                    <span>${(model.size / (1024 * 1024)).toFixed(2)} MB</span>
                </div>
            `).join('');
        } catch (error) {
            showToast('Error loading models', 'error');
        }
    };

    modelDropZone.addEventListener('dragover', handleDragOver);
    modelDropZone.addEventListener('dragleave', handleDragLeave);
    modelDropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            uploadModel(files[0]);
        }
    });

    modelDropZone.addEventListener('click', () => modelInput.click());
    modelInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            uploadModel(e.target.files[0]);
        }
    });

    // Face Database Management
    const faceDropZone = document.getElementById('faceDropZone');
    const faceInput = document.getElementById('faceInput');
    const facesList = document.getElementById('facesList');
    const personNameInput = document.getElementById('personName');
    const addPersonBtn = document.getElementById('addPerson');

    const uploadFace = async (file, personName) => {
        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch(`/api/faces/${personName}`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (response.ok) {
                showToast('Face added successfully');
                loadFaces();
            } else {
                showToast(data.error, 'error');
            }
        } catch (error) {
            showToast('Error uploading face', 'error');
        }
    };

    const loadFaces = async () => {
        try {
            const response = await fetch('/api/faces');
            const faces = await response.json();
            
            // Update faces list
            facesList.innerHTML = faces.map(face => `
                <div class="face-card">
                    <div class="face-card-info">
                        <h4>${face.name}</h4>
                        <p>${face.image_count} images</p>
                    </div>
                </div>
            `).join('');

            // Update verification dropdown
            const verifyPerson = document.getElementById('verifyPerson');
            verifyPerson.innerHTML = faces.map(face => 
                `<option value="${face.name}">${face.name}</option>`
            ).join('');
        } catch (error) {
            showToast('Error loading faces', 'error');
        }
    };

    faceDropZone.addEventListener('dragover', handleDragOver);
    faceDropZone.addEventListener('dragleave', handleDragLeave);
    faceDropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        const personName = personNameInput.value.trim();
        
        if (!personName) {
            showToast('Please enter a person name', 'error');
            return;
        }

        Array.from(files).forEach(file => uploadFace(file, personName));
    });

    faceDropZone.addEventListener('click', () => faceInput.click());
    faceInput.addEventListener('change', (e) => {
        const personName = personNameInput.value.trim();
        
        if (!personName) {
            showToast('Please enter a person name', 'error');
            return;
        }

        Array.from(e.target.files).forEach(file => uploadFace(file, personName));
    });

    // Face Verification
    const verifyDropZone = document.getElementById('verifyDropZone');
    const verifyInput = document.getElementById('verifyInput');
    const verifyResult = document.getElementById('verifyResult');

    const verifyFace = async (file) => {
        const formData = new FormData();
        formData.append('image', file);
        formData.append('person', document.getElementById('verifyPerson').value);

        try {
            const response = await fetch('/api/verify', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (response.ok) {
                verifyResult.classList.remove('hidden');
                verifyResult.className = `verify-result ${data.match ? 'success' : 'error'}`;
                verifyResult.innerHTML = `
                    <div class="result-header">
                        <h3>${data.match ? 'Match Found!' : 'No Match'}</h3>
                    </div>
                    <div class="result-details">
                        <p>Confidence: ${data.confidence.toFixed(2)}%</p>
                    </div>
                `;
            } else {
                showToast(data.error, 'error');
            }
        } catch (error) {
            showToast('Error during verification', 'error');
        }
    };

    verifyDropZone.addEventListener('dragover', handleDragOver);
    verifyDropZone.addEventListener('dragleave', handleDragLeave);
    verifyDropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            verifyFace(files[0]);
        }
    });

    verifyDropZone.addEventListener('click', () => verifyInput.click());
    verifyInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            verifyFace(e.target.files[0]);
        }
    });

    // Initialize
    loadModels();
    loadFaces();
});
