(function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrfToken = getCookie("csrftoken");
    let sessionKey = "{{ request.session.rrweb_session_key }}";
    let rrwebEvents = [];

    rrweb.record({
        emit(event) {
            rrwebEvents.push(event);
        },
    });

    function rrwebSave() {
        const body = JSON.stringify({ sessionKey, rrwebEvents });
        rrwebEvents = [];
        fetch("//{{ request.get_host }}{% url 'rrweb-record' %}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            mode: "same-origin",
            body,
        });
    }

    setInterval(rrwebSave, 1000);
})();
