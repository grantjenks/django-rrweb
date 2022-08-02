from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def rrweb_styles():
    html = """
      <link
        rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/rrweb@1.1.3/dist/rrweb-all.min.css"
      />
    """
    return mark_safe(html)


@register.simple_tag
def rrweb_scripts():
    html = """
      <script
          src="https://cdn.jsdelivr.net/npm/rrweb@1.1.3/dist/rrweb-all.min.js"
      ></script>
      <script>
       function getCookie(name) {
           let cookieValue = null;
           if (document.cookie && document.cookie !== '') {
               const cookies = document.cookie.split(';');
               for (let i = 0; i < cookies.length; i++) {
                   const cookie = cookies[i].trim();
                   // Does this cookie string begin with the name we want?
                   if (cookie.substring(0, name.length + 1) === (name + '=')) {
                       cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                       break;
                   }
               }
           }
           return cookieValue;
       }

       const csrftoken = getCookie('csrftoken');

       function uuidv4() {
           return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
               (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
           );
       }

       let sessionKey = getCookie('rrweb-session-key');

       if (sessionKey === null) {
           sessionKey = uuidv4();
       }

       let rrwebEvents = [];

       rrweb.record({
           emit(event) {
               rrwebEvents.push(event);
           },
       });

       function rrwebSave() {
           const body = JSON.stringify({ sessionKey, rrwebEvents });
           rrwebEvents = [];
           fetch('/backend/rrweb/record/', {
               method: 'POST',
               headers: {
                   'Content-Type': 'application/json',
                   'X-CSRFToken': csrftoken,
               },
               mode: 'same-origin',
               body,
           });
       }

       setInterval(rrwebSave, 1000);
      </script>
    """
    return mark_safe(html)