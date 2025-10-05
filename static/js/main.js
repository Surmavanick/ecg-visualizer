document.getElementById('fileInput').addEventListener('change', handleFileUpload);

async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const viewMode = document.querySelector('input[name="viewMode"]:checked').value;
    
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('loading').style.display = 'block';

    const formData = new FormData();
    formData.append('file', file);
    formData.append('view_mode', viewMode);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            displayResults(data);
        } else {
            alert('Error: ' + data.error);
            resetUpload();
        }
    } catch (error) {
        alert('Upload failed: ' + error.message);
        resetUpload();
    }
}

function displayResults(data) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';

    document.getElementById('duration').textContent = data.duration.toFixed(2) + 's';
    document.getElementById('samples').textContent = data.samples;

    const plotsContainer = document.getElementById('plotsContainer');
    plotsContainer.innerHTML = '';

    data.plots.forEach((plotJSON, index) => {
        const plotDiv = document.createElement('div');
        plotDiv.id = 'plot' + index;
        plotDiv.style.marginBottom = '20px';
        plotsContainer.appendChild(plotDiv);

        Plotly.newPlot(plotDiv.id, JSON.parse(plotJSON).data, JSON.parse(plotJSON).layout, {responsive: true});
    });

    displayStatistics(data.stats);
}

function displayStatistics(stats) {
    const container = document.getElementById('statsContainer');
    container.innerHTML = '';

    const colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c',
                    '#e67e22', '#34495e', '#16a085', '#c0392b',
