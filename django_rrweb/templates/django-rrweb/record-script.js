{% load static %}(function () {
    function rrwebSetup() {
        let rrwebSessionKey = window.rrwebSessionKey || "{{ session_key }}";
        let rrwebEvents = [];

        window.rrwebRecord({
            emit(event) {
                rrwebEvents.push(event);
            }
        });

        function rrwebSave() {
            const body = JSON.stringify({ rrwebEvents, rrwebSessionKey });
            rrwebEvents = [];
            fetch("//{{ request.get_host }}{% url 'django-rrweb-record-events' %}", {
                body,
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                method: "POST",
                mode: "cors"
            });
        }

        setInterval(rrwebSave, 1000);
        window.addEventListener("beforeunload", rrwebSave);
        window.addEventListener("unload", rrwebSave);
    }

    if (window.rrwebRecord === undefined) {
        const scriptTag = document.createElement("script");
        scriptTag.onload = rrwebSetup;
        scriptTag.src = "//{{ request.get_host }}{% static 'django-rrweb/rrweb-record-1-1-3.js' %}";
        document.head.appendChild(scriptTag);
    }
    else {
        rrwebSetup();
    }
}());
