    const canvas = document.getElementById('catCanvas');
    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    ctx.lineWidth = 7;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    let currentColor = '#2A3B8F';
    let currentCoatValue = 'deep_blue';
    let drawing = false;

    const undoStack = [];
    const MAX_UNDO_STEPS = 20;
    const undoBtn = document.getElementById('undoStroke');

    function saveUndoState() {
        undoStack.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
        if (undoStack.length > MAX_UNDO_STEPS) undoStack.shift();
        undoBtn.disabled = false;
    }

    undoBtn.addEventListener('click', () => {
        if (undoStack.length === 0) return;
        const previousState = undoStack.pop();
        ctx.putImageData(previousState, 0, 0);
        if (undoStack.length === 0) undoBtn.disabled = true;
    });

    const existingImageUrl = canvas.dataset.existingImage;
    if (existingImageUrl) {
        const img = new Image();
        img.crossOrigin = 'anonymous';
        img.onload = () => {
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            saveUndoState();
            undoBtn.disabled = true;
        };
        img.src = existingImageUrl;
    } else {
        saveUndoState();
        undoBtn.disabled = true;
    }

    document.querySelectorAll('.swatch').forEach((swatch) => {
        swatch.addEventListener('click', () => {
            document.querySelectorAll('.swatch').forEach((s) => s.classList.remove('active'));
            swatch.classList.add('active');
            currentColor = swatch.dataset.color;
            currentCoatValue = swatch.dataset.value;
            document.getElementById('coatColorInput').value = currentCoatValue;
        });
    });

    const existingColor = canvas.dataset.existingColor;
    if (existingColor) {
        const matchingSwatch = document.querySelector(`.swatch[data-value="${existingColor}"]`);
        if (matchingSwatch) matchingSwatch.click();
    }

    function getPos(e) {
        const rect = canvas.getBoundingClientRect();
        const point = e.touches ? e.touches[0] : e;
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        return {
            x: (point.clientX - rect.left) * scaleX,
            y: (point.clientY - rect.top) * scaleY,
        };
    }

    function startDraw(e) {
        drawing = true;
        saveUndoState();
        const pos = getPos(e);
        ctx.beginPath();
        ctx.moveTo(pos.x, pos.y);
    }
    function draw(e) {
        if (!drawing) return;
        const pos = getPos(e);
        ctx.strokeStyle = currentColor;
        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();
        e.preventDefault();
    }
    function stopDraw() { drawing = false; }

    canvas.addEventListener('mousedown', startDraw);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDraw);
    canvas.addEventListener('mouseleave', stopDraw);
    canvas.addEventListener('touchstart', startDraw);
    canvas.addEventListener('touchmove', draw);
    canvas.addEventListener('touchend', stopDraw);

    document.getElementById('clearCanvas').addEventListener('click', () => {
        saveUndoState();
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    });

    // --- Safe pre-fill placeholders using the element's data attribute ---
    const catCard = document.getElementById('catCard');
    const isEditing = catCard && catCard.dataset.isEditing === 'true';

    if (!isEditing) {
        const nameInput = document.getElementById('id_name');
        const personalityInput = document.getElementById('id_personality');

        if (nameInput) nameInput.placeholder = "e.g., Whiskers, Luna";
        if (personalityInput) personalityInput.placeholder = "e.g., Curious explorer who loves chasing laser pointers and napping in sunbeams.";
    }

    // Returns true if every pixel is fully transparent (nothing drawn)
    function isCanvasBlank(targetCanvas) {
        const blankCtx = targetCanvas.getContext('2d');
        const pixelBuffer = new Uint32Array(
            blankCtx.getImageData(0, 0, targetCanvas.width, targetCanvas.height).data.buffer
        );
        return !pixelBuffer.some((pixel) => pixel !== 0);
    }

    const catForm = document.getElementById('catForm');
    const clientErrorBox = document.getElementById('clientErrorBox');

    catForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const submitBtn = catForm.querySelector('button[type="submit"]');
        if (submitBtn.disabled) return;
        submitBtn.disabled = true;
        const originalBtnText = submitBtn.textContent;
        submitBtn.textContent = 'Saving...';
        clientErrorBox.style.display = 'none';

        if (isCanvasBlank(canvas)) {
            submitBtn.disabled = false;
            submitBtn.textContent = originalBtnText;
            clientErrorBox.textContent = 'Please draw your cat before saving! The canvas is empty.';
            clientErrorBox.style.display = 'block';
            clientErrorBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return;
        }

        canvas.toBlob((blob) => {
            if (!blob) {
                submitBtn.disabled = false;
                submitBtn.textContent = originalBtnText;
            clientErrorBox.textContent = 'Could not read your drawing! Please try again.';
                clientErrorBox.style.display = 'block';
                return;
            }

            const formData = new FormData(catForm);
            formData.set('drawing_image', blob, 'cat-drawing.png');

            fetch(catForm.action || window.location.href, {
                method: 'POST',
                body: formData,
            })
                .then(async (response) => {
                    if (response.redirected) {
                        window.location.href = response.url;
                        return;
                    }

                    const html = await response.text();
                    const parsed = new DOMParser().parseFromString(html, 'text/html');
                    const errorEls = parsed.querySelectorAll('.errorlist li, .alert-danger, .text-danger');
                    const messages = [];
                    errorEls.forEach((el) => {
                        const text = el.textContent.trim();
                        if (text) messages.push(text);
                    });

                    submitBtn.disabled = false;
                    submitBtn.textContent = originalBtnText;
                    clientErrorBox.textContent = messages.length
                        ? messages.join(' · ')
                        : 'Could not save your cat! Please check the form and try again.';
                    clientErrorBox.style.display = 'block';
                    clientErrorBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
                })
                .catch(() => {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalBtnText;
                    clientErrorBox.textContent = 'A network problem stopped your cat from saving. Please try again.';
                    clientErrorBox.style.display = 'block';
                });
        }, 'image/png');
    });