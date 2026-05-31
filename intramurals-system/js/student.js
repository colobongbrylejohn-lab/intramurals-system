document.addEventListener('DOMContentLoaded', () => {
    const API = (window.INTRAMURALS_API_BASE || 'http://localhost:5000') + '/api';

    // Elements
    const sportsSelect = document.getElementById('sports_select');
    const egamesSelect = document.getElementById('egames_select');

    // Fetch sports and populate selects
    fetch(`${API}/sports`).then(r => r.json()).then(list => {
        sportsSelect.innerHTML = '<option value="">Select sport</option>';
        egamesSelect.innerHTML = '<option value="">Select e-game</option>';
        list.forEach(s => {
            const opt = document.createElement('option');
            opt.value = s.id;
            opt.textContent = s.sport_name;
            sportsSelect.appendChild(opt);

            if ((s.category || '').toLowerCase().includes('e-game') || s.sport_name.toLowerCase().includes('codm') || s.sport_name.toLowerCase().includes('mobile')) {
                const eopt = opt.cloneNode(true);
                egamesSelect.appendChild(eopt);
            }
        });
    }).catch(err => {
        console.error('Failed to load sports', err);
        sportsSelect.innerHTML = '<option value="">Failed to load</option>';
        egamesSelect.innerHTML = '<option value="">Failed to load</option>';
    });

    // Helper to POST registration
    async function submitRegistration(data) {
        const res = await fetch(`${API}/register`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.error || 'Failed to submit');
        }
        return res.json();
    }

    // Sports form handler
    const sportsForm = document.getElementById('sportsForm');
    if (sportsForm) {
        sportsForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                student_name: document.getElementById('sports_student_name').value,
                student_number: document.getElementById('sports_student_number').value,
                sport_id: document.getElementById('sports_select').value,
                division: document.getElementById('sports_division').value,
                team_name: document.getElementById('sports_team_name').value,
                course_year: document.getElementById('sports_course_year').value
            };
            try {
                await submitRegistration(data);
                alert('Sports registration submitted');
                sportsForm.reset();
            } catch (err) {
                alert('Error: ' + err.message);
            }
        });
    }

    // E-games form handler
    const egamesForm = document.getElementById('egamesForm');
    if (egamesForm) {
        egamesForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                student_name: document.getElementById('egames_student_name').value,
                student_number: document.getElementById('egames_student_number').value,
                sport_id: document.getElementById('egames_select').value,
                division: document.getElementById('egames_division').value,
                team_name: document.getElementById('egames_team_name').value
            };
            try {
                await submitRegistration(data);
                alert('E-Games registration submitted');
                egamesForm.reset();
            } catch (err) {
                alert('Error: ' + err.message);
            }
        });
    }

});