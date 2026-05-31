document.addEventListener('DOMContentLoaded', () => {
    const API = window.INTRAMURALS_API_BASE ? `${window.INTRAMURALS_API_BASE}/api` : '/api';

    const sportsSelect = document.getElementById('sports_select');
    const egamesSelect = document.getElementById('egames_select');
    if (!sportsSelect || !egamesSelect) {
        console.error('Registration select elements not found');
        return;
    }

    sportsSelect.innerHTML = '<option value="">Loading sports...</option>';
    egamesSelect.innerHTML = '<option value="">Loading e-games...</option>';

    fetch(`${API}/sports`)
        .then(res => {
            if (!res.ok) {
                throw new Error(`API returned status ${res.status}`);
            }
            return res.json();
        })
        .then(list => {
            if (!Array.isArray(list)) {
                throw new Error('Invalid response format from /api/sports');
            }

            sportsSelect.innerHTML = '<option value="">Select sport</option>';
            egamesSelect.innerHTML = '<option value="">Select e-game</option>';

            list.forEach(s => {
                const opt = document.createElement('option');
                opt.value = s.id;
                opt.textContent = s.sport_name;
                sportsSelect.appendChild(opt);

                const category = (s.category || '').toLowerCase();
                const name = (s.sport_name || '').toLowerCase();
                if (category.includes('e-game') || name.includes('codm') || name.includes('mobile')) {
                    egamesSelect.appendChild(opt.cloneNode(true));
                }
            });
        })
        .catch(err => {
            console.error('Failed to load sports', err);
            sportsSelect.innerHTML = '<option value="">Failed to load sports</option>';
            egamesSelect.innerHTML = '<option value="">Failed to load e-games</option>';
        });

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