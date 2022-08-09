(function () {
    let rrwebEvents = [];

    rrwebRecord({
        emit(event) {
            rrwebEvents.push(event);
        },
    });

    function rrwebSave() {
        const body = JSON.stringify({ rrwebEvents });
        rrwebEvents = [];
        fetch("//{{ request.get_host }}{% url 'django-rrweb-record-events' %}", {
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            method: "POST",
            mode: "cors",
            body,
        });
    }

    setInterval(rrwebSave, 10000);
    window.addEventListener('beforeunload', rrwebSave);
    window.addEventListener('unload', rrwebSave);
})();
