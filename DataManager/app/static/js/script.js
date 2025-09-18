let timeLeft = 120;
let timer;

function updateTimer() {
        let minutes = Math.floor(timeLeft / 60);
        let seconds = timeLeft % 60;
        document.getElementById("timer").innerHTML = `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
        timeLeft--;

        if (timeLeft < 0) {
            clearInterval(timer);
            document.getElementById("timeoutMessage").style.display = "block";
            document.getElementById("resendButton").style.display = "block";
        }
    }

    function startTimer() {
        timer = setInterval(updateTimer, 1000);
    }

    function resendCode() {
        fetch('/resend_code', {
            method: 'POST',
            body: JSON.stringify({ email: '{{ email }}' }),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Новый код отправлен!');
                timeLeft = 120;
                startTimer();
                document.getElementById("timeoutMessage").style.display = "none";
                document.getElementById("resendButton").style.display = "none";
            }
        });
    }
    window.onload = function() {
        startTimer();
    };