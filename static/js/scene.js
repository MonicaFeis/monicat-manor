/* global bootstrap */
// static/js/scene.js
(function setSceneBackground() {
    const hour = new Date().getHours();
    const sceneBg = document.getElementById('sceneBg');
    if (!sceneBg) return;

    sceneBg.classList.remove('time-day', 'time-dusk', 'time-night');

    if (hour >= 6 && hour < 17) {
        sceneBg.classList.add('time-day');
    } else if (hour >= 17 && hour < 20) {
        sceneBg.classList.add('time-dusk');
    } else {
        sceneBg.classList.add('time-night');
    }
})();

const catModalEl = document.getElementById('catModal');
const catModal = new bootstrap.Modal(catModalEl);

catModalEl.addEventListener('hide.bs.modal', () => {
    if (document.activeElement && catModalEl.contains(document.activeElement)) {
        document.activeElement.blur();
    }
});
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const currentUsername = window.MANOR_CURRENT_USERNAME || '';
let activeReactUrl = null;
let activePetUrl = null;
let activeWrap = null;

const nameEmojis = ['🐱', '🐈', '😺', '😸'];
const moodEmojis = ['😊', '😽', '🥰', '😌', '😻'];

function pickEmoji(list, seed) {
    const index = seed.length % list.length;
    return list[index];
}

function floatEmojiFrom(button, emoji) {
    const rect = button.getBoundingClientRect();
    const pop = document.createElement('span');
    pop.className = 'float-pop';
    pop.textContent = emoji;
    pop.style.left = (rect.left + rect.width / 2 - 10) + 'px';
    pop.style.top = rect.top + 'px';
    document.body.appendChild(pop);
    setTimeout(() => pop.remove(), 900);
}

document.querySelectorAll('.cat-sprite-wrap').forEach((wrap) => {
    wrap.addEventListener('click', () => {
        const name = wrap.dataset.name;
        const personality = wrap.dataset.personality;

        document.getElementById('catModalName').textContent =
            name + ' ' + pickEmoji(nameEmojis, name);
        document.getElementById('catModalPersonality').textContent =
            pickEmoji(moodEmojis, personality) + ' ' + personality;
        document.getElementById('catModalOwner').textContent = 'Created by ' + wrap.dataset.owner;

        // Support for the profile link if present in the HTML modal
        const modalLink = document.getElementById('catModalLink');
        if (modalLink) {
            modalLink.href = wrap.dataset.url;
        }

        const ownerActions = document.getElementById('catModalOwnerActions');
        if (currentUsername && wrap.dataset.owner === currentUsername) {
            document.getElementById('catModalEditLink').href = wrap.dataset.editUrl;
            document.getElementById('catModalDeleteLink').href = wrap.dataset.deleteUrl;
            ownerActions.style.display = 'block';
        } else {
            ownerActions.style.display = 'none';
        }

        activeReactUrl = wrap.dataset.reactUrl;
        activePetUrl = wrap.dataset.petUrl;
        activeWrap = wrap;

        const pawCountEl = document.getElementById('catModalPawCount');
        if (pawCountEl) pawCountEl.textContent = wrap.dataset.count;
        const pawBtn = document.getElementById('catModalPaw');
        if (pawBtn) pawBtn.classList.toggle('reacted', wrap.dataset.reacted === 'true');

        const petBtn = document.getElementById('catModalPet');
        if (petBtn) {
            const alreadyPetted = wrap.dataset.petted === 'true';
            petBtn.disabled = alreadyPetted;
            petBtn.classList.toggle('petted', alreadyPetted);
            petBtn.textContent = alreadyPetted ? '💗 Petted' : '💗 Pet';
        }

        catModal.show();
    });
});

const pawBtn = document.getElementById('catModalPaw');
if (pawBtn) {
    pawBtn.addEventListener('click', () => {
        if (!activeReactUrl) return;
        fetch(activeReactUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
            .then((res) => res.json())
            .then((data) => {
                document.getElementById('catModalPawCount').textContent = data.count;
                pawBtn.classList.toggle('reacted', data.reacted);

                if (activeWrap) {
                    activeWrap.dataset.count = data.count;
                    activeWrap.dataset.reacted = data.reacted;
                }

                if (data.reacted) floatEmojiFrom(pawBtn, '🐾');
            });
    });
}

const petBtn = document.getElementById('catModalPet');
if (petBtn) {
    petBtn.addEventListener('click', () => {
        if (!activePetUrl || petBtn.disabled) return;
        petBtn.disabled = true;
        petBtn.classList.add('petted');
        petBtn.textContent = '💗 Petted';

        if (activeWrap) activeWrap.dataset.petted = 'true';

        fetch(activePetUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
            .then((res) => res.json())
            .then(() => {
                floatEmojiFrom(petBtn, '💗');
            })
            .catch(() => {
                petBtn.disabled = false;
                petBtn.classList.remove('petted');
                petBtn.textContent = '💗 Pet';
                if (activeWrap) activeWrap.dataset.petted = 'false';
            });
    });
}