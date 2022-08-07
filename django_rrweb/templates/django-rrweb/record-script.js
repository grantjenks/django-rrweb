(function () {
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
        fetch("//{{ request.get_host }}{% url 'django-rrweb-record-events' %}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            mode: "cors",
            body,
        });
    }

    setInterval(rrwebSave, 1000);
})();
